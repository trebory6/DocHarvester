Releasing a new Vikunja version
This checklist is a collection of all steps usually involved when releasing a new version of Vikunja. Not all steps are necessary for every release.
- Website update
- New Features: If there are new features worth mentioning the feature page should be updated.
- New Screenshots: If an overhaul of an existing feature happened so that it now looks different from the existing screenshot, a new one is required.
- Tag a new version: Run
mage dev:tag-release 
(e.g.mage dev:tag-release v1.0.0
). This will:- Update the version badge in README.md
- Generate the changelog using git-cliff
- Clean up and prepend the changelog to CHANGELOG.md
- Commit the changes with message
chore:  release preparations
- Create an annotated tag with the changelog as the message
- Once built: Prune the cloudflare cache so that the new versions show up at dl.vikunja.io
- Update external packages:
- Flathub desktop package
- Nixos
- Coopcloud
- Release Highlights Blogpost
- Include a section about Vikunja in general (totally fine to copy one from the earlier blog posts)
- New Features & Improvements: Mention bigger features, potentially with screenshots. Things like refactoring are sometimes also worth mentioning.
- Publish
- GitHub Release
- Mastodon
- Forum
- Bluesky
- Chat
- Newsletter
- If features in the release were sponsored, send an email to relevant stakeholders
- Update Vikunja Cloud version and other instances
