% rebase('base.tpl', user = user, settings = settings)
<div>
    <form action="/settings" method="post">
        Время хранения данных (дней): <input name="store_days" type="text" value="{{settings['db_settings']['store_days']}}" /><br>
        Порт доступности веб-интерфейса <input name="port" type="text" value="{{settings['web_server']['port']}}"/><br>
        Время авторизованной сессии (дней) <input name="session_expire_days" type="text" value="{{settings['web_server']['session_expire_days']}}"/><br>
        Период обновления данных в базе (сек) <input name="db_update_period" type="text" value="{{settings['socket']['db_update_period']}}"/><br>
        <input value="Применить" type="submit">
    </form>
</div>
<div>
    <a href="/settings/change_password">Сменить пароль учётной записи</a>
    <a href="settings/useradd">Добавить учётную запись</a>
    <a href="settings/userdel">Удалить учётную запись</a>
    <a href="/settings/reboot">Перезагрузить сервер</a>
</div>