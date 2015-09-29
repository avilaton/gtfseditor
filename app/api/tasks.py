#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify
from . import api


@api.route('/mail')
@api.route('/mail/')
def get_mail():
    from app.tasks import sendEmail
    job = sendEmail.delay("test")
    return jsonify({"task": job.id})


@api.route('/compile')
@api.route('/compile/')
def get_feed():
    from app.tasks import buildFeed
    job = buildFeed.delay(upload=True)
    return jsonify({'task': job.id})


@api.route('/list')
@api.route('/list/')
def list_feed():
    from app.tasks import listDir
    job = listDir.delay()
    print("job started: {0}".format(job.result))
    job.wait()
    return jsonify({'task': job.id, "result": job.result})
