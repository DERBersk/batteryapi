# Show Multiple User

Show data of a All _.

**URL** : `/api/user/`

**Method** : `GET`

**Data**: 

```json
{
    
}
```

## Success Response

**Code** : `200 OK`

**Content example**:

```json
[
    {
        "id": 1,
        "email": "PeterMustermann@gmail.com",
        "last_name": "Mustermann",
        "first_name": "Peter",
        "created_date": "Mon, 13 Jan 2025 00:00:00 GMT",
    },
    {
        "id": 2,
        "email": "PetraMusterfrau@gmail.com",
        "last_name": "Musterfrau",
        "first_name": "Petra",
        "created_date": "Mon, 1 Jan 2022 00:00:00 GMT",
    },
    ...
]
```

# Show Single User

Show data of a single User.

**URL** : `/api/user/<user_id>`

**URL Parameters** : `user_id=[integer]` where `user_id` is the ID of the User.

**Method** : `GET`

**Data**: 

```json
{
    
}
```

## Success Response

**Condition** : If User exists.

**Code** : `200 OK`

**Content example**:

```json
{
    "id": 1,
    "email": "PeterMustermann@gmail.com",
    "last_name": "Mustermann",
    "first_name": "Peter",
    "created_date": "Mon, 13 Jan 2025 00:00:00 GMT",
}
```

## Error Responses

**Condition** : If User does not exist with `id` of provided `User_id` parameter.

**Code** : `404 NOT FOUND`

**Content** : `{'message': 'User with id {user_id} not found'}`