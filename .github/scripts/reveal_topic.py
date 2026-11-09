import os
import re
import datetime
from pathlib import Path

import yaml

from zoneinfo import ZoneInfo

from calendar_utils import (
    is_scheduled_run,
    get_target_date,
    get_topics_for_date,
    resolve_file_paths,
)

TOC_PATH = Path("DSBOOK/_toc.yml")
MAPPING_PATH = Path(".github/scripts/topic_mapping.yml")

BERLIN_TZ = ZoneInfo("Europe/Berlin")
TARGET_LOCAL_HOUR = 17  # only proceed on a scheduled run if it's actually 17:00 in Berlin


def is_correct_local_hour() -> bool:
    now_berlin = datetime.datetime.now(BERLIN_TZ)
    return now_berlin.hour == TARGET_LOCAL_HOUR


def reveal_file_in_toc(file_path: str, dry_run: bool = False) -> bool:
    """Uncomment the `- file: <file_path>` line in _toc.yml, if commented."""
    lines = TOC_PATH.read_text().splitlines()
    changed = False

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#") and re.search(rf"file:\s*{re.escape(file_path)}\s*$", stripped):
            new_line = re.sub(r"^(\s*)#\s?", r"\1", line)
            if dry_run:
                print(f"[DRY RUN] Would reveal: {file_path}\n  before: {line}\n  after:  {new_line}")
            else:
                lines[i] = new_line
                print(f"Revealed: {file_path}")
            changed = True
            break  # only one line should match

    if not changed:
        print(f"  No matching commented line found for: {file_path} (already revealed, or path mismatch)")

    if changed and not dry_run:
        TOC_PATH.write_text("\n".join(lines) + "\n")
    return changed


def main():
    # On a cron-triggered run, only proceed if it's actually 17:00 in Berlin
    # right now — this lets the workflow schedule two candidate UTC times
    # (covering both CEST and CET) without ever double-firing.
    if is_scheduled_run() and not is_correct_local_hour():
        print(f"Scheduled run, but not {TARGET_LOCAL_HOUR}:00 in Berlin right now "
              f"(it's {datetime.datetime.now(BERLIN_TZ).strftime('%H:%M')}) — skipping.")
        return

    ics_url = os.environ.get("GCAL_ICS_URL")
    if not ics_url:
        raise SystemExit("GCAL_ICS_URL environment variable is not set.")

    track = os.environ.get("COHORT_TRACK", "").strip().lower()
    if track not in ("aipm", "ds"):
        raise SystemExit(
            f"COHORT_TRACK must be set to 'aipm' or 'ds' (got: {track!r}). "
            f"Set it as a repo variable."
        )

    dry_run = os.environ.get("DRY_RUN", "").strip().lower() in ("1", "true", "yes")
    target_date = get_target_date()
    print(f"Checking date: {target_date} (track: {track}, dry_run: {dry_run})")

    topics = get_topics_for_date(ics_url, target_date)
    if not topics:
        print(f"No all-day topic event found for {target_date}.")
        return

    mapping = yaml.safe_load(MAPPING_PATH.read_text()).get("mappings", {})

    for topic in topics:
        print(f"Topic: {topic!r}")
        entry = mapping.get(topic)

        if entry is None:
            print(f"  No entry in topic_mapping.yml for {topic!r} — skipping. "
                  f"(Add a mapping if this topic should reveal a slide.)")
            continue

        file_paths = resolve_file_paths(entry, track)
        if not file_paths:
            print(f"  Entry exists for {topic!r} but has no path for track {track!r} — skipping.")
            continue

        for file_path in file_paths:
            reveal_file_in_toc(file_path, dry_run=dry_run)


if __name__ == "__main__":
    main()