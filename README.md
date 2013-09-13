gtfseditor
==========

wsgi application to be both a standalone gtfs editor or deployed to google app engine/other wsgi compliant hosting.


Usage
-----

Fetch dependencies using

	bower install

then run

	./dev_server.py

and point your browser to `http://localhost:8080`.

notes
-----
using behind corporate proxy needs

	git config --global url."https://".insteadOf git://

and .bowerrc

	{
		proxy: http://ip:port,
		https-proxy: http://ip:port
	}

