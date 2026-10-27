# Fit rubric

**Version:** 2 · Used by `fit-analyzer`, and through its results by `cv-drafter` and `cv-reviewer`. Every analysis records the rubric version it used.

A posting is broken into items: **qualifications** (what the candidate should have) and **responsibilities** (what the job involves). Each item is rated against the CV, and one score says how much of the job the CV covers.

## 1. Qualifications

Extract each qualification and tag it:
- **Must-have qualification:** stated as required ("you have", "required", "must", "X+ years").
- **Nice-to-have qualification:** stated as a bonus ("nice to have", "bonus", "ideally", "preferably", "would be useful", "a plus").

When a posting doesn't say which, treat an item in the main qualifications list as must-have. Treat a qualifier inside an item ("…, preferably in a regulated environment") as a separate nice-to-have qualification.

Add an **implied must-have qualification** only when the core of the job can't be done without it and no listed qualification covers it, e.g. HR process experience for a People Partner role. Mark it as implied.

Don't score pure attitude or belief statements ("you believe People drives performance"). Mention them in the role-level checks if relevant.

## 2. Responsibilities

Extract each responsibility ("What you'll do", "What you'll own", "You'd be responsible for").

**Overlaps count once, under qualifications.** If a responsibility describes the same capability as a qualification (e.g. "Lead cross-functional initiatives" and "Proven experience leading cross-functional initiatives"), it's listed as "Covered by qualification #N" and not scored. Only responsibilities that add something are scored.

## 3. Rating each item

Quote the CV line that supports the item. Never assume experience the CV doesn't show. If something is likely true but missing from the CV, say *"add this to your CV if it's true"*.

**Story bank:** if the Profile links one, it doesn't change the rating, which is always based on the CV. When the story bank shows evidence the CV doesn't, say so in How to bridge ("in your story bank, not on your CV"), so the CV drafter can use it.

**Qualifications: Match / Partial / Gap**

| Rating | When |
|---|---|
| **Match** | The CV directly shows it, at the level asked for |
| **Partial** | The CV shows something real but short in one way (see below) |
| **Gap** | Nothing in the CV supports it |

A Partial falls short in one of these ways:
- **Amount:** less of it (e.g. the role asks for 5 years; the CV shows 3)
- **Depth:** used it but didn't own it (e.g. "owned the budget" vs. contributed to budget planning)
- **Context:** did it in a neighboring area (e.g. sales operations vs. marketing operations)
- **Similar tool:** a comparable tool (e.g. one BI tool asked for, another one on the CV)

**Responsibilities: Done it / Adjacent / New**

| Rating | When |
|---|---|
| **Done it** | The CV shows this kind of work |
| **Adjacent** | Similar work in a different context, at a smaller scale, or as a contributor rather than an owner |
| **New** | Nothing comparable on the CV |

## 4. Severity (Partial and Gap qualifications only)

| Severity | When |
|---|---|
| **Minor** | It's a nice-to-have qualification |
| **Moderate** | It's a must-have, but it can credibly be bridged with transferable experience or learned quickly (e.g. experience in a new industry, or a tool the CV suggests but doesn't name) |
| **Critical** | It's a must-have that can't be bridged before or during an interview (e.g. a required language, a required certification, years far below the ask, or deep specialist expertise) |

Rule of thumb: a Partial on a must-have is usually Moderate. A Gap on a must-have is Moderate or Critical, depending on whether it can be bridged.

## 5. Fit score

Each scored item earns credit:

| Item | Credit | Weight |
|---|---|---|
| Must-have qualification | Match 1 · Partial 0.5 · Gap 0 | 1 |
| Responsibility (not covered by a qualification) | Done it 1 · Adjacent 0.5 · New 0 | 1 |
| Nice-to-have qualification | Match 1 · Partial 0.5 · Gap 0 | 0.5 |

**Fit score** = sum of (credit × weight) ÷ sum of weights × 100, rounded to a whole number.

It answers one question: what share of this job does the CV cover? Nice-to-haves count half.

## 6. Fit rating

| Fit score | Rating |
|---|---|
| 75–100 | **High** |
| 50–74 | **Medium** |
| below 50 | **Low** |

**Critical gaps cap the rating.** A critical gap barely moves the score (it's one item among many), but it can make the job unattainable. So: **1 critical gap → at most Medium; 2 or more → Low.** The score itself is never adjusted.

## 7. Role-level checks

Always comment on these, even when they don't change the rating:
- **Seniority:** do the level and years asked match the candidate's experience?
- **Scope:** company-wide or one team; individual contributor or people management
- **Function:** is it one of the target role families on the Profile?
- **Domain:** industry knowledge the role expects
- **Company, location and language:** against the Profile's rules
- **Red flags:** e.g. a vague role, signs of high turnover, a title that doesn't match the responsibilities, an unrealistic scope, a posting that may be closed
