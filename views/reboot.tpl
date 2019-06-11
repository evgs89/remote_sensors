% rebase('base.tpl', user = user, accepted = accepted)
% if not accepted:
% if user:
<div>Reboot server</div>
<div><a href="/settings/reboot?accepted=1">Reboot</a></div>
% else:
<div>You are not authorised</div><br>
% end
<div><a href="/">Back to main page</a></div>
% else:
<div>Rebooting server, wait 2 minutes</div>
% end