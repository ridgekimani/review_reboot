# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"Hello World"]
