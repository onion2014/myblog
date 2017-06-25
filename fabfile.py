#!/usr/bin/env python
# -*- coding:utf-8 -*-

from fabric.api import env, run
from fabric.operations import sudo

GIT_REPO = "https://github.com/tengyifeng/myblog"

env.user = "root"
env.password = "feng2013@"

env.hosts = "www.tengyifeng.com"

env.port = '22'

def deploy():
    source_folder = "/home/dengfeng/sites/www.tengyifeng.com/myblog"
    run('cd %s && git pull' % source_folder)
    run("""
            cd {} &&
            ../myblogenv/bin/pip install -r requirements.txt &&
            ../myblogenv/bin/python3 manage.py collectstatic --noinput &&
            ../myblogenv/bin/python3 manage.py migrate
            """.format(source_folder))
    sudo('restart gunicorn-tengyifeng')
    sudo('service nginx reload')