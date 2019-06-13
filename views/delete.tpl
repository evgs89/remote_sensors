% rebase('base.tpl', dev_id = dev_id if dev_id else '', user = user)
% if user:
<div>
    <h1 class="mt-5">Уверены, что хотите удалить данные?</h1>
    <a href="/delete/accept?id={{dev_id}}" class="btn btn-primary my-2">Да</a>
    <a href="/device/{{dev_id}}" class="btn btn-secondary my-2">Нет</a>
</div>
% else:
<div>
    <h1 class="mt-5">Данная операция запрещена без авторизации</h1>
    <a href="/login" class="btn btn-primary my-2">Авторизоваться</a>
</div>
% end