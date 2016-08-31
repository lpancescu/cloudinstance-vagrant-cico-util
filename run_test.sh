#!/bin/sh
set -eux

scl enable sclo-vagrant1 'sh vagrant_add.sh'

cd box
scl enable sclo-vagrant1 'vagrant up c6 --provider libvirt'
scl enable sclo-vagrant1 'vagrant ssh c6 -c "uname -a"'
scl enable sclo-vagrant1 'vagrant destroy c6 -f'

scl enable sclo-vagrant1 'vagrant up c7 --provider libvirt'
scl enable sclo-vagrant1 'vagrant ssh c7 -c "uname -a"'
scl enable sclo-vagrant1 'vagrant destroy c7 -f'

# VirtualBox doesn't support nested virtualization
systemctl stop libvirtd.service
modprobe -r -v kvm_intel kvm_amd kvm
/sbin/rcvboxdrv setup # build and load the VirtualBox kernel modules

scl enable sclo-vagrant1 'vagrant up c6 --provider virtualbox'
scl enable sclo-vagrant1 'vagrant ssh c6 -c "uname -a"'
scl enable sclo-vagrant1 'vagrant destroy c6 -f'

scl enable sclo-vagrant1 'vagrant up c7 --provider virtualbox'
scl enable sclo-vagrant1 'vagrant ssh c7 -c "uname -a"'
scl enable sclo-vagrant1 'vagrant destroy c7 -f'
