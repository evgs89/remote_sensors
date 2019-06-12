% rebase('base.tpl', user = user, accepted = accepted)
% if not accepted:
% if user:
<div>
    <h1 class="mt-5">Перезагрузить сервер?</h1>
    <a href="/" class="btn btn-primary my-2">Нет</a>
    <a href="/settings/reboot?accepted=1" class="btn btn-secondary my-2">Да</a>
</div>
% else:
<div>
    <h1 class="mt-5">Вы не вошли в систему</h1>
    <a href="/login" class="btn btn-primary my-2">Авторизоваться</a>
    <a href="/" class="btn btn-secondary my-2">На главную страницу</a>
</div>
% end
% else:
<div>Rebooting server, wait 2 minutes</div>
% end