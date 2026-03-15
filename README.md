# Makefile Usage

This workspace is managed through the root `Makefile`.

## Available Commands

Sync all managed repositories:

```bash
make sync
```

Sync only specific repositories:

```bash
make sync skillforge
make sync skillforge runlens go-chrome-ai
```

Build all Go projects:

```bash
make build
```

Run tests for all Go projects:

```bash
make test
```

Remove all managed repository directories:

```bash
make clean
```

## `make sync`

`make sync` supports these repositories:

- `skillforge`
- `runlens`
- `ragcheck`
- `promptdeck`
- `datasetlint`
- `go-chrome-ai`
- `homebrew-tap`
- `itamaker`

Behavior for each repository:

- If the directory does not exist, it runs `git clone`.
- If the directory is a Git repository, it runs `git pull --ff-only`.
- If the directory exists but is not a Git repository, it skips that directory.

If you pass an unknown repository name, `make` exits with an error.

## `make build` and `make test`

These commands only apply to the Go project directories:

- `skillforge`
- `runlens`
- `ragcheck`
- `promptdeck`
- `datasetlint`
- `go-chrome-ai`

They do not run against `homebrew-tap` or `itamaker`.

## `make clean`

`make clean` removes these directories from the workspace:

- `skillforge`
- `runlens`
- `ragcheck`
- `promptdeck`
- `datasetlint`
- `go-chrome-ai`
- `homebrew-tap`
- `itamaker`

Use it carefully. It deletes the local directories directly with `rm -rf`.
