#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify
from . import api
from app.tasks import sendEmail
from app.tasks import buildFeed
from app.tasks import listDir


@api.route('/mail')
@api.route('/mail/')
def get_mail():
    job = sendEmail.delay("test")
    return jsonify({"task": job.id})


@api.route('/feed')
@api.route('/feed/')
def get_feed():
    job = buildFeed.delay()
    return jsonify({'task': job.id})


@api.route('/list')
@api.route('/list/')
def list_feed():
    job = listDir.delay()
    print "job started", job.result
    job.wait()
    return jsonify({'task': job.id, "result": job.result})
