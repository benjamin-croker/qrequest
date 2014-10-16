qrequest
========

Instantly create an API and web interface for SQL queries.


1. Write SQL queries to collect the data users can access. Use :keywords for parameters.
2. Put these queries in the sql/ directory
3. Modify the settings below and save as settings/settings.json
4. Then run `python qrequest.py` to get a website which lets users run any of your queries without installing a thing, as well as an API endpoint.

Use the example below for the settings.json file
```
{
    "db_driver": "<name of python module. eg:sqlite3>",
    "db_connection_string": "<database connection string. eg:example.db>",
    "website_title": "qRequest",
    "website_description": "An example page showing how qRequest can be configured",
    "website_port_number": 5000
}
```

Users can view queries through the web interface, and download the json or csv formatted query results.


The URL format for the json endpoint is
```
/api/query_name.json?first_param=value1&second_param=value2
```

The URL format for the CSV endpoint is
```
/api/query_name.csv?first_param=value1&second_param=value2
``` 
