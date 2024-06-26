# Create Projects and Connected Tables

Create or modify one or many Projects and each respective fitted table (ProductsPerProjects, Products)

**URL** : `/api/projects/`

**Method** : `POST`

**Comment** : For the Project and Products: If the id is not given, a new instance is created. If the id is given, the instance is expected to exist and created in a new fashion. The ProductsPerProject is deleted for the Project. so that every given instance is then every existing instance for the respective Project.

**Data example** All fields must be sent except id.

```json
[
    {
        "partner": "New Projectpartner",
        "start_week": 10,
        "start_year": 2025,
        "end_week": 14,
        "end_year": 2025,
        "production_schedule": "Two shifts per day",
        "machine_labor_availability": "High",
        "products": [
        {
            "id": 1,
            "amount": 200,
        }
        ]
    },
    ...
]
```

## Success Response

**Condition** : If everything is OK and for all given id, a respective instance exists.

**Code** : `201 CREATED`

**Content example**: `{'message': 'Projects created/updated successfully'}`

## Error Responses

### 404 Not Found

**Condition** : Either a project id is given without it existing in the database or a product id is given without it existing.

**Code** : `404 NOT FOUND`

**Content** : 

`{'message': 'Product with id {product_id} not found'}`

`{'message': 'Project with id {project_id} not found'}`

### 400 Bad Request

**Condition** : If the format is not given as a List

**Code** : `400 Bad request`

**Content** : 

`{'message': 'Invalid data format. Expected a list of Projects.'}`

