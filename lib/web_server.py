import configparser

from lib.bottle import route, run, template
from lib.data_engine import DataEngine


class WebInterface(object):
    def __init__(self):
        conf = configparser.ConfigParser(allow_no_value = True)
        conf.read('settings.ini')
        self.settings = conf['socket']
        web_settings = conf['web_server']
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
        route('/<id>')(self.messages_by_id)
        route('/delete')(self.delete_messages)
        route('/delete/<id_>')(self.delete_messages)
        route('/delete/accept/')(self.delete_messages_accepted)
        route('/delete/accept/<id_>')(self.delete_messages_accepted)

    def last_messages(self):
        rows = ''
        messages = self.db_engine.get_last_messages()
        for i in messages:
            rows += "<tr><td><a href = '/{0}'>{0}</a></td><td>{1}</td><td>{2}</td></tr>\n".format(i[0], i[1], i[2])
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
                <tr><th>ID</th><th>Data</th><th>Received at:</th>
                {rows}
            </tr>
        </table>
        <div><a href='/delete'>Очистить всю базу данных</a></div>
        </body>
        </html>
        """.format(rows = rows)

    def messages_by_id(self, id):
        rows = ''
        messages = self.db_engine.get_messages_by_id(id)
        for i in messages:
            rows += "<tr><td>{0}</td><td>{1}</td></tr>\n".format(i[1], i[2])
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
                        <tr><th>Data</th><th>Received at:</th>
                        {rows}
                    </tr>
                </table>
                <div><a href='/delete/{id}'>Удалить все сообщения от данного устройства</a></div>
                </body>
                </html>
                """.format(id = id, rows = rows)

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


