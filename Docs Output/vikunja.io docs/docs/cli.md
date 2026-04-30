Command line interface
You can interact with Vikunja using its cli
interface.
If you don’t specify a command, the web
command will be executed.
All commands use the same standard config file.
Using the cli in docker#
When running Vikunja in docker, you’ll need to execute all commands in the vikunja
container.
Instead of running the vikunja
binary directly, run it like this:
docker exec  /app/vikunja/vikunja 
Some commands require an interactive shell. You can run the docker command in an interactive shell using the following flags:
docker exec -it  /app/vikunja/vikunja 
If you need to run a bunch of Vikunja commands, you can also create a shell alias for it:
alias vikunja-docker='docker exec  /app/vikunja/vikunja'
Then use it as vikunja-docker 
.
doctor
#
Runs a series of diagnostic checks to help troubleshoot issues with your Vikunja installation.
Checks performed:
- System: Version, Go version, OS/architecture, running user, working directory
- Configuration: Config file path, public URL, JWT secret, CORS origins
- Database: Connection test, server version (SQLite/MySQL/PostgreSQL)
- Files: Storage path, writability, disk space (Unix only)
- Optional services (when enabled):
- Redis: Connection ping
- Mailer: SMTP connection
- LDAP: Bind authentication test
- OpenID Connect: Discovery endpoint for each configured provider
Usage:
vikunja doctor
Exit codes:
0
- All checks passed1
- One or more checks failed
The doctor command can also detect user namespace issues when running in rootless Docker and suggest fixes.
dump
#
Creates a zip file with all Vikunja-related files. This includes config, version, all files and the full database.
Usage:
vikunja dump
Flags:
-p
,--path
: The folder path where the dump file should be saved. Vikunja will use the configured root path or the binary location if the flag is not provided.-f
,--filename
: The filename of the dump file. If it does not end in ‘.zip’, it will be added as a file extension. Defaults to ‘vikunja-dump\_YYYY-MM-DD\_HH-II-SS.zip’.
help
#
Shows more detailed help about any command.
Usage:
vikunja help [command]
migrate
#
Run all database migrations which didn’t already run.
Usage:
vikunja migrate [flags]
vikunja migrate [command]
migrate list
#
Shows a list with all database migrations.
Usage:
vikunja migrate list
migrate rollback
#
Roll migrations back until a certain point.
Usage:
vikunja migrate rollback [flags]
Flags:
-n
,--name
string: The id of the migration you want to roll back until.
repair
#
Bundles commands to detect and fix various data integrity issues in your Vikunja installation.
Usage:
vikunja repair [command]
All repair subcommands support the --dry-run
flag to preview changes without applying them.
repair file-mime-types
#
Scans all files in the database that have no MIME type set, detects the type from the stored file content, and updates the database.
This is useful after upgrading from a version that did not store MIME types on file creation. Only files with an empty or NULL mime column are affected.
Usage:
vikunja repair file-mime-types [flags]
Flags:
--dry-run
: Preview repairs without making changes.
repair orphan-positions
#
Removes all task position records that reference tasks or project views which no longer exist in the database.
This can happen when tasks or views are deleted but their position records are not fully cleaned up.
Usage:
vikunja repair orphan-positions [flags]
Flags:
--dry-run
: Preview repairs without making changes.
repair projects
#
Finds projects whose parent project no longer exists in the database and re-parents them to the top level.
This can happen when a parent project is deleted but its sub-projects are not fully cleaned up, for example after importing from external services like Trello. Orphaned projects cannot be un-archived, modified, or deleted through the UI because permission checks fail when traversing the broken parent chain.
Usage:
vikunja repair projects [flags]
Flags:
--dry-run
: Preview repairs without making changes.
repair task-positions
#
Scans all project views for tasks with duplicate position values and repairs them.
Duplicate positions can occur due to race conditions or historical bugs, causing tasks to appear in the wrong order or jump around when the page is refreshed.
This command will:
- Scan all project views for duplicate positions
- Attempt localized repair by redistributing conflicting tasks
- Fall back to full view recalculation if localized repair fails
Usage:
vikunja repair task-positions [flags]
Flags:
--dry-run
: Preview repairs without making changes.
restore
#
Restores a previously created dump from a zip file, see dump
.
Usage:
vikunja restore [path to dump zip file]
Flags:
--preserve-config
: Keep the current configuration instead of restoring it from the dump. Useful when migrating to a new environment with different database connection settings or file paths.
testmail
#
Sends a test mail using the configured SMTP connection.
Usage:
vikunja testmail [email to send the test mail to]
user
#
Bundles a few commands to manage users.
user change-status
#
Enable or disable a user. Will toggle the current status if no flag (--enable
or --disable
) is provided.
Usage:
vikunja user change-status [user id] [flags]
Flags:
-d
,--disable
: Disable the user.-e
,--enable
: Enable the user.
user create
#
Create a new user.
Usage:
vikunja user create 
Flags:
-a
,--avatar-provider
: The avatar provider of the new user. Optional.-e
,--email
: The email address of the new user.-p
,--password
: The password of the new user. You will be asked to enter it if not provided through the flag.-u
,--username
: The username of the new user.
user delete
#
Start the user deletion process.
If called without the --now
flag, this command will only trigger an email to the user in order for them to confirm and start the deletion process (this is the same behavior as if the user requested their deletion via the web interface).
With the flag the user is deleted immediately.
USE WITH CAUTION.
vikunja user delete [id] [flags]
Flags:
-n
,--now
If provided, deletes the user immediately instead of emailing them first.
user list
#
Shows a list of all users.
Usage:
vikunja user list
user reset-password
#
Reset a user’s password, either through mailing them a reset link or directly.
Usage:
vikunja user reset-password [user id] [flags]
Flags:
-d
,--direct
: If provided, reset the password directly instead of sending the user a reset mail.-p
,--password
: The new password of the user. Only used in combination with —direct. You will be asked to enter it if not provided through the flag.
user update
#
Update an existing user.
Usage:
vikunja user update [user id]
Flags:
-a
,--avatar-provider
: The new avatar provider of the user.-e
,--email
: The new email address of the user.-u
,--username
: The new username of the user.
version
#
Prints the version of Vikunja.
This is either the semantic version (something like 0.24.0
) or version + git commit hash.
Usage:
vikunja version
web
#
Starts Vikunja’s web server, serving the api and frontend.
Usage:
vikunja web
