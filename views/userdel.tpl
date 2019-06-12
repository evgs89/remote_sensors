% rebase('base.tpl', users = users, user = user, result = result)
% if user:
<div>
    <h1 class="mt-5">Список пользователей:</h1>

    % for i in users:
    <p>{{i}}
        % end
</div>
% if result == 'del':
<div>Пользователь удалён</div>
% elif result == 'error':
<div>Ошибка удаления пользователя</div>
% elif result == 'self':
<div>Вы не можете удалить свою учётную запись</div>
% end
<div>
    <link href="https://getbootstrap.com/docs/4.3/examples/sign-in/signin.css" rel="stylesheet">
<form action="/settings/userdel" method="post" class="form-signin">
  <h1 class="h3 mb-3 font-weight-normal">Для подтверждения действия снова введите имя пользователя и пароль</h1>
  <label for="username" class="sr-only">Ваше имя пользователя</label>
  <input name="username" type="text" id="username" class="form-control" placeholder="Ваше имя пользователя" required autofocus>
  <label for="inputPassword" class="sr-only">Ваш пароль</label>
  <input name="password" type="password" id="inputPassword" class="form-control" placeholder="Password" required>
  <label for="userdel" class="sr-only">Удаляем пользователя</label>
  <input name="userdel" type="text" id="userdel" class="form-control" placeholder="Удаляем пользователя" required autofocus>
  <button class="btn btn-lg btn-primary btn-block" type="submit">Удалить</button>
</form>
</div>
% end