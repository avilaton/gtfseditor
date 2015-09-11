include:
- core

/home/vagrant/venv:
    virtualenv.managed:
        - system_site_packages: False
        - user: vagrant
        - requirements: /home/vagrant/app/requirements.txt
        - require:
            - pkg: python-virtualenv