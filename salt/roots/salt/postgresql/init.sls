pg_hba.conf:
    file.managed:
        - name: /etc/postgresql/9.4/main/pg_hba.conf
        - source: salt://postgresql/pg_hba.conf
        - user: postgres
        - group: postgres
        - mode: 644
        - require:
            - pkg: postgresql-9.4

postgresql:
    pkg:
        - name: postgresql-9.4
        - installed
    service.running:
        - enable: True
        - watch:
            - file: /etc/postgresql/9.4/main/pg_hba.conf

postgresql-9.4-dbg:
    pkg:
        - name: postgresql-9.4-dbg
        - installed

postgresql-server-dev-9.4:
    pkg:
        - name: postgresql-server-dev-9.4
        - installed