include:
- core

/home/vagrant/venv:
    virtualenv.managed:
        - system_site_packages: False
        - user: {{ pillar['system']['user'] }}
        - requirements: {{ pillar['virtualenv']['requirements'] }}
        - require:
            - pkg: python-virtualenv