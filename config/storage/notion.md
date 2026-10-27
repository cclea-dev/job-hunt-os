# Storage: Notion

Skills describe **what** to do with your data ("read the profile", "save the analysis to the job"). This file says **how** to do it in Notion. The other option, plain files in a private repo, is `files.md`; see `README.md` in this folder to compare them. The skills don't need to change.

## Finding the workspace

- The workspace is a Notion page named **Job Hunt OS** (built by the `setup` skill from `notion-workspace.md`).
- Find databases and the Profile page **by name**, under that page. Never hard-code Notion IDs in the repo: they identify a personal workspace.
- **Read databases through a view when you can.** On Notion plans below Business, SQL queries share a small hourly allowance across the whole workspace (all scheduled runs draw on the same allowance), and a query that joins several databases needs Business. View mode (`notion-query-data-sources` with `mode: "view"` and the database's unfiltered **Default view**, found by fetching the database) has no such quota: read the whole database that way and filter in memory. Use SQL only for what a view can't do, one database per query, and never in a loop.

| Name | Type | Holds |
|---|---|---|
| Profile | Page | Search criteria, master CV link, context about the user |
| Recommendations | Database | Weekly suggested roles awaiting a decision |
| Jobs | Database | Approved roles and manual adds: the pipeline |
| Companies | Database | One page per company: a record of the user's interests. *Dream company* marks the ones checked every week |
| Contacts | Database | The user's network (user-maintained only) |
| CV Log | Database | CV drafts and CV reviews |
| Runs | Database | One row per automated run |

## Fields automations must never write

| Database | Field |
|---|---|
| Recommendations | Decision, Skip reason, Skip note |
| Jobs | Applied on. **Status** only through the forward steps below |
| Companies | Dream company |
| Contacts | Every field |

**Job Status forward steps.** Automations may set Status to `Approved` (job created from an approved recommendation), `Analyzed` (fit analysis saved) or `CV drafted` (draft saved), and only when the current Status is empty or earlier in that sequence. Never set Status when it's `Applied`, `Recruiter screen`, `Interviewing`, `Offer`, `Rejected` or `Withdrawn`, and never move it backwards.

**Request checkboxes** (*CV draft request*, *CV review request*) are ticked by the user and unticked by the `cv-requests` run once the work is saved, so the user can tick again to re-run. A ticked box always means "not done yet". If the work fails, the box stays ticked and the next run retries.

## Operations

| Operation | How in Notion |
|---|---|
| Read profile | Fetch the Profile page; read each section by its heading |
| Read story bank | If the Profile's "Story bank" line has a link, read that document (Google Docs or Drive); otherwise skip |
| Read master CV | Take the Google Doc link under "Master CV" on the Profile page; read it with the Google Docs connector |
| Add a recommendation | Create a page in Recommendations: Role, Company name, City, Work mode, Source, Posting URL, Lead URL, Posted on, Found on, Min years required, Why it matched, Decision = `Pending`. Job description goes in the page body. |
| Find duplicates | Query Recommendations and Jobs for the same Posting URL, or the same company and role |
| Read skip reasons | Query Recommendations where Decision = `Skipped`, Found on within the last 8 weeks. Ignore Skip reason = `Already applied`: it says nothing about fit |
| Promote an approval | For a Recommendation with Decision = `Approved` and empty Job: create a Jobs page (Role, Posting URL, City, Work mode, Min years required, Status = `Approved`, Recommendation = that page), copy the Job description section into the body, link Company |
| Find approvals to promote | Query Recommendations where Decision = `Approved` and Job is empty |
| Find manual adds | Query Jobs where Recommendation is empty; of those, the ones whose page body has no Job description section |
| Find companies to fill in | Query Companies where Careers URL and Industry are both empty |
| Find jobs to analyze | Query Jobs where Analyzed on is empty and Status isn't `Withdrawn` or `Rejected` |
| Read job description | The Jobs page body. If it's empty and Posting URL can't be read, add a note at the top of the body asking the user to paste the job description |
| Save fit analysis | Write the readable analysis to the Jobs page body. Set Fit rating, Fit score, Analyzed on. Set Status = `Analyzed` if it's empty or `Approved` |
| Find CV draft requests | Query Jobs where CV draft request = ✓. After saving the draft, set Status = `CV drafted` if it's empty, `Approved` or `Analyzed` |
| Find CV review requests | Query Jobs where CV review request = ✓. Review the CV linked in the job's most recent CV Log entry (*CV work*) that has a CV link; if there is none, the master CV. If that entry is a review with an empty body (the user created it to request this review), fill it in rather than creating a new one |
| Clear a request | Untick the request checkbox once the draft or review is saved |
| Store a CV draft | Copy the master CV (Google Docs) into the Google Drive folder named in the Profile's CV preferences (default `Job Hunt/Tailored CVs`, created if missing), named by the Profile's naming rule (default `<Name>_CV_<Company>`, plus `_<Role>` only for several jobs at one company) |
| Save CV work | Create or update a CV Log page: Title, Type, Job, CV, Last run, Summary; details in the page body. Re-runs on the same CV and job update the existing page |
| Link or create a company | Match by name in Companies; create it if missing. Fill Industry, Stage, Careers URL, Job board system, Cities when empty |
| List dream companies | Pages in Companies with Dream company = ✓ (10 at most; if more are ticked, use the first 10 and note it in the run's Errors) |
| Read search memory | Fetch the "Search memory" page; each line under Ruled out is date · reason · link |
| Update search memory | Append lines (date · reason · link) for postings ruled out this run; delete lines older than 8 weeks |
| Log a run | Create a page in Runs: Run, Type, Started, Sources checked, Found, Filtered out, Filter breakdown, Recommended, Searches used, Postings read, Duration (min), Model, Errors |
