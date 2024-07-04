# Show Multiple Project

Show data of a All Projects ordered by id.

**URL** : `/api/projects/`

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
        "end_week": 5,
        "end_year": 2025,
        "id": 1,
        "partner": "Greene PLC",
        "start_week": 1,
        "start_year": 2025,
        "product_count": 2
    },
    {
        "end_week": 50,
        "end_year": 2024,
        "id": 2,
        "partner": "Allen-Gonzales",
        "start_week": 48,
        "start_year": 2024,
        "product_count": 20
    },
    ...
]
```

# Show Single Project

Show data of a single Project and its associated tables: Products and ProductsPerProject 

**URL** : `/api/projects/<project_id>`

**URL Parameters** : `project_id=[integer]` where `project_id` is the ID of the Project.

**Method** : `GET`

**Data**: 

```json
{
    
}
```

## Success Response

**Condition** : If Project exists.

**Code** : `200 OK`

**Content example**:

```json
{
    "id": 1,
    "end_week": 20,
    "end_year": 2024,
    "materials": [
        {
            "amount": 12,
            "component_parts_type": null,
            "description": "Lithium-Ion Battery Pouch v1",
            "id": 5,
            "raw_material_type": null,
            "specification": "Pouch",
            "external_id":"1131-USA"
        },
        {
            "amount": 45,
            "component_parts_type": null,
            "description": "Lithium-Ion Battery Pouch v3",
            "id": 1,
            "raw_material_type": null,
            "specification": "Pouch",
            "external_id":""
        }
    ],
    "partner": "Greene PLC",
    "start_week": 14,
    "start_year": 2024 
}
```

## Error Responses

**Condition** : If Project does not exist with `id` of provided `project_id` parameter.

**Code** : `404 NOT FOUND`

**Content** : `{'message': 'Project with id {project_id} not found'}`