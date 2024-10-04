# Tournament server

## Models

### User

Inherit default django user.
Read: https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#substituting-a-custom-user-model.

#### Additional fields

- avatar: `models.ImageField`
    - description: "the user avatar picture";
    - `media/default.png` by default;
    - max image resolution 100x100;
    - max image size 5mb;
    - available format: `png`, `jpg`, `jpeg`;
    - use the `media` directory as images storage.
- is_verified: `models.BooleanField`
    - description: "the user email verification status";
    - True by default.
- rating: `models.IntegerField`
    - 0 by default

#### Notes

- create default file inside the `media` directory;
- the `is_verified` user model field is useless, it can be used in future features;
- same for the `rating` field.

### Team

#### Fields

- id
- name: `models.CharField`
    - unique;
    - max length 50;
- avatar: `models.ImageField`:
    - same as `User.avatar`;
- member1: `models.ForeignKey`
    - relation with `User` model;
    - description: user that creates this team instance;
- member2: `models.ForeignKey`
    - relation with `User` model;
    - description: second user that has been invited by the team creator;
- status: `models.CharField`
    - source: https://docs.djangoproject.com/en/5.1/ref/models/fields/#enumeration-types
    - use `models.TextChoices` or `models.IntegerChoices` subclasses
    - available statuses: WAITING, ACTIVE, DISBANDED
    - WAITING by default (on creation)
- description: `models.CharField`
    - empty string by default
    - max length 250 characters
- date_created: `models.DateTimeField`
    - automatically sets on creation
- date_disbanded: `models.DateTimeField`
    - description: date when this team has been disbanded
    - `None` by default

### Tournament

### TournamentTeam

### Match

### UserTournamentHistory

### UserMatchHistory

## Endpoints

### A12n

- POST `/auth/signup/`: create new user instance with received `email`, `username` and `password` fields;
- POST `/auth/login/`: get or create user auth token (read: https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication);
- POST `/auth/logout/`: (!auth token is required) delete all user auth tokens.
- POST `/auth/signup/verify/`: no effect, return 501 without any actions.

### Users

An authentication token is required for all endpoints (read: https://www.django-rest-framework.org/api-guide/permissions/#isauthenticated).

- GET `/users/`: return list of users instances
    - available GET parameters:
        - `username`: search users that starts with provided `username` GET parameter (for example, if the requested url looks like `/users/?username=abc`, then returns all users whose username starts with the `abc` substring).
    - expected fields: id, username, full_name, avatar (as url to the local file).
- GET `/users/me/`: return the current user data
- PUT/PATCH `/users/me/`: update the specific
- GET `/users/<user_id>/`: return the specific (by user_id) user data

### Teams

An authentication token is required for all endpoints (exclude GET `/teams/<team_id>/`).

- GET `/teams/`: return list of teams instances where the current user member1 or member2
    - available GET parameters:
        - `name`: search teams instances that starts with received `name`.
    - expected fields: id, avatar, name, description, member1, member2, date_created, date_disbanded.
- POST `/teams/`: create new team instance
    - additional validation rules:
        - does not exist WAITING or ACTIVE teams with save member1 and member2
        - does not exist DISBANDED team that was disbanded less than a week ago
    - the current user SHOULD be set as `member1`, another user - `member2`
    - note: check, that a client can not to create new team instance with status that not matches with WAITING
- GET `/teams/<team_id>/`: (!auth token is not required) return the specific team data
- PUT/PATCH `/teams/<team_id>/`: update name, description or avatar
    - can be updated only by members
- PATCH `/teams/<team_id>/invite-accept/`: change the team status on ACTIVE
    - available only for `member2` and the team status is WAITING
- PATCH `/teams/<team_id>/invite-reject/`: change the team status on DISBANDED
    - available only for `member2` and the team status is WAITING
    - note: check that `date_disbanded` changes
- PATCH `/teams/<team_id>/disband/`: change the team status on DISBANDED
    - available on for members abd the team status is ACTIVE

### Tournaments

An authentication token is required for all endpoints (exclude GET `/teams/<team_id>/`).

GET `/tournaments/`
POST `/tournaments/`
GET `/tournaments/<tournament_id>/`
PUT/PATCH `/tournaments/<tournament_id>/`

GET `/tournaments/<tournament_id>/teams/`

POST `/tournaments/<tournament_id>/join/`
GET `/tournaments/<tournament_id>/members/`
GET `/tournaments/<tournament_id>/matches/`

