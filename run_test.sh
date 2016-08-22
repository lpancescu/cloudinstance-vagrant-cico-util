#!/bin/sh
set -eux

source ./vagrant_add.sh

scl enable sclo-vagrant1 'vagrant up c6'
scl enable sclo-vagrant1 'vagrant ssh c6 -c "uname -a"'
scl enable sclo-vagrant1 'vagrant destroy c6 -f'

scl enable sclo-vagrant1 'vagrant up c7'
scl enable sclo-vagrant1 'vagrant ssh c7 -c "uname -a"'
scl enable sclo-vagrant1 'vagrant destroy c7 -f'
