qrequest
========

Instantly create an API and web interface for SQL queries.


1. Write SQL queries to collect the data users can access. Use :keywords for parameters.
2. Put the queries in the sql/ directory, and change the database drivers and connection strings in settings/settings.json
3. Then run `python qrequest.py` to get a website which lets users run any of your queries without installing a thing, as well as an API endpoint.

Users can view queries through the web interface, and download the json or csv formatted query results.

Run

```
python qrequest.py
```

then look at the example queries and example sqlite database.

The URL format for the json endpoint is `/api/query_name.json?first_param=value1&second_param=value2` etc.
The URL format for the CSV endpoint is `/api/query_name.csv?first_param=value1&second_param=value2` etc.
