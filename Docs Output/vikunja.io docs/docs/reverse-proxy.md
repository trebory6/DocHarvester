Setup behind a reverse proxy
These examples assume you have an instance of Vikunja running on your server listening on port 3456
.
If you’ve changed this setting, you need to update the server configurations accordingly.
NGINX#
You may need to adjust server\_name
and root
accordingly.
server {
listen 80;
server\_name localhost;
location / {
proxy\_pass http://localhost:3456;
client\_max\_body\_size 20M;
}
}
> **Note**: If you change the max upload size in Vikunja’s settings, you’ll need to also change the client\_max\_body\_size
in the nginx proxy config.
NGINX Proxy Manager (NPM)#
Following the Docker Walkthrough guide, you should be able to get Vikunja to work via HTTP connection to your server IP.
From there, all you have to do is adjust the following things:
In docker-compose.yml
#
- Change
VIKUNJA\_SERVICE\_PUBLICURL:
to your desired domain withhttps://
and/
. - Expose your desired port on host under
ports:
.
example:
vikunja:
image: vikunja/vikunja
environment:
VIKUNJA\_SERVICE\_PUBLICURL: https://vikunja.example.com/ # change vikunja.example.com to your desired domain/subdomain.
VIKUNJA\_DATABASE\_HOST: db
VIKUNJA\_DATABASE\_PASSWORD: secret
VIKUNJA\_DATABASE\_TYPE: postgres
VIKUNJA\_DATABASE\_USER: vikunja
VIKUNJA\_DATABASE\_DATABASE: vikunja
VIKUNJA\_SERVICE\_SECRET: 
ports:
- 3456:3456 # Change 3456 on the left to the port of your choice.
volumes:
- ./files:/app/vikunja/files
depends\_on:
- db
restart: unless-stopped
In your DNS provider#
Add an A
record that points to your server IP.
You are of course free to change them to whatever domain/subdomain you desire and modify the docker-compose.yml
accordingly.
(Tested on Cloudflare DNS. Settings are different for different DNS provider, in this case the end result should be vikunja.your-domain.com
)
In Nginx Proxy Manager#
Add a Proxy Host as you normally would, and you don’t have to add anything extra in Advanced.
Under Details
:
Domain Names:
vikunja.your-domain.com
Scheme:
http
Forward Hostname/IP:
your-server-ip
Forward Port:
3456
Cached Assets:
Optional.
Block Common Exploits:
Toggled.
Websockets Support:
Toggled.
Under SSL
:
SSL Certificate:
However you prefer.
Force SSL:
Toggled.
HTTP/2 Support:
Toggled.
HSTS Enabled:
Toggled.
HSTS Subdomains:
Toggled.
Use a DNS Challenge:
Not toggled.
Email Address for Let's Encrypt:
[email protected]
Your Vikunja service should now work and your HTTPS frontend should be able to reach the API after docker-compose
.
Apache#
Put the following config in /etc/apache2/sites-available/vikunja.conf
:
ServerName localhost
Require all granted
ProxyPass / http://localhost:3456/
ProxyPassReverse / http://localhost:3456/
> **Note**: The apache modules proxy
, proxy\_http
and rewrite
must be enabled for this.
Caddy#
Adjust the following Caddyfile to get Vikunja up and running:
vikunja.example.com {
reverse\_proxy 127.0.0.1:3456
}
