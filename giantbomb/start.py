import mc
import menu

mc.ActivateWindow(14000)

categories = menu.get_categories()
if categories:
    mc.GetWindow(14000).GetList(100).SetItems(categories)
