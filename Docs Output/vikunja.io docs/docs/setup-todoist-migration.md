Todoist Migration Setup
This guide explains how to migrate your tasks and projects from Todoist to Vikunja.
Your Vikunja installation needs to be publicly accessible for the Todoist migration to work.
Setting up the Todoist Integration#
Create a Todoist App#
- In Todoist, go to Settings → Integrations → Developer → Build Integrations
- This will take you to the Todoist Developer app manager
- Click Create a new app
- Enter the following details:
- App name: vikunja
- App service URL: The URL to your Vikunja installation (e.g.,
https://vikunja.yourdomain.com
)
- Click Create app
Configure App Settings#
On the app settings page, configure the following:
- Client ID: Copy this value - you’ll need it for
VIKUNJA\_MIGRATION\_TODOIST\_CLIENTID
- Client secret: Copy this value - you’ll need it for
VIKUNJA\_MIGRATION\_TODOIST\_CLIENTSECRET
- OAuth redirect URL:
https://vikunja.yourdomain.com/migrate/todoist
(must end with/migrate/todoist
) - App name: vikunja
- App service URL:
https://vikunja.yourdomain.com/
Click Save settings.
Install the App#
- On the same page, scroll down to Installation
- Click Install for me
- To verify the installation, go back to Todoist → Settings → Integrations
- In the Installed section, you should see your app named “vikunja”
Configure Vikunja#
To enable the Todoist migration in Vikunja, you need to change your config. You can do this either by editing the config file or by using environment variables in your Docker setup.
For information about the specific migration configuration options, see the config documentation.
If you don’t plan on migrating again, you can remove the settings from your configuration after the migration is complete.
Restart Vikunja#
Restart Vikunja to apply the new configuration.
Using Docker Compose, you can do this by running:
docker compose down
docker compose up -d
If you are using a systemd service, you can restart Vikunja with:
sudo systemctl restart vikunja
Start the Migration#
- Log in to your Vikunja instance
- Click on your avatar in the top-right corner
- Click Settings
- Click Import from other services
- You should see a Todoist icon
- Click the Todoist icon to start the migration
The import will start in the background. Depending on the number of tasks, it should complete within seconds to minutes.
Troubleshooting#
”redirect\_uri\_not\_configured” Error#
If you see this error, check the following:
- Go to the Todoist App Console
- Verify that the OAuth redirect URL is set correctly to a valid, publicly accessible URL
- Ensure your Vikunja instance is reachable from the internet
Migration Not Starting#
If the Todoist icon doesn’t appear in the import section:
- Check that all environment variables are correctly set
- Verify that your Vikunja instance restarted properly
- Check the Vikunja logs for any configuration errors
Cleanup#
After the migration is complete, you can:
- Remove the Todoist integration from your Todoist account if no longer needed
- Remove the configuration for the Todoist migration from your Vikunja configuration file or environment variables
- Restart your Vikunja container to apply the cleanup
The migration is now complete, and all your Todoist tasks and projects should be available in Vikunja.
