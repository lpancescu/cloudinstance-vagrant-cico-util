#!/usr/bin/env python

from __future__ import print_function, unicode_literals
import re
import sys
import subprocess

image_re = {
    'libvirt': re.compile(r'\s*(\S*centos-(\d+)-1-1'
                          r'\.x86_64\.vagrant-libvirt\.box)'),
    'virtualbox': re.compile(r'\s*(\S*centos-(\d+)-1-1'
                             r'\.x86_64\.vagrant-virtualbox\.box)')
    }


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


def cbs_image_path(task_id, provider):
    """Return the filesystem path to the image on cbs.centos.org"""
    p = subprocess.Popen(['cbs', 'taskinfo', '-r', task_id],
                         stdout=subprocess.PIPE)
    output = p.communicate()[0]
    for line in output.splitlines():
        match = image_re[provider].match(line)
        if match:
            return match.group(1)
    raise RuntimeError('Vagrant image for {} not found'.format(provider))


def cbs_image_url(image_path):
    """Return the download url of an image from cbs.centos.org"""
    if image_path.startswith('/mnt/koji'):
        return image_path.replace('/mnt/koji',
                                  'https://cbs.centos.org/kojifiles')
    raise RuntimeError('Image path in an unexpected directory')


def cbs_image_download_command(image_url, provider):
    """Add a box specified by URL to Vagrant"""
    match = image_re[provider].match(image_url)
    if not match:
        raise RuntimeError('Unable to determine CentOS major release number')
    name = 'c{}'.format(match.group(2))
    return 'vagrant box add {} --name {}'.format(image_url, name)


if __name__ == '__main__':
    tasks = cbs_tasks(sys.argv[1])
    for provider in 'libvirt', 'virtualbox':
        paths = [cbs_image_path(t, provider) for t in tasks]
        urls = [cbs_image_url(p) for p in paths]
        cmds = [cbs_image_download_command(u, provider) for u in urls]
        print('\n'.join(cmds))
