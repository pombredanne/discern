Vagrant::Config.run do |config|
  config.vm.box = 'ubuntu-12.04.2-i386-chef-11-omnibus'
  config.vm.box_url = 'https://s3.amazonaws.com/gsc-vagrant-boxes/ubuntu-12.04.2-i386-chef-11-omnibus.box'
  config.vm.forward_port 9000, 8000
  
  # http://docs-v1.vagrantup.com/v1/docs/config/vm/share_folder.html
  # config.vm.share_folder "foo", "/guest/path", "/host/path"
  config.vm.share_folder "ml-service-api", "/home/vagrant/ml-service-api", "."
  config.vm.provision :shell, :inline => %{ \
    touch /var/log/ml-service-api-setup.log; \
    sudo apt-get update -y                                          | tee -a /var/log/ml-service-api-setup.log; \
    cd ml-service-api; sudo xargs -a apt-packages.txt apt-get install -y | tee -a /var/log/ml-service-api-setup.log; \
    sudo virtualenv /opt/edx | tee -a /var/log/ml-service-api-setup.log; \
    source /opt/edx/bin/activate | tee -a /var/log/ml-service-api-setup.log; \
    pip install -r pre-requirements.txt | tee -a /var/log/ml-service-api-setup.log; \
    pip install -r requirements.txt | tee -a /var/log/ml-service-api-setup.log; \
    python manage.py syncdb --settings=ml_service_api.settings --pythonpath=/home/vagrant/ml-service-api | tee -a /var/log/ml-service-api-setup.log; \
    python manage.py migrate --settings=ml_service_api.settings --pythonpath=/home/vagrant/ml-service-api | tee -a /var/log/ml-service-api-setup.log; \
    python manage.py collectstatic -c --noinput --settings=ml_service_api.settings --pythonpath=/home/vagrant/ml-service-api | tee -a /var/log/ml-service-api-setup.log; \
  }
  config.vm.network :hostonly, "33.33.33.10"
end