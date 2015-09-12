# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/trusty64"
  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    # v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.

  config.vm.network "forwarded_port", guest: 80, host: 8080 # NGINX
  config.vm.network "forwarded_port", guest: 5000, host: 5000 # Admin

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  config.vm.synced_folder ".", "/home/vagrant/app", :group =>'vagrant', :owner => 'vagrant'
  config.vm.synced_folder "salt/roots/", "/srv/salt/"

  # Salt provisioning
  config.vm.provision :salt do |salt|
    salt.minion_config = "salt/minion"
    salt.run_highstate = true
    salt.verbose = true
    salt.colorize = true
    salt.bootstrap_options = '-P'
  end
end
