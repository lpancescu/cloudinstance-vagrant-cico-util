#!/bin/sh
set -eux

# accept an optional argument --with-vagrant-vbguest
while [ $# -gt 0 ]; do
	arg="$1"
	case $arg in
		--with-vagrant-vbguest)
			INSTALL_VBGUEST=1
			;;
		*)
			echo "$(basename \"$0\"): invalid argument"
			exit 1
			;;
	esac
	shift
done

yum -y install centos-release-scl
yum -y install sclo-vagrant1 qemu-kvm rsync
# VirtualBox needs to compile its kernel modules
yum -y install gcc make kernel-devel-$(uname -r)
curl -O http://download.virtualbox.org/virtualbox/5.0.30/VirtualBox-5.0-5.0.30_112061_el7-1.x86_64.rpm
curl https://www.virtualbox.org/download/hashes/5.0.30/SHA256SUMS | grep 'el7-1\.x86_64\.rpm$' | sha256sum -c -
yum -y install VirtualBox-5.0-5.0.30_112061_el7-1.x86_64.rpm
if [ ${INSTALL_VBGUEST:-0} -eq 1 ]; then
	yum -y install rh-ruby22-ruby-devel gcc-c++ zlib-devel libvirt-devel
	scl enable sclo-vagrant1 'vagrant plugin install vagrant-vbguest'
fi
systemctl start libvirtd.service
