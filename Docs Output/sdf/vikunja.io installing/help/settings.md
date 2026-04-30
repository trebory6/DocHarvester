Settings
All user settings: general preferences, password, email, avatar, data export, import, CalDAV, API tokens, and account deletion.
To open your settings, click your username in the top right corner and select Settings.
Settings worth checking first#
These settings are worth checking first:
- Default view: choose whether projects open in List, Gantt, Table, or Kanban view.
- Timezone: make sure it matches where you are, or due dates and reminders may be off.
- Email reminders: turn these on if you want to receive reminders and overdue-task summaries by email.
- Quick Add Magic mode: choose Vikunja-style or Todoist-style shortcuts for adding dates, labels, and other task details while typing.
- Privacy settings: decide whether other users can find you by name or email when they want to add you to a team or project.
The rest of this page follows the same section order as the settings screen.
General#
The General tab contains most everyday account preferences.
Name#
Change the display name shown to other users throughout Vikunja.
When you are logged in via an external authentication provider (for example, Vikunja Cloud), your display name is managed by that provider. You will need to change it there instead.
Default project#
Choose which project receives tasks you create from the dashboard.
Default view#
Set the view that is shown when you first open a project. Choose between List, Gantt, Table, and Kanban views.
Minimum priority#
Control which tasks show a colored priority badge in project views. Tasks below this level still appear; they just do not show the badge.
For example, if you set this to High, only tasks marked High, Urgent, or DO NOW will show a priority badge. Tasks with Low or Medium priority will still be listed, but without a visible priority label.
Email reminders#
Choose whether task reminders are sent by email. You can also enable a daily overdue summary.
Language#
Set the language for the Vikunja interface.
Timezone#
Set your timezone so that dates and times display correctly. If your due dates or reminders seem off by a few hours, this is the first thing to check.
Week start day#
Choose which day your week starts on (for example, Sunday or Monday).
Date format#
Choose how dates are displayed.
Color scheme#
Choose between System (follows your operating system setting), Light, or Dark.
Quick Add Magic mode#
Choose between Vikunja-style and Todoist-style quick-add shortcuts. See Quick Add Magic for the full syntax.
Default task relation type#
Set the default relation type used when creating task relations.
Show Kanban bucket task count#
When enabled, every Kanban bucket shows its task count, even without a WIP limit.
Show last viewed projects on the overview page#
Controls whether the Last viewed section appears on your dashboard. Turn it off if you prefer a cleaner dashboard with just the greeting and your upcoming tasks. It is enabled by default and available from Vikunja 2.3.0 onwards.
Background brightness#
Adjust the brightness of custom project backgrounds for readability.
Privacy settings#
These options control whether other users can discover your account when adding people to teams or projects:
- Allow other users to find you by searching for parts of your name: other users can search for your display name (or part of it) to find your account.
- Allow other users to find you by your full email address: others can look you up by typing your exact email address.
If both are disabled, other users can only find you by your exact username. On shared instances, keeping at least one enabled usually makes collaboration easier.
Password and Email#
Update your password or the email address on your account. To change your password, enter your current password first.
When your account uses external authentication (for example, Vikunja Cloud), password and email management is handled by that provider. These sections will be disabled in Vikunja. Make changes through your provider instead.
Avatar#
Choose how your avatar appears across Vikunja:
- Initials: generates an avatar from your name’s initials
- Default avatar: a generic placeholder image
- Gravatar: uses the avatar linked to your email on gravatar.com
- Marble: a colorful, gradient-based avatar generated for your account
- Upload: upload a custom image file to use as your avatar
Data export#
Export all your data from Vikunja. See Import & Export for steps and supported formats.
Import#
Import data from other services. See Import & Export for supported formats and instructions.
CalDAV#
This tab shows the CalDAV details you need to connect external calendar or task apps to Vikunja. You can either generate a dedicated CalDAV token here, or use an API token that includes the CalDAV permission.
See CalDAV for full details on supported properties, URLs, client compatibility, and how to authenticate with an API token.
API Tokens#
Create API tokens so scripts, automations, and integrations can access the Vikunja API without your password.
When creating a token, you can:
- Give it a descriptive title
- Choose specific permissions to limit what the token is allowed to do
One of the available permission groups is CalDAV > Access. A token with this permission can be used as the password when connecting a CalDAV client, as an alternative to generating a separate CalDAV token. Tokens with the CalDAV permission group can still be scoped to other permissions as well, so a single token can cover both API automation and CalDAV sync.
The token value is only shown once, immediately after creation. Vikunja does not store the token in plaintext, so you must copy and save it right away. If you lose it, you will need to create a new token.
Expiry warnings#
If a token has an expiration date set, Vikunja reminds you before it expires so you have time to rotate it. You will get a heads-up 7 days before expiry and a final reminder 1 day before expiry, sent as an email.
Expiry warnings are available from Vikunja 2.3.0 onwards.
For more information on using the API, see the API documentation.
Delete account#
At the bottom of the settings page, you can permanently delete your account. This cannot be undone.
When your account is managed by an external authentication provider (for example, Vikunja Cloud), account deletion may be disabled in Vikunja. You will need to delete your account through that provider instead.
