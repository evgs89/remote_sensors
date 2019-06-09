% rebase('base.tpl', dev_id = dev_id if dev_id else '', user = user)
<header>Удаление данных</header>
% if user:
<div>
    Уверены, что хотите удалить данные?<br>
    <a href="/delete/accept?id={{dev_id}}">Да</a><a href="/device/{{dev_id}}">Нет</a>
</div>
% else:
<div>
    <b>Данная операция запрещена без авторизации</b><br>
    <a href="/login">Авторизоваться</a>
</div>
% end
