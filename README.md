Gtfseditor
==========

A customizable editor for GTFS files which can be used both as a standalone app 
or deployed to a wsgi compliant hosting.


Installation
------------
Clone the project and `cd` into the new folder using
```
$ git clone https://github.com/avilaton/gtfseditor.git
$ cd gtfseditor
```
which will get you the latest version.

Create a new virtual environment (we named it __gtfs__ but you can name it 
anything you like) and activate it using
```
$ mkvirtualenv gtfs
```
You should now see your command line prompt changed to something like
```
(gtfs)$ 
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


Management
----------
A series of database management scripts are accesible from the command line using 
the `manage.py` script. 

To initialize the database, use
```
$ ./manage.py db upgrade
```
In development mode this will create a file called data-dev.sqlite in the same 
directory with a DB looking like the one in production.



Configuration
-------------
The main configuration file for the server is located at `server/config.py`. It 
is being ported to `config.py`.


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

Install postgresql and run

```
createdb -T template0 dbname
```
You are now ready to import a DB dump 
```
```
or initialize this db by using
```
FLASK_CONFIG=dev ./manage.py db upgrade
```
