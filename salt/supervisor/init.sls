supervisor_conf:
  file.managed:
    - name: /etc/supervisor/supervisord.conf
    - source: salt://supervisor/supervisord.conf
    - template: jinja

uwsgi_conf:
  file.managed:
    - name: /etc/supervisor/conf.d/uwsgi.conf
    - source: salt://supervisor/uwsgi.conf
    - template: jinja

supervisor:
  pkg:
    - installed
  service.running:
    - require:
      - pkg: supervisor
    - watch:
      - file: /etc/supervisor/supervisord.conf
      - file: /etc/supervisor/conf.d/uwsgi.conf
      - file: /etc/uwsgi/apps-available/gtfseditor.ini
