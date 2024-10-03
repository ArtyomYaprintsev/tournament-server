# Tournament-server

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
- POST `/auth/logout/`: delete all user auth tokens;

### Users

All endpoints requires auth token (read: https://www.django-rest-framework.org/api-guide/permissions/#isauthenticated).

- GET `/users/`: return list of users instances
    - available parameters:
        - `username`: search users that starts with provided `username` GET parameter (for example, if the requested url looks like `/users/?username=abc`, then returns all users whose username starts with the `abc` substring).
    - expected fields: id, username, full_name, avatar (as url to the local file).
- GET `/users/me/`: return the current user data
- PUT/PATCH `/users/me/`: update the specific
- GET `/users/<username>/`: return the specific (by username) user data
