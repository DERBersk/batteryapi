# Create User and Connected Tables

Create or modify one or many Users.

**URL** : `/api/user/`

**Method** : `POST`

**Data example** All fields must be sent except id.

```json
[
    {
        "id": 1,
        "email": "New john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "created_date": "2024-05-10"
    },
    ...
]
```

## Success Response

**Condition** : If everything is OK and for all given id, a respective instance exists.

**Code** : `201 CREATED`

**Content example**: `{'message': 'User created/updated successfully'}`

## Error Responses

### 404 Not Found

**Condition** : A User id is given without it existing in the database.

**Code** : `404 NOT FOUND`

**Content** : 

`{'message': 'User with id {user_id} not found'}`

### 400 Bad Request

**Condition** : If the format is not given as a List

**Code** : `400 Bad request`

**Content** : 

`{'message': 'Invalid data format. Expected a list of Users.'}`
