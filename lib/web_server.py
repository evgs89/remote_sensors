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
                </body>
                </html>
                """.format(id = id, rows = rows)
