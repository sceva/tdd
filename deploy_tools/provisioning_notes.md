Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv

eg, on Ubuntu:

    sudo apt-get install nginx git python3 python3-pip
    sudo pip-3.3 install virtualenv (or sudo pip3 install virtualenv)

## Nginx Virtual Host Config

* see nginx.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Upstart Job - to auto start the web server

* see gunicorn-upstart.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Folder structure:
Assume we have a user account at /home/username

/home/username
|__sites
   |__SITENAME
      |__database
      |__source
      |__static
      |__virtualenv
