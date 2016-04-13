include:
- requirements

/home/vagrant/.virtualenvs/gtfseditor:
    virtualenv.managed:
        - no_site_packages: True
        - runas: vagrant
        - requirements: salt://flask/requirements.txt
        - require:
            - pkg: python-virtualenv