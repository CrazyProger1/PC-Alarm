import gettext

gettext.bindtextdomain('base', '')
gettext.textdomain('myapplication')
_ = gettext.gettext

print(_('This is a translatable string.'))



