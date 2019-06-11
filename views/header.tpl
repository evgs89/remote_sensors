<div>
    <a href="/"><b>Remote Sensors</b></a>
    % if user:
    <a href="/logout">Выйти из системы</a>
    <a href="/settings">Настройки</a>
    % else:
    <a href="/login">Авторизоваться</a>
    % end
</div>
