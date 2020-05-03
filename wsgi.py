#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname

# 设置当前目录为工作目录
sys.path.insert(0, abspath(dirname(__file__)))

import app

# 必须有一个叫做 application 的变量
# gunicorn 就要这个变量
# 这个变量的值必须是 Flask 实例
application = app.app

# 代码部署到 apache gunicorn nginx 后的配置
"""
建立一个软连接
ln -s /var/www/blog/config/blog_supervisor.conf /etc/supervisor/conf.d/blog.conf
ln -s /var/www/blog/config/blog_nginx /etc/nginx/sites-enabled/blog_nginx
# ➜  ~ cat /etc/supervisor/conf.d/blog.conf

[program:blog]
directory=/var/www/blog
command=/usr/local/bin/gunicorn wsgi wsgi -c gunicorn_config.py
autostart=true
autorestart=true
"""