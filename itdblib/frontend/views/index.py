# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wangzq <wangzhenqing1008@163.com>

import requests
from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    session,
    redirect
)

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    if session.get('rtx_id') == None:
        return redirect(url_for('index.login'))
    return render_template('index.html', pageTitle=u'首页')


@bp.route('/healthcheck.html')
def healthcheckff():
    """ 添加域名，需要加健康检查
    """
    return render_template('healthcheck.html')


# QSSO LOGIN
@bp.route('/login/', methods=['GET', 'POST'])
def login():
    # try:
    #     if (request.method == 'POST'):
    #         token = request.form.get('token')
    #         api_response = requests.get(
    #             'http://qsso.corp.qunar.com/api/verifytoken.php?token=%s'
    #             % token
    #         ).json()
    #         if api_response['ret'] == True:
    #             session.permanent = True
    #             session['rtx_id'] = api_response['userId']
    #             if request.args.get('ret'):
    #                 return redirect(request.args.get('ret'))
    #             else:
    #                 return redirect(url_for('index.index'))
    #     return render_template('login.html', pageTitle="LOGIN")
    # except:
    #     # 显示一个错误页面
    #     return render_template('login.html', pageTitle="LOGIN")
    return render_template('index.html', pageTitle="LOGIN")


# LOGOUT
@bp.route("/logout/")
def logout():
    if(session.get('rtx_id')):
        session.clear()
    if request.args.get('ret') != None:
        return redirect(request.args.get('ret'))
    return redirect(url_for('index.login'))
