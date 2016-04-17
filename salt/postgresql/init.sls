postgresql:
    pkg:
        - name: postgresql-9.3
        - installed
    service.running:
        - enabled: True
        - watch:
            - file: /etc/postgresql/9.3/main/pg_hba.conf