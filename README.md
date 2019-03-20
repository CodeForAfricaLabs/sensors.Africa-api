# sensors.AFRICA API [![Build Status](https://travis-ci.org/CodeForAfricaLabs/sensors.AFRICA-api.svg?branch=master)](https://travis-ci.org/CodeForAfricaLabs/sensors.AFRICA-api)

API to save and access data from deployed sensors in cities all around Africa.

## Development

Gitignore is standardized for this project using [gitignore.io](https://www.gitignore.io/) to support various development platforms.
To get the project up and running:

- Clone this repo

### Virtual environment

- Use virtualenv to create your virtual environment; `virtualenv venv`
- Activate the virtual environment; `source venv/bin/activate`
- Install the requirements; `pip install .`
- Install feinstaub; `pip install git+https://github.com/opendata-stuttgart/feinstaub-api`
- Create a sensorsafrica database with the following sql script:

```sql
CREATE DATABASE sensorsafrica;
CREATE USER sensorsafrica WITH ENCRYPTED PASSWORD 'sensorsafrica';
GRANT ALL PRIVILEGES ON DATABASE sensorsafrica TO sensorsafrica;
```

- Migrate the database; `python manage.py migrate`
- Run the server; `python manage.py runserver`

### Docker

Using docker compose:

- Build the project; `docker-compose build` or `make build`
- Run the project; `docker-compose up -d` or `make up`

Docker compose make commands:

- `make build`
- `make up` - run docker and detach
- `make log` - tail logs
- `make test` - run test
- `make migrate` - migrate database
- `make createsuperuser` - create a super user for admin
- `make compilescss`
- `make enter` - enter docker shell
- `make django` - enter docker django shell

**NOTE:**
`docker-compose` is strictly for development and testing purposes.
The Dockerfile is written for production since dokku is being used and it will look for Dockerfile.

### Migrations

Be sure to check in migrations with every model changes and be sure to review and test these changes.

Open Stuttgart don't check in their migrations and so:

- Install the latest pull from their repo; `pip install git+https://github.com/opendata-stuttgart/feinstaub-api`
- Make sensorsafrica migrations and `feinstaub_migrations` with command; `python manage.py makemigrations`

### Tests

- Virtual Environment; `pytest --pylama`
- Docker; `docker-compose run api pytest --pylama`

**NOTE:**
If entrypoint and start scripts are changed, make sure they have correct/required permissions since we don't grant permissions to the files using the Dockerfile.
Run the commands:

```bash
chmod +x contrib/entrypoint.sh
chmod +x contrib/start.sh
```

## Deployment

### Dokku

On your local machine run:

```bash
git remote add dokku dokku@dokku.me:sensorsafrica-api
git push dokku master
```

For more information read [Deploying to Dokku](http://dokku.viewdocs.io/dokku/deployment/application-deployment/#deploying-to-dokku).

### Cronjob

- Change users to dokku; `sudo su dokku`
- Edit dokku's crontab; `crontab -e`
- To export csv to openAFRICA as archives add the following:

```bash
1 0 * * * dokku enter < dokku app name > web python3 manage.py upload_to_ckan >> /var/log/cron.log 2>&1
```

- To calculate data statistics add the following:

```bash
0 * * * * dokku enter sensorsafrica-staging web python3 manage.py calculate_data_statistics >> /var/log/cron.log 2>&1
```

## Staging

Setup the staging server similar to how you would setup the production server.
Now you can load staging server data using the `staging` app helper commands as follows:

```bash
python manage.py load_Staging
```

You can save data for staging server as follows:

```bash
python manage.py save_staging sensors.Sensor sensors.SensorType sensors.Node sensors.SensorLocation auth
```

NOTE: Only select models are saved for staging and data models are omitted because these files can be massive depending on how much dta is created.
It is best to generate this data.

### Load Test

- Create a staging server that is similar to the production server setup.
- Generate N fake sensors on staging (the sensors have pin as 1 and the uid fake-[1...N])

```bash
# N is a number of swarm you want to hit the server
python manage.py generate_fake_sensors N
```

- Run locust on your computer and specify the host as the staging server and monitor the tests.

## License

GNU GPLv3

Copyright (C) 2018 Code for Africa

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
