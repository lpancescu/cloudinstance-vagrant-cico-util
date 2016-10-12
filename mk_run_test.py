#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import json
import os


def test_provider(images, provider):
    releases = [i['major_release'] for i in images \
                if i['provider'] == provider]
    for r in releases:
        print("""
scl enable sclo-vagrant1 'vagrant up c{0} --provider {1}'
scl enable sclo-vagrant1 'vagrant ssh c{0} -c "uname -a"'
scl enable sclo-vagrant1 'vagrant destroy c{0} -f'
""".format(r, provider))

images = json.loads(os.environ['BUILD_INFO'])

print("""
#!/bin/sh
set -eux

scl enable sclo-vagrant1 'sh vagrant_add.sh'

cd box
""")

test_provider(images, 'libvirt')

print("""
# VirtualBox doesn't support nested virtualization
systemctl stop libvirtd.service
modprobe -r -v kvm_intel kvm_amd kvm
/sbin/rcvboxdrv setup # build and load the VirtualBox kernel modules
""")

test_provider(images, 'virtualbox')
