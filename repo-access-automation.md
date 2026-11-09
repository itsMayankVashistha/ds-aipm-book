# Repo Access Automation: Auto-Granting Internal Repo Access to Cohort Teams

This automatically grants a cohort's GitHub Team read access to the internal
repos needed for the current (next) day's session, so students get access
right as a topic comes up — without anyone manually clicking through repo
settings one topic at a time. Like the ToC automation, it's driven by a
scheduled GitHub Actions workflow that reads the same Google Calendar.

This is a separate, independent automation from
[toc-automation.md](toc-automation.md) — it does **not** depend on whether a
topic has a slide deck in `DSBOOK/_toc.yml`. Some class days have an internal
repo but no slides yet; this automation still needs to run for those days.

## How it works, end to end

1. A GitHub Actions workflow
   ([.github/workflows/sync-team-access.yml](.github/workflows/sync-team-access.yml))
   runs on the same cron schedule as the ToC automation (and can also be
   triggered manually).
2. It calls a Python script
   ([.github/scripts/sync_team_repo_access.py](.github/scripts/sync_team_repo_access.py)),
   which:
   - Fetches the cohort's Google Calendar (the same `.ics` feed used by the
     ToC automation).
   - Looks for all-day event(s) on the **next weekday** (the topic(s) for
     the upcoming class day).
   - Looks up each event's title directly in a mapping file
     ([.github/scripts/repo_access_mapping.yml](.github/scripts/repo_access_mapping.yml))
     to find the internal repo(s) that topic needs.
   - Calls the GitHub API to grant the cohort's GitHub Team **read (`pull`)
     access** to each matched repo.
3. Nothing gets committed to the repo — this automation only makes API calls
   against GitHub's org/team permissions, so there's no push step.

## The pieces

### `.github/workflows/sync-team-access.yml`

- **Triggers:**
  - `schedule`: same DST-safe double-cron pattern as the ToC automation —
    two entries covering both German summer time (CEST, UTC+2) and winter
    time (CET, UTC+1), gated by a `check-time` job so only one of the two
    firings actually runs the sync each day.
  - `workflow_dispatch`: manual run from the Actions tab, with `test_date`
    and `dry_run` inputs, same as the ToC workflow.
- **Steps:** checks out the repo, sets up Python 3.12, installs
  `.github/scripts/requirements.txt`, runs `sync_team_repo_access.py`.
- **No `contents: write` permission needed** — this workflow never modifies
  repo content, only calls the GitHub API.

### `.github/scripts/sync_team_repo_access.py`

- **Date logic is shared** with the ToC automation via `calendar_utils.py`
  (same "next weekday" target date, same calendar-fetching code), so the two
  automations always agree on which day they're checking.
- **Topic → repo mapping is direct** — it looks up the calendar topic title
  straight in `repo_access_mapping.yml`. It does **not** go through
  `topic_mapping.yml` or `_toc.yml` file paths at all. This is intentional:
  tying repo access to slide existence would silently skip days that have a
  repo but no slide deck yet.
