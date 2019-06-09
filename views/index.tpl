% rebase('base.tpl', rows = rows)
<table cellspacing=20>
    <tr>
        <tr><th>ID</th><th>Data</th><th>Balance</th><th>Received at:</th>
        % for row in rows:
        <tr><td><a href = '/device/{{row[0]}}'>{{row[0]}}</a></td><td>{{row[1]}}</td><td>{{row[2]}}</td><td>{{row[3]}}</td></tr>
        % end
</table>
<div>
    <a href='/delete'>Очистить всю базу данных</a>
</div>
