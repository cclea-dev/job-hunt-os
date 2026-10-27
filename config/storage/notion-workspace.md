# Notion workspace structure

The structure of the [Job Hunt OS Notion template](https://mica-waxflower-6c3.notion.site/Job-Hunt-OS-Template-3febf806381381fb9277e4de33ccd0b4), which `notion.md` expects to find. Setup duplicates the template; this file is the fallback for building it by hand with the Notion connector, and the reference for repairing a workspace. Build it in this order, so relations can point at databases that already exist. Every field gets the description shown (Notion shows it as the field's tooltip). Names must match exactly: the skills find things by name.

## Page tree

```
Job Hunt OS                (page, icon 🧭)
├── Profile                (page, icon 👤) – filled from config/profile.example.md
├── Recommendations        (database, 📥)
├── Jobs                   (database, 💼)
├── Companies              (database, 🏢)
├── Contacts               (database, 🤝)
├── CV Log                 (database, 📝)
├── Runs                   (database, 📜)
└── Search memory          (page, icon 🧠)
```

**Job Hunt OS page body:** a short callout ("Every skill reads the Profile page. Automations never change Decision or Outreach status. Job Status moves forward automatically to Approved, Analyzed and CV drafted; everything from Applied onwards is yours.") and a numbered "How it works" list: Recommendations (every Monday, set Decision to Approved or Skipped, with a Skip reason), Jobs (approved roles plus your own adds, analyzed the next weekday morning), CV Log, Companies (filled in automatically; tick Dream company for up to 10 to check every week), Contacts (yours), Runs.

**Search memory page body:** a gray callout ("Maintained by the weekly job recommendations run: postings already checked and ruled out, one line each: date · reason · link. Lines older than 8 weeks are removed.") and an empty `## Ruled out` heading.

Every database keeps its automatic **Default view** (a table with no filters): the scheduled runs read through it, so never filter or delete it.

## 1. Companies

| Field | Type | Options | Description |
|---|---|---|---|
| Name | Title | | Company name. Kept as a record of the companies you are interested in; tick Dream company to have its careers page checked every week |
| Dream company | Checkbox | | Tick for companies you most want to work for (10 at most). The weekly job recommendations run checks their careers pages every Monday. Other companies are kept as a record but not checked |
| Industry | Select | the Profile's preferred industries, plus Other | Filled in automatically |
| Stage | Select | Scale-up, Enterprise | Filled in automatically |
| Cities | Multi-select | the Profile's target locations, plus Remote | Where the company hires, among your target locations. Filled in automatically |
| Careers URL | URL | | The company's jobs page. Checked every Monday for dream companies. Filled in automatically |
| Job board system | Select | Greenhouse, Lever, Ashby, SmartRecruiters, Personio, Workable, Teamtailor, Workday, Other | The software behind the careers page; tells the search how to read it. Filled in automatically |
| Notes | Text | | Your own notes about the company |

## 2. Recommendations

| Field | Type | Options | Description |
|---|---|---|---|
| Role | Title | | Job title from the posting |
| Company name | Text | | Company name from the posting. Linked to Companies once you approve |
| City | Select | the Profile's target locations (e.g. each city, Remote (country), Remote (EU)) | From the posting |
| Work mode | Select | Hybrid, Remote, Onsite | From the posting |
| Source | Select | Company job boards, Career page, plus one per additional source on the Profile | Where the weekly job recommendations run found this role. Company job boards = the search across job-board systems like Greenhouse and Lever (not individual companies' pages). Additional sources appear by name |
| Posting URL | URL | | Link to the full job posting, preferably on the company's own careers page |
| Lead URL | URL | | Where the role was first spotted, e.g. a search result or aggregator page. Empty if same as Posting URL |
| Posted on | Date | | When the company published the posting |
| Found on | Date | | When the weekly job recommendations run found it |
| Min years required | Number | | Lowest years of experience the posting asks for |
| Why it matched | Text | | 2–3 reasons this role fits your criteria (and the salary, if listed). This is a quick match, not the full fit analysis |
| Decision | Select | Pending, Approved, Skipped | Your decision. Set by you only. Approved roles are added to Jobs |
| Skip reason | Select | Too junior, Too senior, Wrong function, Location, Industry, Company, Language, Already applied, Other | Why you skipped it. The weekly job recommendations run learns from these (except Already applied) |
| Skip note | Text | | Optional: more detail on why you skipped it |

**View:** "Inbox", a gallery filtered to Decision = Pending, sorted by Found on (newest first), showing Company name, City, Work mode, Why it matched.

## 3. Jobs

| Field | Type | Options | Description |
|---|---|---|---|
| Role | Title | | Job title. Fill in when adding a job yourself |
| Company | Relation → Companies (two-way, "Jobs" on Companies) | | The company. Fill in when adding a job yourself: pick one, or type a new name and its details are filled in automatically |
| Recommendation | Relation → Recommendations (two-way, "Job" on Recommendations) | | The weekly recommendation this job came from (where it was found, why it matched). Empty if you added the job yourself |
| Posting URL | URL | | Link to the job posting. Fill in when adding a job yourself |
| Status | Select | Approved, Analyzed, CV drafted, Applied, Recruiter screen, Interviewing, Offer, Rejected, Withdrawn | Where this job is in your pipeline. Set automatically to Approved, Analyzed and CV drafted as those steps finish (forward only); everything from Applied onwards is set by you and never changed by automations |
| City | Select | same as Recommendations | Filled in automatically from the posting |
| Work mode | Select | Hybrid, Remote, Onsite | Filled in automatically from the posting |
| Min years required | Number | | Lowest years of experience the posting asks for. Filled in automatically |
| Fit rating | Select | High, Medium, Low | Overall fit against your CV, from the fit analysis. The full analysis is in the page body |
| Fit score | Number | | Fit from 0 to 100, for sorting jobs with the same rating |
| Analyzed on | Date | | When the fit analysis ran. Empty = not analyzed yet; the next JD enrichment run (weekdays 07:00) will analyze it |
| Applied on | Date | | The date you applied |
| CV draft request | Checkbox | | Tick to request a tailored CV for this job. Requests run weekdays 08:00. Unticked automatically once done; tick again to re-run |
| CV review request | Checkbox | | Tick to have the next CV requests run (weekdays 08:00) review this job's CV (from its CV Log entry, or your master CV if there is none) against the job. Unticked automatically once done; tick again to re-run |
| Contacts | Rollup: Company → Contacts (show original) | | People you know at this job's company, from Contacts. To add one, link the contact to the company. Add it after Contacts is built |

**Views:** "Pipeline", a board grouped by Status, sorted by Fit score (highest first); "Stalled", Status = Analyzed and Analyzed on before one week ago.

## 4. Contacts

| Field | Type | Options | Description |
|---|---|---|---|
| Name | Title | | Contact's name. This database is filled in by you only |
| Company | Relation → Companies (two-way, "Contacts" on Companies) | | Where they work |
| Relationship | Select | School alum, Company alum, Event, Warm intro | How you know them |
| LinkedIn URL | URL | | Their LinkedIn profile |
| Outreach status | Select | To contact, Contacted, Replied, Had a call, Referred, No response | Where your outreach stands. Set by you only |
| Last contact | Date | | When you last reached out or spoke |
| Next follow-up | Date | | When to follow up. Shows in the Follow-ups view once due |
| Notes | Text | | Your notes |

**View:** "Follow-ups", Next follow-up on or before today.

## 5. CV Log

| Field | Type | Options | Description |
|---|---|---|---|
| Title | Title | | What this entry is, e.g. "Review: Acme – Product Ops Manager" |
| Type | Select | CV draft, CV review | CV draft: a tailored CV was created for a job. CV review: line-by-line feedback on a CV, which is never edited |
| Job | Relation → Jobs (two-way, "CV work" on Jobs, described "CV drafts and reviews for this job, in the CV Log") | | The job this draft or review is for. Empty for a review of your master CV |
| CV | URL | | Link to the Google Doc that was drafted or reviewed |
| Last run | Date | | When the draft or review was last run. Re-running on the same CV updates this entry |
| Summary | Text | | One-line verdict. Full details are in the page body |

## 6. Runs

| Field | Type | Options | Description |
|---|---|---|---|
| Run | Title | | Name of the run, e.g. "Weekly job recommendations – 2026-10-26" |
| Type | Select | Weekly job recommendations, JD enrichment, CV requests | Which automated run this was |
| Started | Date | | When the run started |
| Sources checked | Number | | How many job sources were checked (weekly job recommendations only) |
| Found | Number | | New postings found before filtering |
| Filtered out | Number | | Postings dropped by your criteria |
| Filter breakdown | Text | | How many postings each filter dropped, e.g. "Location: 12, Too senior: 5" |
| Recommended | Number | | How many roles were added to Recommendations |
| Searches used | Number | | Web searches run (weekly job recommendations budget: about 12) |
| Postings read | Number | | Full postings opened and checked (weekly job recommendations budget: about 20) |
| Duration (min) | Number | | How long the run took, in minutes |
| Model | Text | | Claude model that ran it |
| Errors | Text | | Anything that went wrong in this run, e.g. a source that could not be read |

## Notes for building it with the Notion connector

- Create the databases with `notion-create-database` (one per call), add descriptions with `ALTER COLUMN … COMMENT`, and two-way relations with `RELATION('<data source>', DUAL '<name on the other side>')`.
- When changing a select later, restate **every** option you want to keep: options left out are removed.
- Fields added through the connector can be hidden in existing views; add them to the view's shown properties.
