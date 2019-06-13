% rebase('base.tpl', user = user, settings = settings)
<div>
    <form action="/settings" method="post">
    <div class="row">
        <div class="col-md-6 mb-4">
            <label for="store_days">Время хранения данных (дней):</label>
            <input id="store_days" name="store_days" type="text" class="form-control" value="{{settings['db_settings']['store_days']}}" />
        </div>
        <div class="col-md-6 mb-4">
            <label for="session_expire_days">Время авторизованной сессии (дней):</label>
            <input id="session_expire_days" name="session_expire_days" class="form-control" type="text" value="{{settings['web_server']['session_expire_days']}}"/>
        </div>
        </div>
        <div class="container-fluid mb-5">
            <input class="btn btn-lg btn-primary btn-block" value="Применить" type="submit">
        </div>
    </form>
</div>
<div class="row">
    <a href="/settings/change_password" class="btn btn-primary btn-block col-lg-2 mr-2 mb-4">Сменить пароль</a>
    <a href="settings/useradd" class="btn btn-secondary col-lg-3 mr-2 mb-4">Добавить учётную запись</a>
    <a href="settings/userdel" class="btn btn-secondary col-lg-3 mr-2 mb-4">Удалить учётную запись</a>
    <a href="/settings/reboot" class="btn btn-secondary col-lg-3 mr-2 mb-4">Перезагрузить сервер</a>
</div>

<footer class="footer mt-auto py-3">
  <div class="container">
    <span class="text-muted">
        server application developer: <a href="mailto:evgs89@gmail.com">evgs89</a><br>
        home icon by: <a href="https://pngtree.com/free-icons/commodity  home button">from pngtree.com</a>
    </span>
  </div>
</footer>

