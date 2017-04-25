#!/bin/sh
yum -y install libvirt qemu-kvm rsync
yum -y install https://releases.hashicorp.com/vagrant/1.9.4/vagrant_1.9.4_x86_64.rpm
systemctl start libvirtd.service
