from GroupFacebookClass import GroupFacebook

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


def followers(group,uid):
    print(uid)
    print(group.get_followers_count(uid))