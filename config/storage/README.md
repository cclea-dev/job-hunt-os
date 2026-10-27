# Storage: where your data lives

The skills describe **what** to do with your data ("add a recommendation", "save the fit analysis"). A storage file says **how** for one place your data can live. Pick one:

| Option | File | Your data lives in | You work in | Good for |
|---|---|---|---|---|
| **Notion** | `notion.md` | A Notion workspace duplicated from the [Job Hunt OS template](https://mica-waxflower-6c3.notion.site/Job-Hunt-OS-Template-3febf806381381fb9277e4de33ccd0b4) | Notion (web, desktop or phone app) | People who like boards, filters and a phone app |
| **Files** | `files.md` | Markdown files in a private GitHub repo of your own (start from [`templates/data-repo/`](../../templates/data-repo/)) | Chat with Claude ("show this week's recommendations", "approve 1 and 3"), or GitHub's file editor | People who'd rather work only in Claude, with no other tool |

Both options keep the same records (Profile, Recommendations, Jobs, Companies, Contacts, CV Log, Runs, Search memory), the same rules about which fields only you change, and the same operations. Switching later means moving the records, not changing the skills.

## Which one a skill uses

- **Scheduled runs:** the run's instructions name the storage file (e.g. "use `config/storage/files.md` with the data repo `<you>/job-hunt-data`").
- **In chat:** the user's setup says which one (the Claude project's instructions, or the user tells Claude). If nothing says, and a Notion page named "Job Hunt OS" is reachable, use Notion.

## What each option needs

| | Notion | Files |
|---|---|---|
| Connectors | Notion; Google Docs and Google Drive for CVs in Google Docs | none; Google Docs and Google Drive only if your CVs are Google Docs |
| Scheduled runs | the job-hunt-os repo | the job-hunt-os repo **and** your data repo (runs commit their results to it) |
