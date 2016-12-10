system:
  user: vagrant
  group: vagrant
  home: /home/vagrant
  user_password: vagrant

application:
  path: /home/vagrant/gtfseditor
  statics_dir: /home/vagrant/static
  flask_config: production
  feed_name: feed_name

virtualenv:
  path: /home/vagrant/.virtualenvs
  requirements: /home/vagrant/gtfseditor/requirements.txt
