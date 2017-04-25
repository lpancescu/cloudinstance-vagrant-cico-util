#!/bin/sh
yum -y install qemu libvirt libvirt-devel ruby-devel gcc qemu-kvm rsync
yum -y install https://releases.hashicorp.com/vagrant/1.9.3/vagrant_1.9.3_x86_64.rpm
vagrant plugin install vagrant-libvirt
systemctl start libvirtd.service
