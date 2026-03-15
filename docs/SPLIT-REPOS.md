# Workspace Repos

This workspace is managed from the root `Makefile`.

## Daily Workflow

Sync all managed repositories:

```bash
make sync
```

Sync only specific repositories:

```bash
make sync skillforge
make sync skillforge runlens go-chrome-ai
```

Managed repositories:

- `skillforge`
- `runlens`
- `ragcheck`
- `promptdeck`
- `datasetlint`
- `go-chrome-ai`
- `homebrew-tap`
- `itamaker`

`make sync` behavior:

- If the directory does not exist, it runs `git clone`.
- If the directory is a Git repository, it runs `git pull --ff-only`.
- If the directory exists but is not a Git repository, it skips that directory.
- If you pass an unknown repository name, `make` exits with an error.

Remove all managed repository directories:

```bash
make clean
```

## Go Project Commands

These commands only apply to the Go project directories:

- `skillforge`
- `runlens`
- `ragcheck`
- `promptdeck`
- `datasetlint`
- `go-chrome-ai`

Build all Go projects:

```bash
make build
```

Run tests for all Go projects:

```bash
make test
```

`homebrew-tap` and `itamaker` are synced by `make sync`, but they are not included in `make build` or `make test`.

## Export Snapshots

`scripts/export-repos.sh` is an optional helper for exporting portable snapshots of the six Go project directories. It is not required for the normal sync workflow.

```bash
bash scripts/export-repos.sh /tmp/ai-cli-repos
```

That creates:

- `/tmp/ai-cli-repos/skillforge`
- `/tmp/ai-cli-repos/runlens`
- `/tmp/ai-cli-repos/ragcheck`
- `/tmp/ai-cli-repos/promptdeck`
- `/tmp/ai-cli-repos/datasetlint`
- `/tmp/ai-cli-repos/go-chrome-ai`

Use this only when you want a clean exported copy outside the managed workspace.

## Homebrew Publishing

Homebrew publishing is still handled manually in this workspace:

- The five CLI tools render formula files into `homebrew-tap/Formula/`.
- `go-chrome-ai` renders a cask into `homebrew-tap/Casks/`.

For the five CLI tools, you can render formulas with:

```bash
bash scripts/render-tap-formulas.sh --owner itamaker --version <tag>
```

For `go-chrome-ai`, use its local cask renderer:

```bash
cd go-chrome-ai
./scripts/render-homebrew-cask.sh --owner itamaker --version <tag> > /path/to/homebrew-tap/Casks/go-chrome-ai.rb
```
