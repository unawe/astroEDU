#!/usr/bin/env bash

sudo useradd --create-home --shell /bin/bash --groups sudo test4

sudo mkdir /home/test4/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAt7IAKxCWHDXJu+APGYYnSQDfsXrJYvv2RYLNtnOg0DbWf+M92HA6xpiD/iNgMjva5c81ibqD7G1ijdnesUp9Lriq2DRxSceyMRqaPi42sVYHQTNAbG0GsErVn91agtYMcp9bHBcqZxirCCIwQnafSiXFEG7sV81USuIkDXn536Z2OKngSLWnvPeQtjNe9+zNvZeDn9IOKSzUj0KVZ0LXL0occvnfWslEah5aLqueGT995dSZ/5xPzqtf0LLqqMZhwpmaAgSkXTHUctyd1vfwm9EZrZcgAHvvioMMZVOmvvU2B6dLi4jCGu6J6NEYW/vtj7gX0oyTvJ+Tln7I0mLf4Q== rino@aire.local" | sudo tee -a /home/test4/.ssh/authorized_keys >/dev/null
sudo chmod 700 /home/test4/.ssh
sudo chown test4 /home/test4/.ssh
sudo chmod 600 /home/test4/.ssh/authorized_keys
sudo chown test4 /home/test4/.ssh/authorized_keys

# don't ask for password! by adding the following line to /etc/sudoers:
echo "test4 ALL=(ALL) NOPASSWD: ALL" | sudo tee -a /etc/sudoers >/dev/null




# apt-get update
# apt-get install -y nginx
# apt-get install -y monit
# apt-get install -y git
# apt-get install -y apache2-utils
# apt-get install -y ghostscript
# apt-get install -y imagemagick
# apt-get install -y python-dev
# apt-get install -y libjpeg62 libjpeg62-dev
# # apt-get install -y python-imaging
# apt-get install -y python-lockfile
# apt-get install -y memcached
# apt-get install -y python-pip
# apt-get install -y libmysqlclient-dev


# apt-get install -y mysql-server

# pip install -U pip
# pip install virtualenvwrapper


# mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql


# mkdir ~/dev/astroEDU27
# cd ~/dev/astroEDU27

# mkvirtualenv astroEDU27
# deactivate

# workon astroEDU27
# git clone git@github.com:unawe/astroEDU.git .
# cp ../astroEDU/astroedu/secrets.py astroedu/

