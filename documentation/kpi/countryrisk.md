# Show Country-Risk Index for all countries

Show data of a calculated Country-Risk Index

**URL** : `/api/kpi/countryrisk`

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
        "countrycode":"AF",
        "description":"Afghanistan",
        "no.":0.915
    },
    {
        "countrycode":"AX",
        "description":"Aland Islands",
        "no.":0.26
    },
    {
        "countrycode":"AL",
        "description":"Albania",
        "no.":0.293
    },
    ...
]
```