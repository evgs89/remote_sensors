% rebase('base.tpl', rows = rows, user = user)
<link href="https://getbootstrap.com/docs/4.3/examples/blog/blog.css" rel="stylesheet">
<h1 class="mt-5">Сервер активен</h1>
<div class="table-responsive">
    <table class="table table-striped table-sm">
        <thead>
            <tr>
                <th>ID</th><th>Data</th><th>Balance</th><th>Received at:</th>
            </tr>
        </thead>
        <tbody>
            % for row in rows:
            <tr>
                <td><a href = '/device/{{row[0]}}'>{{row[0]}}</a></td>
                <td>{{row[1]}}</td>
                <td>{{row[2]}}</td>
                <td>{{row[3]}}</td>
            </tr>
            % end
        </tbody>
    </table>
</div>
    % if user:
    <div>
        <a href='/delete'>Очистить всю базу данных</a>
    </div>
    % end

