# Contents
- [Contents](#contents)
- [1. Prerequisites and installation:](#1-prerequisites-and-installation)
  - [a. Workflow](#a-workflow)
  - [b. URLs:](#b-urls)
- [2. Backend local dev env](#2-backend-local-dev-env)
  - [a. General workflow](#a-general-workflow)
  - [b. Structures](#b-structures)
  - [c. Docker Compose Override](#c-docker-compose-override)
  - [d. REPL](#d-repl)
  - [e. Backend tests](#e-backend-tests)
    - [Test running stack](#test-running-stack)
    - [Local tests](#local-tests)
    - [Test Coverage](#test-coverage)
  - [f. Development with Jupyter Notebooks](#f-development-with-jupyter-notebooks)
    - [Environment](#environment)
    - [Packages](#packages)
  - [g. Migrations](#g-migrations)
  - [h. Working with db](#h-working-with-db)
  - [i. Working with queue](#i-working-with-queue)
  - [k. Working with websocket](#k-working-with-websocket)
  - [h. Working with MLFlow](#h-working-with-mlflow)
    - [Added services](#added-services)
    - [Artifacts](#artifacts)
    - [Database for model registry](#database-for-model-registry)
    - [API & Dataflow](#api--dataflow)
- [3. Development domain name](#3-development-domain-name)
  - [a. Development in `localhost` with a custom domain](#a-development-in-localhost-with-a-custom-domain)
  - [b. Development with a custom IP](#b-development-with-a-custom-ip)
  - [c. Change the development "domain" name](#c-change-the-development-domain-name)
- [4. Frontend development](#4-frontend-development)
  - [a. Start development](#a-start-development)
  - [b. WebSocket and CORS gotcha](#b-websocket-and-cors-gotcha)
  - [c. (Optional) Removing frontend](#c-optional-removing-frontend)

---

# 1. Prerequisites and installation:
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.
* Node.js (with `npm`) for Frontend (usage of `nvm` is recommended).

## a. Workflow
- Create `.env` file:
```bash
$ cp .env.example .env
```
- From here change the necessary variables, especially the `_PORT` variables to *access services from the host*, and not colliding with any existing ports on your local machine. Note that this is for host access only, internal communication within the `docker` stack use the internal port the application binds to.
- Change `PROJECT_ROOT` to point to your working directory, absolute path (tested on linux). This is important for MLFlow local dev.

- Build stack (make sure error-free):
```bash
$ docker-compose build
```

- Start the stack with Docker Compose:

```bash
$ docker-compose up -d
```

## b. URLs:
- Frontend: http://localhost
- Backend API: http://localhost/api/
- Swagger UI: http://localhost/docs
- Alternative doc (ReDoc): http://localhost/redoc
- PGAdmin (for Postgres): http://localhost:${PGADMIN_PORT}
- Flower (for Celery tasks): http://localhost:${FLOWER_PORT}
- Traefik dashboard, for proxy info: http://localhost:8090

If you change any ports in .env, use appropriate url to browse.

- To check the logs of a specific service, add the name of the service, e.g.:

```bash
$ docker-compose logs -f backend
```

---

# 2. Backend local dev env

## a. General workflow

- Install [Poetry](https://python-poetry.org/).
- Dependencies:
```console
$ cd `backend/app/`
```
- Make sure `poetry.toml` has the right config (not modified):
```console
$ cat poetry.toml
```
Output:
```toml
[virtualenvs]
create = true
# uncomment in-project to create .venv within the proj (not recommended)
# in-project = true
```
- Start a shell session (venv):
```console
$ poetry shell
```
- Get packages
```console
$ poetry install
```
- In your IDE, point python interpreter and environment to the one `poetry` created, e.g. `./backend/app/.venv/bin/python3.8` (if in-project is uncommented in `poetry.toml`), otherwise `~/.cache/pypoetry/virtualenvs/app-[random_string]-py3.8/bin/python3.8`

- If new packages added to `pyproject.toml`, run update to resolve dependencies and create new lockfile:
```console
$ poetry update
```

_**Note**: Poetry host's virtual envs do not affect docker environment bootstrapped by `docker-compose`. It's purely for IDE and intellisense. If you install new packages from one environment, make sure you do for the other environment to._

## b. Structures
- SQLAlchemy models: `./backend/app/app/models/`
- CRUD utils: `./backend/app/app/crud/`
- Pydantic schemas: `./backend/app/app/schemas/`
- API endpoints: `./backend/app/app/api/api_v1`
- Websockets endpoints: `./backend/app/app/api/ws`
- Celery worker's tasks in `./backend/app/app/worker.py`
- MLFlow modules in `./backend/app/ml`
- MLFlow environment and artifacts `./mlflow-env`

## c. Docker Compose Override
- Overrides only take effect for local dev env, to achieve this, modify `docker-compose.override.yml`.
- E.g., volume mount, allowing changes to be reflected, without having to rebuild Docker image (development only)
- For prod, build the Docker image, preferably in CI.
- Command override `/start-reload.sh` in-place of `/start.sh` starts a single server process (instead of multi-threaded, which is suitable for prod). Often the container exits, you have to re-issue command:

```console
$ docker-compose up -d
```

- `command` override is commented out. Uncomment it and comment the default one makes backend container run a process that does "nothing", but keeps the container alive, allows `exec` into running container, e.g. running python REPL, start-reload, start Jupyter nb, etc.

- To achieve this:

```console
$ docker-compose up -d
```

and then:

```console
$ docker-compose exec backend bash
```

Output:

```console
root@7f2607af31c3:/app#
```

Which allows executing scripts such as:
```console
root@7f2607af31c3:/app# bash /start-reload.sh
```

- This keeps the container alive instead of exiting.

## d. REPL

- `ipython` is installed as REPL, to use, cd into backend folder and invoke it:
```console
$ cd backend/app
$ ipython
```
- In here you can import backend's modules and test snippets/functions:
```
 $  ipython
Python 3.8.0 (default, Feb 25 2021, 22:10:10)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.28.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from fastapi import FastAPI

In [2]: from .app.models.item import Item
```

## e. Backend tests
- To test the backend run:

```console
$ DOMAIN=backend sh ./scripts/test.sh
```

- `./scripts/test.sh` generates a testing `docker-stack.yml` file, which starts the stack and test it.
- The tests run with Pytest: `./backend/app/app/tests/`.
- Gitlab CI is included which runs tests.

### Test running stack
- If stack is up, use:

```bash
$ docker-compose exec backend /app/tests-start.sh
```

### Local tests
- Start the stack:

```Bash
$ DOMAIN=backend sh ./scripts/test-local.sh
```
- `./backend/app` will be mounted as "host volume" inside the docker container (set in the file `docker-compose.dev.volumes.yml`).
- Rerun the test on live code:

```Bash
$ docker-compose exec backend /app/tests-start.sh
```

- `/app/tests-start.sh` simply calls `pytest`. Extra args to `pytest` will be forwarded, e.g., stopping on first error:
```bash
$ docker-compose exec backend bash /app/tests-start.sh -x
```

### Test Coverage
- Enable HTML report, `pytest` fashion, by passing `--cov-report=html`:
```Bash
$ DOMAIN=backend sh ./scripts/test-local.sh --cov-report=html
```
- For live stack:
```bash
$ docker-compose exec backend bash /app/tests-start.sh --cov-report=html
```

## f. Development with Jupyter Notebooks
### Environment
- `docker-compose.override.yml` file sends variable `env` = `dev` to the build process of the Docker image (local development), while `Dockerfile` has steps to install and configure Jupyter within the container.
- `exec` into running container:
```bash
$ docker-compose exec backend bash
```
- Use environment variable `$JUPYTER` to run a Jupyter Notebook with everything configured. Can visit from host's web browser.

- Sample output:

```console
root@73e0ec1f1ae6:/app# $JUPYTER
[I 12:02:09.975 NotebookApp] Writing notebook server cookie secret to /root/.local/share/jupyter/runtime/notebook_cookie_secret
[I 12:02:10.317 NotebookApp] Serving notebooks from local directory: /app
[I 12:02:10.317 NotebookApp] The Jupyter Notebook is running at:
[I 12:02:10.317 NotebookApp] http://(73e0ec1f1ae6 or 127.0.0.1):8888/?token=f20939a41524d021fbfc62b31be8ea4dd9232913476f4397
[I 12:02:10.317 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[W 12:02:10.317 NotebookApp] No web browser found: could not locate runnable browser.
[C 12:02:10.317 NotebookApp]

    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://(73e0ec1f1ae6 or 127.0.0.1):8888/?token=f20939a41524d021fbfc62b31be8ea4dd9232913476f4397
```

- Replace the "host" to be `localhost` (or relevant domain):
```
http://localhost:8888/token=f20939a41524d021fbfc62b31be8ea4dd9232913476f4397
```

### Packages
- Since Jyputer notebooks run within the container, changes to the packages/dependencies warrant a re-build and restart of the container/service. After using `poetry add` to install new package, in the host, within `backend/app` folder, run:
```console
$ docker-compose build backend
```
Then
```console
$ docker-compose up -d backend
```
- And continue with notebooks development.

## g. Migrations
- Run migrations using `alembic` commands inside the container, migration code will be in your app directory, with volume mounting.
- `exec` into backend:
```console
$ docker-compose exec backend bash
```
- For every new model in `./backend/app/app/models/`, import it in `./backend/app/app/db/base.py`, which will be used by Alembic.
- After modifying the model, inside the container, create a revision:
```console
$ alembic revision --autogenerate -m "Add column last_name to User model"
```
Output:
```console
root@54b8181cdcfb:/app# alembic revision --autogenerate -m "Add column last_name to User model and dbschema"
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.ddl.postgresql] Detected sequence named 'user_id_seq' as owned by integer column 'user(id)', assuming SERIAL and omitting
INFO  [alembic.ddl.postgresql] Detected sequence named 'item_id_seq' as owned by integer column 'item(id)', assuming SERIAL and omitting
INFO  [alembic.autogenerate.compare] Detected added column 'user.last_name'
INFO  [alembic.autogenerate.compare] Detected NOT NULL on column 'user.email'
INFO  [alembic.autogenerate.compare] Detected NOT NULL on column 'user.hashed_password'
  Generating /app/alembic/versions/14ca970985f2_add_column_last_name_to_user_model_and_.py
  ...  done

```
- Double-check new file generated under `backend/app/alembic/versions`
- Run the migration to apply changes to database:

```console
$ alembic upgrade head
```
Output
```console
root@54b8181cdcfb:/app# alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade d4867f3a4c0a -> 14ca970985f2, Add column last_name to User model and dbschema
```
- Don't forget to commit.

**Note**: If you don't want to use migrations at all, uncomment the line in the file at `./backend/app/app/db/init_db.py` with:

```python
Base.metadata.create_all(bind=engine)
```

and comment the line in the file `prestart.sh` that contains:

```console
$ alembic upgrade head
```

## h. Working with db
- You can browse the db via psql inside the db container:
```console
$ docker-compose exec db psql --user=postgres app
```
- Then some psql commands or sql queries:
```console
psql (12.8 (Debian 12.8-1.pgdg110+1))
Type "help" for help.

app-# \dt
```
Output:
```console
app-# \dt
              List of relations
 Schema |      Name       | Type  |  Owner
--------+-----------------+-------+----------
 public | alembic_version | table | postgres
 public | item            | table | postgres
 public | user            | table | postgres
(3 rows)
```
```console
app=# select * from public.user;
```
Output:
```console
app=# select * from public.user;
 id | full_name |         email         |                       hashed_password
             | is_active | is_superuser | last_name
----+-----------+-----------------------+-------------------------------------------------
-------------+-----------+--------------+-----------
  1 |           | admin@fastapi-app.com | $2b$12$JA82XxbBWmnmHK2.71y/sOQ4172GvOO/mulsCuFT7
wca.dZiLurhW | t         | t            |
(1 row)

```
**Note**: This is simply a hash for "123456" for development purposes.

## i. Working with queue
- `celery` handler and tasks are defined in `app/worker.py` for the moment. It might make sense to split it into 2 files: one only containing the celery handler and configs, the other with all the declared tasks to be invoked by controller.
- Queue using `celery` is configured with `redis` pub/sub and backend for persistence. To inspect the queue, cli into `redis` container (service `queue`, as declared in `docker-compose.yml`):
```console
$ docker-compose exec queue redis-cli
```
- To view task's results, get the specific task using `GET` (simple key - string value mapping):
```
127.0.0.1:6379> KEYS **
 1) "_kombu.binding.celery.pidbox"
 2) "celery-task-meta-c4f0990d-8d13-4848-8f5f-39be4e07c5ad"
 3) "celery-task-meta-04db80d2-9994-4058-8d41-8875c50534dd"
 4) "celery-task-meta-5a9d9666-9049-4a78-b02a-b514236d5265"
 5) "celery-task-meta-01e16094-76b3-418f-a80a-9f6a2b76c400"
 6) "celery-task-meta-456c7a24-297a-4e0e-bef5-34cb6b3643e4"
 7) "_kombu.binding.celery"
 8) "celery"
 9) "_kombu.binding.main-queue"
10) "_kombu.binding.celeryev"

127.0.0.1:6379> GET celery-task-meta-c4f0990d-8d13-4848-8f5f-39be4e07c5ad
"{\"status\": \"SUCCESS\", \"result\": \"test task return test fr vue again\", \"traceback\": null, \"children\": [], \"date_done\": \"2021-11-01T09:14:34.166946\", \"task_id\": \"c4f0990d-8d13-4848-8f5f-39be4e07c5ad\"}"
```
- To inspect queued (but not picked up by `celery`) tasks, use list retrieval for `celery` key:
```console
127.0.0.1:6379> LRANGE celery 1 10
```

## k. Working with websocket
- Websocket support is already built into FastAPI core. Logging from websocket requests is also standard, just like other (HTTP) API routes.
- For authorization, since native browser WebSocket does not support any standard authorization headers, we make use of cookies. Upon logging in, the backend will respond with a `set-cookie` response header, directing the browser to persist this token:
```py
# api.api_v1.endpoints.login
    response.set_cookie(key="token", value=access_token, path="/", expires=access_token_expires)
```
- Then this `token` cookie will automatically be attached to the WS request from frontend.
- Read further below in 4. [b. WebSocket and CORS gotcha](#b-websocket-and-cors-gotcha)

## h. Working with MLFlow
### Added services
- `mlflow` provides utilities to manage training executions and models. `mlflow server` can be created as a separate API server providing interfaces to track these executions and models. For the docker stack, it's added under the `mlflow` service.
- When invoking from another docker service, we will use the port that `mlflow server` command binds to, by default `:5000`, and hostname (and internal routing) will be managed by `docker-compose`. In `python`:
```python
mlflow.set_tracking_uri('http://mlflow:5000')
```
- When executing from host, for example `poetry` venv (direct invocation or ipython), we need to hit `mlflow` via interface and port exposed/mapped to host. Mapped port is configured in `.env.` with variable `MLFLOW_PORT`. In `poetry`'s `ipython`:
```
In [1]: import mlflow

In [2]: mlflow.set_tracking_uri('http://localhost:5005')

In [3]: mlflow.get_artifact_uri()
```

### Artifacts
- The intended setup for remote `mlflow server` (server and client live on separate systems), is to use a third-party filesystem, e.g. AWS S3, then point both client and server to this filesystem.
- `mlflow client` instance will run machine learning code and persist artifacts (figures, serialised models, etc.) on this remote filesystem, then `mlflow server` can refer to and serve them as static as well.
- To achieve this exact behaviour without code modification between environment, we use volume mounting, and fixate the path on both client & server to be absolute. The host's specific folder will be mounted in exact path onto each `mlflow` client and server docker services. With `PROJECT_ROOT` set in `.env`, in `docker-compose`:
```yaml
  # FastAPI backend and celeryworker will run mlflow client code
  backend:
    volumes:
      - ./backend/app:/app
      - ${PROJECT_ROOT}/mlflow-env:${PROJECT_ROOT}/mlflow-env
  ...
  celeryworker:
    volumes:
      - ./backend/app:/app
      - ${PROJECT_ROOT}/mlflow-env:${PROJECT_ROOT}/mlflow-env
  ...
  # mlflow server will use this exact absolute path to serve artifacts (e.g. via UI)
  mlflow:
    volumes:
      - ${PROJECT_ROOT}/mlflow-env:${PROJECT_ROOT}/mlflow-env
  ...
  mlflowui:
    volumes:
      - ${PROJECT_ROOT}/mlflow-env:${PROJECT_ROOT}/mlflow-env
```

### Database for model registry
- `mlflow server` is configured to rely on `postgresql` database for model registry. We'll use the same postgres service in the stack, under a separate database, by default `mldb`.
- A script under `./scripts/postgres/create-multi-db.sh` will be added into the `postgres` container entrypoint via volumes. It will read `.env`'s `POSTGRES_MULTI_DB`, check if exists necessary database for `mlflow` and create them.
- `mlflow` upon bootup will generate necessary schemas under this db.
- For now, `FastAPI` `backend` and `celeryworker` won't read directly from this database but via `mlflow`, however might be necessary to do so in the future for performance reasons.
- To browse this database, similarly to the default `app` database:
```bash
$ docker-compose exec db psql --user=postgres mldb
```
Output:
```
psql (12.9 (Debian 12.9-1.pgdg110+1))
Type "help" for help.

mldb=#
```
- Use `\c [database_name]` if necessary to switch between 2 databases.

### API & Dataflow
- `python` code that uses `import mlflow` are treated as `mlflow client`, which will invoke necessary endpoint of `mlflow server` to submit tracking details of the current training run.
- `mlflow` log functions that persist artifacts such as figures, serialised models, etc. write directly to filesystem instead of via `mlflow server`. It'll however, submit to the server necessary metadata so server can serve them on its own UI later, and also keep track of the artifacts location for queries.
- We'll avoid running `mlflow serve` a model directly from the filesystem (and using model via `invocations` api). Instead we use `mlflow client`, query the model path, load it onto memory via deserialisation and invoke model function such as predict, refit data, etc. as necessary, via worker, console or web routes.
- Similarly, `mlflow client` will query from the server model metadata and artifact path in the filesystem, then go to read the filesystem directly to load models into memory to predict, refit, validate etc.
- Ideally a system should always have a version of the model available for live prediction, training can overwrite a new version separately.

---

# 3. Development domain name

## a. Development in `localhost` with a custom domain
- With hostname/CORS/cookies issues, you can use `localhost.tiangolo.com`, it is set up to point to `localhost` (to the IP `127.0.0.1`) and all subdomains.
- `localhost.tiangolo.com` was configured to be allowed. Otherwise, add it to the list in the variable `BACKEND_CORS_ORIGINS` in the `.env` file.
- To configure it in your stack, follow [c. Change the development "domain" name](#c-change-the-development-domain-name) below, using domain `localhost.tiangolo.com`.
- You should be able to open: http://localhost.tiangolo.com, it will be server by your stack in `localhost`.

## b. Development with a custom IP
- If you are running Docker in an IP address different than `127.0.0.1` (`localhost`) and `192.168.99.100` (the default of Docker Toolbox), you will need to use a fake local domain (`dev.fastapi-app.com`) and make your computer think that the domain is is served by the custom IP (e.g. `192.168.99.150`).
- `dev.fastapi-app.com` was configured to be allowed. If you want a custom one, add it to the list in the variable `BACKEND_CORS_ORIGINS` in the `.env` file.
- Open `/etc/hosts`, added line might look like:
```
192.168.99.100    dev.fastapi-app.com
```
- To configure it in your stack, follow the section **Change the development "domain"** below, using domain `dev.fastapi-app.com`.

- You should be able to open: http://dev.fastapi-app.com, it will be server by your stack in `localhost`.

## c. Change the development "domain" name

If you need to use your local stack with a different domain than `localhost`, you need to make sure the domain you use points to the IP where your stack is set up. See the different ways to achieve that in the sections above (i.e. using Docker Toolbox with `local.dockertoolbox.tiangolo.com`, using `localhost.tiangolo.com` or using `dev.fastapi-app.com`).

To simplify your Docker Compose setup, for example, so that the API docs (Swagger UI) knows where is your API, you should let it know you are using that domain for development. You will need to edit 1 line in 2 files.

* Open the file located at `./.env`. It would have a line like:

```
DOMAIN=localhost
```

* Change it to the domain you are going to use, e.g.:

```
DOMAIN=localhost.tiangolo.com
```

That variable will be used by the Docker Compose files.

* Now open the file located at `./frontend/.env`. It would have a line like:

```
VUE_APP_DOMAIN_DEV=localhost
```

* Change that line to the domain you are going to use, e.g.:

```
VUE_APP_DOMAIN_DEV=localhost.tiangolo.com
```

That variable will make your frontend communicate with that domain when interacting with your backend API, when the other variable `VUE_APP_ENV` is set to `development`.

After changing the two lines, you can re-start your stack with:

```bash
docker-compose up -d
```

and check all the corresponding available URLs in the section at the end.

---

# 4. Frontend development
## a. Start development
- Enter the `frontend` directory:
```bash
cd frontend
npm install
npm run serve
```
- Then browse to http://localhost:8080
- It's recommended to work with frontend in host env for live-reload, fast npm tools, etc..
- You can build the frontend image and start it, to test in a production-like environment.
- Check `package.json`.
- Can point local frontend to staging env. To achieve this,modify `./frontend/.env`, change:

```
VUE_APP_ENV=development
# VUE_APP_ENV=staging
```
to:
```
# VUE_APP_ENV=development
VUE_APP_ENV=staging
```

## b. WebSocket and CORS gotcha
- If you went with the default development environment, with Vue at `localhost:8080` and FastAPI at `localhost`, you will run into CORS issues with `set-cookie`.
- Specifically, `set-cookie` directs the browser to set one at `localhost:8080`, then afterwards, WebSocket connection is calling `localhost`, for which the browser will not provide the `token` for.
- The work around for development is obtain a valid token, e.g. via Swagger, then manually set it in browser for `localhost`, or launch the Vue app at `localhost` (online via docker service) and login normally, which will make browser persist a `token` for `localhost` instead of `localhost:8080` via `set-cookie` response header, which makes other requests to api/ws at `localhost` from Vue include this `token` cookie.

## c. (Optional) Removing frontend
If you wish to remove in favour of other frontends:
- Remove the `./frontend` directory.
- In the `docker-compose.yml` file, remove the whole service / section `frontend`.
- In the `docker-compose.override.yml` file, remove the whole service / section `frontend`.
- You have a frontend-less (api-only) app.
- You can also remove the `FRONTEND` environment variables from:
  * `.env`
  * `.gitlab-ci.yml`
  * `./scripts/*.sh`

---
