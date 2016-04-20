pg_hba.conf:
    file.managed:
        - name: /etc/postgresql/9.3/main/pg_hba.conf
        - source: salt://postgresql/pg_hba.conf
        - user: postgres
        - group: postgres
        - mode: 644
        - require:
            - pkg: postgresql-9.3


postgresql:
    pkg:
        - name: postgresql-9.3
        - installed
    service.running:
        - watch:
            - file: /etc/postgresql/9.3/main/pg_hba.conf