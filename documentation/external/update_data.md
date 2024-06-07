# Update Supplier Data

Update the data for a supplier using a unique token-based authentication.

**URL** : `/api/external/update_data/<token>`

**Method** : `GET`, `POST`

**Data** : None (GET), Form data (POST)

## Parameters

**token** (string, required) - The unique token provided to authenticate and authorize the supplier to update their data.

## Success Response

**Code** : `200 OK`

**Content** : `Data updated successfully`

## Error Responses

**Code** : `404 Not Found`

**Content** : `Invalid Supplier.`

**Code** : `403 Forbidden`

**Content** : `Link has expired.`

**Code** : `400 Bad Request`

**Content** : `Invalid Link.`

## Description

This endpoint allows a supplier to update their data securely by providing a unique token received via email. Upon accessing the update link, the supplier is presented with a form pre-filled with their existing data, including details of associated materials. The supplier can modify the data as needed and submit the form to apply the changes.

The endpoint supports both `GET` and `POST` methods. 
- When accessed via `GET`, the endpoint renders an HTML form populated with the supplier's current data.
- Upon form submission (`POST`), the endpoint updates the supplier's information in the database with the provided data.

![Supplier Form](lib/images/SupplierForm.jpeg)

The token passed in the URL is validated against a pre-generated list of tokens to ensure the authenticity of the request. Additionally, the expiration time of the token is checked to prevent unauthorized access after the token's validity period.

