LDAP Authentication
Vikunja supports authentication through LDAP (Lightweight Directory Access Protocol), using LDAP Bind authentication to authorize users. This allows you to integrate Vikunja with existing directory services.
How It Works#
When a user attempts to log in, Vikunja:
- Connects to the configured LDAP server using the provided bind credentials
- Searches for the user using the provided filter
- If found, attempts to bind with the user’s credentials
- On successful binding, creates or updates the user account in Vikunja using the configured LDAP attributes
Basic Setup#
To enable LDAP authentication, you need to configure the following basic settings in a config file or via environment variables:
auth:
ldap:
enabled: true
host: ldap.example.com
port: 389
basedn: dc=example,dc=com
userfilter: "(&(objectClass=person)(uid=%[1]s))"
binddn: "cn=admin,dc=example,dc=com"
bindpassword: "secretpassword"
Check out the available config options to learn more about the variables and their default values.
While the examples here use a config file, you can configure all of it via environment variables as well. Check out the config reference to see how that works.
Security Settings#
If possible, you should only connect to the LDAP server via TLS. Only disable this if you absolutely know what you’re doing.
By default, Vikunja will try to connect to the server using TLS. If you absolutely need it, you can disable this:
auth:
ldap:
usetls: false
If you have TLS configured on your LDAP server, but don’t have a valid certificate, you can disable checking the certificate chain by setting the verifytls
option to false
:
auth:
ldap:
usetls: true
verifytls: false
User Search Configuration#
To configure how Vikunja searches for users:
auth:
ldap:
userfilter: "(&(objectClass=person)(uid=%[1]s))"
binddn: "cn=admin,dc=example,dc=com"
bindpassword: "secretpassword"
The %[1]s
in the userfilter
setting will be replaced with the username entered during login.
You can use the placeholder multiple times, for example to search for users using username and email address:
auth:
ldap:
userfilter: "(&(objectClass=Person)(|(uid=%[1]s)(mail=%[1]s)))"
binddn: "cn=admin,dc=example,dc=com"
bindpassword: "secretpassword"
Usually, you’ll need to adjust at least the objectClass
.
Bind Account#
You need to configure a service account used for searching users in the LDAP directory. This account should only have minimal permissions.
Attribute Mapping#
Vikunja will map attributes from the directory to users. You can configure how they are mapped to Vikunja user properties:
auth:
ldap:
attribute:
username: uid
email: mail
displayname: displayName
Note that Vikunja requires users to have an email address to work correctly.
Avatar Synchronization#
Vikunja can synchronize user avatars from LDAP if your directory stores user photos. To enable this feature, configure the LDAP attribute that contains the raw image data:
auth:
ldap:
avatarsyncattribute: jpegPhoto
Using environment variables:
VIKUNJA\_AUTH\_LDAP\_AVATARSYNCATTRIBUTE=jpegPhoto
When this is configured, Vikunja will use the binary image data from this attribute as the user’s avatar during login.
Group Synchronization#
Vikunja can automatically create and synchronize teams based on LDAP groups. When enabled, users will be automatically added to Vikunja teams that match their LDAP groups.
To enable group synchronization:
auth:
ldap:
groupsyncenabled: true
groupsyncfilter: "(&(objectclass=\*)(|(objectclass=group)(objectclass=groupOfNames)))" # This is the default filter
Using environment variables:
VIKUNJA\_AUTH\_LDAP\_GROUPSYNCENABLED=true
VIKUNJA\_AUTH\_LDAP\_GROUPSYNCFILTER="(&(objectclass=\*)(|(objectclass=group)(objectclass=groupOfNames)))"
When a user logs in, Vikunja will:
- Search for groups in the LDAP directory using the configured filter
- Create teams in Vikunja that match these groups (if they don’t already exist)
- Add the user to the appropriate teams based on their group membership
You may need to adjust the groupsyncfilter
based on your LDAP directory structure. The default filter looks for objects with class group
or groupOfNames
.
Example Configurations#
Active Directory#
Here’s a minimal example configuration for Active Directory:
auth:
ldap:
enabled: true
host: ad.your-domain.tld
basedn: "DC=company,DC=com"
userfilter: "(&(objectClass=user)(sAMAccountName=%[1]s))"
binddn: "CN=ServiceAccount,OU=ServiceAccounts,DC=company,DC=com"
bindpassword: "very-secret-password"
attribute:
username: sAMAccountName
The same config with environment variables:
VIKUNJA\_AUTH\_LDAP\_ENABLED=true
VIKUNJA\_AUTH\_LDAP\_HOST=ad.your-domain.tld
VIKUNJA\_AUTH\_LDAP\_BASEDN="DC=company,DC=com"
VIKUNJA\_AUTH\_LDAP\_USERFILTER="(&(objectClass=user)(sAMAccountName=%[1]s))"
VIKUNJA\_AUTH\_LDAP\_BINDDN="CN=ServiceAccount,OU=ServiceAccounts,DC=company,DC=com"
VIKUNJA\_AUTH\_LDAP\_BINDPASSWORD="very-secret-password"
VIKUNJA\_AUTH\_LDAP\_ATTRIBUTE\_USERNAME=sAMAccountName
Authentik#
This config assumes:
- You have created an LDAP provider in Authentik
- Your LDAP outpost is reachable on port
636
- You have configured that provider to use TLS
- You have a service account called
ldap-service-account
which has permission to search the full LDAP directory
auth:
ldap:
enabled: true
host: auth.your-domain.tld
port: 636
verifytls: false
basedn: dc=ldap,dc=your-domain,dc=tld
userfilter: (&(objectClass=user)(cn=%s))
binddn: cn=ldap-service-account,ou=users,dc=ldap,dc=your-domain,dc=tld
bindpassword: very-secret-password
The same config with environment variables:
VIKUNJA\_AUTH\_LDAP\_ENABLED=true
VIKUNJA\_AUTH\_LDAP\_PORT=636
VIKUNJA\_AUTH\_LDAP\_VERIFYTLS=false
VIKUNJA\_AUTH\_LDAP\_HOST=auth.your-domain.tld
VIKUNJA\_AUTH\_LDAP\_BASEDN=dc=ldap,dc=your-domain,dc=tld
VIKUNJA\_AUTH\_LDAP\_USERFILTER="(&(objectClass=user)(cn=%s))"
VIKUNJA\_AUTH\_LDAP\_BINDDN="cn=ldap-service-account,ou=users,dc=ldap,dc=your-domain,dc=tld"
VIKUNJA\_AUTH\_LDAP\_BINDPASSWORD="very-secret-password"
