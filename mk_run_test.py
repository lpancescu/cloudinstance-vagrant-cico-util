#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import json
import os
import sys

from jinja2 import Environment, FileSystemLoader


if __name__ == '__main__':
    images = json.loads(os.environ['BUILD_INFO'])
    with_vbguest = (len(sys.argv) == 2 and
                    sys.argv[1] == '--with-vagrant-vbguest')


    env = Environment(loader=FileSystemLoader('templates'))
    # the 'equalto' filter was introduced in jinja 2.8
    if 'equalto' not in env.tests:
        env.tests['equalto'] = lambda value, other : value == other
    template = env.get_template('run_test.j2')
    print(template.render(images=images, with_vbguest=with_vbguest))
