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
created_task_re = re.compile(r'Created task: (\d+)')
successful_task_re = re.compile(r'(\d+) image.*completed successfully')


class FailedTasksError(RuntimeError):
    def __init__(self, failed_tasks):
        self.failed_tasks = failed_tasks
    def __str__(self):
        return ','.join(self.failed_tasks)


def cbs_tasks(cbs_log):
    """Return a set of successfully completed CBS task ids

    The cbs_log argument should be a file-like object containing the output of
    "cbs image-build". If there was any task that didn't complete successfully,
    a FailedTasksError exception is raised.
    """
    created_tasks = set()
    successful_tasks = set()
    for line in cbs_log:
        match = created_task_re.match(line)
        if match:
            created_tasks.add(match.group(1))
        match = successful_task_re.match(line)
        if match:
            successful_tasks.add(match.group(1))
    failed_tasks = created_tasks - successful_tasks
    if len(failed_tasks):
        raise FailedTasksError(failed_tasks)
    return successful_tasks


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
    tasks = cbs_tasks(sys.stdin)
    for task in tasks:
        images.extend(cbs_images(task))
    if not images:
        raise RuntimeError("No images found")
    print("BUILD_INFO={}".format(json.dumps(images)))
