Full-text Search with ParadeDB
Vikunja supports using ParadeDB for improved full-text search capabilities. ParadeDB is a PostgreSQL extension that provides fast, fuzzy matching search similar to Typesense, but without requiring a separate service.
Requirements#
- PostgreSQL database: ParadeDB only works with PostgreSQL (not MySQL or SQLite)
- pg\_search extension: The ParadeDB pg\_search extension must be installed in your PostgreSQL instance
Setup#
Using the ParadeDB Docker Image#
The easiest way to get started is using the official ParadeDB Docker image, which comes with all extensions pre-installed and can be used as a drop-in replacement for a standard PostgreSQL container:
services:
db:
image: paradedb/paradedb:latest
environment:
POSTGRES\_PASSWORD: changeme
POSTGRES\_USER: vikunja
POSTGRES\_DB: vikunja
volumes:
- ./db:/var/lib/postgresql/data
restart: unless-stopped
healthcheck:
test: ["CMD-SHELL", "pg\_isready -h localhost -U $$POSTGRES\_USER"]
interval: 2s
start\_period: 30s
That’s it! Vikunja will automatically detect ParadeDB and enable full-text search.
Using an Existing PostgreSQL Installation#
If you’re running your own PostgreSQL server:
- Install the pg\_search extension following the ParadeDB installation guide
- Ensure the extension is available in your Vikunja database
- Restart Vikunja - it will automatically detect and use ParadeDB
Migration from Typesense#
If you’re currently using Typesense and want to migrate to ParadeDB:
- Set up PostgreSQL with ParadeDB (see setup instructions above)
- If you’re not already using PostgreSQL, migrate your database first
- Remove the Typesense configuration from your Vikunja config
- Restart Vikunja
Vikunja will automatically detect ParadeDB and begin using it for search. Your existing task data will be indexed automatically.
How It Works#
When ParadeDB is available, Vikunja creates a BM25 search index on your tasks table. This index enables:
- Fast full-text search across task titles and descriptions
- Fuzzy matching for typo tolerance
- Relevance-based result ranking
The index is maintained automatically as tasks are created, updated, or deleted.
