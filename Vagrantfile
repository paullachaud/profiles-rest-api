# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
 # The most common configuration options are documented and commented below.
 # For a complete reference, please see the online documentation at
 # https://docs.vagrantup.com.

 # Every Vagrant development environment requires a box. You can search for
 # boxes at https://vagrantcloud.com/search.
 config.vm.box = "ubuntu/bionic64"
 config.vm.box_version = "~> 20200304.0.0"

 config.vm.network "forwarded_port", guest: 8000, host: 8000


 config.vm.provision "shell", inline: <<-SHELL
   systemctl disable apt-daily.service
   systemctl disable apt-daily.timer
 
   sudo apt-get update
   sudo apt-get install -y python3-venv zip
   touch /home/vagrant/.bash_aliases
   if ! grep -q PYTHON_ALIAS_ADDED /home/vagrant/.bash_aliases; then
     echo "# PYTHON_ALIAS_ADDED" >> /home/vagrant/.bash_aliases
     echo "alias python='python3'" >> /home/vagrant/.bash_aliases
   fi
 SHELL

config.vm.provider "virtualbox" do |v|
    v.memory = 4096
    v.cpus = 4
    # Basebox ubuntu/xenial64 comes with following Vagrantfile config and causes https://github.com/joelhandwell/ubuntu_vagrant_boxes/issues/1
    # vb.customize [ "modifyvm", :id, "--uart1", "0x3F8", "4" ]
    # vb.customize [ "modifyvm", :id, "--uartmode1", "file", File.join(Dir.pwd, "ubuntu-xenial-16.04-cloudimg-console.log") ]
    # following config will address the issue
    v.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
end
#  config.vm.synced_folder "/mnt/c/Users/paull/Documents/Development/Study/Courses/Udemy/Python_Rest_Api/profiles-rest-api", "/project"
end