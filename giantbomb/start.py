import mc
import menu

menu.lf_category = 0
menu.lf_video = 0

mc.ActivateWindow(14000)

categories = menu.get_categories()
if categories:
    mc.GetWindow(14000).GetList(100).SetItems(categories)
