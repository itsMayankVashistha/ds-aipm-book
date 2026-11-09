"""
Shared logic for resolving "which topic(s) apply to a given date" from the
Google Calendar ICS feed. Used by both reveal_topic.py and
sync_team_repo_access.py so the two stay consistent.
"""

import os
import datetime
from zoneinfo import ZoneInfo

import requests
from icalendar import Calendar

BERLIN_TZ = ZoneInfo("Europe/Berlin")


def is_scheduled_run() -> bool:
    return os.environ.get("GITHUB_EVENT_NAME", "") == "schedule"


def get_target_date() -> datetime.date:
    """
    Return the date to check.
    - TARGET_DATE env var always wins (manual testing override).
    - Otherwise: default to the NEXT WEEKDAY (skipping Sat/Sun), since these
      workflows run the evening before to prep the next class day.
      A Friday-evening run therefore targets Monday, not Saturday.
    """
    override = os.environ.get("TARGET_DATE", "").strip()
    if override:
        try:
            return datetime.datetime.strptime(override, "%Y-%m-%d").date()
        except ValueError:
            raise SystemExit(f"TARGET_DATE must be in YYYY-MM-DD format (got: {override!r})")

    now_berlin = datetime.datetime.now(BERLIN_TZ)
    target = now_berlin.date() + datetime.timedelta(days=1)

    # Monday=0 ... Saturday=5, Sunday=6 — keep advancing past weekend days
    while target.weekday() >= 5:
        target += datetime.timedelta(days=1)

    return target


def get_topics_for_date(ics_url: str, target_date: datetime.date) -> list[str]:
    """Return all-day calendar event titles for the given date (a day can have more than one topic)."""
    resp = requests.get(ics_url, timeout=30)
    resp.raise_for_status()
    cal = Calendar.from_ical(resp.text)

    topics = []
    for component in cal.walk("VEVENT"):
        dtstart = component.get("dtstart")
        if dtstart is None:
            continue
        dt = dtstart.dt

        is_all_day = not isinstance(dt, datetime.datetime)
        if not is_all_day or dt != target_date:
            continue

        topics.append(str(component.get("summary", "")).strip())

    return topics


def resolve_file_paths(mapping_entry, track: str) -> list[str]:
    """
    mapping_entry can be:
      - a plain string            -> single file, same for both tracks
      - a list of strings         -> multiple files, same for both tracks
      - a dict {"aipm": ..., "ds": ...} -> track-specific, value can itself
        be a string or a list
    Always returns a list (possibly empty).
    """
    if isinstance(mapping_entry, str):
        return [mapping_entry]
    if isinstance(mapping_entry, list):
        return mapping_entry
    if isinstance(mapping_entry, dict):
        value = mapping_entry.get(track)
        if value is None:
            return []
        return resolve_file_paths(value, track)
    return []


def normalize(text: str) -> str:
    """Lowercase, collapse whitespace, strip — kills the most common mismatch causes."""
    return " ".join(text.strip().lower().split())


def find_mapping_key(topic: str, mapping: dict, fuzzy_cutoff: float = 0.87) -> str | None:
    """
    Find the mapping key that best represents `topic`, in tiers:
      1. Exact match (as-is)
      2. Normalized match (case/whitespace-insensitive)
      3. Substring match (one contains the other, normalized)
      4. Fuzzy match (difflib) above `fuzzy_cutoff` — catches typos like
         "Manuel of Me" vs "Manual of Me"

    Returns the ORIGINAL key from `mapping` (so callers still index with the
    real key), or None if nothing clears the bar. Every non-exact match is
    logged so mismatches stay visible rather than silently "fixing" things.
    """
    if topic in mapping:
        return topic

    norm_topic = normalize(topic)
    if not norm_topic:
        return None
    norm_to_key = {normalize(k): k for k in mapping.keys()}

    if norm_topic in norm_to_key:
        matched_key = norm_to_key[norm_topic]
        print(f"  [normalized match] {topic!r} -> {matched_key!r}")
        return matched_key

    for norm_key, original_key in norm_to_key.items():
        if norm_key in norm_topic or norm_topic in norm_key:
            print(f"  [substring match] {topic!r} -> {original_key!r}")
            return original_key

    import difflib
    close = difflib.get_close_matches(norm_topic, list(norm_to_key.keys()), n=1, cutoff=fuzzy_cutoff)
    if close:
        matched_key = norm_to_key[close[0]]
        print(f"  [fuzzy match, cutoff={fuzzy_cutoff}] {topic!r} -> {matched_key!r} — verify this is correct")
        return matched_key

    return None
