% rebase('base.tpl', user = user, result = result)
% if result == 'created':
    <div>Пользователь создан.</div>
% elif result == 'error':
    <div>Ошибка создания пользователя</div>
% elif result == 'duplicate':
    <div>Данное имя пользователя уже используется</div>
% end
<form action="/settings/useradd" method="post">
    Username: <input name="username" type="text" /><br>
    Default password is '12345678'<br>
    <input value="Add user" type="submit">
</form>