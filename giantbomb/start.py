import mc
import menu

menu.lf_category = 0
menu.lf_video = 0

mc.ActivateWindow(14000)

categories = menu.get_categories()
if categories:
    mc.GetWindow(14000).GetList(100).SetItems(categories)

mc.GetActiveWindow().PushState()
mc.GetActiveWindow().GetList(100).SetFocusedItem(0)

cat_id = mc.GetFocusedItem(14000, 100).GetProperty('id')

if cat_id == 'live':
    pass
else:
    mc.ShowDialogWait()
    mc.GetActiveWindow().GetList(120).SetItems(items)
    mc.GetActiveWindow().GetControl(120).SetVisible(True)
    mc.HideDialogWait()
    mc.GetActiveWindow().GetControl(120).SetFocus()
