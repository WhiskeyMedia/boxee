import mc
import simplejson
import urllib2

def get_category_menu():
    response = urllib2.urlopen('http://api.giantbomb.com/video_types/?api_key=e5529a761ee3394ffbd237269966e9f53a4c7bf3&format=json')
    categories = simplejson.loads(response.read())['results']

    category_menu = mc.ListItems()
    for cat in categories:
        item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
        item.SetLabel(str(cat['name']))
        item.SetPath(str(cat['id']))
        category_menu.append(item)

    return category_menu