import configparser

from lib.bottle import route, run, template, request
from lib.data_engine import DataEngine


class WebInterface(object):
    def __init__(self):
        conf = configparser.ConfigParser(allow_no_value = True)
        conf.read('settings.ini')
        self.settings = conf['socket']
        web_settings = conf['web_server']
        self.page_size = 30
        self.db_engine = DataEngine(self.settings['host'],
                                    self.settings['port'],)
        self.db_engine.start_sync_loop(self.settings['db_update_period'])
        self.bound_bottle()
        try:
            run(host = web_settings['host'], port = int(web_settings['port']))
        except OSError as e:
            print(e)

    def bound_bottle(self):
        route('/')(self.last_messages)
        route('/device/<dev_id>')(self.messages_by_id)
        route('/delete')(self.delete_messages)
        route('/delete/<id_>')(self.delete_messages)
        route('/delete/accept/')(self.delete_messages_accepted)
        route('/delete/accept/<id_>')(self.delete_messages_accepted)

    def last_messages(self):
        rows = ''
        messages, pages = self.db_engine.get_last_messages()
        for i in messages:
            rows += "<tr><td><a href = '/device/{0}'>{0}</a></td><td>{1}</td><td>{2}</td><td>{3}</td></tr>\n".format(*i)
        return """
        <!DOCTYPE html>
        <html>
        <head>
        <title>Remote Sensors</title>
        </head>
        <body>
        <hr>
        <header>Сервер активен.</header>
        <table cellspacing=20>
            <tr>
                <tr><th>ID</th><th>Data</th><th>Balance</th><th>Received at:</th>
                {rows}
            </tr>
        </table>
        <div><a href='/delete'>Очистить всю базу данных</a></div>
        </body>
        </html>
        """.format(rows = rows)

    def messages_by_id(self, dev_id):
        rows = ''
        sort_by = request.query.sort_by or 'received_at'
        page = int(request.query.page or 1)
        reverse = bool(int(request.query.reverse or 0))
        messages, pages = self.db_engine.get_messages_by_id(id_ = dev_id,
                                                            sort_by = sort_by,
                                                            reverse = reverse,
                                                            page = page,
                                                            page_size = self.page_size)
        # """
        # "↑↓"
        # <a href="/{id}?page={page}&sort_by={key}&reversed=False">↓</a>
        # <a href="/{id}?page={page}&sort_by={key}&reversed=True">↑</a>
        # """
        for i in messages:
            rows += "<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>\n".format(i[1], i[2], i[3])
        page_selector = ""
        for i in range(pages):
            page_selector += '<td><a href="/device/{id}?page={i}&sort_by={key}&reverse={rev}">{i1}</a></td>'.format(id = dev_id,
                                                                                                             i = i + 1,
                                                                                                             key = sort_by,
                                                                                                             rev = int(reverse),
                                                                                                             i1 = "<b>{i}</b>".format(i = i + 1) if i + 1 == page else str(i + 1))
        return """
                <!DOCTYPE html>
                <html>
                <head>
                <title>Remote Sensors</title>
                </head>
                <body>
                <hr>
                <header>Данные от отправителя: {id}</header>
                <table cellspacing=20>
                    <tr>
                        <tr><th>Data
                        <a href="/device/{id}?page={page}&sort_by=data&reverse=0">↓</a>
                        <a href="/device/{id}?page={page}&sort_by=data&reverse=1">↑</a></th>
                        <th>Balance
                        <a href="/device/{id}?page={page}&sort_by=balance&reverse=0">↓</a>
                        <a href="/device/{id}?page={page}&sort_by=balance&reverse=1">↑</a></th>
                        <th>Received at:
                        <a href="/device/{id}?page={page}&sort_by=received_at&reverse=0">↓</a>
                        <a href="/device/{id}?page={page}&sort_by=received_at&reverse=1">↑</a></th>
                        {rows}
                    </tr>
                </table>
                <div>
                <table cellspacing=30><tr>{page_selector}</tr></table>
                </div>
                <div><a href='/delete/{id}'>Удалить все сообщения от данного устройства</a></div>
                </body>
                </html>
                """.format(id = dev_id, rows = rows, page = page, page_selector = page_selector)

    def delete_messages(self, id_ = None):
        return """
        <!DOCTYPE html>
                <html>
                <head>
                <title>Remote Sensors</title>
                </head>
                <body>
                <hr>
                <header>Удаление данных</header>
                <div>
                Уверены, что хотите удалить данные?<br>
                <a href="/delete/accept/{id}">Да</a><a href="/{id}">Нет</a>
                </div>
                </body>
                </html>
                """.format(id = id_ if id_ else '')

    def delete_messages_accepted(self, id_ = None):
        deleted = self.db_engine.delete_messages(id_)
        return """
        Удалено {0} записей. <br>
        <a href="/">На главную</a>
        """.format(deleted)
