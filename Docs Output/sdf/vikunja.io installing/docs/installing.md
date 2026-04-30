Installing
Architecturally, Vikunja is made up of two parts: API and frontend.
Both are bundled into one single deployable binary (or docker container). That means you only need to install one thing to be able to use Vikunja.
New to Vikunja? Try the interactive install wizard for a guided setup with copy-pasteable commands.
You can also:
- Use the desktop app, which is essentially the web frontend packaged for easy installation on desktop devices
- Use the mobile app only, but as of right now it only supports the very basic features of Vikunja
If you intend to run Vikunja with MySQL or MariaDB and/or to use non-latin characters make sure your db is utf-8 compatible.
Vikunja can be installed in various ways. This document provides an overview and instructions for the different methods:
- Installing from binary (manual)
- Build from source
- Docker
- Debian/Ubuntu
- RPM (Fedora/RHEL)
- Arch Linux
- Alpine
- FreeBSD
- Kubernetes
- Ansible
And after you installed Vikunja, you may want to check out these other resources:
- Configuration
- UTF-8 Settings
- Reverse proxies
- Full docker example
- Backups
- Harden systemd service
- Fail2Ban
Getting a server to host Vikunja on
If you want the easy experience of just using Vikunja, we recommend our own hosted offering Vikunja Cloud. With Vikunja Cloud, we take care of everything and make it very easy for you, to sign up and use it, hassle-free.
If you want more control, you need to install and run Vikunja on a server. Since it's designed as a web application, it is not really possible to host it standalone on a desktop device only. If you know what you're doing, you can get it working but that's out of scope for this guide.
To get a server, we recommend one of these hosting providers (affiliate links):
- Hetzner - German provider, we're using them to host a bunch of Vikunja-related infrastructure. Sign up with our link to get 20 € in hosting credits.
- Digital Ocean - Well known cloud provider with a lot of options to choose from. Sign up with our link to get $ 200 USD in hosting credits.
All of these are affiliate links. If you sign up for one of these providers, we get a commission which helps support the project.
Install from binary#
Download a copy of Vikunja from the download page for your architecture.
wget 
Verify the GPG signature#
All releases are signed using GPG.
To validate the downloaded zip file use the signature file .asc
and the key FF054DACD908493A
:
gpg --keyserver keyserver.ubuntu.com --recv FF054DACD908493A
gpg --verify vikunja--linux-amd64-full.zip.sig vikunja--linux-amd64-full.zip
Set it up#
Once you’ve verified the signature, you need to unzip and make it executable.
You’ll also need to create a symlink to the binary, so that you can execute Vikunja by typing vikunja
on your system.
We’ll install Vikunja to /opt/vikunja
, change the path where needed if you want to install it elsewhere.
Run these commands to install it:
mkdir -p /opt/vikunja
unzip  -d /opt/vikunja
chmod +x /opt/vikunja
sudo ln -s /opt/vikunja/vikunja /usr/bin/vikunja
The default configuration has CORS enabled, which requires a public URL to be set.
You must either set service.publicurl
in your config file to the URL where Vikunja will be reachable, or disable CORS by setting cors.enable
to false
.
Systemd service#
To automatically start Vikunja when your system boots and to ensure all dependent services are met, you want to use an init system like systemd.
Save the following service file to /etc/systemd/system/vikunja.service
and adapt it to your needs:
[Unit]
Description=Vikunja
After=syslog.target
After=network.target
# Depending on how you configured Vikunja, you may want to uncomment these:
#Requires=mysql.service
#Requires=mariadb.service
#Requires=postgresql.service
#Requires=redis.service
[Service]
RestartSec=2s
Type=simple
WorkingDirectory=/opt/vikunja
ExecStart=/usr/bin/vikunja
Restart=always
# If you want to bind Vikunja to a port below 1024 uncomment
# the two values below
###
#CapabilityBoundingSet=CAP\_NET\_BIND\_SERVICE
#AmbientCapabilities=CAP\_NET\_BIND\_SERVICE
[Install]
WantedBy=multi-user.target
If you’ve installed Vikunja to a directory other than /opt/vikunja
, you need to adapt WorkingDirectory
accordingly.
After you made all necessary modifications, it’s time to start the service:
sudo systemctl enable vikunja
sudo systemctl start vikunja
For additional security, you can follow the systemd hardening guide to run Vikunja with reduced privileges and sandboxing options.
Build from source#
To build Vikunja from source, see building from source.
Updating#
Simply replace the binary with the new version, then restart Vikunja. It will automatically run all necessary database migrations. Make sure to take a look at the changelog for the new version to not miss any manual steps the update may involve!
Docker#
This assumes some familiarity with docker.
To get up and running quickly, use this command:
mkdir $PWD/files $PWD/db
chown 1000 $PWD/files $PWD/db
docker run -p 3456:3456 -v $PWD/files:/app/vikunja/files -v $PWD/db:/db vikunja/vikunja
This will expose Vikunja on port 3456
on the host running the container and use SQLite as database backend.
The default configuration has CORS enabled, which requires a public URL to be set.
You must either set the VIKUNJA\_SERVICE\_PUBLICURL
environment variable to the URL where Vikunja will be reachable, or disable CORS by setting VIKUNJA\_CORS\_ENABLE
to false
.
> **Note**: The container runs as the user 1000
and no group by default.
You can use Docker’s --user
flag to change that.
Make sure the new user has required permissions on the db
and files
folder.
Check out the docker examples for more advanced configuration using PostgreSQL or MySQL and a reverse proxy.
Using a configuration file with docker#
You can mount a local configuration like so:
mkdir $PWD/files $PWD/db
chown 1000 $PWD/files $PWD/db
docker run -p 3456:3456 -v /path/to/config/on/host.yml:/app/vikunja/config.yml:ro -v $PWD/files:/app/vikunja/files -v $PWD/db:/db vikunja/vikunja
Though it is recommended to use environment variables or .env
files to configure Vikunja in docker.
See config for a list of available configuration options.
Files volume#
By default, the container stores all files uploaded and used through Vikunja inside of /app/vikunja/files
which is
created as a docker volume. You should mount the volume somewhere to the host to permanently store the files and
don’t lose them if the container restarts.
Docker compose#
Check out the docker examples for more advanced configuration using docker compose.
Debian packages#
Vikunja is available as a deb package for installation on Debian-like systems.
Package repositories are only available from Vikunja 2.4.0 onwards. The unstable
channel is available now.
Available architectures: amd64
, arm64
, armhf
.
Via apt repository#
# Import the GPG signing key
curl -fsSL https://dl.vikunja.io/repos/gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/vikunja.gpg
# Add the repository
echo "deb [signed-by=/usr/share/keyrings/vikunja.gpg] https://dl.vikunja.io/repos/apt stable main" \
| sudo tee /etc/apt/sources.list.d/vikunja.list
sudo apt update && sudo apt install vikunja
Replace stable
with unstable
to track builds from the main development branch.
Via direct download#
Grab a .deb
file from the download page and run:
dpkg -i vikunja.deb
This will install Vikunja to /opt/vikunja
.
To configure it, use the config file in /etc/vikunja/config.yml
.
The default configuration has CORS enabled, which requires a public URL to be set.
You must either set service.publicurl
in your config file to the URL where Vikunja will be reachable, or disable CORS by setting cors.enable
to false
.
RPM#
Vikunja is available as an rpm package for installation on Fedora, CentOS, RHEL and others.
Package repositories are only available from Vikunja 2.4.0 onwards. The unstable
channel is available now.
Available architectures: x86\_64
, aarch64
, armv7
.
Via dnf/yum repository#
sudo tee /etc/yum.repos.d/vikunja.repo <<'EOF'
[vikunja]
name=Vikunja
baseurl=https://dl.vikunja.io/repos/rpm/stable/$basearch
enabled=1
gpgcheck=1
gpgkey=https://dl.vikunja.io/repos/gpg.key
EOF
sudo dnf install vikunja
Replace stable
with unstable
in the baseurl
to track builds from the main development branch.
Via direct download#
Grab a .rpm
file from the download page and run:
rpm -i vikunja.rpm
To configure Vikunja, use the config file in /etc/vikunja/config.yml
.
The default configuration has CORS enabled, which requires a public URL to be set.
You must either set service.publicurl
in your config file to the URL where Vikunja will be reachable, or disable CORS by setting cors.enable
to false
.
Arch Linux#
Vikunja provides a pacman repository for Arch Linux.
Package repositories are only available from Vikunja 2.4.0 onwards. The unstable
channel is available now.
Available architectures: x86\_64
, aarch64
, armv7
.
Add the following to /etc/pacman.conf
:
[vikunja]
Server = https://dl.vikunja.io/repos/pacman/stable/$arch
Then import and locally sign the GPG key:
curl -s https://dl.vikunja.io/repos/gpg.key | sudo pacman-key --add -
sudo pacman-key --lsign-key FF054DACD908493A
Finally, install Vikunja:
sudo pacman -Sy vikunja
Replace stable
with unstable
to track builds from the main development branch.
To configure Vikunja, use the config file in /etc/vikunja/config.yml
.
The default configuration has CORS enabled, which requires a public URL to be set.
You must either set service.publicurl
in your config file to the URL where Vikunja will be reachable, or disable CORS by setting cors.enable
to false
.
Alpine#
Vikunja provides an Alpine package repository.
Package repositories are only available from Vikunja 2.4.0 onwards. The unstable
channel is available now.
Available architectures: x86\_64
, aarch64
, armv7
.
# Add the APK signing key
wget -O /etc/apk/keys/vikunja-apk.rsa.pub https://dl.vikunja.io/repos/apk/vikunja-apk.rsa.pub
# Add the repository
echo "https://dl.vikunja.io/repos/apk/stable/main" >> /etc/apk/repositories
apk update && apk add vikunja
Replace stable
with unstable
to track builds from the main development branch.
To configure Vikunja, use the config file in /etc/vikunja/config.yml
.
The default configuration has CORS enabled, which requires a public URL to be set.
You must either set service.publicurl
in your config file to the URL where Vikunja will be reachable, or disable CORS by setting cors.enable
to false
.
FreeBSD / FreeNAS#
Unfortunately, we currently can’t provide pre-built binaries for FreeBSD. As a workaround, it is possible to compile Vikunja for FreeBSD directly on a FreeBSD machine, a guide is available below:
Thanks to HungrySkeleton who originally created this guide in the forum.
Jail Setup#
- Create a jail named
vikunja
- Set jail properties to ‘auto start’
- Mount storage (
/mnt
tojailData/vikunja
) - Start jail & SSH into it
Installing packages#
pkg update && pkg upgrade -y
pkg install nano git go gmake
go install github.com/magefile/mage
Clone Vikunja repo#
mkdir /mnt/GO/code.vikunja.io
cd /mnt/GO/code.vikunja.io
git clone https://code.vikunja.io/vikunja
cd vikunja
> **Note**: Check out the version you want to build with git checkout VERSION
- replace VERSION
with the version you want
to use. If you don’t do this, you’ll build the latest unstable build, which might contain bugs.
Compile binaries#
cd frontend
pnpm install
pnpm run build
cd ..
mage build
Create folder to install Vikunja into#
mkdir /mnt/vikunja
cp /mnt/GO/code.vikunja.io/api/vikunja /mnt/vikunja
cd /mnt/vikunja
chmod +x /mnt/vikunja
Set Vikunja to boot on startup#
nano /etc/rc.d/vikunja
Then paste into the file:
#!/bin/sh
. /etc/rc.subr
name=vikunja
rcvar=vikunja\_enable
command="/mnt/vikunja/${name}"
load\_rc\_config $name
run\_rc\_command "$1"
Save and exit. Then execute:
chmod +x /etc/rc.d/vikunja
nano /etc/rc.conf
Then add line to bottom of file:
vikunja\_enable="YES"
Test if Vikunja now works with
service vikunja start
Vikunja is now available through IP:
192.168.1.XXX:3456
The default configuration has CORS enabled, which requires a public URL to be set.
You must either set service.publicurl
in your config file to the URL where Vikunja will be reachable, or disable CORS by setting cors.enable
to false
.
Ansible#
There is an Ansible role made available by Bitwarden which you can deploy directly or use as a starting point for your own deployment. The role deploys Vikunja behind a nginx reverse proxy for TLS termination and uses their secrets manager to provide credentials for smtp and database.
Other installation resources#
- Docker Compose is MUCH Easier Than you Think - Let’s Install Vikunja (Youtube)
- Setup Vikunja using Docker Compose - Homelab Wiki
- A Closer look at Vikunja - Email Notifications - Enable or Disable Registrations - Allow Attachments (Youtube)
- Install Vikunja in Docker for self-hosted Task Tracking
- Self-Hosted To-Do List with Vikunja in Docker (Youtube)
- Vikunja self-hosted (step by step)
- How to Install Vikunja on Your Synology NAS
- Installing Vikunja with supervisord - UberLab 7
Configuration#
See available configuration options.
Default Password#
After successfully installing Vikunja, there is no default user or password. You only need to register a new account and set all the details when creating it.
