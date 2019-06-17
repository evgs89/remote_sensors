% page = page
<header>
<!-- Fixed navbar -->
    <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
    <a class="navbar-brand" href="/"><img class="mr-3" src="/static/home.png"/ width="25" height="25">Remote sensors</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav mr-auto">
            % if user:
            % if page == 'settings':
            <li class="nav-item active">
            % else:
            <li class="nav-item">
            % end
                <a class="nav-link" href="/settings">Настройки</a>
            </li>
            % if page == 'logout':
            <li class="nav-item active">
            % else:
            <li class="nav-item">
            % end
                <a class="nav-link" href="/logout">Выйти из системы</a>
            </li>
            % else:
            % if page == 'login':
            <li class="nav-item active">
            % else:
            <li class="nav-item">
            % end
                <a class="nav-link" href="/login">Авторизация</a>
            </li>
            % end
        </ul>
    </div>
    </nav>
</header>