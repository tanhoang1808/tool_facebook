import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

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
        
    
    def login_facebook_cookie(self,cookie):

        options = Options()
        options.headless = True
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-renderer-backgrounding')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.maximize_window()
        driver.get("https://www.facebook.com/")
        # Giả sử cookie là một dictionary với tên và giá trị cookie
        script = 'javascript:void(function(){ function setCookie(t) { var list = t.split("; "); console.log(list); for (var i = list.length - 1; i >= 0; i--) { var cname = list[i].split("=")[0]; var cvalue = list[i].split("=")[1]; var d = new Date(); d.setTime(d.getTime() + (7*24*60*60*1000)); var expires = ";domain=.facebook.com;expires="+ d.toUTCString(); document.cookie = cname + "=" + cvalue + "; " + expires; } } function hex2a(hex) { var str = ""; for (var i = 0; i < hex.length; i += 2) { var v = parseInt(hex.substr(i, 2), 16); if (v) str += String.fromCharCode(v); } return str; } setCookie("'+cookie+'"); location.href = "https://facebook.com"; })();'
        
        driver.execute_script(script)
        # Đợi một chút để đảm bảo cookies đã được thiết lập và trang đã tải
        time.sleep(10)
        return driver
    
    def get_group_members(self, group_id, cookies):
        max_member = 1000
        members = []
        driver = self.login_facebook_cookie(cookies)
        
        time.sleep(2)
        url = f'https://www.facebook.com/groups/{group_id}/members/'
        driver.get(url)
        
        # Chờ trang tải xong
        time.sleep(2)

        # Cuộn trang xuống nhiều lần để tải thêm thành viên
        scroll_pause_time = 2  # Thời gian chờ sau khi cuộn
        scroll_limit = 10  # Số lần cuộn tối đa (tùy chọn)
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll = 0
        while(scroll <= scroll_limit):
            number_temp_members = []
            # Cuộn xuống dưới cùng trang
           
           
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            scroll +=1
            # Chờ một chút để trang tải thêm dữ liệu
            time.sleep(scroll_pause_time)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            for user in soup.find_all('a', href=True):
                href = user['href']
                if f'/groups/{group_id}/user/' in href:
                    user_id = href.split(f'/groups/{group_id}/user/')[1].split('/')[0]
                    number_temp_members.append(user_id)
            print(len(number_temp_members))

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        for user in soup.find_all('a', href=True):
            href = user['href']
            if f'/groups/{group_id}/user/' in href:
                user_id = href.split(f'/groups/{group_id}/user/')[1].split('/')[0]
                if user_id not in members:
                    members.append(user_id)  
    
        with open('UID_list.txt', 'w') as f:
            for uid in members:
                f.write(f"{uid}\n")

        print(f"Tổng số thành viên lấy được: {len(members)}. Danh sách UID đã lưu vào UID_list.txt.")
        input("Press Enter to exit...")
        
        driver.quit()
        return members

    def check_members_live(self, uids):
        for uid in uids:
            url = f"https://mbasic.facebook.com/profile.php?id={uid}"
            
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 404 or 'Trang này không có sẵn' in response.text or 'This Page Isn\'t Available' in response.text or 'Bạn hiện không xem được nội dung này' in response.text:
                print(f"UID [{uid}] đã chết.")
                
            else:
                print(f"UID [{uid}] còn sống.")

    def check_uid_live(self, uid):
        try:
            for _ in range(20):  # Thử lại tối đa 20 lần
                try:
                    response = requests.get(f"https://graph.facebook.com/{uid}/picture?type=normal")
                    break  # Thoát khỏi vòng lặp nếu thành công
                except requests.exceptions.RequestException:
                    continue  # Bỏ qua lỗi và thử lại
            else:
                return False  # Nếu vượt quá số lần thử mà không thành công
            
            if "static.xx.fbcdn.net" in response.url:
                print(f"UID {uid} die")
                return False  # UID đã chết
            elif "scontent." in response.url:
                print(f"UID {uid} live")
                return True  # UID còn sống
            else:
                return True  # UID còn sống (phòng trường hợp khác)
        
        except Exception as ex:
            print(f"Lỗi: {str(ex)}")
            return False
