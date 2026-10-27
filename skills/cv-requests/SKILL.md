---
name: cv-requests
description: The weekday run that does the CV work the user asked for. Drafts a tailored CV for each job with "CV draft request" ticked and reviews the CV for each job with "CV review request" ticked, then unticks the boxes. Use for the weekday scheduled run, or when the user asks to process pending CV requests.
---

# CV requests

Runs the `cv-drafter` and `cv-reviewer` skills for the jobs where the user ticked a request box. This run has Google Drive access (to copy the master CV into the drafts folder), so it **never reads web pages**: everything it needs is already in storage (the job description and fit analysis) and in the user's own documents.

Each step uses the user's storage file in `config/storage/` (see `config/storage/README.md`) for every data operation.

**Safety:** follow `config/safety.md`. Write only where the storage file says; never share, change permissions of, move, trash or delete any file or page.

## Rules

- **No web access.** Don't search the web or open postings or other web pages. Use the job's saved Job description and Fit analysis. If a job has no job description yet, skip it, leave the box ticked, and note it in the run log: the JD enrichment run will add it.
- **A ticked request box means "not done yet".** Untick it only once the work is saved. If the work fails, leave it ticked so the next run retries, and note the failure in the run log. The user ticks it again to re-run.
- **Job Status only moves forward:** a saved draft sets `CV drafted` if the job is empty, `Approved` or `Analyzed`. Reviews don't change Status. Never touch a job that's `Applied` or later, `Rejected` or `Withdrawn`.
- **Never write to Decision**, Applied on, Contacts, or any other field the storage file lists as user-only.
- **Don't wait for answers.** The run is unattended: the CV drafter's questions go in the CV Log entry, and the user re-ticks the box after answering.
- **One problem doesn't stop the run.** Note it and move on to the next job.

## Steps

1. **Find requests:** jobs with *CV draft request* or *CV review request* ticked (storage file: *Find CV draft requests*, *Find CV review requests*). If there are none, stop: no run log row.
2. **Load once:** the Profile, the master CV and the story bank (if the Profile links one).
3. **CV drafts.** For each job with *CV draft request* ticked, run the `cv-drafter` skill. If the job has no fit analysis yet, skip it and leave the box ticked (the JD enrichment run analyzes it first).
4. **CV reviews.** For each job with *CV review request* ticked, run the `cv-reviewer` skill on the CV the storage file points to (the job's latest CV Log entry with a CV link, or the master CV).
5. **Log the run** in Runs, Type = `CV requests`: in Filter breakdown, e.g. "CV drafts 1 · CV reviews 1"; Duration, Model, and Errors (requests skipped or failed, and why).
6. **Report** (only when run in chat): links to each draft and CV Log entry, and any questions the drafter left for the user.
