#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''WEB Server

process the request
'''

import traceback
import functools
import time

from flask import Flask
from flask import request, jsonify
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import InternalServerError
from flask import make_response

from Logger import Logger

app = Flask(__name__)

def jsonify_api(func):
    '''decorator used to validate request and jsonify response'''
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        try:
            if request.content_length > 0 and request.mimetype is not None:
                if request.mimetype != 'application/json':
                    raise BadRequest(
                            'Unsupported Mimetype: {}, JSON required'.format(
                                request.mimetype))
                elif request.json is None:
                    raise BadRequest('Invalid JSON')
                if request.charset != 'utf-8':
                    raise BadRequest(
                            'Invalid Charset: {}, utf-8 expected'.format(
                                request.charset))
            resp = func(*args, **kwargs)
            return resp
        except BadRequest as e:
            Logger.error('args={}, kwargs={}, err={}, traceback={}'.format(
                args, kwargs, e, traceback.format_exc()))
            return jsonify({'code': 1,
                            'error': e.description}), 400
        except InternalServerError as e:
            Logger.error('args={}, kwargs={}, err={}, traceback={}'.format(
                args, kwargs, e, traceback.format_exc()))
            return jsonify({'code': 1,
                            'error': e.message}), 500
        except NotFound as e:
            Logger.error('args={}, kwargs={}, err={}, traceback={}'.format(
               args, kwargs, e, traceback.format_exc()))
            return jsonify({'code': 1,
                            'error': e.message}), 404
        except:
            Logger.error('args={}, kwargs={}, traceback={}'.format(
               args, kwargs, traceback.format_exc()))
            return jsonify({'code': 1,
                            'error': 'Internal Server Error'}), 500
    return decorator

@app.before_request
def pre_process():
    '''pre process

    * set timestamp attr which will be used in the post
    process to log elapsed time
    '''
    setattr(request, 'timestamp', time.time())

@app.after_request
def post_process(resp):
    '''post process after request

    * logging in the apache web server log format
    '''
    logname = '-'
    username = request.remote_user if request.remote_user is not None else '-'
    timestamp = time.strftime('%FT%T %z')
    elapsed = time.time() - request.timestamp
    Logger.info('{} {} {} [{}] "{} {}" {} {} {}'.format(
            request.host,
            logname,
            username,
            timestamp,
            request.method,
            request.url,
            resp.status_code,
            resp.content_length,
            int(elapsed)
            ))
    return resp

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'code': 1,
        'error': 'Not Found'}), 404)

def main():
    app.run(host='0.0.0.0', port=5000, threaded=True)


if __name__ == '__main__':
    main()
