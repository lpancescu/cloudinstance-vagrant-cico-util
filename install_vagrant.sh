#!/bin/sh
yum -y install qemu libvirt libvirt-devel ruby-devel gcc qemu-kvm rsync
yum -y install https://releases.hashicorp.com/vagrant/2.2.4/vagrant_2.2.4_x86_64.rpm
vagrant plugin install vagrant-libvirt
systemctl start libvirtd.service
