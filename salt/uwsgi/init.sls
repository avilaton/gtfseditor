uwsgiinstall:
  pkg:
    - name: uwsgi
    - installed

gtfseditor_uwsgi_conf:
  file.managed:
    - name: /etc/uwsgi/apps-available/gtfseditor.ini
    - source: salt://uwsgi/gtfseditor.ini
    - template: jinja

enable_gtfseditor_uwsgi_app:
    file.symlink:
        - name: /etc/uwsgi/apps-enabled/gtfseditor.ini
        - target: /etc/uwsgi/apps-available/gtfseditor.ini
        - force: false
        - require:
            - file: gtfseditor_uwsgi_conf

# Set directory owner
uwsgi_log_dir_structure:
  file.directory:
    - name: /var/log/uwsgi
    - mode: 777

uwsgi:
  service.running:
    - require:
      - pkg: uwsgi
    - watch:
      - file: /etc/uwsgi/apps-available/gtfseditor.ini