Gtfseditor
==========

A customizable editor for GTFS files which can be used both as a standalone app 
or deployed to a wsgi compliant hosting.

Management
----------
A series of database management scripts are accesible from the command line using 
the `manage.py` script. 

To initialize the database, use 
```
$ python manage.py init-db
```


Installation
------------
Clone the project and `cd` into the new folder using
```
$ git clone git@github.com:avilaton/gtfseditor.git
$ cd gtfseditor
```

Create a new virtual environment and activate it using
```
$ mkdir venv
$ virtualenv venv
$ source venv/bin/activate
```

Install the projects dependencies using
```
pip install -r requirements.txt
```

You can now run the server using
```
./wsgi.py
```

and open your web browser at `http://localhost:8000`.

Configuration
-------------
The main configuration file for the server is located at `server/config.py`.

Development
-----------

The project has two main parts,

- a client application, located at `app/`
- a API server + some building tools at `server/`

The client application uses

- require.js to load javascript modules,
- backbone.js to structure models and views,
- openlayers.js to create and manage the map components,
- bootstrap.js for styling, scaffolding and plugins,
- handlebars.js as a templating engine.

The API server uses

- bottle.py for WSGI,
- SQLAlchemy for database abstraction,
- transitfeed.py for gtfs building and validation.

among other auxiliary packages.

Database
--------

Development and local usage are best served by using **SQLite** as a db engine. It 
allows for rapid setup and portability. 

Some hosted services do not support sqlite as a db engine (heroku), and 
**postgres** can be used.

