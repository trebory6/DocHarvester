Vikunja vs WeKan
Looking for a new home for your boards? Here's how they compare.
WeKan has been one of the go-to open-source Kanban boards for a long time, and for good reason. But the project has been going through a rough stretch. The v8 release introduced CSS changes that broke desktop layouts for many users, and features like SSO and labels have had regressions in recent releases. Maintaining open-source software solo is hard (I know the feeling), and these things happen. But if your team depends on their board every day, you need something stable.
I built Vikunja because I wanted a self-hosted task manager I could rely on. It does everything WeKan does and quite a bit more: lists, Kanban, Gantt charts, tables, CalDAV, reminders, and a full REST API. It ships as a single Go binary with SQLite, so it's lightweight to run and straightforward to maintain.
There's a built-in WeKan importer that brings your boards over in minutes. Export your board as JSON in WeKan, upload it in Vikunja, done. Tasks, labels, and buckets come across in one go.
Why people are looking for alternatives
These are some of the concerns WeKan users have raised on GitHub:
"Many of us have end users depending on WeKan daily. When the UI breaks, they flood us with support requests."
"Latest versions UI is broken [...] and it looks like a samsung smartphone UI or something that is just not professional."
What changes when you switch
Updates you can actually install
Every Vikunja release has a detailed changelog. Breaking changes are documented before they land. Upgrades don't hang your database or break your login screen. You stop treating "don't touch it" as an ops strategy.
Four views, not just Kanban
WeKan gives you a Kanban board. Vikunja gives you List, Kanban, Gantt, and Table on the same data. Your project manager uses Gantt while your developers use Kanban. Switch between them anytime.
A clean, consistent UI
Vikunja's interface is designed for desktop and mobile alike. It looks clean, stays consistent across updates, and won't surprise your team after an upgrade.
Lightweight to run
Vikunja is a single Go binary. No Meteor, no Node.js runtime, no MongoDB. It runs on SQLite by default and uses around 50 MB of RAM. It'll happily run on a Raspberry Pi alongside the rest of your homelab.
CalDAV and a full API
CalDAV support means your tasks show up in Thunderbird, Apple Reminders, or any CalDAV client. The REST API has full OpenAPI docs, so you can integrate Vikunja into your existing workflows.
Side by side
| Vikunja | WeKan | |
|---|---|---|
| Open source | AGPLv3 | MIT |
| Self-hostable | Yes | Yes |
| Views | List, Kanban, Gantt, Table | Kanban only |
| Backend | Go (single binary) | Meteor.js / Node.js |
| Database | SQLite, PostgreSQL, or MySQL | MongoDB (required) |
| RAM usage | ~50 MB typical | 500 MB+ (maintainer recommends 64 GB for larger installs) |
| CalDAV | Yes | No |
| REST API | All functionality available via API | Limited |
| Reminders | Yes | No |
| Due dates | Start date, end date, repeating | Due date only |
| Quick add (natural language) | Yes | No |
| Assignees | Multiple per task | Multiple per card |
| Labels | Global and per-project | Per-board |
| Saved filters | Yes | No |
| File attachments | Yes | Yes |
| Link sharing | Yes (read, write, admin) | No |
| SSO / OIDC | Yes | Yes (has had regressions recently) |
| Webhooks | Yes | Limited |
| Import from WeKan | Yes (JSON upload) | — |
Pricing
Both Vikunja and WeKan are free and open source for self-hosting. If you'd rather not manage a server, Vikunja Cloud starts at 4 €/month for personal use and 5 €/user/month for teams, hosted on EU infrastructure.
The bigger difference is operational: Vikunja is a single binary with SQLite, while WeKan requires MongoDB and Node.js, which means more resources on your server. If you're running a homelab or a small VPS, that matters.
See Vikunja pricing for details.
How to switch
The whole process takes a few minutes per board:
- Set up Vikunja (Docker, binary, or start a free Cloud trial)
- In WeKan, export each board as JSON (board menu > Export board > JSON)
- In Vikunja, go to the import page and upload your JSON files
- Your tasks, labels, and buckets come across automatically
Try it with one board first. If it works the way you expect, bring the rest over. Check the import guide for the full walkthrough.
Frequently Asked Questions
Can I import my WeKan boards into Vikunja?
Yes. Export your WeKan board as JSON (board menu > Export board > JSON), then upload it on Vikunja's import page. Tasks, labels, and buckets all come across in one go.
Does Vikunja have Kanban boards like WeKan?
Yes, and more. Vikunja supports four views: List, Kanban, Gantt, and Table. You can switch between them anytime. Same data, different perspective.
Does Vikunja support swimlanes?
Vikunja's Kanban view uses buckets (columns) that you can create and reorder freely. If you need to organize cards across multiple dimensions, you can use labels and saved filters to slice your data however you need.
Can I self-host Vikunja on the same server where WeKan runs?
Yes. Vikunja runs as a single binary or Docker container. It uses SQLite by default (no separate database server needed), or PostgreSQL/MySQL if you prefer. It'll use a fraction of the resources WeKan needs. See the installation guide.
What about mobile access?
Vikunja works as a progressive web app on any device. You can also access your tasks via CalDAV, which means they show up in your phone's native calendar and to-do apps.
Will my WeKan data come across cleanly?
The importer brings over your tasks, labels, and buckets. You'll want to double-check a board or two after import, but in most cases everything lands where you expect it.
Give it a try
Import one WeKan board and see how it feels. If it works, bring the rest over.
Use the open-source version on your own server
Get StartedDon't have a server or don't want to deal with it?
Meet Vikunja Cloud
