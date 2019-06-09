% rebase('base.tpl', dev_id = dev_id if dev_id else '')
<header>Удаление данных</header>
<div>
    Уверены, что хотите удалить данные?<br>
    <a href="/delete/accept?id={{dev_id}}">Да</a><a href="/device/{{dev_id}}">Нет</a>
</div>
