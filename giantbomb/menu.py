import mc
import simplejson

API_PATH = 'http://api.giantbomb.com'
API_KEY = '57659bff0faacdf8ab9b2500b552e7fd37b4b677' # Default API key

lf_category = 0
lf_video = 0

def get_categories():
    categories = mc.ListItems()

    # Live streams
    response = mc.Http().Get(API_PATH + '/chats/?api_key=' + API_KEY + '&format=json')
    chat_data = simplejson.loads(response)['results']

    for chat in chat_data:
        # src_url = urllib.quote('http://www.justin.tv/widgets/live_embed_player.swf?channel=' + chat['channel_name'] + '&auto_play=true&start_volume=25')
        # if chat['password']:
        #     src_url += '&publisherGuard=' + chat['password']
        # bx_jsactions_url = urllib.quote('http://localhost:8001/media/chat/js/boxee.js')
        # url = 'flash://www.justin.tv/src=' + src_url + '&bx-jsactions=' + bx_jsactions_url

        url = 'http://www.justin.tv/widgets/live_embed_player.swf?channel=' + chat['channel_name'] + '&auto_play=true&start_volume=25'
        if chat['password']:
            url += '&publisherGuard=' + chat['password']

        item = mc.ListItem(mc.ListItem.MEDIA_VIDEO_CLIP)
        item.SetLabel('LIVE: ' + chat['title'].encode('utf-8'))
        item.SetProperty('id', 'live'.encode('utf-8'))
        item.SetDescription(chat['deck'].encode('utf-8'))
        item.SetThumbnail(chat['image']['super_url'].encode('utf-8'))
        item.SetPath(url.encode('utf-8'))
        categories.append(item)

    response = mc.Http().Get(API_PATH + '/video_types/?api_key=' + API_KEY + '&format=json')
    category_data = simplejson.loads(response)['results']

    # Latest
    item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
    item.SetLabel('Latest'.encode('utf-8'))
    item.SetProperty('id', 'latest'.encode('utf-8'))
    categories.append(item)

    for cat in category_data:
        item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
        item.SetLabel(cat['name'].encode('utf-8'))
        item.SetProperty('id', str(cat['id']).encode('utf-8'))
        categories.append(item)

    # Search
    item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
    item.SetLabel('Search'.encode('utf-8'))
    item.SetProperty('id', 'search'.encode('utf-8'))
    categories.append(item)

    # Link Account
    api_key = mc.GetApp().GetLocalConfig().GetValue('api_key')
    if not api_key:
        item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
        item.SetLabel('Link Account'.encode('utf-8'))
        item.SetProperty('id', 'link'.encode('utf-8'))
        categories.append(item)

    return categories

def get_eruns():
    eruns = mc.ListItems()

    item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
    item.SetLabel('Deadly Premonition'.encode('utf-8'))
    item.SetProperty('id', '5-DP'.encode('utf-8'))
    eruns.append(item)

    item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
    item.SetLabel('Persona 4'.encode('utf-8'))
    item.SetProperty('id', '5-P4'.encode('utf-8'))
    eruns.append(item)

    item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
    item.SetLabel('The Matrix Online: Not Like This'.encode('utf-8'))
    item.SetProperty('id', '5-MO'.encode('utf-8'))
    eruns.append(item)

    return eruns

def get_api_key(link_code):
    if link_code and len(link_code) == 6:
        try:
            response = mc.Http().Get(API_PATH + '/validate?link_code=' + link_code + '&format=json')
            data = simplejson.loads(response)
            api_key = data['api_key']
            return str(api_key)
        except:
            return None
    else:
        return None

def link_account():
    mc.ShowDialogOk("Let's do this.", "To link your account, visit www.giantbomb.com/boxee to get a link code.\n\nEnter this code on the next screen.")

    link_code = mc.ShowDialogKeyboard("Enter your link code.", "", False).upper()
    new_api_key = get_api_key(link_code)
    if new_api_key:
        mc.GetApp().GetLocalConfig().SetValue('api_key', new_api_key)
        global API_KEY
        API_KEY = new_api_key
        return True
    else:
        return False

def get_videos(cat_id):
    if cat_id == 'latest':
        response = mc.Http().Get(API_PATH + '/videos/?api_key=' + API_KEY + '&sort=-publish_date&format=json')
    elif cat_id == 'search':
        query = mc.ShowDialogKeyboard("Search", "", False).replace(' ', '%20')
        response = mc.Http().Get(API_PATH + '/search/?api_key=' + API_KEY + '&resources=video&query=' + query + '&format=json')
    elif cat_id == '5-DP':
        response = mc.Http().Get(API_PATH + '/videos/?api_key=' + API_KEY + '&video_type=5&offset=161&format=json')
    elif cat_id == '5-P4':
        response = mc.Http().Get(API_PATH + '/videos/?api_key=' + API_KEY + '&video_type=5&format=json')
    elif cat_id == '5-MO':
        response = mc.Http().Get(API_PATH + '/videos/?api_key=' + API_KEY + '&video_type=5&offset=105&limit=21&format=json')
    else:
        response = mc.Http().Get(API_PATH + '/videos/?api_key=' + API_KEY + '&video_type=' + cat_id + '&sort=-publish_date&format=json')

    video_data = simplejson.loads(response)['results']

    if cat_id == '5-P4':
        response = mc.Http().Get(API_PATH + '/videos/?api_key=' + API_KEY + '&video_type=5&offset=100&limit=61&format=json')
        video_data += simplejson.loads(response)['results']
        video_data = [video for video in video_data if not video['name'].startswith('The Matrix Online')]
    elif cat_id == '5-MO':
        video_data = [video for video in video_data if video['name'].startswith('The Matrix Online')]

    videos = mc.ListItems()

    border = 'bg_imgFlare_640x360.png'.encode('utf-8')
    for vid in video_data:
        if 'hd_url' in vid:
            url = vid['hd_url'] + '&api_key=' + API_KEY
        else:
            url = vid['high_url']
        date = vid['publish_date'].encode('utf-8').split(' ')[0].split('-')

        item = mc.ListItem(mc.ListItem.MEDIA_VIDEO_CLIP)
        item.SetLabel(vid['name'].encode('utf-8'))
        item.SetDescription(vid['deck'].encode('utf-8'))
        item.SetThumbnail(vid['image']['super_url'].encode('utf-8'))
        item.SetImage(0, border)
        item.SetPath(url.encode('utf-8'))
        item.SetDate(int(date[0]), int(date[1]), int(date[2]))
        item.SetDuration(vid['length_seconds'])
        videos.append(item)

        if border == 'bg_imgFlare_640x360.png'.encode('utf-8'):
            border = 'bg_imgFlare2_640x360.png'.encode('utf-8')
        else:
            border = 'bg_imgFlare_640x360.png'.encode('utf-8')

    return videos
