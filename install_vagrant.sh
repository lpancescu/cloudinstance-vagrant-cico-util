#!/bin/sh
set -eux

yum -y install centos-release-scl
yum -y install sclo-vagrant1 qemu-kvm rsync
curl -O http://download.virtualbox.org/virtualbox/5.0.30/VirtualBox-5.0-5.0.30_112061_el7-1.x86_64.rpm
curl -O https://www.virtualbox.org/download/hashes/5.0.30/SHA256SUMS
sha256sum --ignore-missing --check SHA256SUMS
yum -y install VirtualBox-5.0-5.0.30_112061_el7-1.x86_64.rpm
yum -y install gcc make kernel-devel-$(uname -r)
systemctl start libvirtd.service
