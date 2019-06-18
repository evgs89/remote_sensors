% rebase('base.tpl', user = user, settings = settings, footer = True, page = 'settings')
<style>
.container {
  width: auto;
  max-width: 1800px;
  padding: 0 15px;
}
</style>

<div class="container">
    <form action="/settings" method="post" class="form-group">
    <div class="row">
        <div class="col-12 col-xl-3 mb-4">
            <label for="page_size">Размер страницы для отображения данных (записей):</label>
            <input id="page_size" name="page_size" class="form-control" type="text" value="{{settings['web_server']['page_size']}}"/>
        </div>
        <div class="col-md-4 col-xl-3 mb-4">
            <label for="store_days">Время хранения данных (дней):</label>
            <input id="store_days" name="store_days" type="text" class="form-control" value="{{settings['db_settings']['store_days']}}" />
        </div>
        <div class="col-md-4 col-xl-3 mb-4">
            <label for="session_expire_days">Время авторизованной сессии (дней):</label>
            <input id="session_expire_days" name="session_expire_days" class="form-control" type="text" value="{{settings['web_server']['session_expire_days']}}"/>
        </div>
        <div class="container col-12 col-md-4 col-xl-3 mb-4">
            <input class="btn btn-lg btn-primary btn-block align-text-bottom" value="Применить" type="submit">
        </div>
    </div>
    </form>

</div>

<div class="container row">
    <a href="/settings/change_password" class="btn btn-primary btn-block col-lg-2 mb-4">Сменить пароль</a>
    <a href="settings/useradd" class="btn btn-secondary col-lg-3 mb-4">Добавить учётную запись</a>
    <a href="settings/userdel" class="btn btn-secondary col-lg-3 mb-4">Удалить учётную запись</a>
    <a href="/settings/reboot" class="btn btn-secondary col-lg-3 mb-4">Перезагрузить сервер</a>
    </div>
