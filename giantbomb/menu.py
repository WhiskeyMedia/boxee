import mc
import simplejson
import urllib2

API_KEY = 'e5529a761ee3394ffbd237269966e9f53a4c7bf3'

def get_categories():
    response = urllib2.urlopen('http://api.giantbomb.com/video_types/?api_key=' + API_KEY + '&format=json')
    category_data = simplejson.loads(response.read())['results']

    categories = mc.ListItems()
    for cat in category_data:
        item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
        item.SetLabel(str(cat['name']))
        item.SetProperty('id', str(cat['id']))
        categories.append(item)

    return categories

def get_videos(cat_id):
    response = urllib2.urlopen('http://api.giantbomb.com/videos/?api_key=' + API_KEY + '&video_type=' + cat_id + '&sort=-publish_date&format=json')
    video_data = simplejson.loads(response.read())['results']

    videos = mc.ListItems()
    for vid in video_data:
        item = mc.ListItem(mc.ListItem.MEDIA_VIDEO_CLIP)
        item.SetLabel(str(vid['name']))
        item.SetPath(str(vid['url']).replace('.mp4', '_1500.mp4'))
        videos.append(item)

    return videos