- **Matching is tiered**, via `calendar_utils.find_mapping_key()`:
  1. Exact match
  2. Normalized match (case-insensitive, whitespace-collapsed)
  3. Substring match (one string contains the other)
  4. Fuzzy match (typo-tolerant, via `difflib`, similarity ≥ 0.87 by
     default)

  Every non-exact match is logged with the tier that selected it. To verify
  a fuzzy/substring match before access is granted, run the workflow in dry-run
  mode; a scheduled non-dry run proceeds immediately after logging the match.
  *first* matching key is used, so a combined-topic day (e.g. "Discovery +
  Prototyping") needs its own explicit combined entry in the mapping file if
  it should grant more than one repo — otherwise only the first partial
  match's repo(s) get granted.
- **Granting access:** calls
  `PUT /orgs/{org}/teams/{team_slug}/repos/{owner}/{repo}` with
  `{"permission": "pull"}` for each resolved repo. This call is idempotent —
  re-running it is always safe — but it **sets** the permission rather than
  only raising it, so if a repo was manually granted something higher than
  `pull` beforehand, a sync run will quietly reset it back to `pull`.
- **Safety:** topics with no mapping entry (at any matching tier) are
  skipped with a log message rather than failing the run.

### `.github/scripts/repo_access_mapping.yml`

The link between calendar event titles and internal GitHub repos. Key
points:

- Keyed by the **exact calendar topic text** — the same keys used in
  `topic_mapping.yml` — not by `_toc.yml` file paths.
- Entry formats:
  1. Plain string — same repo for both tracks
  2. List — multiple repos granted for one topic
  3. Dict with `aipm`/`ds` keys — tracks need genuinely different repos for
     the same calendar day (resolved via the `COHORT_TRACK` variable)
- Purely non-technical days (career sessions, "Time for Career", policy
  discussions, Graduation, personal-reflection exercises, etc.) have no repo
  and are simply left out of the mapping.
- A commented-out `TODO` block tracks topics with no confirmed repo yet.

### `.github/scripts/calendar_utils.py`

Shared logic used by **both** automations, so they never drift out of sync
with each other:

- `get_target_date()` — next-weekday resolution, with `TARGET_DATE`
  override for testing
- `get_topics_for_date()` — fetches and parses the `.ics` feed
- `resolve_file_paths()` — resolves string/list/dict-with-track mapping
  entries (used for both `_toc.yml` file paths and, via
  `sync_team_repo_access.py`'s `resolve_repos()`, for repo names too)
- `find_mapping_key()` — the tiered exact → normalized → substring → fuzzy
  matcher described above

### `.github/scripts/requirements.txt`

Python dependencies: `requests` (fetch the calendar and call the GitHub
API), `icalendar` (parse the `.ics` feed), `pyyaml` (read the mapping
files).

## One-time setup

Unlike the ToC automation, this one needs an **org-admin-level credential**,
which has a different setup story depending on whether this repo is a
one-off or a template used to spin up new cohort repos.

### Org-level (set once, ever — not per repo) -> **is DONE at ORG level**

Because `ds-book-template` is used to generate a new repo per cohort, and
**repository secrets/variables are not copied when a repo is created from a
template**, the org-wide constants should live at the **organization**
level instead, so every future cohort repo inherits them automatically with
zero setup:

1. **github.com/organizations/neuefische/settings/secrets/actions →
   Secrets → New organization secret**
   - Name: `ORG_ADMIN_TOKEN`
   - Value: a Personal Access Token with `admin:org` + `repo` scopes
     (classic), or an equivalent fine-grained token with org **Members**
     (write) and repo **Administration** (write) — belonging to someone
     with real org-owner/admin rights. This **cannot** be the default
     `GITHUB_TOKEN`.
   - Repository access: **All repositories** — this is what makes it
     available to every future cohort repo automatically.
2. Same page, **Variables → New organization variable**
   - Name: `GH_ORG`
   - Value: `neuefische`
   - Repository access: **All repositories**

This token is not tied to any specific team — `admin:org` covers all teams
in the org, including ones created after the token itself. It only ever
needs replacing if it's rotated/expired, not per cohort.

### Per-repo (set once per new cohort repo)

1. **Repo → Settings → Secrets and variables → Actions → Secrets tab → New
   repository secret**
   - `GCAL_ICS_URL` — same secret iCal address used by the ToC automation
2. **Variables tab → New repository variable**, add both:
   - `COHORT_TRACK` — `aipm` or `ds`
   - `TEAM_SLUG` — the cohort's GitHub Team slug (from the team's URL,
     `github.com/orgs/neuefische/teams/<this-part>`)

Update `TEAM_SLUG` (and `COHORT_TRACK`/`GCAL_ICS_URL` if either changes)
once per new cohort.

### Optional: adjusting the access level

By default, teams get **read-only (`pull`)** access — appropriate since
these are template repos students use via "Use this template," not repos
they push to directly. To grant a different level, add a repo variable:

- `TEAM_PERMISSION` — `pull` (default), `push`, or `admin`

## Testing it manually

Use the **Run workflow** button on the `Sync cohort team repo access`
workflow in the Actions tab:

- Leave `test_date` blank to check "the next weekday," or set it to a
  specific `YYYY-MM-DD` to simulate a given day.
- Leave `dry_run` set to `true` (the default) to see what *would* be granted
  in the workflow logs, without calling the GitHub API.
- Set `dry_run` to `false` to actually grant access for real.

Check the logs for `[normalized match]`, `[substring match]`, or `[fuzzy
match]` lines — these flag any topic that didn't match its mapping key
exactly, so you can confirm the match was correct (or fix the mapping if
not).

## Maintaining the mapping

When a new internal repo needs to be granted for a topic, add an entry to
`repo_access_mapping.yml` using the calendar event's exact title as the key.
If a topic combines two concepts that already have their own separate
entries (e.g. "Discovery + Prototyping"), add an explicit combined entry
covering both repos rather than relying on substring matching to catch it —
substring matching only returns the first match, so a combined day with two
split-key entries will silently grant only one of the two repos. Topics with
no internal repo don't need an entry at all.