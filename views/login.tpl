% rebase('base.tpl', user = user)
<link href="https://getbootstrap.com/docs/4.3/examples/sign-in/signin.css" rel="stylesheet">
<form action="/login" method="post" class="form-signin">
  <h1 class="h3 mb-3 font-weight-normal">Введите Ваши данные</h1>
  <label for="login" class="sr-only">Имя пользователя</label>
  <input name="username" type="text" id="login" class="form-control" placeholder="Login" required autofocus>
  <label for="inputPassword" class="sr-only">Пароль</label>
  <input name="password" type="password" id="inputPassword" class="form-control" placeholder="Password" required>
  <button class="btn btn-lg btn-primary btn-block" type="submit">Авторизоваться</button>
</form>
