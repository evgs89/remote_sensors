% rebase('base.tpl', user = user, success = success)
<!--<link href="https://getbootstrap.com/docs/4.3/examples/sign-in/signin.css" rel="stylesheet">-->
% if user:
<form action="/settings/change_password" method="post" class="form-signin">
  <h1 class="h3 mb-3 font-weight-normal">Смена пароля</h1>
  <label for="old_pwd" class="sr-only">Текущий пароль</label>
  <input name="old_password" type="password" id="old_pwd" class="form-control mb-3" placeholder="Текущий пароль" required autofocus>
  <label for="new_pwd1" class="sr-only">Новый пароль</label>
  <input name="new_password_1" type="password" id="new_pwd1" class="form-control mb-3" placeholder="Новый пароль" required>
  <label for="new_pwd2" class="sr-only">Повторите пароль</label>
  <input name="new_password_2" type="password" id="new_pwd2" class="form-control mb-3" placeholder="Повторите пароль" required>
  <button class="btn btn-lg btn-primary btn-block" type="submit">Сменить пароль</button>
</form>
% end
% if success:
Вы сменили пароль!
% end
