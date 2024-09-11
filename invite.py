from random import randint
from time import sleep
from GroupFacebookClass import GroupFacebook
from followers import followers
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


def main(cookies, uid_group):
    group = GroupFacebook(cookies)
    if group.check_live_cookie() != False:
        fb_dtsg= group.get_data()
        if fb_dtsg != False:
            print("fb_dtsg : ", fb_dtsg)
            group.check_uid_live("100016289472955")
            while True:
                uid = read_uid('uid.txt')
                if uid:
                    members = group.get_group_members(uid_group,cookies)
                    group.check_members_live(members)
                    if group.add_member_graphql(fb_dtsg, uid, uid_group) != False:
                        delay = randint(5, 15)
                        print(f'RANDOM DELAY TIME - {delay} seconds')
                        sleep(delay)
                        return 200  # Mời thành công
                    else:
                        print('FACEBOOK SPAM - BLOCK TÍNH NĂNG')
                        sleep(5)
                        return 201  # Không thể thêm user vào group (do Facebook chặn)
                else:
                    print('Hết uid')
                    return 202  # Tất cả UID đã được xử lý
    else:
        return 204  # Cookie bị die



