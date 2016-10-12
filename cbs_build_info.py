#!/usr/bin/env python

from __future__ import print_function, unicode_literals
import json
import re
import sys
import subprocess

image_re = {
    'libvirt': re.compile(r'\s*(\S*centos-(\d+)-1-1'
                          r'\.x86_64\.vagrant-libvirt\.box)'),
    'virtualbox': re.compile(r'\s*(\S*centos-(\d+)-1-1'
                             r'\.x86_64\.vagrant-virtualbox\.box)')
    }


def cbs_tasks():
    """Return a list of CBS task ids"""
    tasks = []
    task_re = re.compile(r'Created task: (\d+)')
    for line in sys.stdin:
        match = task_re.match(line)
        if match:
            tasks.append(match.group(1))
    if len(tasks):
        return tasks
    raise RuntimeError("No CBS tasks found")


def cbs_image_url(image_path):
    """Return the download url of an image from cbs.centos.org"""
    if image_path.startswith('/mnt/koji'):
        return image_path.replace('/mnt/koji',
                                  'https://cbs.centos.org/kojifiles')
    raise RuntimeError('Image path in an unexpected directory')


def cbs_images(task_id):
    """Return a list of dicts containing image info"""
    p = subprocess.Popen(['cbs', 'taskinfo', '-r', task_id],
                         stdout=subprocess.PIPE)
    output = p.communicate()[0]
    images = []
    for line in output.splitlines():
        for provider in image_re.keys():
            match = image_re[provider].match(line)
            if match:
                images.append({'provider': provider,
                               'major_release': match.group(2),
                               'url': cbs_image_url(match.group(1))})
    return images


if __name__ == '__main__':
    images = []
    tasks = cbs_tasks()
    for task in tasks:
        images.extend(cbs_images(task))
    if len(images):
        print("BUILD_INFO={}".format(json.dumps(images)))
    else:
        print("No images found", file=sys.stderr)
        sys.exit(1)
