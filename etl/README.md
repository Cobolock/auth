# ETL Service

ETL for data transfer from PostgreSQL to Elasticsearch.

## Run in docker

```
docker compose --profile infra --profile etl up -d
```

## Run locally

1. [Prepare python environment](#prepare-python-environment)

2. Prepare environment variables

```
cp .env.example .env
```

3. Run infrastructure in Docker:

```
docker compose --profile infra up -d
```

4. Run ETL service:

```
make up
```

## Prepare python environment

1. If you don't have `Poetry` installed run:

```bash
make poetry-download
```

2. Initialize poetry and install `pre-commit` hooks:

```bash
make install
make pre-commit-install
```

3. Run formatters and linters. Make sure there is no errors.

```bash
make format lint
```

### Makefile usage

[`Makefile`](https://github.com/a1d4r/new_admin_panel_sprint_3/blob/master/Makefile) contains a lot of functions for
faster development.

<details>
<summary>1. Download and remove Poetry</summary>
<p>

To download and install Poetry run:

```bash
make poetry-download
```

To uninstall

```bash
make poetry-remove
```

</p>
</details>

<details>
<summary>2. Install all dependencies and pre-commit hooks</summary>
<p>

Install requirements:

```bash
make install
```

Pre-commit hooks could be installed after `git init` via

```bash
make pre-commit-install
```

</p>
</details>

<details>
<summary>3. Codestyle</summary>
<p>

Automatic formatting uses `black` and `ruff`.

```bash
make codestyle

# or use synonym
make format
```

Codestyle checks only, without rewriting files:

```bash
make check-codestyle
```

Update all dev libraries to the latest version using one command

```bash
make update-dev-deps
```

</p>
</details>

<details>
<summary>4. Code security</summary>
<p>

This command identifies security issues with `Safety`:

```bash
make check-safety
```

To validate `pyproject.toml` use

```bash
make check-poetry
```

</p>
</details>

<details>
<summary>5. Linting and type checks</summary>
<p>

Run static linting with `ruff` and `mypy`:

```bash
make static-lint
```

</p>
</details>

<details>
<summary>6. Tests with coverage</summary>
<p>

Run tests:

```bash
make test
```

</p>
</details>

<details>
<summary>7. All linters</summary>
<p>

Of course there is a command to ~~rule~~ run all linters in one:

```bash
make lint
```

</p>
</details>

<details>
<summary>8. Docker</summary>
<p>

```bash
make docker-build
```

which is equivalent to:

```bash
make docker-build VERSION=latest
```

Remove docker image with

```bash
make docker-remove
```

More information [about docker](https://github.com/a1d4r/new_admin_panel_sprint_3/tree/master/docker).

</p>
</details>

<details>
<summary>9. Cleanup</summary>
<p>
Delete pycache files

```bash
make pycache-remove
```

Remove package build

```bash
make build-remove
```

Delete .DS_STORE files

```bash
make dsstore-remove
```

Remove .mypycache

```bash
make mypycache-remove
```

Or to remove all above run:

```bash
make cleanup
```

</p>
</details>

## Credits

This project was generated with [`python-package-template`](https://github.com/a1d4r/python-package-template)
