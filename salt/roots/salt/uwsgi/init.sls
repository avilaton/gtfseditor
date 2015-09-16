# uwsgi/init.sls

# include:
#   - dependencies
python-pip:
  pkg.installed

uwsgi_package:
  pip.installed:
    - name: uwsgi
    - require:
      - pkg: python-pip

/etc/uwsgi/apps-available/app_wsgi.ini:
  file:
    - managed
    - source: salt://uwsgi/app_wsgi.ini
    - user: vagrant
    - group: vagrant
    - makedirs: True
    - template: jinja
    - mode: 755
    # - require:
    #     - pkg: python3-pip
    #     - cmd: install-requirements

/etc/uwsgi/apps-enabled/app_wsgi.ini:
  file:
    - symlink
    - target: /etc/uwsgi/apps-available/app_wsgi.ini
    - makedirs: True
    - require:
        - file: /etc/uwsgi/apps-available/app_wsgi.ini

/etc/init/uwsgi.conf:
  file:
    - managed
    - source: salt://uwsgi/uwsgi.conf
    - file_mode: 744
    # - require:
    #     - pkg: python3-pip
    #     - cmd: install-requirements

/var/log/uwsgi:
    file:
        - directory
        - user: vagrant
        - group: vagrant
        - makedirs: True
        # - require: 
        #     - pkg: python3-pip
        #     - cmd: install-requirements

uwsgi:
  service:
    - running
    - enable: True
    - require:
        - file: /etc/uwsgi/apps-enabled/app_wsgi.ini
        - file: /etc/init/uwsgi.conf
        - file: /var/log/uwsgi

