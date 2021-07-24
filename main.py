import requests
import time
from config import *


class BiliBot:
    def checking_at(self):
        try:
            result = requests.get(url=checking_at_url, headers=headers)
            data_json = result.json()
            if data_json['code'] == 0:
                return data_json['data']['at']
            return 0
        except Exception:
            return 0

    def get_at_data(self):
        result = requests.get(url=get_at_url, headers=headers)
        data_json = result.json()
        if data_json['code'] == 0:
            return data_json['data']['items']

    def reply(self, oid, type, root, parent, message, ater, plat=1):
        reply_data = {"oid": oid, "type": type, "root": root, "parent": parent, "message": message, "plat": plat,
                      "csrf": csrf}
        result = requests.post(url=reply_url, headers=sender_headers, data=reply_data)
        data_json = result.json()
        if data_json['code'] == 0:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "评论发送成功！")
            if code := self.send_msg(ater, message)['code'] == 0:
                print("私信发送:{}成功！".format(ater))
            else:
                print(code)
        else:
            message = "评论发送失败自动转为私信\n" + message
            if code := self.send_msg(ater, message)['code'] == 0:
                print("私信发送:{}成功！".format(ater))
            else:
                print(code)

    def get_uid(self, root, oid, type):
        result = requests.get(url=uid_url.format(root, oid, type))
        data_json = result.json()
        if data_json['code'] == 0:
            for i in data_json['data']['replies']:
                if i['rpid'] == root:
                    return i['mid'], i['member']['uname']
                else:
                    try:
                        for j in i['replies']:
                            if j['rpid'] == root:
                                return j['mid'], j['member']['uname']
                    except Exception:
                        continue

    def get_common(self, uid, name):
        result = requests.get(url=common_url.format(uid), headers=headers)
        data_json = result.json()
        if data_json['code'] == 0:
            names = "此人(@{} )关注的VUP有：\n".format(name)
            if data_json['data']['list']:
                for i in data_json['data']['list']:
                    names += i['uname'] + '、'
                return names[:-1]
            else:
                return "此人(@{} )未发现共同关注的VUP！".format(name)
        else:
            return "此人(@{} )未打开关注列表".format(name)

    def get_medal(self, uid):
        result = requests.get(url=medal_wall_url.format(uid), headers=headers)
        data_json = result.json()
        first_line = '粉丝牌：\n'
        medal_wall = str()
        if data_json['code'] == 0 and data_json['data']['list']:
            num = 10 if len(data_json['data']['list']) > 10 else len(data_json['data']['list'])
            for i in range(num):
                medal_wall = medal_wall + data_json['data']['list'][i]['medal_info']['medal_name'] + str(
                    data_json['data']['list'][i]['medal_info']['level']) + '级' + '\t{}\n'.format(
                    data_json['data']['list'][i]['target_name'])
            return first_line + medal_wall[:-1]
        else:
            return '此人粉丝牌墙未打开。'

    def send_msg(self, receiver_id, msg):
        data = {
            "msg[sender_uid]": self_uid,
            "msg[receiver_id]": receiver_id,
            "msg[receiver_type]": 1,
            "msg[msg_type]": 1,
            "msg[msg_status]": 0,
            "msg[dev_id]": dev_id,
            "msg[timestamp]": int(time.time()),
            "msg[content]": str({"content": "{}".format(msg)}).replace("\'", "\""),
            "csrf_token": csrf,
            "csrf": csrf
        }
        result = requests.post(url=send_msg_url, headers=sender_headers, data=data)
        data_json = result.json()
        return data_json

    def run(self):
        while True:
            if (num := self.checking_at()) > 0:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "发现被@{}次".format(num))
                if num > 10:
                    num = 10
                at_data = self.get_at_data()
                for i in range(num):
                    try:
                        oid = at_data[i]["item"]["subject_id"]
                        type = at_data[i]["item"]["business_id"]
                        root = at_data[i]["item"]["target_id"]
                        parent = at_data[i]["item"]["source_id"]
                        nickname = "回复 @{} :".format(at_data[i]["user"]["nickname"])
                        ater_id = at_data[i]["user"]["mid"]
                        time_str = "\n查询时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        end_str = '\n数据来源：https://b23.tv/SgRBMG'
                        if root != 0:
                            print("查：" + str(s := self.get_uid(root, oid, type)))
                            uid, name = s
                            if ater_id != uid:
                                message = self.get_common(uid, name) + '\n' + self.get_medal(uid)
                                print(message)
                                self.reply(oid, type, root, parent, nickname + message + time_str + end_str, ater_id)
                            else:
                                continue
                        time.sleep(5)
                    except Exception as e:
                        print(e)
                        continue
            time.sleep(10)


if __name__ == '__main__':
    bot = BiliBot()
    bot.run()
