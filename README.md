# Job Hunt OS

A personal operating system for your job search, built on Claude, with your data in Notion or in plain files, and CVs in Google Docs.

- **Weekly job recommendations:** every Monday it finds 3–10 new roles that match your criteria. You approve or skip each one.
- **Fit analysis:** each approved role gets a High / Medium / Low rating against your CV, with the matches, the gaps and how severe each gap is.
- **CV drafter:** a tailored CV draft for a specific role, built only from your real experience.
- **CV reviewer:** line-by-line feedback on any CV. It never edits the CV itself.

## Get started

Open Claude Code in a copy of this repo and ask: **"Set up my Job Hunt OS."** The `setup` skill walks you through it in about 30–45 minutes: where to store your data, your search criteria, your CV, and the scheduled runs. See [skills/setup](skills/setup/SKILL.md) for the steps.

Using Notion? Setup starts from the **[Job Hunt OS Notion template](https://mica-waxflower-6c3.notion.site/Job-Hunt-OS-Template-3febf806381381fb9277e4de33ccd0b4)**: open it and choose **Duplicate** to copy it into your workspace.

## How it runs

Three scheduled runs do the work in the cloud, so your computer can be off:

- **Weekly job recommendations** (Mondays 06:00): adds new roles to Recommendations. Set each one's Decision to Approved or Skipped (with a Skip reason) in Notion, or tell Claude in chat with files storage.
- **JD enrichment** (weekdays 07:00): turns roles you approved into jobs, completes jobs you added yourself (job description, city, work mode, years), and runs the fit analysis on new jobs. Roles you approve before 07:00 on Monday are picked up the same morning; later approvals wait for the next weekday.
- **CV requests** (weekdays 08:00): does the CV drafts and reviews you've asked for. It's kept separate because it's the only run with Google Drive access, and it never reads web pages.

You make the decisions. The automations never change your Decision on a recommendation, and they only move a job's Status forward through their own steps (Approved, Analyzed, CV drafted), never once you've applied.

### Asking for a CV draft or review

Each job has two checkboxes: **CV draft request** and **CV review request**.

1. **Tick the box** on the job.
2. The next CV requests run (weekdays 08:00) does the work: a draft goes to your Drive folder, a review goes in the CV Log, and either one is linked to the job under *CV work*. A draft also moves the job's Status to *CV drafted*.
3. **The run unticks the box** once the work is saved. A ticked box always means "waiting to be done".
4. **To run it again**, e.g. after answering the drafter's questions in the CV Log, tick the box again. A re-run updates the same CV Log entry.

If the work fails (e.g. Drive can't be reached), the box stays ticked and the next run tries again; the failure is noted in Runs. Need it sooner? Ask Claude in chat ("draft a CV for the Acme job").

## How fit is rated

A posting is broken into **qualifications** (must-have or nice-to-have) and **responsibilities**. Each one is rated against your CV:

- **Qualifications:** Match · Partial (real but short: fewer years, less depth, a neighboring area, or a similar tool) · Gap
- **Responsibilities:** Done it · Adjacent · New. A responsibility that repeats a qualification counts once, under qualifications.

Shortfalls on qualifications get a severity: **Minor** (a nice-to-have), **Moderate** (a must-have you can credibly bridge), or **Critical** (a must-have you can't bridge before or during an interview, e.g. a required language).

**Fit score** = the share of the job your CV covers. Full credit for a Match or Done it, half for a Partial or Adjacent; nice-to-haves count half. **Rating:** High (75+), Medium (50–74), Low (below 50). One critical gap caps the rating at Medium, two or more at Low. See [the full rubric](config/rubric.md).

> **Status:** in daily use with Notion storage. The files storage option and the `setup` skill haven't been tried by a new user yet. See [the design doc](docs/design.md) for the full architecture and decisions.

## Structure

| Folder | What's inside |
|---|---|
| `skills/` | The Claude skills that do the work |
| `config/` | The fit rubric, the job sources, a profile template for new users, and storage files (`storage/`): how the skills read and write your data in Notion or in plain files. |
| `docs/` | Design doc and decision log |
| `templates/data-repo/` | A starting point for your private data repo, if you choose files storage |

Your personal data (CV, criteria, tracker) lives in your own storage, never in this repo: either **Notion** or **plain files in a private GitHub repo** of your own, for working only in Claude. See [config/storage/](config/storage/README.md).

**Safety:** the skills read web pages written by strangers, so they treat web content as data, never as instructions, and only write to your Job Hunt OS pages and drafts folder. See [config/safety.md](config/safety.md). For scheduled runs, use a cloud environment with **Custom** network access limited to job-board sites, and attach only the connectors each run needs (the weekly job recommendations run and JD enrichment need Notion and Google Docs; only CV requests, which reads no web pages, also gets Google Drive). Scheduled tasks can't yet block individual connector tools (such as Drive's share tool), so the instructions and the safety rules are what keep runs from sharing or deleting.
