#!/bin/sh
set -eux

yum -y install centos-release-scl
yum -y install sclo-vagrant1 qemu-kvm
systemctl start libvirtd.service
