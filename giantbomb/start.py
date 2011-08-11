import mc
import menu

menu.lf_category = 0
menu.lf_erun = 0
menu.lf_video = 0

mc.ActivateWindow(14000)

api_key = mc.GetApp().GetLocalConfig().GetValue('api_key')
if api_key:
    menu.API_KEY = api_key

categories = menu.get_categories()
if categories:
    mc.GetWindow(14000).GetList(100).SetItems(categories)
