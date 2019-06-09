import configparser

from lib.bottle import route, run, post, request, view, template, abort
from lib.data_engine import DataEngine


class WebInterface(object):
    def __init__(self):
        conf = configparser.ConfigParser(allow_no_value = True)
        conf.read('settings.ini')
        self.user = None
        self.settings = conf['socket']
        self.web_settings = conf['web_server']
        self.page_size = 30
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

    @view('index')
    def last_messages(self):
        messages, pages = self.db_engine.get_last_messages()
        return dict(rows = messages, user = self.user)

    @view('device')
    def messages_by_id(self, dev_id):
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
        id_ = request.query.id or None
        if id_ == "None": id_ = None
        return dict(dev_id = id_, user = self.user)

    @view('deleted')
    def delete_messages_accepted(self):
        id_ = request.query.id or None
        if id_ == "None": id_ = None
        if self.user:
            deleted = self.db_engine.delete_messages(id_)
            return dict(deleted = deleted)
        else:
            abort(401, "You have no access to this page")

    @view('login')
    def login(self):
        return dict()

    def do_login(self):
        username = request.forms.get('username')
        password = request.forms.get('password')
        if self.db_engine.validate_user(username, password):
            self.user = username
        else:
            self.user = None
        return template('login_result', user = self.user)
