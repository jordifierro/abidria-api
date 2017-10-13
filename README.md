# Abidria API

This repo contains the backend code for Abidria project.
This simple app aims to be a reference
to discover interesting places
and also to record our past experiences,
sharing content with other people.

Application domain is composed by `scenes`,
which are defined as something that happened
or can be done/seen in a located place.
A group of `scenes` are defined as an `experience`.

## API Endpoints

### `GET /experiences/`

_Response:_
```json
[
    {
        "id": "2",
        "title": "Baboon",
        "description": "Mystical place...",
        "picture": {
            "small_url": "https://experiences/8c29.small.jpg",
            "medium_url": "https://experiences/8c29.medium.jpg",
            "large_url": "https://experiences/8c29.large.jpg"
        }
    },
    {
        "id": "3",
        "title": "Magic Castle of Lost Swamps",
        "description": "Don't even try to go there!",
        "picture": null
    }
]
```

### `GET /scenes/?experience=<experience_id>`

_Response:_
```json
[
    {
        "id": "5",
        "title": "Plaça Mundial",
        "description": "World wide square!",
        "picture": {
            "small_url": "https://scenes/37d6.small.jpeg",
            "medium_url": "https://scenes/37d6.medium.jpeg",
            "large_url": "https://scenes/37d6.large.jpeg"
        },
        "latitude": 1.000000,
        "longitude": 2.000000,
        "experience_id": "5"
    },
    {
        "id": "4",
        "title": "I've been here",
        "description": "",
        "picture": null,
        "latitude": 0.000000,
        "longitude": 1.000000,
        "experience_id": "5"
    },
]
```

## Documentation

This project has been developed using Django framework,
with Postgres as database and S3 as storage service.

Code structure follows a Clean Architecture approach
([explained in detail here](http://jordifierro.com/django-clean-architecture)),
emphasizing on code readability, responsibility decoupling
and unit testing.

## Setup

Follow these instructions to start working locally on the project:

* Download code cloning this repo:
```bash
git clone https://github.com/jordifierro/abidria-api.git
```
* Install postgres and run:
```bash
./abidria/setup/postgres.sh
```
to create user and database.
* Run postgres:
```bash
postgres -D /usr/local/var/postgres &
```
* Install python version specified on `runtime.txt`
and run:
```bash
virtualenv -p `which python3.6` ../env
```
* Get into the environment:
```bash
source ../env/bin/activate
```
and install dependencies:
```bash
pip install -r requirements.txt
```
* Migrate database:
```bash
python manage.py migrate
```
* Create django admin super user:
```bash
python manage.py createsuperuser
```
* Finally, you should be able to run unit and integration tests:
```bash
pytest                # python tests
python manage.py test # django tests
```

Once we have made the first time setup,
we can start everything up running:
```bash
source abidria/setup/startup.sh
```
