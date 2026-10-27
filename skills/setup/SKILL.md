---
name: setup
description: Set up the Job Hunt OS for a new user, step by step - choose where data is stored (Notion or files in a private repo), fill in the Profile, connect the CV, seed the Companies list, and create the cloud scheduled runs. Use when someone wants to start using the Job Hunt OS, or to rebuild or repair their setup.
---

# Setup

Walks a new user through everything the Job Hunt OS needs, in conversation. It does the parts Claude can do, and gives clear, one-step-at-a-time instructions for the parts only the user can do (account settings, permissions, network access). Expect 30–45 minutes, most of it the Profile.

**Safety:** follow `config/safety.md`. Setup changes the user's accounts, so **say what you'll create before creating it**, and never change sharing, permissions, network or account settings yourself: walk the user through those.

## Before starting

Tell the user what they'll end up with (weekly recommendations, fit analyses, CV drafts and reviews, all running in the cloud) and what they need:
- A **Claude** plan with Claude Code cloud sessions (Pro or above).
- A **GitHub** account (to give the scheduled runs access to the skills).
- Either a **Notion** account or nothing else (files storage).
- Their **CV**, ideally as a Google Doc (Google Docs and Google Drive connectors), or as Markdown.

Then go through the steps in order, and confirm each one is done before the next. If the user stops halfway, the steps are safe to resume: check what already exists first.

## 1. Choose where the data lives

Explain the two options from `config/storage/README.md` in two or three sentences each (Notion: boards, filters, phone app; files: a private GitHub repo, everything in chat with Claude) and ask which one they want. Recommend Notion for people who like to see and click things, files for people who'd rather only talk to Claude.

## 2. Create the storage

**Notion:**
1. Check the Notion connector is connected (search for anything). If not, ask the user to add it at claude.ai → Settings → Connectors, then continue.
2. Check there's no existing page named "Job Hunt OS"; if there is, ask whether to use it (repair it against `config/storage/notion-workspace.md`) or start fresh.
3. Ask the user to open the **[Job Hunt OS Notion template](https://mica-waxflower-6c3.notion.site/Job-Hunt-OS-Template-3febf806381381fb9277e4de33ccd0b4)**, choose **Duplicate** (top right), pick their workspace, and rename the copy from "Job Hunt OS (Template)" to **"Job Hunt OS"**: the skills find it by that name. Wait until they say it's done, then find the page and check that the six databases and the Profile and Search memory pages are there.
4. The template's select options (cities, industries, sources) are examples. Update them after step 3, once the Profile gives the real ones: restate every option to keep, since options left out are removed.
5. **Fallback**, only if the template can't be duplicated: build the page tree and the six databases from `config/storage/notion-workspace.md`, in its order, with every field description, select option and view it lists. This takes many more steps, so say so first.

**Files:**
1. Ask the user to create a new **private** GitHub repo (e.g. `job-hunt-data`), and copy in the contents of `templates/data-repo/` (with `gh` if it's available and they agree: `gh repo create <name> --private`, then push the template files). Never make it public.
2. Confirm you can read and write it (clone it, check the folders).

## 3. Fill in the Profile

The Profile is what every skill reads, so do it carefully, as an interview, one section at a time. Use the section list in `config/profile.example.md`:
- **Target roles** and **scope**, **seniority** (titles and years, what's too junior and too senior), **locations and work mode**, **languages** (and which posting languages to filter out), **compensation** minimums per location (used only when a posting lists salary), **company rules** (stage, type), **preferred industries** with example companies, **additional sources** (optional), **context** (what they're optimizing for).
- Ask for examples when an answer is vague ("operations" → which kind?). Don't invent criteria.
- Write it to the Profile page (Notion) or `profile.md` (files), then read it back to the user and fix anything they correct.

## 4. Connect the CV

1. Ask for the **master CV**: a Google Doc link (recommended; drafts keep its formatting) or a Markdown file for files storage. Add it under "Master CV".
2. Ask for **CV preferences**: anything left out on purpose (e.g. contact details), the drafts folder (Google Drive folder name or `cv/drafts/`), and the draft file name pattern. Add them under "CV preferences".
3. Ask whether they have a **story bank** (a doc of achievements and examples). If yes, add its link under "Story bank".
4. Read the CV once to check access works.

## 5. Seed Companies

From the Profile's preferred industries and example companies, add each company to Companies (name, industry, stage). Then ask whether any are **dream companies** whose careers pages should be checked every week (10 at most; none is fine), and tick Dream company for those. For each, find its careers page and job-board system (Greenhouse, Lever, Ashby, SmartRecruiters and others; see `config/sources.md`), and fill Careers URL and Job board system. Keep it light: about one search per company. Companies without a public job board still go on the list.

## 6. Set up the scheduled runs

Follow `config/schedules.md`. The user does the account steps; you create the runs.
1. **GitHub access:** the user installs the Claude GitHub app for this repo (their fork or copy of job-hunt-os) and, with files storage, their data repo: https://github.com/apps/claude/installations/new
2. **Cloud environment:** walk the user through creating an environment named "Job Hunt" with Custom network access and the allowed domains in `config/schedules.md` (claude.ai/code → environment selector under the message box → New environment). Add their additional sources' sites.
3. **Connectors:** check the connectors each run needs are connected at claude.ai → Settings → Connectors.
4. **Create the three runs** with the instructions in `config/schedules.md`, filling in `<STORAGE>`, their time zone, the Job Hunt environment and only the listed connectors. Create them **switched off**. (In Claude Code, use the `schedule` skill or `/schedule`; otherwise give the user the settings to enter at claude.ai/code/routines.)
5. **Check:** create a one-off read-only check run as described in `config/schedules.md`, run it, and read its result with the user. Fix anything that fails (usually a missing allowed domain or connector), then switch the three runs on.

## 7. Wrap up

Summarize what was set up, with links (workspace or data repo, scheduled runs), and what happens next:
- **Monday 06:00:** the first recommendations. Set each one's Decision to Approved or Skipped, with a Skip reason (in Notion, or in chat with files storage).
- **Weekdays 07:00:** approved roles become jobs with a fit analysis (approve before 07:00 on Monday to get them the same morning).
- **Weekdays 08:00:** CV drafts and reviews for jobs where they ticked a request.
- Anytime in chat: "analyze this posting <link>", "draft a CV for <job>", "review my CV".

Offer to run the first weekly job recommendations now (the `weekly-job-recos` skill), so they don't have to wait until Monday.
