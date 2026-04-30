Fail2Ban Setup
To protect your Vikunja instance from brute-force and abusive requests, you can use Fail2Ban, which monitors logs and blocks IPs at the network level after repeated failed logins.
Use the ratelimit options to limit request frequency across endpoints, and Fail2Ban when you want to ban clients entirely.
Both mechanisms can be used together to provide layered protection against abuse and unauthorized access attempts.
Configure Vikunja#
First, make sure Vikunja is logging HTTP requests to a file. Add or adjust the following section in your config.yml
:
log:
path: "/var/lib/vikunja/logs"
enabled: true
http: "file"
Adjust the path value if your environment uses a different log location.
Configure Fail2Ban#
Set up Fail2Ban according to your distribution’s documentation or the official Fail2Ban documentation.
Create a Filter#
Add a new filter for Vikunja HTTP logs at /etc/fail2ban/filter.d/vikunja.conf
:
[Definition]
datepattern = ^time=%%Y-%%m-%%dT%%H:%%M:%%S%%Z
failregex = ^.\*\bmsg="POST\s+/api/v\d+/login[^"]\*".\*\bstatus=(?:400|403|412)\b.\*\bremote\_ip=\b.\*$
This filter matches failed login attempts recorded in the HTTP log.
Create a Jail#
Next, add a jail definition for Vikunja to your /etc/fail2ban/jail.local
:
Adjust the logfile
path to match your http.log
file.
[vikunja]
enabled = true # Enable this jail
backend = auto # Automatically select the backend
filter = vikunja # Use the filter defined in filter.d/vikunja.conf
port = http,https # Ports to be banned
logpath = /var/lib/vikunja/logs/http.log # Path to Vikunja http log file
maxretry = 3 # Allow 3 failures before banning
findtime = 600 # Count failures over 10 minutes (600s)
bantime = 3600 # Ban the IP for 1 hour (3600s)
Make sure the logpath points to the correct HTTP log file configured earlier.
Verification#
After restarting Fail2Ban, you can verify that the jail is active and monitoring logs with:
fail2ban-client status vikunja
This should show the jail’s status, including any currently banned IPs.
