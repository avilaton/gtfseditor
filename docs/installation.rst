Installation
============

This part of the documentation covers the installation of Transit Manager.


Clone the project and move into the new folder using::

    git clone https://github.com/avilaton/gtfseditor.git
    cd gtfseditor


which will get you the latest version.

Create a new virtual environment (we named it ``gtfseditor`` but you can name it 
anything you like) and activate it using
::

    mkvirtualenv gtfs

You should now see your command line prompt changed to something like
::

    (gtfs)$


Install the projects dependencies using
::

    pip install -r requirements.txt


You can now run the server using
::

    honcho start

and open your web browser at `http://localhost:5000`_ .

.. _http://localhost:5000: https://localhost:5000