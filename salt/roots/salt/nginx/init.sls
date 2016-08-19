# nginx/init.sls

include:
  - uwsgi

nginx:
  pkg:
    - installed
  service:
    - running
    - enable: True
    - reload: True
    - require:
      - pkg: nginx
      - file: /etc/nginx/nginx.conf
      - file: /etc/nginx/sites-available/app.conf
      - file: /etc/nginx/sites-enabled/app.conf
      - file: /etc/nginx/sites-enabled/default
      - service: uwsgi-service
    - watch:
      - service: uwsgi-service

/etc/nginx/nginx.conf:
  file:
    - managed
    - source: salt://nginx/nginx.conf
    - template: jinja
    - require:
        - pkg: nginx

/etc/nginx/sites-available/app.conf:
  file:
    - managed
    - source: salt://nginx/app.conf
    - template: jinja
    - require:
        - pkg: nginx

/etc/nginx/sites-enabled/app.conf:
  file:
    - symlink
    - target: /etc/nginx/sites-available/app.conf
    - require:
        - file: /etc/nginx/sites-available/app.conf

/etc/nginx/sites-enabled/default:
  file:
    - absent
