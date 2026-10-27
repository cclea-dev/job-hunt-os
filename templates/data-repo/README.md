# My job hunt data

The data for my [Job Hunt OS](https://github.com/cclea-dev/job-hunt-os), stored as plain files (the **files** storage option). Keep this repo **private**: it holds your CV details and job search.

## Set up

1. Create a new **private** GitHub repo from this folder (copy the files in, or use it as a template).
2. Fill in `profile.md`.
3. Point your Job Hunt OS scheduled runs at this repo, with the instructions to use `config/storage/files.md`.

## What's here

| File or folder | Holds | Who edits it |
|---|---|---|
| `profile.md` | Your search criteria, CV links and context | You |
| `recommendations/` | Roles the weekly job recommendations run found, one file each | The search adds them; you set `decision` |
| `jobs/` | Your pipeline, one file per job, with its fit analysis | The runs, and you (`status`, `applied_on`, CV requests) |
| `cv-log/` | CV drafts and reviews | The runs |
| `companies.md` | Companies you're interested in, and your dream companies | The runs, and you (only you set Dream company) |
| `contacts.md` | Your network | Only you |
| `runs.md` | A log of each automated run | The runs |
| `search-memory.md` | Postings already checked and ruled out | The runs |

Day to day, ask Claude in chat: "show this week's recommendations", "approve 1 and 3, skip 2 as too junior", "what's in my pipeline?".
