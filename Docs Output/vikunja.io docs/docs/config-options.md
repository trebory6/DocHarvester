Configuration options
You can either use a config.yml
file in the root directory of Vikunja or set almost all config options with environment variables. If you have both, the value set in the config file is used.
Variables are nested in the config.yml
, these nested variables become VIKUNJA\_FIRST\_CHILD
when configuring via
environment variables. So setting
export VIKUNJA\_FIRST\_CHILD=true
is the same as defining it in a config.yml
like so:
first:
child: true
Formats#
Vikunja supports using toml
, yaml
, hcl
, ini
, json
, envfile, env variables and Java Properties files.
We recommend yaml or toml, but you’re free to use whatever you want.
Vikunja provides a default config.yml
file which you can use as a starting point.
Config file locations#
Vikunja will search in various places for a config file:
- Next to the location of the binary
- In the
service.rootpath
location set in a config (remember you can set config arguments via environment variables) - In
/etc/vikunja
- In
~/.config/vikunja
The service.rootpath
setting is used only while finding the first config file.
You can therefore set VIKUNJA\_SERVICE\_ROOTPATH
to point Vikunja to that
initial config file, but any new service.rootpath
defined inside it will not be
considered for further config lookup.
export VIKUNJA\_SERVICE\_ROOTPATH=/etc/vikunja
vikunja
Assuming /etc/vikunja/config.yml
contains:
service:
rootpath: /opt/vikunja
Vikunja reads /etc/vikunja/config.yml
but does not check
/opt/vikunja/config.yml
afterward.
Using a config file with Docker Compose#
In case you are using Docker Compose you need to edit the docker-compose.yml
to load config.yml
.
Mount the config.yml
file into the Vikunja container, by adding this line to the volumes of the Vikunja container and replacing the ./path/to/config.yml
with the relative path from the docker-compose.yml
to your config.yml
:
volumes:
- ./path/to/config.yml:/etc/vikunja/config.yml
After all the setup is done, start Vikunja as shown in the Docker Compose setup.
Common configuration tasks#
Here are some frequently requested configuration changes:
| Task | Config option | Docs |
|---|---|---|
| Disable public link sharing | service.enablelinksharing: false | Details |
| Disable user registration | service.enableregistration: false | Details |
| Enable OIDC authentication | auth.openid.enabled: true | OpenID guide |
| Configure SMTP for emails | mailer.\* | Details |
| Set up rate limiting | ratelimit.\* | Details |
| Change the default language | service.defaultlanguage | Details |
Reading config values from files#
Vikunja can read any config value from a file saved on disk when the path to that file is
specified in the config with the target config path as child file
.
This works with environment variables as well, note that there you’ll need to add a \_FILE
suffix.
Files are evaluated after any previously set values. That means if you set both, the value from the file will override any previously set value.
If the specified file is not accessible, Vikunja will fail to start.
For example, setting this in your config.yml:
database:
password:
file: /path/to/password
will load the content from the file at /path/to/password
and set it as the config value of database.password
.
With an environment variable for the same config variable, you’d need to set the VIKUNJA\_DATABASE\_PASSWORD\_FILE
environment variable to /path/to/password
.
Using environment variables in file paths#
This feature is available from Vikunja 2.3.0 onwards (or unstable builds).
The file path supports environment variable expansion. This is useful when integrating with secret management systems like systemd’s LoadCredential
.
For example:
mailer:
password:
file: $CREDENTIALS\_DIRECTORY/smtp.secret
Any environment variable in the path (e.g. $CREDENTIALS\_DIRECTORY
, $HOME
) will be expanded to its value before reading the file.
All environment variables available to the Vikunja process will be expanded in the file path. Make sure that untrusted users cannot set environment variables in the Vikunja process environment, as this could cause Vikunja to read unintended files from disk.
Default configuration with explanations#
The following explains all possible config variables and their defaults. You can find a full example configuration file here.
If you don’t provide a value in your config file, their default will be used.
Nesting#
Most config variables are nested under some “higher-level” key.
For example, the interface
config variable is a child of the service
key.
The docs below aim to reflect that leveling, but please also have a look at the default config file to better grasp what the nesting looks like.
service #
secret #
This secret is used to sign JWT tokens and for other cryptographic operations. Default is a random secret which will be generated at each startup of Vikunja. (This means all already issued tokens will be invalid once you restart Vikunja)
Default: 
Full path: service.secret
Environment path:
VIKUNJA\_SERVICE\_SECRET
JWTSecret #
Deprecated: use service.secret instead. If set, its value will be copied to service.secret.
Default: 
Full path: service.JWTSecret
Environment path:
VIKUNJA\_SERVICE\_JWTSECRET
jwtttl #
The duration of the issued JWT tokens in seconds. The default is 259200 seconds (3 Days).
Default: 259200
Full path: service.jwtttl
Environment path:
VIKUNJA\_SERVICE\_JWTTTL
jwtttllong #
The duration of the "remember me" time in seconds. When the login request is made with the long param set, the token returned will be valid for this period. The default is 2592000 seconds (30 Days).
Default: 2592000
Full path: service.jwtttllong
Environment path:
VIKUNJA\_SERVICE\_JWTTTLLONG
jwtttlshort #
The duration of short-lived JWT tokens in seconds. These tokens are used together with refresh tokens for session-based authentication. The default is 600 seconds (10 minutes).
Default: 600
Full path: service.jwtttlshort
Environment path:
VIKUNJA\_SERVICE\_JWTTTLSHORT
interface #
The interface on which to run the webserver
Default: :3456
Full path: service.interface
Environment path:
VIKUNJA\_SERVICE\_INTERFACE
unixsocket #
Path to Unix socket. If set, it will be created and used instead of tcp
Default: 
Full path: service.unixsocket
Environment path:
VIKUNJA\_SERVICE\_UNIXSOCKET
unixsocketmode #
Permission bits for the Unix socket. Note that octal values must be prefixed by "0o", e.g. 0o660
Default: 
Full path: service.unixsocketmode
Environment path:
VIKUNJA\_SERVICE\_UNIXSOCKETMODE
publicurl #
The public facing URL where your users can reach Vikunja. Used in emails and for the communication between api and frontend. The url must be a valid http or https url. This setting is required when cors.enable is true.
Default: 
Full path: service.publicurl
Environment path:
VIKUNJA\_SERVICE\_PUBLICURL
rootpath #
The base path on the file system where Vikunja stores its data (database, files, logs, plugins). Defaults to the current working directory. When running as a systemd service, this respects the WorkingDirectory= setting. Vikunja will also look in this path for a config file, so you could provide only this variable to point to a folder with a config file which will then be used.
Default: 
Full path: service.rootpath
Environment path:
VIKUNJA\_SERVICE\_ROOTPATH
maxitemsperpage #
The max number of items which can be returned per page
Default: 50
Full path: service.maxitemsperpage
Environment path:
VIKUNJA\_SERVICE\_MAXITEMSPERPAGE
enablecaldav #
Enable the caldav endpoint, see the docs for more details
Default: true
Full path: service.enablecaldav
Environment path:
VIKUNJA\_SERVICE\_ENABLECALDAV
motd #
Set the motd message, available from the /info endpoint
Default: 
Full path: service.motd
Environment path:
VIKUNJA\_SERVICE\_MOTD
enablelinksharing #
Enable sharing of project via a link
Default: true
Full path: service.enablelinksharing
Environment path:
VIKUNJA\_SERVICE\_ENABLELINKSHARING
enableregistration #
Whether to let new users registering themselves or not
Default: true
Full path: service.enableregistration
Environment path:
VIKUNJA\_SERVICE\_ENABLEREGISTRATION
enabletaskattachments #
Whether to enable task attachments or not
Default: true
Full path: service.enabletaskattachments
Environment path:
VIKUNJA\_SERVICE\_ENABLETASKATTACHMENTS
timezone #
The time zone all timestamps are in. Please note that time zones have to use the official tz database names. UTC or GMT offsets won't work.
Default: GMT
Full path: service.timezone
Environment path:
VIKUNJA\_SERVICE\_TIMEZONE
enabletaskcomments #
Whether task comments should be enabled or not
Default: true
Full path: service.enabletaskcomments
Environment path:
VIKUNJA\_SERVICE\_ENABLETASKCOMMENTS
enabletotp #
Whether totp is enabled. In most cases you want to leave that enabled.
Default: true
Full path: service.enabletotp
Environment path:
VIKUNJA\_SERVICE\_ENABLETOTP
testingtoken #
If not empty, this will enable /test/{table}
endpoints which allow to put any content in the database.
Used to reset the db before frontend tests. Because this is quite a dangerous feature allowing for lots of harm,
each request made to this endpoint needs to provide an Authorization: 
header with the token from below.
You should never use this unless you know exactly what you're doing
Default: 
Full path: service.testingtoken
Environment path:
VIKUNJA\_SERVICE\_TESTINGTOKEN
enableemailreminders #
If enabled, Vikunja will send an email to everyone who is either assigned to a task or created it when a task reminder is due.
Default: true
Full path: service.enableemailreminders
Environment path:
VIKUNJA\_SERVICE\_ENABLEEMAILREMINDERS
enableuserdeletion #
If true, will allow users to request the complete deletion of their account. When using external authentication methods it may be required to coordinate with them in order to delete the account. This setting will not affect the cli commands for user deletion.
Default: true
Full path: service.enableuserdeletion
Environment path:
VIKUNJA\_SERVICE\_ENABLEUSERDELETION
maxavatarsize #
The maximum size clients will be able to request for user avatars. If clients request a size bigger than this, it will be changed on the fly.
Default: 1024
Full path: service.maxavatarsize
Environment path:
VIKUNJA\_SERVICE\_MAXAVATARSIZE
demomode #
If set to true, the frontend will show a big red warning not to use this instance for real data as it will be cleared out. You probably don't need to set this value, it was created specifically for usage on try.
Default: false
Full path: service.demomode
Environment path:
VIKUNJA\_SERVICE\_DEMOMODE
allowiconchanges #
Allow changing the logo and other icons based on various occasions throughout the year.
Default: true
Full path: service.allowiconchanges
Environment path:
VIKUNJA\_SERVICE\_ALLOWICONCHANGES
customlogourl #
Allow using a custom logo via external URL.
Default: 
Full path: service.customlogourl
Environment path:
VIKUNJA\_SERVICE\_CUSTOMLOGOURL
customlogourldark #
Allow using a custom logo for dark mode via external URL. If not set, the regular logo will be used for both light and dark modes.
Default: 
Full path: service.customlogourldark
Environment path:
VIKUNJA\_SERVICE\_CUSTOMLOGOURLDARK
enablepublicteams #
Enables the public team feature. If enabled, it is possible to configure teams to be public, which makes them discoverable when sharing a project, therefore not only showing teams the user is member of.
Default: false
Full path: service.enablepublicteams
Environment path:
VIKUNJA\_SERVICE\_ENABLEPUBLICTEAMS
bcryptrounds #
The number of bcrypt rounds to use during registration. Each increment of this number doubles the computational cost. You probably don't need to change this value.
Default: 11
Full path: service.bcryptrounds
Environment path:
VIKUNJA\_SERVICE\_BCRYPTROUNDS
enableopenidteamusersearch #
If enabled, users will only find other users who are part of an existing team when they are searching for a user by their partial name. The other existing team may be created from openid. It is still possible to add users to teams with their exact email address even when this is enabled.
Default: false
Full path: service.enableopenidteamusersearch
Environment path:
VIKUNJA\_SERVICE\_ENABLEOPENIDTEAMUSERSEARCH
ipextractionmethod #
Method for extracting client IP addresses. 'direct' (default) uses the TCP remote address and ignores forwarding headers — use this when Vikunja faces the internet directly. 'xff' extracts from the X-Forwarded-For header — use this behind proxies like nginx, Traefik, or cloud load balancers. 'realip' extracts from the X-Real-IP header. When using 'xff' or 'realip', configure 'service.trustedproxies' with your proxy CIDR ranges.
Default: direct
Full path: service.ipextractionmethod
Environment path:
VIKUNJA\_SERVICE\_IPEXTRACTIONMETHOD
trustedproxies #
Comma-separated list of CIDR ranges for trusted reverse proxies. Only used when service.ipextractionmethod is 'xff' or 'realip'. X-Forwarded-For / X-Real-IP headers are only trusted from these addresses. Example: '127.0.0.1/32,::1/128,10.0.0.0/8,172.16.0.0/12'
Default: 
Full path: service.trustedproxies
Environment path:
VIKUNJA\_SERVICE\_TRUSTEDPROXIES
sentry #
enabled #
If set to true, enables anonymous error tracking of api errors via Sentry. This allows us to gather more information about errors in order to debug and fix it.
Default: false
Full path: sentry.enabled
Environment path:
VIKUNJA\_SENTRY\_ENABLED
dsn #
Configure the Sentry dsn used for api error tracking. Only used when Sentry is enabled for the api.
Default: https://[email protected]/4504254983634944
Full path: sentry.dsn
Environment path:
VIKUNJA\_SENTRY\_DSN
frontendenabled #
If set to true, enables anonymous error tracking of frontend errors via Sentry. This allows us to gather more information about errors in order to debug and fix it.
Default: false
Full path: sentry.frontendenabled
Environment path:
VIKUNJA\_SENTRY\_FRONTENDENABLED
frontenddsn #
Configure the Sentry dsn used for frontend error tracking. Only used when Sentry is enabled for the frontend.
Default: https://[email protected]/6024480
Full path: sentry.frontenddsn
Environment path:
VIKUNJA\_SENTRY\_FRONTENDDSN
database #
type #
Database type to use. Supported values are mysql, postgres and sqlite. Vikunja is able to run with MySQL 8.0+, Mariadb 10.2+, PostgreSQL 12+, and sqlite.
Default: sqlite
Full path: database.type
Environment path:
VIKUNJA\_DATABASE\_TYPE
user #
Database user which is used to connect to the database.
Default: vikunja
Full path: database.user
Environment path:
VIKUNJA\_DATABASE\_USER
password #
Database password
Default: 
Full path: database.password
Environment path:
VIKUNJA\_DATABASE\_PASSWORD
host #
Database host
Default: localhost
Full path: database.host
Environment path:
VIKUNJA\_DATABASE\_HOST
database #
Database to use
Default: vikunja
Full path: database.database
Environment path:
VIKUNJA\_DATABASE\_DATABASE
path #
When using sqlite, this is the path where to store the database file. Can be an absolute path or relative path.
Relative paths are resolved as follows:
- If
service.rootpath
is explicitly configured (differs from the binary location), the database path is resolved relative to that directory. - Otherwise, relative paths are resolved to a platform-specific user data directory to prevent database files from being created in system directories (like
C:\Windows\System32
on Windows when running as a service):- Windows:
%LOCALAPPDATA%\Vikunja
(e.g.,C:\Users\username\AppData\Local\Vikunja
) - macOS:
~/Library/Application Support/Vikunja
- Linux:
$XDG\_DATA\_HOME/vikunja
or~/.local/share/vikunja
Recommendation: Use an absolute path for production deployments, especially when running Vikunja as a Windows service, to have full control over the database location.
- Windows:
Default: ./vikunja.db
Full path: database.path
Environment path:
VIKUNJA\_DATABASE\_PATH
maxopenconnections #
Sets the max open connections to the database. Only used when using mysql and postgres.
Default: 100
Full path: database.maxopenconnections
Environment path:
VIKUNJA\_DATABASE\_MAXOPENCONNECTIONS
maxidleconnections #
Sets the maximum number of idle connections to the db.
Default: 50
Full path: database.maxidleconnections
Environment path:
VIKUNJA\_DATABASE\_MAXIDLECONNECTIONS
maxconnectionlifetime #
The maximum lifetime of a single db connection in milliseconds.
Default: 10000
Full path: database.maxconnectionlifetime
Environment path:
VIKUNJA\_DATABASE\_MAXCONNECTIONLIFETIME
sslmode #
Secure connection mode. Only used with postgres. (see https://pkg.go.dev/github.com/lib/pq?tab=doc#hdr-Connection\_String\_Parameters)
Default: disable
Full path: database.sslmode
Environment path:
VIKUNJA\_DATABASE\_SSLMODE
sslcert #
The path to the client cert. Only used with postgres.
Default: 
Full path: database.sslcert
Environment path:
VIKUNJA\_DATABASE\_SSLCERT
sslkey #
The path to the client key. Only used with postgres.
Default: 
Full path: database.sslkey
Environment path:
VIKUNJA\_DATABASE\_SSLKEY
sslrootcert #
The path to the ca cert. Only used with postgres.
Default: 
Full path: database.sslrootcert
Environment path:
VIKUNJA\_DATABASE\_SSLROOTCERT
tls #
Enable SSL/TLS for mysql connections. Options: false, true, skip-verify, preferred
Default: false
Full path: database.tls
Environment path:
VIKUNJA\_DATABASE\_TLS
schema #
The PostgreSQL schema to use. Only used with postgres. If you have an existing Vikunja installation where the tables were created in a non-public schema (e.g. via the database user's search\_path), you must set this to match that schema name.
Default: public
Full path: database.schema
Environment path:
VIKUNJA\_DATABASE\_SCHEMA
redis #
enabled #
Whether to enable redis or not
Default: false
Full path: redis.enabled
Environment path:
VIKUNJA\_REDIS\_ENABLED
host #
The host of the redis server including its port.
Default: localhost:6379
Full path: redis.host
Environment path:
VIKUNJA\_REDIS\_HOST
password #
The password used to authenticate against the redis server
Default: 
Full path: redis.password
Environment path:
VIKUNJA\_REDIS\_PASSWORD
db #
0 means default database
Default: 0
Full path: redis.db
Environment path:
VIKUNJA\_REDIS\_DB
cors #
enable #
Whether to enable or disable cors headers. By default, this is enabled only for requests from the desktop application running on localhost. Note: If you want to put the frontend and the api on separate domains or ports, you will need to adjust this setting accordingly.
Default: true
Full path: cors.enable
Environment path:
VIKUNJA\_CORS\_ENABLE
origins #
A list of origins which may access the api. These need to include the protocol (http://
or https://
) and port, if any.
Full path: cors.origins
Environment path:
VIKUNJA\_CORS\_ORIGINS
Default: http://127.0.0.1:\*
Default: http://localhost:\*
maxage #
How long (in seconds) the results of a preflight request can be cached.
Default: 0
Full path: cors.maxage
Environment path:
VIKUNJA\_CORS\_MAXAGE
mailer #
enabled #
Whether to enable the mailer or not. If it is disabled, all users are enabled right away and password reset is not possible.
Default: false
Full path: mailer.enabled
Environment path:
VIKUNJA\_MAILER\_ENABLED
host #
SMTP Host
Default: 
Full path: mailer.host
Environment path:
VIKUNJA\_MAILER\_HOST
port #
SMTP Host port.
> **Note**: If you're unable to send mail and the only error you see in the logs is an EOF
, try setting the port to 25
.
Default: 587
Full path: mailer.port
Environment path:
VIKUNJA\_MAILER\_PORT
authtype #
SMTP Auth Type. Can be either plain
, login
or cram-md5
.
Default: plain
Full path: mailer.authtype
Environment path:
VIKUNJA\_MAILER\_AUTHTYPE
username #
SMTP username
Default: user
Full path: mailer.username
Environment path:
VIKUNJA\_MAILER\_USERNAME
password #
SMTP password
Default: 
Full path: mailer.password
Environment path:
VIKUNJA\_MAILER\_PASSWORD
skiptlsverify #
Whether to skip verification of the tls certificate on the server
Default: false
Full path: mailer.skiptlsverify
Environment path:
VIKUNJA\_MAILER\_SKIPTLSVERIFY
fromemail #
The default from address when sending emails
Default: mail@vikunja
Full path: mailer.fromemail
Environment path:
VIKUNJA\_MAILER\_FROMEMAIL
queuelength #
The length of the mail queue.
Default: 100
Full path: mailer.queuelength
Environment path:
VIKUNJA\_MAILER\_QUEUELENGTH
queuetimeout #
The timeout in seconds after which the current open connection to the mailserver will be closed.
Default: 30
Full path: mailer.queuetimeout
Environment path:
VIKUNJA\_MAILER\_QUEUETIMEOUT
forcessl #
By default, Vikunja will try to connect with starttls, use this option to force it to use ssl.
Default: false
Full path: mailer.forcessl
Environment path:
VIKUNJA\_MAILER\_FORCESSL
log #
path #
A folder where all the logfiles should go.
Default: logs
Full path: log.path
Environment path:
VIKUNJA\_LOG\_PATH
enabled #
Whether to show any logging at all or none
Default: true
Full path: log.enabled
Environment path:
VIKUNJA\_LOG\_ENABLED
standard #
Where the normal log should go. Possible values are stdout, stderr, file or off to disable standard logging.
Default: stdout
Full path: log.standard
Environment path:
VIKUNJA\_LOG\_STANDARD
level #
Change the log level. Possible values (case-insensitive) are CRITICAL, ERROR, WARNING, NOTICE, INFO, DEBUG.
Default: INFO
Full path: log.level
Environment path:
VIKUNJA\_LOG\_LEVEL
format #
Logging format. Can be either text
or structured
to output JSON.
Default: text
Full path: log.format
Environment path:
VIKUNJA\_LOG\_FORMAT
database #
Whether or not to log database queries. Useful for debugging. Possible values are stdout, stderr, file or off to disable database logging.
Default: off
Full path: log.database
Environment path:
VIKUNJA\_LOG\_DATABASE
databaselevel #
The log level for database log messages. Possible values (case-insensitive) are CRITICAL, ERROR, WARNING, NOTICE, INFO, DEBUG.
Default: WARNING
Full path: log.databaselevel
Environment path:
VIKUNJA\_LOG\_DATABASELEVEL
http #
Whether to log http requests or not. Possible values are stdout, stderr, file or off to disable http logging.
Default: stdout
Full path: log.http
Environment path:
VIKUNJA\_LOG\_HTTP
events #
Whether or not to log events. Useful for debugging. Possible values are stdout, stderr, file or off to disable events logging.
Default: off
Full path: log.events
Environment path:
VIKUNJA\_LOG\_EVENTS
eventslevel #
The log level for event log messages. Possible values (case-insensitive) are ERROR, INFO, DEBUG.
Default: info
Full path: log.eventslevel
Environment path:
VIKUNJA\_LOG\_EVENTSLEVEL
mail #
Whether or not to log mail log messages. This will not log mail contents. Possible values are stdout, stderr, file or off to disable mail-related logging.
Default: off
Full path: log.mail
Environment path:
VIKUNJA\_LOG\_MAIL
maillevel #
The log level for mail log messages. Possible values (case-insensitive) are ERROR, WARNING, INFO, DEBUG.
Default: info
Full path: log.maillevel
Environment path:
VIKUNJA\_LOG\_MAILLEVEL
ratelimit #
enabled #
whether or not to enable the rate limit
Default: false
Full path: ratelimit.enabled
Environment path:
VIKUNJA\_RATELIMIT\_ENABLED
kind #
The kind on which rates are based. Can be either "user" for a rate limit per user or "ip" for an ip-based rate limit.
Default: user
Full path: ratelimit.kind
Environment path:
VIKUNJA\_RATELIMIT\_KIND
period #
The time period in seconds for the limit
Default: 60
Full path: ratelimit.period
Environment path:
VIKUNJA\_RATELIMIT\_PERIOD
limit #
The max number of requests a user is allowed to do in the configured time period
Default: 100
Full path: ratelimit.limit
Environment path:
VIKUNJA\_RATELIMIT\_LIMIT
store #
The store where the limit counter for each user is stored. Possible values are "keyvalue", "memory" or "redis". When choosing "keyvalue" this setting follows the one configured in the "keyvalue" section.
Default: keyvalue
Full path: ratelimit.store
Environment path:
VIKUNJA\_RATELIMIT\_STORE
noauthlimit #
The number of requests a user can make from the same IP to all unauthenticated routes (login, register, password confirmation, email verification, password reset request) per minute. This limit cannot be disabled. You should only change this if you know what you're doing.
Default: 10
Full path: ratelimit.noauthlimit
Environment path:
VIKUNJA\_RATELIMIT\_NOAUTHLIMIT
files #
basepath #
The path where files are stored
Default: ./files
Full path: files.basepath
Environment path:
VIKUNJA\_FILES\_BASEPATH
maxsize #
The maximum size of a file, as a human-readable string. Warning: The max size is limited 2^64-1 bytes due to the underlying datatype
Default: 20MB
Full path: files.maxsize
Environment path:
VIKUNJA\_FILES\_MAXSIZE
type #
The type of file storage backend. Supported values are local
and s3
.
Default: local
Full path: files.type
Environment path:
VIKUNJA\_FILES\_TYPE
s3 #
Configuration for S3 storage backend
Full path: files.s3
Environment path:
VIKUNJA\_FILES\_S3
endpoint #
The S3 endpoint to use. Can be used with S3-compatible services like MinIO or Backblaze B2.
Default: 
Full path: files.s3.endpoint
Environment path:
VIKUNJA\_FILES\_S3\_ENDPOINT
bucket #
The name of the S3 bucket to store files in.
Default: 
Full path: files.s3.bucket
Environment path:
VIKUNJA\_FILES\_S3\_BUCKET
region #
The S3 region where the bucket is located.
Default: 
Full path: files.s3.region
Environment path:
VIKUNJA\_FILES\_S3\_REGION
accesskey #
The S3 access key ID.
Default: 
Full path: files.s3.accesskey
Environment path:
VIKUNJA\_FILES\_S3\_ACCESSKEY
secretkey #
The S3 secret access key.
Default: 
Full path: files.s3.secretkey
Environment path:
VIKUNJA\_FILES\_S3\_SECRETKEY
usepathstyle #
Whether to use path-style addressing (e.g., https://s3.amazonaws.com/bucket/key) instead of virtual-hosted-style (e.g., https://bucket.s3.amazonaws.com/key). This is commonly needed for self-hosted S3-compatible services. Some providers only support one style or the other.
Default: false
Full path: files.s3.usepathstyle
Environment path:
VIKUNJA\_FILES\_S3\_USEPATHSTYLE
disablesigning #
When enabled, the S3 client will send UNSIGNED-PAYLOAD instead of computing a SHA256 hash for request signing. Some S3-compatible providers (such as Ceph RadosGW, Clever Cloud Cellar) do not correctly verify payload signatures and return XAmzContentSHA256Mismatch errors. Enabling this option works around the issue. Only applies over HTTPS.
Default: false
Full path: files.s3.disablesigning
Environment path:
VIKUNJA\_FILES\_S3\_DISABLESIGNING
migration #
To use any of the available migrators, you usually need to configure credentials for the appropriate service and enable it. Find instructions below on how to do this for the provided migrators.
todoist #
Full path: migration.todoist
Environment path:
VIKUNJA\_MIGRATION\_TODOIST
enable #
Whether to enable the Todoist migrator.
Default: false
Full path: migration.todoist.enable
Environment path:
VIKUNJA\_MIGRATION\_TODOIST\_ENABLE
clientid #
The client id, required for making requests to the Todoist api You need to register your Vikunja instance at https://developer.todoist.com/appconsole.html to get this.
Default: 
Full path: migration.todoist.clientid
Environment path:
VIKUNJA\_MIGRATION\_TODOIST\_CLIENTID
clientsecret #
The client secret, also required for making requests to the Todoist api. Obtain it at https://developer.todoist.com/appconsole.html after registering your Vikunja instance.
Default: 
Full path: migration.todoist.clientsecret
Environment path:
VIKUNJA\_MIGRATION\_TODOIST\_CLIENTSECRET
redirecturl #
The url where clients are redirected after they authorized Vikunja to access their Todoist items.
In Todoist, this is called OAuth redirect URL
and it needs to match the url you entered when registering
your Vikunja instance at the Todoist developer console.
When using the official Vikunja frontend, set this to /migrate/todoist
(the default value).
Otherwise, set this to an url which then makes a request to /api/v1/migration/todoist/migrate
with the code obtained from the Todoist api.
Default: /migrate/todoist
Full path: migration.todoist.redirecturl
Environment path:
VIKUNJA\_MIGRATION\_TODOIST\_REDIRECTURL
trello #
Full path: migration.trello
Environment path:
VIKUNJA\_MIGRATION\_TRELLO
enable #
Whether to enable the Trello migrator.
Default: false
Full path: migration.trello.enable
Environment path:
VIKUNJA\_MIGRATION\_TRELLO\_ENABLE
key #
The client id, required for making requests to the trello api.
You need to register your Vikunja instance at https://trello.com/app-key (log in before you visit that link) to get one. Copy the Personal Key
and set it as the client id. Add your Vikunja domain to the Allowed Origins list.
Default: 
Full path: migration.trello.key
Environment path:
VIKUNJA\_MIGRATION\_TRELLO\_KEY
redirecturl #
The url where clients are redirected after they authorized Vikunja to access their trello cards.
This needs to match the url you entered when registering your Vikunja instance at trello.
When using the official Vikunja frontend, set this to /migrate/trello
(the default value).
Otherwise, set this to an url which then makes a request to /api/v1/migration/trello/migrate
with the code obtained from the Trello api.
Default: /migrate/trello
Full path: migration.trello.redirecturl
Environment path:
VIKUNJA\_MIGRATION\_TRELLO\_REDIRECTURL
microsofttodo #
Full path: migration.microsofttodo
Environment path:
VIKUNJA\_MIGRATION\_MICROSOFTTODO
enable #
Whether to enable the Microsoft Todo migrator.
Default: false
Full path: migration.microsofttodo.enable
Environment path:
VIKUNJA\_MIGRATION\_MICROSOFTTODO\_ENABLE
clientid #
The client id, required for making requests to the Microsoft graph api. See https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#register-an-application for information about how to register your Vikunja instance.
Default: 
Full path: migration.microsofttodo.clientid
Environment path:
VIKUNJA\_MIGRATION\_MICROSOFTTODO\_CLIENTID
clientsecret #
The client secret, also required for making requests to the Microsoft graph api
Default: 
Full path: migration.microsofttodo.clientsecret
Environment path:
VIKUNJA\_MIGRATION\_MICROSOFTTODO\_CLIENTSECRET
redirecturl #
The url where clients are redirected after they authorized Vikunja to access their Microsoft todo tasks.
This needs to match the url you entered when registering your Vikunja instance at Microsoft.
When using the official Vikunja frontend, set this to /migrate/microsoft-todo
(the default value).
Otherwise, set this to an url which then makes a request to /api/v1/migration/microsoft-todo/migrate
with the code obtained from the Microsoft Todo api.
Default: /migrate/microsoft-todo
Full path: migration.microsofttodo.redirecturl
Environment path:
VIKUNJA\_MIGRATION\_MICROSOFTTODO\_REDIRECTURL
avatar #
gravatarexpiration #
When using gravatar, this is the duration in seconds until a cached gravatar user avatar expires
Default: 3600
Full path: avatar.gravatarexpiration
Environment path:
VIKUNJA\_AVATAR\_GRAVATAREXPIRATION
gravatarbaseurl #
If you use a Gravatar-compatible service other than gravatar.com, you may configure the base URL for the service here. For instance, gravatarbaseurl: 'https://libravatar.org'. The default is https://www.gravatar.com.
Default: https://www.gravatar.com
Full path: avatar.gravatarbaseurl
Environment path:
VIKUNJA\_AVATAR\_GRAVATARBASEURL
backgrounds #
enabled #
Whether to enable backgrounds for projects at all.
Default: true
Full path: backgrounds.enabled
Environment path:
VIKUNJA\_BACKGROUNDS\_ENABLED
providers #
Full path: backgrounds.providers
Environment path:
VIKUNJA\_BACKGROUNDS\_PROVIDERS
upload #
Full path: backgrounds.providers.upload
Environment path:
VIKUNJA\_BACKGROUNDS\_PROVIDERS\_UPLOAD
enabled #
Whether to enable uploaded project backgrounds
Default: true
Full path: backgrounds.providers.upload.enabled
Environment path:
VIKUNJA\_BACKGROUNDS\_PROVIDERS\_UPLOAD\_ENABLED
unsplash #
Full path: backgrounds.providers.unsplash
Environment path:
VIKUNJA\_BACKGROUNDS\_PROVIDERS\_UNSPLASH
enabled #
Whether to enable setting backgrounds from unsplash as project backgrounds
Default: false
Full path: backgrounds.providers.unsplash.enabled
Environment path:
VIKUNJA\_BACKGROUNDS\_PROVIDERS\_UNSPLASH\_ENABLED
accesstoken #
You need to create an application for your installation at https://unsplash.com/oauth/applications/new and set the access token below.
Default: 
Full path: backgrounds.providers.unsplash.accesstoken
Environment path:
VIKUNJA\_BACKGROUNDS\_PROVIDERS\_UNSPLASH\_ACCESSTOKEN
applicationid #
The unsplash application id is only used for pingback and required as per their api guidelines. You can find the Application ID in the dashboard for your API application. It should be a numeric ID. It will only show in the UI if your application has been approved for Enterprise usage, therefore if you’re in Demo mode, you can also find the ID in the URL at the end: https://unsplash.com/oauth/applications/:application\_id
Default: 
Full path: backgrounds.providers.unsplash.applicationid
Environment path:
VIKUNJA\_BACKGROUNDS\_PROVIDERS\_UNSPLASH\_APPLICATIONID
legal #
Legal urls Will be shown in the frontend if configured here
imprinturl #
Default: 
Full path: legal.imprinturl
Environment path:
VIKUNJA\_LEGAL\_IMPRINTURL
privacyurl #
Default: 
Full path: legal.privacyurl
Environment path:
VIKUNJA\_LEGAL\_PRIVACYURL
keyvalue #
Key Value Storage settings The Key Value Storage is used for different kinds of things like metrics and a few cache systems.
type #
The type of the storage backend. Can be either "memory" or "redis". If "redis" is chosen it needs to be configured separately.
Default: memory
Full path: keyvalue.type
Environment path:
VIKUNJA\_KEYVALUE\_TYPE
auth #
local #
Local authentication will let users log in and register (if enabled) through the db. This is the default auth mechanism and does not require any additional configuration.
Full path: auth.local
Environment path:
VIKUNJA\_AUTH\_LOCAL
enabled #
Enable or disable local authentication
Default: true
Full path: auth.local.enabled
Environment path:
VIKUNJA\_AUTH\_LOCAL\_ENABLED
openid #
OpenID configuration will allow users to authenticate through a third-party OpenID Connect compatible provider.
The provider needs to support the openid
, profile
and email
scopes.
> **Note**: Some openid providers (like Gitlab) only make the email of the user available through OpenID if they have set it to be publicly visible.
If the email is not public in those cases, authenticating will fail.
Note 2: The frontend expects the third party to redirect the user 127.0.0.1
.
Full path: auth.openid
Environment path:
VIKUNJA\_AUTH\_OPENID
enabled #
Enable or disable OpenID Connect authentication
Default: false
Full path: auth.openid.enabled
Environment path:
VIKUNJA\_AUTH\_OPENID\_ENABLED
providers #
A list of enabled providers. You can freely choose the 
. Note that you must add at least one key to a config file if you want to read values from an environment variable as the provider won't be known to Vikunja otherwise.
Full path: auth.openid.providers
Environment path:
VIKUNJA\_AUTH\_OPENID\_PROVIDERS
 #
Full path: auth.openid.providers.
Environment path:
VIKUNJA\_AUTH\_OPENID\_PROVIDERS\_
name #
The name of the provider as it will appear in the frontend.
Default: 
Full path: auth.openid.providers..name
Environment path:
VIKUNJA\_AUTH\_OPENID\_PROVIDERS\_\_NAME
authurl #
The auth url to send users to if they want to authenticate using OpenID Connect.
Default: 
Full path: auth.openid.providers..authurl
Environment path:
VIKUNJA\_AUTH\_OPENID\_PROVIDERS\_\_AUTHURL
logouturl #
The oidc logouturl that users will be redirected to on logout. Leave empty or delete key, if you do not want to be redirected.
Default: 
Full path: auth.openid.providers..logouturl
Environment path:
VIKUNJA\_AUTH\_OPENID\_PROVIDERS\_\_LOGOUTURL
clientid #
The client ID used to authenticate Vikunja at the OpenID Connect provider.
Default: 
Full path: auth.openid.providers..clientid
Environment path:
VIKUNJA\_AUTH\_OPENID\_PROVIDERS\_\_CLIENTID
clientsecret #
The client secret used to authenticate Vikunja at the OpenID Connect provider.
Default: 
Full path: auth.openid.providers..clientsecret
Environment path:
VIKUNJA\_AUTH\_OPENID\_PROVIDERS\_\_CLIENTSECRET
scope #
The scope necessary to use oidc. If you want to use the Feature to create and assign to Vikunja teams via oidc, you have to add the custom "vikunja\_scope" and check openid.md. e.g. scope: openid email profile vikunja\_scope
Default: openid email profile
Full path: auth.openid.providers..scope
Environment path:
VIKUNJA\_AUTH\_OPENID\_PROVIDERS\_\_SCOPE
usernamefallback #
This option allows to look for a local account where the OIDC Issuer match the Vikunja local username. Allowed value is either true
or false
. That option can be combined with emailfallback
.
Use with caution, this can allow the 3rd party provider to connect to any local account and therefore potential account hijaking.
Default: false
Full path: auth.openid.providers..usernamefallback
Environment path:
VIKUNJA\_AUTH\_OPENID\_PROVIDERS\_\_USERNAMEFALLBACK
emailfallback #
This option allows to look for a local account where the OIDC user's email match the Vikunja local email. Allowed value is either true
or false
. That option can be combined with usernamefallback
.
Use with caution, this can allow the 3rd party provider to connect to any local account and therefore potential account hijaking.
Default: false
Full path: auth.openid.providers..emailfallback
Environment path:
VIKUNJA\_AUTH\_OPENID\_PROVIDERS\_\_EMAILFALLBACK
forceuserinfo #
This option forces the use of the OpenID Connect UserInfo endpoint to retrieve user information instead of relying on claims from the ID token. When set to true
, user data (email, name, username) will always be obtained from the UserInfo endpoint even if the information is available in the token claims. This is useful for providers that don't include complete user information in their tokens or when you need the most up-to-date user data. Allowed value is either true
or false
.
Default: false
Full path: auth.openid.providers..forceuserinfo
Environment path:
VIKUNJA\_AUTH\_OPENID\_PROVIDERS\_\_FORCEUSERINFO
requireavailability #
This option requires the OpenID Connect provider to be available during Vikunja startup. When set to true
, Vikunja will crash if it cannot connect to the provider during initialization, allowing container orchestrators like Kubernetes to handle the failure by restarting the application. This is useful in environments where you want to ensure all authentication providers are available before the application starts serving requests. Allowed value is either true
or false
.
Default: false
Full path: auth.openid.providers..requireavailability
Environment path:
VIKUNJA\_AUTH\_OPENID\_PROVIDERS\_\_REQUIREAVAILABILITY
ldap #
Authentication via an external LDAP server.
Full path: auth.ldap
Environment path:
VIKUNJA\_AUTH\_LDAP
enabled #
Enable or disable LDAP authentication.
Default: false
Full path: auth.ldap.enabled
Environment path:
VIKUNJA\_AUTH\_LDAP\_ENABLED
host #
The hostname of the LDAP server.
Default: localhost
Full path: auth.ldap.host
Environment path:
VIKUNJA\_AUTH\_LDAP\_HOST
port #
The port of the LDAP server.
Default: 389
Full path: auth.ldap.port
Environment path:
VIKUNJA\_AUTH\_LDAP\_PORT
basedn #
The Base DN used for LDAP search requests.
Default: 
Full path: auth.ldap.basedn
Environment path:
VIKUNJA\_AUTH\_LDAP\_BASEDN
userfilter #
The string that will be used to filter users in the directory. %[1]s
will be substituted with the username entered in the login form.
Default: 
Full path: auth.ldap.userfilter
Environment path:
VIKUNJA\_AUTH\_LDAP\_USERFILTER
usetls #
Whether to try and connect via a TLS-encrypted channel to the LDAP server.
Default: true
Full path: auth.ldap.usetls
Environment path:
VIKUNJA\_AUTH\_LDAP\_USETLS
verifytls #
Whether to verify the TLS certificate offered by the LDAP server.
Default: true
Full path: auth.ldap.verifytls
Environment path:
VIKUNJA\_AUTH\_LDAP\_VERIFYTLS
binddn #
The DN of the account used to search the LDAP directory for users when they want to log in.
Default: 
Full path: auth.ldap.binddn
Environment path:
VIKUNJA\_AUTH\_LDAP\_BINDDN
bindpassword #
The password of the account used to search the LDAP directory.
Default: 
Full path: auth.ldap.bindpassword
Environment path:
VIKUNJA\_AUTH\_LDAP\_BINDPASSWORD
groupsyncenabled #
If enabled, Vikunja will automagically add users to teams in Vikunja matching groupsyncfilter
. The teams will be automatically created and kept in sync by Vikunja.
Default: false
Full path: auth.ldap.groupsyncenabled
Environment path:
VIKUNJA\_AUTH\_LDAP\_GROUPSYNCENABLED
groupsyncfilter #
The filter to search for group objects in the ldap directory. Only used when groupsyncenabled
is set to true
.
Default: (&(objectclass=\*)(|(objectclass=group)(objectclass=groupOfNames)))
Full path: auth.ldap.groupsyncfilter
Environment path:
VIKUNJA\_AUTH\_LDAP\_GROUPSYNCFILTER
avatarsyncattribute #
The LDAP attribute where an image, decoded as raw bytes, can be found. If provided, Vikunja will use the value as avatar.
Default: 
Full path: auth.ldap.avatarsyncattribute
Environment path:
VIKUNJA\_AUTH\_LDAP\_AVATARSYNCATTRIBUTE
attribute #
The directory attributes that are used to create accounts in Vikunja.
Default: 
Full path: auth.ldap.attribute
Environment path:
VIKUNJA\_AUTH\_LDAP\_ATTRIBUTE
username #
The LDAP attribute used to set the username in Vikunja.
Default: uid
Full path: auth.ldap.attribute.username
Environment path:
VIKUNJA\_AUTH\_LDAP\_ATTRIBUTE\_USERNAME
email #
The LDAP attribute used to set the email in Vikunja.
Default: mail
Full path: auth.ldap.attribute.email
Environment path:
VIKUNJA\_AUTH\_LDAP\_ATTRIBUTE\_EMAIL
displayname #
The LDAP attribute used to set the displayed name in Vikunja.
Default: displayName
Full path: auth.ldap.attribute.displayname
Environment path:
VIKUNJA\_AUTH\_LDAP\_ATTRIBUTE\_DISPLAYNAME
memberid #
The LDAP attribute used to check group membership of a team in Vikunja. Only used when groups are synced to Vikunja.
Default: member
Full path: auth.ldap.attribute.memberid
Environment path:
VIKUNJA\_AUTH\_LDAP\_ATTRIBUTE\_MEMBERID
metrics #
Prometheus metrics endpoint
enabled #
If set to true, enables a /metrics endpoint for prometheus to collect metrics about Vikunja. You can query it from /api/v1/metrics
.
Default: false
Full path: metrics.enabled
Environment path:
VIKUNJA\_METRICS\_ENABLED
username #
If set to a non-empty value the /metrics endpoint will require this as a username via basic auth in combination with the password below.
Default: 
Full path: metrics.username
Environment path:
VIKUNJA\_METRICS\_USERNAME
password #
If set to a non-empty value the /metrics endpoint will require this as a password via basic auth in combination with the username below.
Default: 
Full path: metrics.password
Environment path:
VIKUNJA\_METRICS\_PASSWORD
defaultsettings #
Provide default settings for new users. When a new user is created, these settings will automatically be set for the user. If you change them in the config file afterwards they will not be changed back for existing users.
avatar\_provider #
The avatar source for the user. Can be gravatar
, initials
, upload
or marble
. If you set this to upload
you'll also need to specify defaultsettings.avatar\_file\_id
.
Default: initials
Full path: defaultsettings.avatar\_provider
Environment path:
VIKUNJA\_DEFAULTSETTINGS\_AVATAR\_PROVIDER
avatar\_file\_id #
The id of the file used as avatar.
Default: 0
Full path: defaultsettings.avatar\_file\_id
Environment path:
VIKUNJA\_DEFAULTSETTINGS\_AVATAR\_FILE\_ID
email\_reminders\_enabled #
If set to true users will get task reminders via email.
Default: false
Full path: defaultsettings.email\_reminders\_enabled
Environment path:
VIKUNJA\_DEFAULTSETTINGS\_EMAIL\_REMINDERS\_ENABLED
discoverable\_by\_name #
If set to true will allow other users to find this user when searching for parts of their name.
Default: false
Full path: defaultsettings.discoverable\_by\_name
Environment path:
VIKUNJA\_DEFAULTSETTINGS\_DISCOVERABLE\_BY\_NAME
discoverable\_by\_email #
If set to true will allow other users to find this user when searching for their exact email.
Default: false
Full path: defaultsettings.discoverable\_by\_email
Environment path:
VIKUNJA\_DEFAULTSETTINGS\_DISCOVERABLE\_BY\_EMAIL
overdue\_tasks\_reminders\_enabled #
If set to true will send an email every day with all overdue tasks at a configured time.
Default: true
Full path: defaultsettings.overdue\_tasks\_reminders\_enabled
Environment path:
VIKUNJA\_DEFAULTSETTINGS\_OVERDUE\_TASKS\_REMINDERS\_ENABLED
overdue\_tasks\_reminders\_time #
When to send the overdue task reminder email.
Default: 9:00
Full path: defaultsettings.overdue\_tasks\_reminders\_time
Environment path:
VIKUNJA\_DEFAULTSETTINGS\_OVERDUE\_TASKS\_REMINDERS\_TIME
default\_project\_id #
The id of the default project. Make sure users actually have access to this project when setting this value.
Default: 0
Full path: defaultsettings.default\_project\_id
Environment path:
VIKUNJA\_DEFAULTSETTINGS\_DEFAULT\_PROJECT\_ID
week\_start #
Start of the week for the user. 0
is sunday, 1
is monday and so on.
Default: 0
Full path: defaultsettings.week\_start
Environment path:
VIKUNJA\_DEFAULTSETTINGS\_WEEK\_START
language #
The language of the user interface. Must be an ISO 639-1 language code followed by an ISO 3166-1 alpha-2 country code. Check https://code.vikunja.io/vikunja/tree/main/frontend/src/i18n/lang for a list of possible languages. Will default to the browser language the user uses when signing up.
Default: 
Full path: defaultsettings.language
Environment path:
VIKUNJA\_DEFAULTSETTINGS\_LANGUAGE
timezone #
The time zone of each individual user. This will affect when users get reminders and overdue task emails.
Default: 
Full path: defaultsettings.timezone
Environment path:
VIKUNJA\_DEFAULTSETTINGS\_TIMEZONE
webhooks #
enabled #
Whether to enable support for webhooks
Default: true
Full path: webhooks.enabled
Environment path:
VIKUNJA\_WEBHOOKS\_ENABLED
timeoutseconds #
The timeout in seconds until a webhook request fails when no response has been received.
Default: 30
Full path: webhooks.timeoutseconds
Environment path:
VIKUNJA\_WEBHOOKS\_TIMEOUTSECONDS
proxyurl #
Deprecated: use outgoingrequests.proxyurl instead. The URL of a mole instance to use to proxy outgoing webhook requests. You should use this and configure appropriately if you're not the only one using your Vikunja instance. More info about why: https://webhooks.fyi/best-practices/webhook-providers#implement-security-on-egress-communication. Must be used in combination with webhooks.password
(see below).
Default: 
Full path: webhooks.proxyurl
Environment path:
VIKUNJA\_WEBHOOKS\_PROXYURL
proxypassword #
Deprecated: use outgoingrequests.proxypassword instead. The proxy password to use when authenticating against the proxy.
Default: 
Full path: webhooks.proxypassword
Environment path:
VIKUNJA\_WEBHOOKS\_PROXYPASSWORD
allownonroutableips #
Deprecated: use outgoingrequests.allownonroutableips instead. If set to true, webhook target URLs may resolve to non-globally-routable IP addresses (private networks, loopback, link-local, etc). When false (the default), Vikunja blocks outgoing webhook requests to these addresses to prevent SSRF attacks. Set this to true if you need webhooks to reach services on your internal network.
Default: false
Full path: webhooks.allownonroutableips
Environment path:
VIKUNJA\_WEBHOOKS\_ALLOWNONROUTABLEIPS
outgoingrequests #
allownonroutableips #
If set to true, outgoing HTTP requests (webhooks, avatar downloads, migration imports) may resolve to non-globally-routable IP addresses. When false (the default), Vikunja blocks these to prevent SSRF attacks. Set to true only if you need these to reach services on your internal network.
Default: false
Full path: outgoingrequests.allownonroutableips
Environment path:
VIKUNJA\_OUTGOINGREQUESTS\_ALLOWNONROUTABLEIPS
proxyurl #
The URL of a mole instance to use to proxy outgoing HTTP requests. Applies to webhooks, avatar downloads, and migration imports. You should use this and configure appropriately if you're not the only one using your Vikunja instance. More info about why: https://webhooks.fyi/best-practices/webhook-providers#implement-security-on-egress-communication. Must be used in combination with outgoingrequests.proxypassword
.
Default: 
Full path: outgoingrequests.proxyurl
Environment path:
VIKUNJA\_OUTGOINGREQUESTS\_PROXYURL
proxypassword #
The proxy password for authenticating against the proxy.
Default: 
Full path: outgoingrequests.proxypassword
Environment path:
VIKUNJA\_OUTGOINGREQUESTS\_PROXYPASSWORD
autotls #
enabled #
If set to true, Vikunja will automatically request a TLS certificate from Let's Encrypt and use it to serve Vikunja over TLS. By enabling this option, you agree to Let's Encrypt's TOS.
You must configure a service.publicurl
with a valid TLD where Vikunja is reachable to make this work. Furthermore, it is reccomened to set service.interface
to :443
if you're using this.
Default: false
Full path: autotls.enabled
Environment path:
VIKUNJA\_AUTOTLS\_ENABLED
email #
A valid email address which will be used to register certificates with Let's Encrypt. You must provide this value in order to use autotls.
Default: 
Full path: autotls.email
Environment path:
VIKUNJA\_AUTOTLS\_EMAIL
renewbefore #
A duration when certificates should be renewed before they expire. Valid time units are ns
, us
(or µs
), ms
, s
, m
, h
.
Default: 30d
Full path: autotls.renewbefore
Environment path:
VIKUNJA\_AUTOTLS\_RENEWBEFORE
plugins #
enabled #
Whether to enable the plugin system.
Default: false
Full path: plugins.enabled
Environment path:
VIKUNJA\_PLUGINS\_ENABLED
dir #
The directory where plugins are stored.
Default: plugins
Full path: plugins.dir
Environment path:
VIKUNJA\_PLUGINS\_DIR
loader #
The plugin loader to use. "yaegi" loads plugins from Go source files (directories of .go files). "native" (deprecated) loads compiled Go plugin shared libraries (.so files).
Default: native
Full path: plugins.loader
Environment path:
VIKUNJA\_PLUGINS\_LOADER
license #
key #
The license key for Vikunja. If empty or absent, Vikunja runs in community mode with all non-licensed features available.
Default: 
Full path: license.key
Environment path:
VIKUNJA\_LICENSE\_KEY
