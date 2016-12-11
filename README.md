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
$ ./manage.py db upgrade
```
In development mode this will create a file called data-dev.sqlite in the same
directory with a DB looking like the one in production.



Configuration
-------------
The main configuration file for the server is located at `config.py`. Environment variables 
can be overriden by writing them inside a .env file at the root level.


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

- flask.py for WSGI,
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
You are now ready to initialize an empty DB by using
```
FLASK_CONFIG=dev ./manage.py db upgrade
```

Importing a DB dump
-------------------

To create a database dump use
```
pg_dump -Fc --no-acl --no-owner dbname > mydb.dump
```

To import a DB dump run
```
pg_restore -d dbname dump.tar
```
where **dbname** is the name of your database.


Deployment to EC2
=================

Set up an ubuntu instance in Amazon EC2. On it, run
```
$ sudo apt-get update
$ sudo apt-get install python-pip libpq-dev python-dev nginx postgresql postgresql-contrib
```

Configuring nginx
-----------------

Create a site file in `/etc/nginx/sites-available/` by copying the example file `nginx.site.example` over and editing it appropriately. Once you are done, enable the site using
```
$ sudo ln -s \
/etc/nginx/sites-available/mydomain.com \
/etc/nginx/sites-enabled/mydomain.com
```
where `mydomain.com` is the name of the file you created.

Configuring Postgresql
----------------------

Create a database user with the same name as your current username
```
$ sudo -u postgres createuser --superuser $USER
```
and change it's password using
```
$ sudo -u postgres psql
...
postgres=# \password $USER
```
This user will not need a password to connect to the DB.
