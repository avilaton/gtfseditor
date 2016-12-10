base:
  '*':
    - settings
    {% if salt['file.file_exists']('/srv/salt/pillar/local.sls') %}
    - local
    {% else %}
    - default
    {% endif %}