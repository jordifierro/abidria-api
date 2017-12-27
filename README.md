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

A `person` can use api as anonymous guest.
Later, she can register specifying just username and email.
Posterior email confirmation is required to create content.
There is no password, so login will be implemented using email token system.

A `person` can `save` their favourite `experiences`.

For the moment, the api is only consumed by
[abidria-android](https://github.com/jordifierro/abidria-android) project.

## API Endpoints

### `GET /experiences`
_Request:_
You can specify `mine` filter param to fetch only experiences you have created.
You can also specify `saved` filter param to fetch only experiences you have saved.
Both params are set to `false` by default, you can ignore them.

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

### `POST /experiences`

_Request(application/x-www-form-urlencoded):_
```json
{
    "title": "My travel",
    "description": "and other adventures",
}
```

_Response:_

_201_
```json
{
    "id": "8",
    "title": "My travel",
    "description": "and other adventures",
    "picture": null,
}
```

_422_
```json
{
    "error": {
        "source": "title",
        "code": "empty_attribute",
        "message": "Title cannot be empty"
    }
}
```

### `PATCH /experiences/<experience_id>`

_Request(application/x-www-form-urlencoded):_
```json
{
    "title": "",
    "description": "A new description",
}
```
It is also allowed to not define some fields
(if defined blank value will be set to blank).

_Response:_

_200_
```json
{
    "id": "8",
    "title": "MainSquare",
    "description": "A new description",
    "picture": null,
}
```

_404_
```json
{
    "error": {
        "source": "entity",
        "code": "not_found",
        "message": "Entity not found"
    }
}
```

_422_
```json
{
    "error": {
        "source": "title",
        "code": "wrong_size",
        "message": "Title must be between 1 and 30 chars"
    }
}
```


### `POST /experiences/<experience_id>/save/`

Endpoint to save experience as favourite.

_Response:_

_201_

### `DELETE /experiences/<experience_id>/save/`

Endpoint to unsave experience as favourite.

_Response:_

_204_


### `POST /experiences/<experience_id>/picture/`

_Request(multipart/form-data):_

Param name to send the file: `picture`

_Response:_

_200_
```json
{
    "id": "8",
    "title": "My travel",
    "description": "and other adventures",
    "picture": {
        "small_url": "https://scenes/37d6.small.jpeg",
        "medium_url": "https://scenes/37d6.medium.jpeg",
        "large_url": "https://scenes/37d6.large.jpeg"
    },
}
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

### `POST /scenes`

_Request(application/x-www-form-urlencoded):_
```json
{
    "title": "Plaça Major",
    "description": "The main square",
    "latitude": 1.2,
    "longitude": 0.3,
    "experience_id": "3"
}
```

_Response:_

_201_
```json
{
    "id": "8",
    "title": "Plaça Major",
    "description": "The main square",
    "picture": null,
    "latitude": 1.2,
    "longitude": 0.3,
    "experience_id": "3"
}
```

_422_
```json
{
    "error": {
        "source": "title",
        "code": "empty_attribute",
        "message": "Title cannot be empty"
    }
}
```

### `PATCH /scenes/<scene_id>`

_Request(application/x-www-form-urlencoded):_
```json
{
    "title": "",
    "description": "A new description",
    "latitude": -0.3,
    "longitude": 0.56,
}
```
It is also allowed to not define some fields
(if defined blank value will be set to blank).

_Response:_

_200_
```json
{
    "id": "8",
    "title": "MainSquare",
    "description": "A new description",
    "picture": null,
    "latitude": 1.2,
    "longitude": 0.56,
    "experience_id": "3"
}
```

_404_
```json
{
    "error": {
        "source": "entity",
        "code": "not_found",
        "message": "Entity not found"
    }
}
```

_422_
```json
{
    "error": {
        "source": "title",
        "code": "wrong_size",
        "message": "Title must be between 1 and 30 chars"
    }
}
```



### `POST /scenes/<scene_id>/picture/`

_Request(multipart/form-data):_

Param name to send the file: `picture`

_Response:_

_200_
```json
{
    "id": "8",
    "title": "Plaça Major",
    "description": "The main square",
    "picture": {
        "small_url": "https://scenes/37d6.small.jpeg",
        "medium_url": "https://scenes/37d6.medium.jpeg",
        "large_url": "https://scenes/37d6.large.jpeg"
    },
    "latitude": 1.2,
    "longitude": 0.3,
    "experience_id": "3"
}
```

### `POST /people/`

This endpoint is to create a `person` instance.
This `person` will be anonymous guest (until registration)
and has limited permissions (basically get information).
The response of this endpoint will be `auth_token` credentials,
composed by `access_token` and `refresh_token`,
that have to be persisted on the client.

_Request(application/x-www-form-urlencoded):_
```json
{
    "client_secret_key": "XXXX",
}
```

_Response:_

_201_
```json
{
    "access_token": "A_T_12345",
    "refresh_token": "R_T_67890",
}
```

### `PATCH /people/me`

This endpoint is to register a guest `person`.
Username and email is required.
`person` status change to registered
but will not have full permissions until email confirmation
(an email is sent with confirmation token).

_Request(application/x-www-form-urlencoded):_

_(http headers)_

`Authorization: Token ABXZ` (previous endpoint `access_token` response)

```json
{
    "username": "user.name",
    "email": "email@example.com"
}
```

_Response:_

_200_
```json
{
    "is_registered": true,
    "username": "user.name",
    "email": "email@example.com",
    "is_email_confirmed": false
}
```

### `POST /people/me/email-confirmation`

This endpoint is to confirm email and finish `person` register.
On previous endpoint, an email is sent with a confirmation token.
That token has to be sent as parameter.

_Request(application/x-www-form-urlencoded):_

_(http headers)_

`Authorization: Token ABXZ`

```json
{
    "confirmation_token": "C_T_ABXZ",
}
```

_Response:_

_200_
```json
{
    "is_registered": true,
    "username": "user.name",
    "email": "email@example.com",
    "is_email_confirmed": true
}
```


## Documentation

This project has been developed using Django framework,
with Postgres as database and S3 as storage service.

Code structure follows a Clean Architecture approach
([explained in detail here](http://jordifierro.com/django-clean-architecture)),
emphasizing on code readability, responsibility decoupling
and unit testing.

Authentication part is a little bit custom (to better fit requirements and also with learning purposes).
It doesn't uses Django `User` model nor django-rest-framework, everything is handmade
(everything but cryptography, obviously :) ) and framework untied.
Special things are described here:
* There is anonymous guest user status. That allow users to enter to the app without register
but we can track and analyze them. That also helps making app more secure because
calls are made from guest users but authenticated and we can also control the number of registrations.
* There is no password. Guest user can register just with username and email,
which makes registration process easier. Login will be implemented using token validation via email.
* User is called person. Developer tends to treat a user like a model or a number,
`person` naming aims to remember who is really behind the screen.


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
* Add this to the end of `../env/bin/activate` file:
```bash
source abidria/setup/envvars.sh
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
