# Storage: files

Your data lives as Markdown files in a **private GitHub repo of your own** (the "data repo"), started from [`templates/data-repo/`](../../templates/data-repo/). There's no other tool: you read and decide in chat with Claude, or in GitHub's file editor. This file says how each operation works on those files. See `README.md` in this folder for how it compares with Notion.

## The data repo

```
job-hunt-data/                  private repo, yours
├── profile.md                  search criteria, CV links, context (same sections as config/profile.example.md)
├── recommendations/            one file per suggested role
│   └── 2026-10-26-acme-senior-product-manager.md
├── jobs/                       one file per job in your pipeline
│   └── acme-senior-product-manager.md
├── cv-log/                     one file per CV draft or review
│   └── 2026-10-27-draft-acme.md
├── cv/                         only if your CVs are Markdown, not Google Docs
│   ├── master.md
│   └── drafts/
├── companies.md                companies you're interested in, one table row each
├── contacts.md                 your network (only you edit it)
├── runs.md                     one table row per automated run, newest first
└── search-memory.md            postings already checked and ruled out
```

**File names:** lowercase, words joined with `-`, no accents: `<company>-<role>`, shortened to about 60 characters. Recommendations and CV Log entries start with the date (`YYYY-MM-DD-`). If a name is taken, add `-2`.

**Records are front matter plus a body.** Each recommendation, job and CV Log file starts with YAML front matter (the fields), then Markdown sections (the job description, the fit analysis, the CV feedback), exactly as the Notion page bodies would hold them.

```markdown
---
role: Senior Product Manager
company: Acme
city: Lisbon
work_mode: Hybrid
source: Career page
posting_url: https://jobs.ashbyhq.com/acme/...
lead_url:
posted_on: 2026-10-13
found_on: 2026-10-26
min_years_required: 7
why_it_matched: "Owns the onboarding product end to end · B2B SaaS · Asks for 7+ years"
decision: pending        # pending · approved · skipped (yours to set)
skip_reason:             # yours to set: Too junior · Too senior · Wrong function · Location · Industry · Company · Language · Already applied · Other
skip_note:               # yours to set
job:                     # path of the job file, set when the role is promoted
---

## Job description
...
```

**Job fields:** `role`, `company`, `status` (Approved · Analyzed · CV drafted · Applied · Recruiter screen · Interviewing · Offer · Rejected · Withdrawn, or empty), `city`, `work_mode`, `posting_url`, `recommendation` (path, empty for jobs you added), `min_years_required`, `fit_rating`, `fit_score`, `analyzed_on`, `applied_on`, `cv_draft_request` (true/false), `cv_review_request` (true/false), `cv_work` (list of CV Log paths). Body: `## Job description`, then `## Fit analysis`.

**CV Log fields:** `title`, `type` (CV draft · CV review), `job` (path), `cv` (link or path), `last_run`, `summary`. Body: the change log or the review table, as the CV skills describe.

**Tables** (`companies.md`, `runs.md`) are Markdown tables with the same columns as the Notion databases. `search-memory.md` keeps the `## Ruled out` list: one line per posting, `date · reason · link`.

## Fields automations must never write

| File | Field |
|---|---|
| recommendations/ | `decision`, `skip_reason`, `skip_note` |
| jobs/ | `applied_on`. `status` only through the forward steps below |
| companies.md | the Dream company column |
| contacts.md | the whole file |

**Job status forward steps.** Automations may set `status` to `Approved` (job created from an approved recommendation), `Analyzed` (fit analysis saved) or `CV drafted` (draft saved), and only when the current status is empty or earlier in that sequence. Never when it's `Applied` or later, `Rejected` or `Withdrawn`, and never backwards.

**Request flags** (`cv_draft_request`, `cv_review_request`) are set to `true` by the user and back to `false` by the `cv-requests` run once the work is saved. `true` always means "not done yet". If the work fails, the flag stays `true` and the next run retries.

## Saving changes

