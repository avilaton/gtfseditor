dbuser:
    postgres_user.present:
        - name: {{ pillar['dbuser'] }}
        - password: {{ pillar['dbpassword'] }}
        - user: postgres
        - require:
            - service: postgresql

db:
    postgres_database.present:
        - name: {{ pillar['dbname'] }}
        - encoding: UTF8
        - lc_ctype: en_US.UTF8
        - lc_collate: en_US.UTF8
        - template: template0
        - owner: {{ pillar['dbuser'] }}
        - user: postgres
        - require:
            - postgres_user: dbuser

# Activate virtualenv on login
bashrc:
  file.append:
    - name: {{ pillar['system']['home'] + '/.bashrc' }}
    - text:
      - {{ "source " + pillar['virtualenv']['path'] + "/bin/activate"}}
      - "cd gtfseditor/"
      - "export DATABASE_URL=\"postgresql://{{ pillar['dbuser'] }}:{{ pillar['dbpassword'] }}@localhost:5432/{{ pillar['dbname'] }}\""

sync_db:
  cmd.run:
    - user: {{ pillar['system']['user'] }}
    - group: {{ pillar['system']['group'] }}
    - cwd: {{ pillar['application']['path'] }}
    - env:
        - 'DATABASE_URL': 'postgresql://{{ pillar['dbuser'] }}:{{ pillar['dbpassword'] }}@localhost:5432/{{ pillar['dbname'] }}'
    - names:
      - {{ pillar['virtualenv']['path'] + '/bin/python manage.py deploy' }}
      - sudo service uwsgi reload
