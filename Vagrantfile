Vagrant::Config.run do |config|
  config.vm.box = 'ubuntu-12.04.2-i386-chef-11-omnibus'
  config.vm.box_url = 'https://s3.amazonaws.com/gsc-vagrant-boxes/ubuntu-12.04.2-i386-chef-11-omnibus.box'
  config.vm.forward_port 9022, 9022
  config.vm.forward_port 80, 9022
  
  # http://docs-v1.vagrantup.com/v1/docs/config/vm/share_folder.html
  # config.vm.share_folder "foo", "/guest/path", "/host/path"
  config.vm.share_folder "discern", "/home/vagrant/discern", "."
  # setting an IP address with config.vm.network, we can use Fabric to configure the Vagrant box
  config.vm.network :hostonly, "33.33.33.10"
end