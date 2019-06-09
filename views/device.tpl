% rebase('base.tpl', page_info = page_info, data = data)
<header>Данные от отправителя: {{page_info['id']}}</header>
<table cellspacing=20>
    <tr>
        <tr><th>Data
        <a href="/device/{{page_info['id']}}?page={{page_info['page']}}&sort_by=data&reverse=0">↓</a>
        <a href="/device/{{page_info['id']}}?page={{page_info['page']}}&sort_by=data&reverse=1">↑</a></th>
        <th>Balance
        <a href="/device/{{page_info['id']}}?page={{page_info['page']}}&sort_by=balance&reverse=0">↓</a>
        <a href="/device/{{page_info['id']}}?page={{page_info['page']}}&sort_by=balance&reverse=1">↑</a></th>
        <th>Received at:
        <a href="/device/{{page_info['id']}}?page={{page_info['page']}}&sort_by=received_at&reverse=0">↓</a>
        <a href="/device/{{page_info['id']}}?page={{page_info['page']}}&sort_by=received_at&reverse=1">↑</a></th>
        % for row in data:
        <tr><td>{{row[1]}}</td><td>{{row[2]}}</td><td>{{row[3]}}</td></tr>
        % end
    </tr>
</table>
<div>
<table cellspacing=30><tr>
    % for i in range(page_info['pages']):
    % if page_info['page'] == i + 1:
    <td><b>{{i+1}}</b></td>
    % else:
    <td><a href="/device/{{page_info['id']}}?page={{i + 1}}&sort_by={{page_info['sort_by']}}&reverse={{int(page_info['reverse'])}}">{{i + 1 }}</a></td>
    % end
    % end
</tr></table>
</div>
<div><a href="/delete?id={{page_info['id']}}">Удалить все сообщения от данного устройства</a></div>