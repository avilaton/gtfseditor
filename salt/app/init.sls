include:
- system

gtfseditor_repository:
    git.latest:
        - user: vagrant
        - name: https://github.com/avilaton/gtfseditor.git
        - branch: develop
        - target: /home/vagrant/gtfseditor/
        - require:
            - pkg: git


/home/vagrant/.virtualenvs/gtfseditor:
    virtualenv.managed:
        - user: vagrant
        - requirements: /home/vagrant/gtfseditor/requirements.txt
        - pip_exists_action: s
        - require:
            - pkg: python-virtualenv
            - git: gtfseditor_repository


gtfs_db_user:
    postgres_user.present:
        - name: dbuser
        - password: dbpassword
        - user: postgres
        - require:
            - service: postgresql


gtfs_db:
    postgres_database.present:
        - name: gtfseditor
        - encoding: UTF8
        - lc_ctype: en_US.UTF8
        - lc_collate: en_US.UTF8
        - template: template0
        - owner: dbuser
        - user: postgres
        - require:
            - postgres_user: gtfs_db_user


# uwsgi_service:
#   supervisord.running:
#     - name: uwsgi
#     - restart: True