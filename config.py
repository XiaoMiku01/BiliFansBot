headers = {
    "Cookie": ""
}
self_uid = 0
csrf = str()
for i in headers['Cookie'].split(';'):
    if 'bili_jct' in i:
        csrf = i.split('=')[1]

dev_id = '478CADC4-5F73-487C-84E7-0CB6A5BEF71E'

checking_at_url = 'https://api.bilibili.com/x/msgfeed/unread'

get_at_url = 'https://api.bilibili.com/x/msgfeed/at?build=0&mobi_app=web'

reply_url = 'https://api.bilibili.com/x/v2/reply/add'

uid_url = 'https://api.bilibili.com/x/v2/reply/jump?rpid={}&oid={}&type={}'

common_url = 'https://api.bilibili.com/x/relation/same/followings?vmid={}'

medal_wall_url = 'https://api.live.bilibili.com/xlive/web-ucenter/user/MedalWall?target_id={}'

send_msg_url = 'https://api.vc.bilibili.com/web_im/v1/web_im/send_msg'