- **Pull before you read, commit after you write.** Every run starts from the latest data repo, and ends with one commit to its default branch with a plain message, e.g. `Weekly job recommendations 2026-10-26: 5 recommendations` or `JD enrichment: 2 jobs analyzed`. Push it.
- **Only the data repo, only these folders.** Runs never commit to the job-hunt-os repo or any other repo (see `config/safety.md`).
- **If the push is rejected** because the user changed something meanwhile: pull, redo only the edits that still apply (never overwrite the user's fields), and push again once. If it still fails, log it in the run's Errors.
- **In chat**, when the user makes a decision ("approve 1 and 3, skip 2 as too junior"), Claude edits those fields for them and commits with a message naming the change. These are the user's own edits, made on their request.

## Operations

| Operation | How with files |
|---|---|
| Read profile | Read `profile.md`; each section by its heading |
| Read story bank | If the profile's "Story bank" line has a link or path, read it (a Google Doc via Google Docs, or a file in the data repo); otherwise skip |
| Read master CV | The profile's "Master CV": a Google Doc link (read with Google Docs) or `cv/master.md` |
| Add a recommendation | Create `recommendations/<date>-<company>-<role>.md` with the fields above, `decision: pending`, and the `## Job description` section |
| Find duplicates | Search `recommendations/` and `jobs/` for the same `posting_url`, or the same company and role |
| Read skip reasons | Recommendations with `decision: skipped` and `found_on` within the last 8 weeks. Ignore `skip_reason: Already applied` |
| Find approvals to promote | Recommendations with `decision: approved` and an empty `job` |
| Promote an approval | Create `jobs/<company>-<role>.md` (role, company, posting_url, city, work_mode, min_years_required, `status: Approved`, `recommendation:` the recommendation's path) with its `## Job description` section; set the recommendation's `job:` to the new path. Add the company to `companies.md` if it's missing |
| Find manual adds | Job files with an empty `recommendation` and no `## Job description` section |
| Find companies to fill in | Rows in `companies.md` with empty Careers URL and Industry |
| Find jobs to analyze | Job files with an empty `analyzed_on` and a `status` other than `Withdrawn` or `Rejected` |
| Read job description | The job file's `## Job description` section. If it's missing and the posting can't be read, add a note at the top of the body asking the user to paste the job description |
| Save fit analysis | Write the `## Fit analysis` section (replace it on a re-run). Set `fit_rating`, `fit_score`, `analyzed_on`; set `status: Analyzed` if it's empty or `Approved` |
| Find CV draft requests | Job files with `cv_draft_request: true`. After saving the draft, set `status: CV drafted` if it's empty, `Approved` or `Analyzed` |
| Find CV review requests | Job files with `cv_review_request: true`. Review the CV in the job's latest `cv_work` entry that has a `cv`; if none, the master CV |
| Clear a request | Set the flag back to `false` once the draft or review is saved |
| Store a CV draft | If the master CV is a Google Doc: copy it into the Drive folder named in the profile's CV preferences, as with Notion. If it's `cv/master.md`: copy it to `cv/drafts/<name>.md`, named by the profile's naming rule |
| Save CV work | Create or update `cv-log/<date>-<type>-<company>.md`; add its path to the job's `cv_work`. Re-runs on the same CV and job update the same file |
| Link or create a company | Match by name in `companies.md`; add a row if missing. Fill Industry, Stage, Careers URL, Job board system, Cities when empty |
| List dream companies | Rows in `companies.md` with `yes` in Dream company (10 at most) |
| Read search memory | `search-memory.md`, the lines under `## Ruled out` |
| Update search memory | Append `date · reason · link` lines for postings ruled out this run; delete lines older than 8 weeks |
| Log a run | Add a row at the top of the table in `runs.md`: Run, Type, Started, Sources checked, Found, Filtered out, Filter breakdown, Recommended, Searches used, Postings read, Duration (min), Model, Errors |

## Working in chat

Typical requests, which Claude answers from the files and, for decisions, by editing them:

- "Show this week's recommendations": list the pending ones, numbered, with role, company, city and why they matched.
- "Approve 1 and 3, skip 2 as too junior": set `decision` (and `skip_reason`), then commit.
- "What's in my pipeline?": jobs grouped by status, with fit ratings.
- "Draft a CV for the Acme job" or "tick a CV review for Globex": run the skill now, or set the flag for the next weekday run.
