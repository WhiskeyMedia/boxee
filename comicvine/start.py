import mc
import menu
import simplejson

menu.lf_category = 0
menu.lf_video = 0

mc.ActivateWindow(14000)

api_key = mc.GetApp().GetLocalConfig().GetValue('api_key')
if api_key:
    response = mc.Http().Get(menu.API_PATH + '/chats/?api_key=' + api_key + '&format=json')
    data = simplejson.loads(response)
    if data['status_code'] == 100:
        # Revert to the default key
        mc.GetApp().GetLocalConfig().ResetAll()
    else:
        menu.API_KEY = api_key

categories = menu.get_categories()
if categories:
    mc.GetActiveWindow().GetList(100).SetItems(categories)

mc.GetActiveWindow().GetList(100).SetFocusedItem(0)

# cat_id = mc.GetFocusedItem(14000, 100).GetProperty('id')

# if cat_id == 'live':
#     pass
# else:
#     mc.GetActiveWindow().PushState()
#     mc.ShowDialogWait()
#     items = menu.get_videos(cat_id)
#     mc.GetActiveWindow().GetList(120).SetItems(items)
#     mc.GetActiveWindow().GetControl(120).SetVisible(True)
#     mc.HideDialogWait()
#     mc.GetActiveWindow().GetControl(120).SetFocus()