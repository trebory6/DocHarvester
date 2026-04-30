CalDAV
Sync tasks with external apps using CalDAV. Covers supported properties, URLs, and client compatibility.
> **Warning**: The CalDAV integration is in an early alpha stage and has bugs. It works well with some clients while having issues with others. If you encounter issues, please report them
Vikunja supports managing tasks via the caldav VTODO extension.
You can find your CalDAV connection details in your Settings under the CalDAV tab.
Authentication#
When you connect a CalDAV client, use your Vikunja username and one of the following as the password:
- Your account password — the easiest option, and the one we recommend whenever it works for you. Local accounts, including those provisioned via LDAP, can use their normal password directly. If your account signs in through an external identity provider (OIDC) — for example on Vikunja Cloud — the CalDAV settings tab shows a hint asking you to use a dedicated token instead, because your password isn’t stored in Vikunja. Passwords also don’t work when two-factor authentication is enabled on your account.
- A dedicated CalDAV token generated on the CalDAV settings tab. Use this if your account signs in via OIDC, or if you have two-factor authentication enabled.
- An API token with the CalDAV permission group, available from Vikunja 2.3.0 onwards. Use the token value (it starts with
tk\_
) as the password. This is handy if you want to manage all your automation credentials in one place, or if you want a single token to cover both CalDAV sync and API access.
URLs#
All URLs are located under the /dav
subspace.
URLs are:
/principals//
: Returns URLs for project discovery. Use this URL when connecting a new client./projects/
: Used to manage projects/projects//
: Used to manage a single project/projects//
: Used to manage a task on a project
Supported properties#
Vikunja currently supports the following properties:
UID
SUMMARY
DESCRIPTION
PRIORITY
CATEGORIES
COMPLETED
CREATED
(only Vikunja → Client)DUE
(Due date)DURATION
DTSTAMP
DTSTART
LAST-MODIFIED
(only Vikunja → Client)RELATED-TO
(parent/child relations)RRULE
(Recurrence) (only Vikunja → Client)STATUS
(onlyCOMPLETED
status, used to mark tasks as done)VALARM
(Reminders)
Vikunja currently does not support these properties:
ATTACH
CLASS
COMMENT
CONTACT
GEO
LOCATION
ORGANIZER
(disabled)PERCENT-COMPLETE
RECURRENCE-ID
RESOURCES
SEQUENCE
URL
Tested Clients#
Working#
Not working#
- Thunderbird (68)
- iOS CalDAV Sync (See #753)
