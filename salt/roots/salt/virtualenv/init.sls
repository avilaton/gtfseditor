include:
- core

gtfsvenv:
    virtualenv.managed:
        - name: {{ pillar['system']['home']}} + '/venv'
        - system_site_packages: False
        - user: {{ pillar['system']['user'] }}
        - requirements: {{ pillar['virtualenv']['requirements'] }}
        - require:
            - pkg: python-virtualenv