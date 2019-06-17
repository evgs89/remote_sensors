import configparser
import os
from time import sleep

from lib.bottle import route, run, post, request, view, template, abort, response, redirect, static_file
from lib.data_engine import DataEngine
from datetime import datetime, timedelta
import sqlite3


class WebInterface(object):
    def __init__(self):
        conf = configparser.ConfigParser(allow_no_value = True)
        conf.read('settings.ini')
        self.user = None
        self.settings = conf['socket']
        self.web_settings = conf['web_server']
        self.page_size = int(self.web_settings['page_size'])
        self.db_engine = DataEngine(self.settings['host'],
                                    self.settings['port'],)
        self.db_engine.start_sync_loop(self.settings['db_update_period'])
        self.bound_bottle()
        try:
            run(host = self.web_settings['host'], port = int(self.web_settings['port']))
        except OSError as e:
            print(e)

    def bound_bottle(self):
        route('/')(self.last_messages)
        route('/device/<dev_id>')(self.messages_by_id)
        route('/delete')(self.delete_messages)
        route('/delete/accept')(self.delete_messages_accepted)
        route('/login')(self.login)
        post('/login')(self.do_login)
        route('/logout')(self.logout)
        route('/settings')(self.change_settings)
        post('/settings')(self.do_change_settings)
        route('/settings/change_password')(self.change_password)
        post('/settings/change_password')(self.do_change_password)
        route('/settings/useradd')(self.useradd)
        post('/settings/useradd')(self.do_useradd)
        route('/settings/userdel')(self.userdel)
        post('/settings/userdel')(self.do_userdel)
        route('/settings/reboot')(self.reboot)
        route('/static/<filename>')(self.server_static)

    def _check_cookie(self):
        session_id = request.get_cookie('session_id')
        if session_id:
            self.user = self.db_engine.validate_session(session_id)
            if self.user:
                response.set_cookie('session_id', session_id,
                                    expires = datetime.now() +
                                    timedelta(days = int(self.web_settings['session_expire_days'])))

    def server_static(self, filename):
        return static_file(filename, root = './static')

    @view('index')
    def last_messages(self):
        self._check_cookie()
        sort_by = request.query.sort_by or 'received_at'
        page = int(request.query.page or 1)
        reverse = bool(int(request.query.reverse or 0))
        messages, pages = self.db_engine.get_last_messages(sort_by = sort_by,
                                                           reverse = reverse,
                                                           page = page,
                                                           page_size = self.page_size)
        page_info = {'sort_by': sort_by, 'page': page, 'reverse': reverse, 'pages': pages}
        return dict(rows = messages, page_info = page_info, user = self.user)

    @view('device')
    def messages_by_id(self, dev_id):
        self._check_cookie()
        sort_by = request.query.sort_by or 'received_at'
        page = int(request.query.page or 1)
        reverse = bool(int(request.query.reverse or 0))
        messages, pages = self.db_engine.get_messages_by_id(id_ = dev_id,
                                                            sort_by = sort_by,
                                                            reverse = reverse,
                                                            page = page,
                                                            page_size = self.page_size)
        page_info = {'id':dev_id, 'sort_by': sort_by, 'page': page, 'reverse': reverse, 'pages': pages}
        return dict(data = messages, page_info = page_info, user = self.user)

    @view('delete')
    def delete_messages(self):
        self._check_cookie()
        id_ = request.query.id or None
        if id_ == "None": id_ = None
        return dict(dev_id = id_, user = self.user)

    @view('deleted')
    def delete_messages_accepted(self):
        self._check_cookie()
        id_ = request.query.id or None
        if id_ == "None": id_ = None
        if self.user:
            deleted = self.db_engine.delete_messages(id_)
            return dict(deleted = deleted, user = self.user)
        else:
            abort(401, "You have no access to this page")

    @view('login')
    def login(self):
        return dict(user = self.user)

    def do_login(self):
        username = request.forms.get('username')
        password = request.forms.get('password')
        session_id = self.db_engine.validate_user(username, password)
        if session_id:
            self.user = username
            response.set_cookie('session_id', session_id,
                                expires = datetime.now() +
                                          timedelta(days = int(self.web_settings['session_expire_days'])))
        else:
            self.user = None
        return template('login_result', user = self.user)

    @view('logout')
    def logout(self):
        accepted = request.query.accepted or 0
        if accepted:
            self.user = None
            response.delete_cookie('session_id')
            return template('login_result', user = None)
        else:
            return dict(user = self.user)

    @view('settings')
    def change_settings(self):
        self._check_cookie()
        conf = configparser.ConfigParser(allow_no_value = True)
        conf.read('settings.ini')
        if self.user:
            return dict(settings = conf, user = self.user)
        else:
            abort(401, "You have no access to this page")

    def do_change_settings(self):
        self._check_cookie()
        conf = configparser.ConfigParser(allow_no_value = True)
        conf.read('settings.ini')
        conf['socket']['db_update_period'] = request.forms.get('db_update_period')
        conf['web_server']['port'] = request.forms.get('port')
        conf['web_server']['session_expire_days'] = request.forms.get('session_expire_days')
        conf['db_settings']['store_days'] = request.forms.get('store_days')
        if self.user:
            with open('settings.ini', 'w') as file:
                conf.write(file)
        redirect('/settings')

    @view('change_password')
    def change_password(self):
        self._check_cookie()
        success = request.query.success or 0
        if str(success) == '1':
            return template('change_password', user = self.user, success = True)
        else:
            if self.user: return dict(user = self.user, success = False)
            else: abort(401, 'You are not authorised')

    def do_change_password(self):
        old_pwd = request.forms.get('old_password')
        new_pwd = request.forms.get('new_password_1')
        new_pwd_2 = request.forms.get('new_password_2')
        print("DEBUG: ", self.user, new_pwd)
        if self.user and new_pwd == new_pwd_2:
            self.db_engine.change_password(self.user, old_pwd, new_pwd)
            redirect('/settings/change_password?success=1')
        else: redirect('/settings')

    @view('useradd')
    def useradd(self):
        self._check_cookie()
        result = request.query.result
        if self.user: return dict(user = self.user, result = result)
        else: abort(401, 'You are not authorised')

    def do_useradd(self):
        username = request.forms.get('username')
        if self.user:
            try:
                if self.db_engine.add_user(username):
                    redirect('/settings/useradd?result=created')
                else:
                    redirect('/settings/useradd?result=error')
            except sqlite3.IntegrityError:
                redirect('/settings/useradd?result=duplicate')
            except sqlite3.OperationalError:
                redirect('/settings/useradd?result=error')
        else: abort(401, 'You are not authorised')

    @view('userdel')
    def userdel(self):
        self._check_cookie()
        result = request.query.result
        if self.user:
            return dict(user = self.user, result = result, users = self.db_engine.get_user_list())
        else: abort(401, 'You are not authorised')

    def do_userdel(self):
        self._check_cookie()
        user = request.forms.get('username')
        passwd = request.forms.get('password')
        userdel = request.forms.get('userdel')
        if user == userdel:
            redirect('/settings/userdel?result=self')
        else:
            if self.db_engine.delete_user(user, passwd, userdel):
                print('redirecting')
                redirect('/settings/userdel?result=del')

    @view('reboot')
    def reboot(self):
        self._check_cookie()
        accepted = bool(int(request.query.accepted or 0))
        if self.user:
            if accepted:
                sleep(.1)
                os.popen('sudo reboot')
            return dict(user = self.user, accepted = accepted)
