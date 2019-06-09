% rebase('base.tpl', user = user)
% if user:
<div>You successfully logged in</div>
% else:
<div>You are not authorised</div><br>
<div><a href="/login">Log in</a></div>
% end
<div><a href="/">Back to main page</a></div>