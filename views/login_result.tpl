% rebase('base.tpl', user = user)
% if user:
<div>
    <h1 class="mt-5">Вы успешно авторизовались</h1>
    <a href="/" class="btn btn-primary my-2">На главную страницу</a>
</div>
% else:
<div>
    <h1 class="mt-5">Вы не вошли в систему</h1>
    <a href="/login" class="btn btn-primary my-2">Авторизоваться</a>
    <a href="/" class="btn btn-secondary my-2">На главную страницу</a>
</div>
% end
