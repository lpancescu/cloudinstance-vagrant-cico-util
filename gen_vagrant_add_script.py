#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import json
import os
import sys


def cbs_image_download_command(image_info):
    """Return the Vagrant command to add specific box"""
    name = 'c{}'.format(image_info['major_release'])
    url = image_info['url']
    return 'vagrant box add {} --name {}'.format(url, name)


if __name__ == '__main__':
    images = json.loads(os.environ['BUILD_INFO'])
    cmds = [cbs_image_download_command(i) for i in images]
    print('\n'.join(cmds))
