"""
Grants the current cohort's GitHub Team access to internal repos that map
to the topic(s) scheduled for the target date (same date logic as
reveal_topic.py — defaults to the next class day).

IMPORTANT: this looks up repos directly by calendar topic text — it does
NOT go through topic_mapping.yml / _toc.yml file paths. That's intentional:
some days have a repo but no slide (no _toc.yml entry exists), so tying
repo access to slide existence would silently skip those days.

Requires:
  GH_ORG            - GitHub org name, e.g. "neuefische"
  TEAM_SLUG         - the cohort's team slug (repo variable, update per cohort)
  ORG_ADMIN_TOKEN   - a PAT (classic, scopes: admin:org + repo) or a
                       fine-grained token with org "Members" (write) and
                       target repos' "Administration" (write) permissions.
                       This CANNOT be the default GITHUB_TOKEN — that token
                       has no permission to manage team-repo access.
  GCAL_ICS_URL      - same secret iCal feed used by reveal_topic.py
  COHORT_TRACK      - "aipm" or "ds", same as reveal_topic.py
"""

import os
from pathlib import Path

import requests
import yaml

from calendar_utils import (
    get_target_date,
    get_topics_for_date,
    resolve_file_paths,
    find_mapping_key,
)

REPO_ACCESS_MAPPING_PATH = Path(".github/scripts/repo_access_mapping.yml")

GITHUB_API = "https://api.github.com"


def resolve_repos(entry, track: str) -> list[str]:
    """
    repo_access_mapping.yml entries can be:
      - a plain string             -> single repo, same for both tracks
      - a list of strings          -> multiple repos, same for both tracks
      - a dict {"aipm": ..., "ds": ...} -> track-specific (value can itself
        be a string or a list) — needed because most technical topics share
        the same DS repo across tracks, but pure PM topics (e.g. Intro to
        AIPM) instead need the aipm-course-curriculum meta repo.
    """
    return resolve_file_paths(entry, track)


def grant_team_repo_access(org: str, team_slug: str, repo_full_name: str,
                            token: str, permission: str = "pull", dry_run: bool = False) -> None:
    """
    repo_full_name is "owner/repo". Calls:
      PUT /orgs/{org}/teams/{team_slug}/repos/{owner}/{repo}
    """
    owner, repo = repo_full_name.split("/", 1)
    url = f"{GITHUB_API}/orgs/{org}/teams/{team_slug}/repos/{owner}/{repo}"

    if dry_run:
        print(f"[DRY RUN] Would grant team '{team_slug}' '{permission}' access to {repo_full_name}")
        return

    resp = requests.put(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        json={"permission": permission},
        timeout=30,
    )

    if resp.status_code not in (204, 200):
        raise RuntimeError(
            f"Failed to grant access to {repo_full_name}: "
            f"{resp.status_code} {resp.text}"
        )
    print(f"Granted team '{team_slug}' '{permission}' access to {repo_full_name}")


def main():
    ics_url = os.environ.get("GCAL_ICS_URL")
    if not ics_url:
        raise SystemExit("GCAL_ICS_URL environment variable is not set.")

    track = os.environ.get("COHORT_TRACK", "").strip().lower()
    if track not in ("aipm", "ds"):
        raise SystemExit(f"COHORT_TRACK must be 'aipm' or 'ds' (got: {track!r}).")

    org = os.environ.get("GH_ORG", "").strip()
    team_slug = os.environ.get("TEAM_SLUG", "").strip()
    token = os.environ.get("ORG_ADMIN_TOKEN", "").strip()

    if not org or not team_slug or not token:
        raise SystemExit("GH_ORG, TEAM_SLUG, and ORG_ADMIN_TOKEN must all be set.")

    dry_run = os.environ.get("DRY_RUN", "").strip().lower() in ("1", "true", "yes")
    permission = os.environ.get("TEAM_PERMISSION", "pull").strip()  # pull/push/admin

    target_date = get_target_date()
    print(f"Checking date: {target_date} (track: {track}, team: {team_slug}, dry_run: {dry_run})")

    topics = get_topics_for_date(ics_url, target_date)
    if not topics:
        print(f"No all-day topic event found for {target_date}.")
        return

    repo_mapping = yaml.safe_load(REPO_ACCESS_MAPPING_PATH.read_text()).get("repos", {})

    for topic in topics:
        print(f"Topic: {topic!r}")
        matched_key = find_mapping_key(topic, repo_mapping)

        if matched_key is None:
            print(f"  No repo mapped for topic {topic!r} — skipping.")
            continue

        repo_entry = repo_mapping[matched_key]

        for repo_full_name in resolve_repos(repo_entry, track):
            grant_team_repo_access(org, team_slug, repo_full_name, token,
                                    permission=permission, dry_run=dry_run)


if __name__ == "__main__":
    main()
