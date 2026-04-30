Import & Export
Export your Vikunja data or import tasks from CSV files, TickTick, WeKan, Todoist, Trello, and Microsoft To Do.
Vikunja lets you export all of your data and import tasks from other services, making it easy to back up your work or migrate from another tool.
Export#
You can export all your data from Vikunja, including projects, tasks, attachments, and more.
To start an export:
- Open your Settings and navigate to the Data Export section.
- Confirm your password to proceed.
If you are using third-party authentication (for example, through Vikunja Cloud), you will see a confirmation step instead of a password prompt.
Once confirmed, Vikunja will generate a ZIP file containing all of your data. You can download this file and keep it as a backup or use it to re-import your data into Vikunja later.
Import#
To import data into Vikunja:
- Open your Settings and navigate to the Import tab.
- Select the source you want to import from.
- Follow the on-screen steps to complete the import.
Vikunja supports importing from the following sources:
- Vikunja export: Re-import a previously exported ZIP file.
- CSV: Import tasks from any CSV file with custom column mapping.
- TickTick
- WeKan (available from version 2.3.0)
- Todoist
- Trello
- Microsoft To Do
You can also sync tasks with external apps using CalDAV.
Importing from CSV#
This feature is available from Vikunja 2.3.0 onwards (or unstable builds).
The CSV import lets you bring tasks into Vikunja from any spreadsheet or tool that can export CSV files. It works in three steps:
- Upload your CSV file. Select a
.csv
or.txt
file. Vikunja will auto-detect the delimiter, date format, and column mappings. - Review and adjust the mapping. Each column in your file can be mapped to a task attribute: title, description, due date, start date, end date, priority, labels, project, reminder, or set to “ignore”. The preview below the mapping updates automatically as you change settings.
- Import. Once you’re happy with the preview, click “Import Tasks” to create all tasks in Vikunja.
Parsing options#
You can adjust these settings if the auto-detection didn’t get it right:
- Delimiter: Comma, semicolon, tab, or pipe.
- Date format: Choose the format that matches dates in your file (e.g. YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, etc.).
- Skip rows: Skip a number of rows at the top of the file if they contain metadata or headers that aren’t part of your task data.
Column mapping#
At least one column must be mapped to Title for the import to work. All other attributes are optional:
- Labels are parsed as comma-separated values within a single column.
- Priority accepts numbers (0–5) or text like “low”, “medium”, “high”, “urgent”.
- Done accepts values like “true”, “yes”, “1”, “done”, or “completed”.
- Project groups tasks into sub-projects. If no project column is mapped, or all tasks have the same project value, they are imported into a single “Imported from CSV” project.
Importing from WeKan#
This feature is available from Vikunja 2.3.0 onwards (or unstable builds).
To import a WeKan board, first export it as JSON in WeKan (board menu > Export board > JSON), then select the WeKan icon on the import page and upload the file.
Each board export creates one Vikunja project. Lists become kanban buckets, cards become tasks, and labels, checklists, comments, and dates are all preserved.
