% rebase('base.tpl', users = users, user = user, result = result)
% if result == 'del':
    <div>Пользователь удалён</div>
% elif result == 'error':
    <div>Ошибка удаления пользователя</div>
% elif result == 'self':
    <div>Вы не можете удалить свою учётную запись</div>
% end
% if user:
<div>
Список пользователей:
% for i in users:
    <p>{{i}}
% end
</div>
<div>
<p>Для подтверждения действия снова введите имя пользователя и пароль</p>
<form action="/settings/userdel" method="post">
    Your username: <input name="username" type="text" /><br>
    Your password: <input name="password" type="password" /><br>
    Deleting user: <input name="userdel" type="text" /><br>
    <input value="Delete user" type="submit">
</form>
</div>
% end