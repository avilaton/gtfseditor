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
/home/vagrant/.bashrc:
  file.append:
    - text:
      - "source venv/bin/activate"
      - "cd app/"
      - "export DATABASE_URL=\"postgresql://{{ pillar['dbuser'] }}:{{ pillar['dbpassword'] }}@localhost:5432/{{ pillar['dbname'] }}\""