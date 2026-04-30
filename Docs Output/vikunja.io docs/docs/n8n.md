Using Vikunja with n8n
Vikunja maintains a community node for n8n, allowing you to easily integrate Vikunja with all kinds of other tools and services.
Installation#
To install the node in your n8n installation:
- In your n8n instance, go to Settings > Community Nodes.
- Select Install.
- Enter
n8n-nodes-vikunja
as the npm Package Name - Agree to the risks of using community nodes: select I understand the risks of installing unverified code from a public source.
- Select Install. n8n installs the node, and returns to the Community Nodes list in Settings.
- Vikunja actions and triggers are now available in n8n.
Official n8n docs about the installation
Authentication#
To authenticate your automation against Vikunja:
- In Vikunja, go to Settings > API Tokens and create a new token. Use all scopes for the kind of task you want to
do.
> **Note**: If you want to use the webhook trigger node, the api token should have permissions to create, read and delete webhooks. - Now in n8n, go to Credentials and then click on Add Credential.
- Search for
Vikunja API
and click Continue - Enter the API key you created in step 1.
- Enter the API URL of your Vikunja instance, with the
/api/v1
suffix. - When you now create a Vikunja node, select the created credentials.
