# Auth Service

## Installation

1. Create and activate virtual environment based on Python 3.12.

2. If you don't have `Poetry` installed run:

```bash
make poetry-download
```

3. Initialize poetry and install `pre-commit` hooks:

```bash
make install
make pre-commit-install
```

4. Run formatters, and linters. Make sure there is no errors.

```bash
make format lint
```

## Run

Prepare environment variables:

```bash
cp envs/.env.example envs/.env
cp infra/postgres/.env.example infra/postgres/.env
```

### Run API locally

1. Run infrastructure (databases) in Docker:

```bash
docker compose -f docker-compose.debug.yml up -d
```

2. Run API:

```bash
make api
```

To stop:

```bash
docker compose -f docker-compose.debug.yml down
```

3. Create superuser:

```bash
python -m auth.core.manage superadmin superpassword
```

Change superuser's username and password to your liking.

### Run everything in Docker

Run all services in Docker:

```
docker compose -f docker-compose.debug.yml --profile with-auth up -d
```

To stop:

```bash
docker compose -f docker-compose.debug.yml down
```

### Run in Docker with production image

```
docker compose up -d --build
```

## Migrations

Create migration:

```bash
alembic revision --autogenerate -m "Message"
```

Apply migrations:

```bash
alembic upgrade head
```

Revert last migration:

```bash
alembic downgrade -1
```

Revert all migrations:

```bash
alembic downgrade base
```

## Makefile usage

[`Makefile`](https://github.com/Cobolock/Auth_1_M3S1/blob/master/Makefile) contains a lot of functions for faster
development.

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

Automatic formatting uses `ruff`.

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

More information [about docker](https://github.com/Cobolock/Auth_1_M3S1/tree/master/docker).

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
