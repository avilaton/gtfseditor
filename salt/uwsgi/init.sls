uwsgiinstall:
  pkg:
    - name: uwsgi
    - installed

gtfseditor_uwsgi_conf:
  file.managed:
    - name: /etc/uwsgi/gtfseditor.ini
    - source: salt://uwsgi/gtfseditor.ini
    - template: jinja

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
      - file: /etc/uwsgi/gtfseditor.ini