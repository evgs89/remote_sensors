% rebase('base.tpl', user = user, success = success)
% if user:
<form action="/settings/change_password" method="post">
    Old password: <input name="old_password" type="password" /><br>
    New password: <input name="new_password_1" type="password" /><br>
    Retype new password: <input name="new_password_2" type="password" /><br>
    <input value="Change password" type="submit">
</form>
% end
% if success:
You successfully changed password
% end
