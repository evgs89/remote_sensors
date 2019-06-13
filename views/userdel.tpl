% rebase('base.tpl', users = users, user = user, result = result)
% if user:
<div>
    <h1 class="mt-5">Список пользователей:</h1>

    <ul class="list-group list-group-horizontal-md list-group-flush">
        % for i in users:
        <li class="list-group-item">{{i}}</li>
        % end
    </ul>

</div>
% if result == 'del':
<div>Пользователь удалён</div>
% elif result == 'error':
<div>Ошибка удаления пользователя</div>
% elif result == 'self':
<div>Вы не можете удалить свою учётную запись</div>
% end
<div>
<form action="/settings/userdel" method="post" class="form-signin">
  <h1 class="h3 mb-3 font-weight-normal">Для подтверждения действия снова введите имя пользователя и пароль</h1>
  <div class="row">
  <label for="username" class="sr-only">Ваше имя пользователя</label>
  <input name="username" type="text" id="username" class="form-control col-md-3 mb-5 mr-4" placeholder="Ваше имя пользователя" required autofocus>
  <label for="inputPassword" class="sr-only">Ваш пароль</label>
  <input name="password" type="password" id="inputPassword" class="form-control col-md-3 mb-5 mr-4" placeholder="Password" required>
  <label for="userdel" class="sr-only">Удаляем пользователя</label>
  <input name="userdel" type="text" id="userdel" class="form-control col-md-3 mb-5 mr-4" placeholder="Удаляем пользователя" required autofocus>
  </div>
  <button class="btn btn-lg btn-primary btn-block" type="submit">Удалить</button>
</form>
</div>
% end