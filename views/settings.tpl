% rebase('base.tpl', user = user, settings = settings, footer = True, page = 'settings')
<div>
    <form action="/settings" method="post">
    <div class="row">
        <div class="col-12 col-xl-4 mb-4">
            <label for="page_size">Размер страницы для отображения данных (записей):</label>
            <input id="page_size" name="page_size" class="form-control" type="text" value="{{settings['web_server']['page_size']}}"/>
        </div>
        <div class="col-md-6 col-xl-4 mb-4">
            <label for="store_days">Время хранения данных (дней):</label>
            <input id="store_days" name="store_days" type="text" class="form-control" value="{{settings['db_settings']['store_days']}}" />
        </div>
        <div class="col-md-6 col-xl-4 mb-4">
            <label for="session_expire_days">Время авторизованной сессии (дней):</label>
            <input id="session_expire_days" name="session_expire_days" class="form-control" type="text" value="{{settings['web_server']['session_expire_days']}}"/>
        </div>
        </div>
        <div class="container pb-5 mb-5">
            <input class="btn btn-lg btn-primary btn-block col-md-3 float-right" value="Применить" type="submit">
        </div>
    </form>
</div>
<div class="row">
    <a href="/settings/change_password" class="btn btn-primary btn-block col-lg-2 mr-2 mb-4">Сменить пароль</a>
    <a href="settings/useradd" class="btn btn-secondary col-lg-3 mr-2 mb-4">Добавить учётную запись</a>
    <a href="settings/userdel" class="btn btn-secondary col-lg-3 mr-2 mb-4">Удалить учётную запись</a>
    <a href="/settings/reboot" class="btn btn-secondary col-lg-3 mr-2 mb-4">Перезагрузить сервер</a>
</div>


