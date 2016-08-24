#!/usr/bin/env python

from __future__ import print_function, unicode_literals
import re
import sys
import subprocess


def cbs_tasks(log_path):
    """Return a list of CBS task ids
    
    Arguments:
    - log_path: the path to the Koji output log file
    """
    tasks = []
    task_re = re.compile(r'Created task: (\d+)')
    with open(log_path) as log_file:
        for line in log_file:
            match = task_re.match(line)
            if match:
                tasks.append(match.group(1))
    return tasks


def cbs_image_path(task_id):
    """Return the filesystem path to a qcow2 image on cbs.centos.org"""
    kvm_image_re = re.compile(r'\s*(.*centos-\d+-1-1\.[^.]+\.qcow2)')
    p = subprocess.Popen(['cbs', 'taskinfo', '-r', task_id],
                         stdout=subprocess.PIPE)
    output = p.communicate()[0]
    for line in output.splitlines():
        match = kvm_image_re.match(line)
        if match:
            return match.group(1)
    raise RuntimeError('Vagrant image for libvirt-kvm not found')


def cbs_image_url(image_path):
    """Return the download url of an image from cbs.centos.org"""
    if image_path.startswith('/mnt/koji'):
        return image_path.replace('/mnt/koji',
                                  'https://cbs.centos.org/kojifiles')
    raise RuntimeError('Image path in an unexpected directory')


def cbs_image_download_command(image_url):
    """Add a box specified by URL to Vagrant"""
    match = re.search(r'centos-(\d+)-1-1\.[^.]+\.qcow2', image_url)
    if not match:
        raise RuntimeError('Unable to determine CentOS major release number')
    name = 'c{}'.format(match.group(1))
    return ('curl -o box.img {0}\n'
            'tar -czvf {1}.box metadata.json Vagrantfile box.img\n'
            'vagrant box add {1}.box --name {1}').format(image_url, name)


if __name__ == '__main__':
    tasks = cbs_tasks(sys.argv[1])
    paths = [cbs_image_path(t) for t in tasks]
    urls = [cbs_image_url(p) for p in paths]
    cmds = [cbs_image_download_command(u) for u in urls]
    print('cd box\n' + '\n'.join(cmds))
