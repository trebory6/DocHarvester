## DocHarvester

Cross-platform command-line documentation puller and converter.

It pulls docs from:
- GitHub repos (prefer raw `.md/.mdx`)
- HTML documentation sites (crawl + convert)
- PDFs (local or URL)
- EPUBs (local or URL)

And exports a clean folder of Markdown files plus an `index.md`.

### Install

These steps assume you have **Python 3.10+** installed and available as `python`.

#### Option A (recommended): Install with pipx

1. Clone the repo and enter it:

```bash
git clone https://github.com/trebory6/DocHarvester.git
cd DocHarvester
```

2. Install with `pipx`:

```bash
pipx install .
```

3. Verify the command is available:

```bash
docpull --help
```

To upgrade later:

```bash
git pull
pipx reinstall .
```

To uninstall:

```bash
pipx uninstall docharvester
```

#### Option B: Run from a virtual environment (venv)

1. Clone the repo and enter it:

```bash
git clone https://github.com/trebory6/DocHarvester.git
cd DocHarvester
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate it and install:

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -U pip
pip install .
docpull --help
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -U pip
pip install .
docpull --help
```

4. Running later (venv):

- Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
docpull
```

- Linux/macOS:

```bash
source .venv/bin/activate
docpull
```

### Usage

DocHarvester runs **interactive by default**:

```bash
docpull
```

Non-interactive examples:

```bash
docpull pull --source "https://docs.example.com" --output "./Example Docs"
docpull pull --source "./book.epub" --output "./Book Markdown"
docpull pull --source "https://example.com/file.pdf" --output "./PDF Output" --yes
docpull pull --source "https://github.com/org/repo" --output "./Repo Docs" --github
```

You can also use the project name command:

```bash
docharvester pull --source "https://docs.python.org/3/" --output "./Python Docs"
```

### HTML crawling options

```bash
docpull pull --source "https://docs.example.com" --output "./Docs" --max-pages 200 --max-depth 8 --delay 0.5
docpull pull --source "https://docs.example.com" --output "./Docs" --ignore-robots
```

### GitHub API rate limits

If you hit GitHub API limits, set `GITHUB_TOKEN`:

- Windows PowerShell:

```powershell
$env:GITHUB_TOKEN="ghp_..."
```

- Linux/macOS:

```bash
export GITHUB_TOKEN="ghp_..."
```

### Output layout

Each run creates a subfolder inside your chosen output directory, and writes:
- One `.md` per page/chapter/file (depending on source)
- `index.md` linking to the pulled Markdown

