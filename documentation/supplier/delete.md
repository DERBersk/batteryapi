# Delete Suppliers

Delete one Supplier via id and associated MaterialsPerSupplier and Prices.

**URL** : `/api/supplier/<supplier_id>`

**URL Parameters** : `supplier_id=[integer]` where `supplier_id` is the ID of the Supplier.

**Method** : `DELETE`

**Data** : 

```json
{

}
```

## Responses

#### Success Response

**Condition** : If the Supplier exists.

**Code** : `200 OK`

**Content** : `{'message':'Supplier and associated records deleted successfully'}`

#### Error Responses

**Condition** : If there was no Supplier available to delete.

**Code** : `404 NOT FOUND`

**Content** : `{'error': 'Supplier not found'}`


## Example 

**Call**: `DELETE /api/supplier/1`

**Data**:

```json
{

}
```

**Response**: 

`200 OK`

`{'message':'Supplier and associated records deleted successfully'}`
