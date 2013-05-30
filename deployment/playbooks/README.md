	Install ansible:

	$ pip install ansible

Install Vagrant 1.1 and vagrant-ansible plugin:

	$ vagrant plugin install vagrant-ansible

From the root directory, run this command:

	$ ansible-playbook deployment/playbooks/setup.yml --verbose -i "127.0.0.1," -c local -e working_dir=`pwd`
