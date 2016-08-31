#!/bin/sh
set -eux

yum -y install centos-release-scl
yum -y install sclo-vagrant1 qemu-kvm rsync
yum -y install http://download.virtualbox.org/virtualbox/5.0.26/VirtualBox-5.0-5.0.26_108824_el7-1.x86_64.rpm
yum -y install gcc make kernel-devel-$(uname -r)
systemctl start libvirtd.service
