#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import json
import os
import sys


def test_provider(images, provider):
    releases = [i['major_release'] for i in images \
                if i['provider'] == provider]
    for r in releases:
        print("""
scl enable sclo-vagrant1 'vagrant up c{0} --provider {1}'
scl enable sclo-vagrant1 'vagrant ssh c{0} -c "uname -a"'
scl enable sclo-vagrant1 'vagrant destroy c{0} -f'
""".format(r, provider))


if __name__ == '__main__':
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

# VirtualBox needs to compile its kernel modules
yum -y install gcc make kernel-devel-$(uname -r)
curl -O http://download.virtualbox.org/virtualbox/5.0.30/VirtualBox-5.0-5.0.30_112061_el7-1.x86_64.rpm
curl https://www.virtualbox.org/download/hashes/5.0.30/SHA256SUMS | grep 'el7-1\.x86_64\.rpm$' | sha256sum -c -
yum -y install VirtualBox-5.0-5.0.30_112061_el7-1.x86_64.rpm

/sbin/rcvboxdrv setup # build and load the VirtualBox kernel modules
""")

    if len(sys.argv) == 2 and sys.argv[1] == '--with-vagrant-vbguest':
        print("""
yum -y install rh-ruby22-ruby-devel gcc-c++ zlib-devel libvirt-devel
scl enable sclo-vagrant1 'vagrant plugin install vagrant-vbguest'
""")

    test_provider(images, 'virtualbox')

    print("""
yum -y remove VirtualBox-5.0
curl -O http://download.virtualbox.org/virtualbox/5.1.12/VirtualBox-5.1-5.1.12_112440_el7-1.x86_64.rpm
curl https://www.virtualbox.org/download/hashes/5.1.12/SHA256SUMS | grep 'el7-1\.x86_64\.rpm$' | sha256sum -c -
yum -y install VirtualBox-5.1-5.1.12_112440_el7-1.x86_64.rpm
/sbin/rcvboxdrv setup # build and load the VirtualBox kernel modules
""")

    test_provider(images, 'virtualbox')
