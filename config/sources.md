# Job sources

Used by `weekly-job-recos`. The search is **discovery-first**: its main job is to find roles and companies the user wouldn't have found or thought of themselves. Every user gets the **standard sources** below, built from their Profile (target roles, locations, languages, CV). It works with no other setup. Users can list **additional sources** on their Profile, and those are searched on top.

## Standard sources

### 1. Job-board system search

Most companies post jobs on a hosted job-board system (an "applicant tracking system"). Searching those systems' domains directly finds postings from any company using them, often before they reach aggregators.

**Domains:** always search the whole domain, never a single subdomain. Job-board systems use many subdomains (e.g. `jobs.eu.lever.co` for Lever's EU postings, `job-boards.greenhouse.io`, `careers-<company>.icims.com`), and a whole-domain search covers all of them.

```
site:ashbyhq.com · site:greenhouse.io · site:lever.co · site:icims.com · site:jobvite.com
site:bamboohr.com · site:smartrecruiters.com · site:jazz.co · site:workable.com
site:myworkdayjobs.com · site:taleo.net · site:personio.de · site:personio.com
site:teamtailor.com · site:recruitee.com · site:docs.google.com (low priority: many old documents)
```

**Query pattern:** one query per role term, with the location terms, e.g.

```
(site:ashbyhq.com OR site:greenhouse.io OR site:lever.co OR …) ("Product Manager" OR "Product Owner") ("Lisbon" OR "Porto" OR "Remote")
```

**Role terms**, generated each run (kept internal, not written to the Profile):
- **Target roles** from the Profile, with common spellings (e.g. "BD Manager" for "Business Development Manager")
- **Title variants:** other names for the same work, e.g. for product roles: "Product Owner", "Product Lead", "Technical Product Manager", "Growth Product Manager"; for sales and business development roles: "Partnerships Manager", "Account Executive", "Commercial Manager", "New Business Manager"
- **Emerging roles** that match the user's experience and interests from the CV and Profile, e.g. for a product manager who has shipped AI features: "AI Product Manager", "Applied AI Product Lead"; for a salesperson who has sold AI tools: "AI Solutions Consultant", "AI Partnerships Manager"

Never add a **work mode** clause ("remote" OR "hybrid") unless the Profile makes work mode a filter: it drops roles that don't say.

### 2. Skill-based search

Roles of any title whose posting asks for what the user has actually done. Build queries from the strongest themes in the CV (e.g. "product discovery" with "A/B testing", "pipeline generation" with "enterprise accounts"), with the same domains and locations. This finds roles under titles nobody would think to search.

### 3. Local-language search

When the user speaks a target location's language, also search with role terms in that language (e.g. for Spain: "Responsable de Producto", "Gerente de Desarrollo de Negocio", "Ejecutivo de Cuentas"). Many local companies post only in the local language. Language filters from the Profile still apply.

### 4. New companies

Find companies in the target locations that recently raised funding or are expanding (startup news sites and their funding round-ups, new office announcements; general web search for funding news works poorly), in the Profile's preferred stages and industries. Check their job boards now, and add promising ones to Companies as a record.

### 5. Dream companies

The careers pages of the companies the user ticked as **Dream company** in Companies (10 at most), checked every run through their job-board system where known, or by reading the page. Other companies in Companies are a record of the user's interests, not checked every week: the search is about finding what the user wouldn't find themselves. With no dream companies ticked, this source is skipped.

## Checking every result

Search engines lag and keep listing closed postings, and don't know when a posting went up. So **every result is opened and checked** before it counts: still open, posted since the last run where a date is shown, and passing the Profile's filters.

In practice, most search hits for job postings are already closed. The reliable pattern is: **use search to find companies, then scan each company's whole job board through its public API** (below, and `scripts/board_scan.py`), which lists only open roles with exact publish dates. A company found this way is added to Companies as a record; later runs find it again through search if it keeps posting matching roles.

### Reading postings that won't load

Many careers pages embed their job board in a frame that only loads in a browser, so a plain page read comes back empty. Use the job-board system's public API instead:

| System | Public API |
|---|---|
| Ashby | `https://api.ashbyhq.com/posting-api/job-board/<board>`; the board name is in the embed URL `jobs.ashbyhq.com/<board>/<job id>` |
| Greenhouse | `https://boards-api.greenhouse.io/v1/boards/<board>/jobs?content=true` |
| Lever | `https://api.lever.co/v0/postings/<company>?mode=json` (EU boards: `https://api.eu.lever.co/v0/postings/<company>?mode=json`) |
| SmartRecruiters | `https://api.smartrecruiters.com/v1/companies/<company>/postings` |

Greenhouse also hosts EU boards (`job-boards.eu.greenhouse.io`); their API host isn't known yet (`boards-api.eu.greenhouse.io` doesn't resolve), so open those postings directly.

If no API is available, look for the same role on another public listing (e.g. an aggregator), and note that the copy didn't come from the company's own page.

## Additional sources (from the Profile)

Listed by the user on their Profile, e.g. regional job boards, VC portfolio boards, niche communities. Each is read as a public page; the search follows each listing to the company's own posting where possible. A source that can't be read is logged in Runs, not silently skipped.

## Never used

- **LinkedIn job pages directly:** terms of service and account risk.
- **LinkedIn job alert emails:** tested and dropped (Oct 2026). The leads were rarely useful: titles were broad, roles listed as new were often old, and many couldn't be found on the company's own site, so each lead cost several searches to check.
- **Indeed, Glassdoor:** heavy bot blocking, and their alert emails have the same problems as LinkedIn's.
- **Scraping Google directly:** the search uses Claude's web search with the same `site:` operators.
