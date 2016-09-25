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
      - '{{ pillar.virtualenv.path + '/bin/python manage.py db upgrade' }}'
      - 'sudo service uwsgi reload'

feeds_folder:
  file.directory:
    - name: '{{pillar.system.home}}/feeds'
    - user: {{pillar.system.user}}
    - group: {{pillar.system.group}}

{% set feed_dir = pillar.system.home + '/feeds/' + pillar.application.feed_name %}

feed_folder:
  file.directory:
    - name: '{{feed_dir}}'
    - user: {{pillar.system.user}}
    - group: {{pillar.system.group}}
    - require:
      - file: feeds_folder

static_folder:
  file.directory:
    - name: '{{pillar.system.home}}/static'
    - user: {{pillar.system.user}}
    - group: {{pillar.system.group}}

buildfeed_env:
  cron.env_present:
    - name: 'DATABASE_URL'
    - user: {{ pillar.system.user }}
    - value: 'postgresql://{{ pillar['dbuser'] }}:{{ pillar['dbpassword'] }}@localhost:5432/{{ pillar['dbname'] }}'

buildfeed_env_target_folder:
  cron.env_present:
    - name: 'GTFSEDITOR_FEED_FOLDER'
    - user: {{ pillar.system.user }}
    - value: '{{pillar.system.home}}/feeds/{{pillar.application.feed_name}}/'
    - require:
      - file: feed_folder

buildfeed:
  cron.present:
    - user: {{ pillar.system.user }}
    - hour: 0
    - minute: 0
    - dayweek: '1-5'
    - identifier: buildfeed_job
    - name: 'cd {{ pillar.application.path }} && {{ pillar.virtualenv.path }}/bin/python manage.py buildfeed 2>&1 | tee {{feed_dir}}/build_log.txt | /usr/bin/logger -t buildfeed'
    - require:
      - cron: buildfeed_env
      - cron: buildfeed_env_target_folder
