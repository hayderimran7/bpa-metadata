#!/bin/bash

sudo apt-key update
sudo apt-get update
sudo apt-get -y install puppet
sudo puppet module install puppetlabs-apache --force

sudo chown ubuntu.ubuntu -R /home/ubuntu

