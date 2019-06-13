% rebase('base.tpl', rows = rows, user = user, page_info = page_info)
<link href="https://getbootstrap.com/docs/4.3/examples/blog/blog.css" rel="stylesheet">
<h1 class="mt-5">Сервер активен</h1>
<div class="table-responsive">
    <table class="table table-striped table-sm">
        <thead>
            <tr>
                <th>
                    ID
                    <a href="/?page={{page_info['page']}}&sort_by=dev_id&reverse=0">↓</a>
                    <a href="/?page={{page_info['page']}}&sort_by=dev_id&reverse=1">↑</a>
                </th>
                <th>
                    Data
                    <a href="/?page={{page_info['page']}}&sort_by=data&reverse=0">↓</a>
                    <a href="/?page={{page_info['page']}}&sort_by=data&reverse=1">↑</a>
                </th>
                <th>
                    Balance
                    <a href="/?page={{page_info['page']}}&sort_by=balance&reverse=0">↓</a>
                    <a href="/?page={{page_info['page']}}&sort_by=balance&reverse=1">↑</a>
                </th>
                <th>
                    Received at:
                    <a href="/?page={{page_info['page']}}&sort_by=received_at&reverse=0">↓</a>
                    <a href="/?page={{page_info['page']}}&sort_by=received_at&reverse=1">↑</a>
                </th>
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
<div>
    <nav class="blog-pagination">
        % if page_info['pages'] > 1:
        % for i in range(page_info['pages']):
        % if page_info['page'] == i + 1:
        <a class="btn btn-outline-secondary disabled" href="#" tabindex="-1" aria-disabled="true">{{i+1}}</a>
        % else:
        <a class="btn btn-outline-primary" href="?page={{i + 1}}&sort_by={{page_info['sort_by']}}&reverse={{int(page_info['reverse'])}}">{{i + 1 }}</a></td>
        % end
        % end
        % end
      </nav>
</div>

    % if user:
    <div>
        <a href='/delete'>Очистить всю базу данных</a>
    </div>
    % end

