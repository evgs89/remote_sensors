% rebase('base.tpl', user = user)
<header>Выход из системы</header>
% if user:
<div>
    Уверены, что хотите выйти?<br>
    <a href="/logout?accepted=1">Да</a><a href="/">Нет</a>
</div>
% else:
<div>
    <b>Вы не вошли в систему</b><br>
    <a href="/login">Авторизоваться</a><a href="/">На главную</a>
</div>
% end