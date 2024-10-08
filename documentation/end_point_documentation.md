### KPI related

Under this endpoint, all KPIs can be accessed and / or generated. The KPIs are Country-Risk, ... 

* [Show Country-Risk](kpi/countryrisk.md) `GET /api/kpi/countryrisk`
* [Show and Calculate Weekly Material Demand](kpi/weeklyDemand.md) `GET /api/kpi/materialDemand`
* [Show and Calculate Optimal Orders](kpi/optimalOrder.md) `GET /api/kpi/optimalOrders` & `GET /api/kpi/optimalOrdersOneWeek`
* [Calculate Supplier Reliability](kpi/reliability.md) `GET /api/kpi/reliability`
* [Calculate Supplier Risk](kpi/riskindex.md) `GET /api/kpi/riskindex`
* [Calculate Supplier Sustainability](kpi/sustainabilityindex.md) `GET /api/kpi/susindex`
* [Show Critical Suppliers](kpi/criticalSuppliers.md) `GET /api/kpi/criticalSuppliers`
* [Show all incoming Orders](kpi/incomingOrders.md) `GET /api/kpi/incomingOrders`
* [Show all Materials without Supplier](kpi/materialWithoutSupplier.md) `GET /api/kpi/materialWithoutSupplier`
* [Show Material Per Supplier Entries Without Price](kpi/materialPerSupplierWithoutPrice.md) `GET /api/kpi/MaterialPerSupplierWithoutPrice`
* [Show Products without BOM](kpi/productsWithoutMaterials.md) `GET /api/kpi/productsWithoutMaterials`
* [Show the most produced Product](kpi/mostProduced.md) `GET /api/kpi/mostProduced`
* [Show the Order Volume in the past year](kpi/orderVolume.md) `GET /api/kpi/orderVolume`
* [Show and Calculate Weekly Production](kpi/production.md) `GET /api/kpi/production`
* [Show Material Demand over the next 5 weeks](kpi/materialDemand5Weeks.md) `GET /api/kpi/materialDemand5Weeks`
* [Show Product Demand over the next 5 weeks](kpi/productDemand5Weeks.md) `GET /api/kpi/productDemand5Weeks`

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

### External Production Data related

The External Production Data endpoint allows for management of additional production plans to the projects. External Production Data can be retrieved and updated using respective HTTP methods.

* [Show External Production Data](external_production/get.md) : `GET /api/externalproduction/`
* [Create External Production Data](external_production/post.md) : `POST /api/externalproduction/`

### Order related

The Order endpoint allows for management of Historical and current Orders. Order Data can be retrieved, created and deleted using respective HTTP methods.

* [Show Orders](order/get.md) : `GET /api/order/`
* [Create Orders](order/post.md) : `POST /api/order/`
* [Delete Order](order/delete.md) : `DELETE /api/order/`

### External Communication related

The Communication endpoints allow for emails to be sent out to suppliers including a link to the `update-form.html`, which then allows the supplier to enter necessary data themselves.

* [Send Email Link](external/generate_link.md) : `POST /api/external/generate_link/`
* [Update Supplier Data Form](external/update_data.md) : `POST,GET /api/external/generate_link/`

### Options related

The Options endpoint allows for management of the general Options. Order Data can be retrieved, created and edited using respective HTTP methods.

* [Show Options](options/get.md) : `GET /api/options/` | `GET /api/options/weights`
* [Create/Edit Options](options/post.md) : `POST /api/options/`| `POST /api/options/weights`