% rebase('base.tpl', user = user)
% if user:
<div>You successfully logged in</div>
% else:
<div>Login error</div><br>
<div><a href="/login">Try again</a></div>
% end
<div><a href="/">Back to main page</a></div>