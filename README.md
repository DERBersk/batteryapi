# Battery API Documentation

Currently launched on the vercel environment under the following link: https://batteryapi-phi.vercel.app/.

## Data Structure

![Data Structure Image](lib/images/UML.drawio.png)

* Suppliers provide various Materials. Each material has specific Prices that can vary over time and have different lead_times based on the supplier.
* Materials are used in Products, and the amount of material required is recorded in the Material_per_Product relationship.
* Projects involve the production of certain Products over specified time periods.
* Weekly_Material_Demand and Base_Production_Volume manage the weekly demand and the user defined production volumes for each week, respectively.
* Users and Options tables are used for managing user information and strategy options.

## Endpoints

The Battery API offers a range of endpoints to facilitate interactions with user data, supplier information, pricing details, product management, project tracking, and test data generation. Each endpoint serves a specific purpose within the system, allowing integration and manipulation of data to meet diverse requirements. Below is a comprehensive list of endpoints categorized based on their respective functionalities. 

[Endpoint Documentation](documentation/end_point_documentation.md) : List of all API Endpoints and their implemented methods

## Development Environment Setup

### Regular setup

1. Pull the Repository from GitHub ([Repository Link](https://github.com/DERBersk/batteryapi))
2. Install python ([Python Installation](https://www.python.org/downloads/))
3. Install all packages from the [requirements.txt](requirements.txt) file
4. Configure the [config.json](config.json) document by entering:
    * the Email information
    * the Company Name
    * the database (when developing, a path to a data.db file suffices)
5. Run `python api/app.py` in the terminal (also possible in VSCode or other editors)

When completing the steps, the BatteryAPI is running. An other way to launch the application is to use Docker, which is described in the following.

### Installation with Docker

1. Pull the Repository from GitHub ([Repository Link](https://github.com/DERBersk/batteryapi))
2. Install docker ([Docker Installation](https://docs.docker.com/get-docker/))
3. Configure the [config.json](config.json) document by entering:
    * the Email information
    * the Company Name
    * the database (when developing, a path to a data.db file suffices)
4. Run `docker build --tag batteryapi .` to build an image
5. Run `docker run -d -p 5000:5000 batteryapi` to start the image

After these four steps, the Container is built and deployed.

### Development Information

Local development is the fastest way to implement new features and to test them. Generally it is advised to work with a regular setup, as with docker, after every change, the image has to be stopped, rebuild and started, while with the regular installation, the testing can start in a matter of seconds.

## File Structure

The code is currently structured the following way:

```
├── api
│   ├── app.py
├── documentation
│   ├── ...
├── functions
│   ├── ...
├── lib
│   ├── ...
├── models
│   ├── ...
├── routes
│   ├── ...
├── templates
│   ├── ...
└── extensions.py
```

* `api/app.py` is the core of the project and activates all routes and initiates the database. This file is called when starting the application.
* `documentation` encompasses all Markdown files regarding routing and a guide on how to add new fields.
* `functions` includes all python files regarding more complex functions to be separated from the route files.
* `lib` holds all files that are in the category of either data or images.
* `models` includes all database structures (tables and columns) and their respective functions to be used on one specific instance of the table.
* `routes` regards all defined routes. These do not have to be, but currently are all registered in the app.py file.
* `templates` includes all html files used for supplier access.
* `extensions.py` defines all Singleton objects, such as the database and the scheduler