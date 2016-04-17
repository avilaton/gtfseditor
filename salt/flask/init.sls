include:
- requirements

/home/vagrant/.virtualenvs/gtfseditor:
    virtualenv.managed:
        - user: vagrant
        - requirements: salt://flask/requirements.txt
        - require:
            - pkg: python-virtualenv