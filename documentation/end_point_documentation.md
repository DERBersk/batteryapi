### KPI related

Under this endpoint, all KPIs can be accessed and / or generated. The KPIs are Country-Risk, ... 

* [Show Country-Risk](kpi/countryrisk.md) `GET /api/kpi/countryrisk`
* [Show and Calculate Weekly Material Demand](kpi/weeklyDemand.md) `GET /api/kpi/weeklyDemand`
* [Show and Calculate Optimal Orders](kpi/optimalOrder.md) `GET /api/kpi/optimalOrders`
* [Calculate Supplier Reliability](kpi/reliability.md) `GET /api/kpi/reliability`

### Material related

The Material endpoint provides functionality for managing material data within the Battery API. Materials can be retrieved, created, and deleted using respective HTTP methods.

* [Show Material](material/get.md) : `GET /api/materials/`
* [Create Material](material/post.md) : `POST /api/materials/`
* [Delete Material](material/delete.md) : `DELETE /api/materials/`


### User related

The User endpoint provides functionality for managing user data within the Battery API. Users can be retrieved, created, and deleted using respective HTTP methods.

* [Show User](user/get.md) : `GET /api/user/`
* [Create User](user/post.md) : `POST /api/user/`
* [Delete User](user/delete.md) : `DELETE /api/user/`

### Supplier related

The Supplier endpoint enables the management of supplier information within the Battery API. Suppliers can be retrieved, created, and deleted using respective HTTP methods.

* [Show Supplier](supplier/get.md) : `GET /api/supplier/`
* [Create Supplier](supplier/post.md) : `POST /api/supplier/`
* [Delete Supplier](supplier/delete.md) : `DELETE /api/supplier/`

### Price related

The Price endpoint offers functionality for managing pricing details within the Battery API. Prices can be retrieved, created, and deleted using respective HTTP methods.

* [Show Price](price/get.md) : `GET /api/price/`
* [Create Price](price/post.md) : `POST /api/price/`
* [Delete Price](price/delete.md) : `DELETE /api/price/`

### Product related

The Product endpoint provides capabilities for managing product data within the Battery API. Products can be retrieved, created, and deleted using respective HTTP methods.

* [Show Product](product/get.md) : `GET /api/product/`
* [Create Product](product/post.md) : `POST /api/product/`
* [Delete Product](product/delete.md) : `DELETE /api/product/`

### Project related

The Project endpoint facilitates the management of project information within the Battery API. Projects can be retrieved, created, and deleted using respective HTTP methods.

* [Show Project](project/get.md) : `GET /api/project/`
* [Create Project](project/post.md) : `POST /api/project/`
* [Delete Project](project/delete.md) : `DELETE /api/project/`

### Base Production related

The Base Production endpoint allows for management of additional production plans to the projects. Base Production Data can be retrieved, created and deleted using respective HTTP methods.

* [Show Base Production](base_production/get.md) : `GET /api/baseproduction/`
* [Create Base Production](base_production/post.md) : `POST /api/baseproduction/`
* [Delete Base Production](base_production/delete.md) : `DELETE /api/baseproduction/`

### Order related

The Order endpoint allows for management of Historical and current. Order Data can be retrieved, created and deleted using respective HTTP methods.

* [Show Orders](order/get.md) : `GET /api/order/`
* [Create Orders](order/post.md) : `POST /api/order/`
* [Delete Order](order/delete.md) : `DELETE /api/order/`

### External Communication related

The Communication endpoints allow for emails to be sent out to suppliers including a link to the `update-form.html`, which then allows the supplier to enter necessary data themselves.

* [Send Email Link](external/generate_link.md) : `POST /api/external/generate_link/`
* [Update Supplier Data Form](external/update_data.md) : `POST,GET /api/external/generate_link/`