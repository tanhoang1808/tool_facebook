import requests
from bs4 import BeautifulSoup
from random import randint
from time import sleep

def read_uid(path):
    try:
        account = open(path).readlines()
        uid = account[0].split('|')[0].strip()

        account.remove(account[0])
        file2 = open(path, 'w')
        for text in account:
            file2.write(text)
        return uid
    except:
        return False

class GroupFacebook:
    def __init__(self, cookies):
        self.cookies = cookies
        self.headers = {
            "cookie": cookies,
            "Host": "d.facebook.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "connection": "keep-alive",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
        }

    def check_live_cookie(self):
        url = 'https://mbasic.facebook.com/profile.php'
        payload = {}

        response = requests.get(url, headers=self.headers, data=payload)
        if 'Log in' in response.text:
            print('COOKIE DIE => VUI LÒNG GET LẠI COOKIE')
            return False
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            name = soup.find('title').text
            uid = soup.find('input', {'type': 'hidden', 'name': 'target'})['value']
            print(f'COOKIE LIVE => NAME [ {name} ] => UID [ {uid} ]')

    def get_data(self):
        try:
            response = requests.get(url="https://d.facebook.com/", headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            fb_dtsg = soup.find('input', {'name': 'fb_dtsg'})['value']
            jazoest = soup.find('input', {'name': 'jazoest'})['value']
            return fb_dtsg
        except:
            return False

    def add_member_graphql(self, fb_dtsg, uid, uid_group):
        url = 'https://www.facebook.com/api/graphql/'
        print("uid in add : ",uid)
        payload = {
            '__user': uid,
            'fb_dtsg': fb_dtsg,
            'variables': '''
                    {
                    "input": {
                        "attribution_id_v2": "CometGroupDiscussionRoot.react,comet.group,unexpected,1703385977900,792285,2361831622,,;GroupsCometCrossGroupFeedRoot.react,comet.groups.feed,tap_bookmark,1703385975809,246315,2361831622,,",
                        "email_addresses": [],
                        "group_id": "'''+uid_group+'''",
                        "source": "comet_invite_friends",
                        "user_ids": [
                        "'''+uid+'''"
                        ],
                        "actor_id": "'''+uid+'''",
                        "client_mutation_id": "14"
                        },
                    "groupID": "'''+uid_group+'''"
                    }
                ''',
            'doc_id': '7019631194753826'
        }

        headers = {
            'cookie': self.cookies
            }
        response = requests.post(url, headers=headers, data=payload).json()
        try:
            response['errors'][0]['message'] == 'Rate limit exceeded'
            return False
        except Exception as e:
            print(e)
            pass
        
        try:
            print(response['data']['group_add_member']['added_users'][0]['id'])
            response['data']['group_add_member']['added_users'][0]['id'] == uid
            print(f'Mời UID [{uid}] tham gia Group [{uid_group}] thành công.')
            return True
        except Exception as e:
            print("exception :",e)
            print(f'Mời UID [{uid}] tham gia Group [{uid_group}] không thành công.')
            return False


def main(cookies, uid_group):
    group = GroupFacebook(cookies)
    if group.check_live_cookie() != False:
        fb_dtsg= group.get_data()
        if fb_dtsg != False:
            print("fb_dtsg : ",fb_dtsg)
            while True:
                uid = read_uid('uid.txt')
                if uid:
                    print(uid)
                    if group.add_member_graphql(fb_dtsg, uid, uid_group) != False:
                        delay = randint(5,15)
                        print(f'RANDOM DELAY TIME - {delay} seconds')
                        sleep(delay)
                        return 200
                    else:
                        print('FACEBOOK SPAM - BLOCK TÍNH NĂNG')
                        sleep(5)
                        return 201
                else:
                    print('Hết uid')
                    return 202


