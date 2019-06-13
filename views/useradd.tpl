% rebase('base.tpl', user = user, result = result)
<h1 class="mt-5">Добавление пользователей:</h1>
% if result == 'created':
    <div class="container">Пользователь создан.</div>
% elif result == 'error':
    <div class="container">Ошибка создания пользователя</div>
% elif result == 'duplicate':
    <div class="container">Данное имя пользователя уже используется</div>
% end
<div class="container">
<div class="mt-5 mb-5">
При создании пользователю присваивается пароль '12345678'
</div>
<form class="form-inline" action="/settings/useradd" method="post">
<div class="form-group mb-2 mr-5">
    <label for="username" class="mr-4">Имя нового пользователя:</label>
    <input name="username" id="username" class="form-control mr-4" type="text" />
    <input value="Добавить пользователя" type="submit" class="btn btn-primary mr-4">
</div>

</form>