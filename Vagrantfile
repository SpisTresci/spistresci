# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "precise32"
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"
  config.vm.network "private_network", type: "dhcp"
  config.ssh.forward_agent = true
  config.ssh.private_key_path = [ '~/.vagrant.d/insecure_private_key', '~/.ssh/id_rsa' ]
  config.vm.provision :shell, :path => "init.sh"
end
