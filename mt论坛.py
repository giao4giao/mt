import requests,re,os
print(os.environ)
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]
 
def start():
    session = requests.Session()
    push_text = 'mt论坛：'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }
    # 获取登陆所需loginhash和formhash
    getHash_url = 'https://bbs.binmt.cc/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login'
    page_text = session.get(headers=headers, url=getHash_url).text
    loginhash_ex = 'loginhash=(.*?)">'
    formhash_ex = 'formhash" value="(.*?)".*? />'
    loginhash = re.findall(loginhash_ex, page_text, re.S)[0]
    formhash = re.findall(formhash_ex, page_text, re.S)[0]
    # print(loginhash, formhash)
    # 模拟登陆
    login_url = 'https://bbs.binmt.cc/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash=' + loginhash + '&inajax=1'
    data = {
        'formhash': formhash,
        'referer': 'https://bbs.binmt.cc/index.php',
        'loginfield': 'username',
        'username': username,
        'password': password,
        'questionid': '0',
        'answer': '',
    }
    page_text1 = session.post(headers=headers, url=login_url, data=data).text
    #print(page_text1)
    # 验证是否登陆成功
    check_ex = 'root'
    check = re.findall(check_ex, page_text1, re.S)
    if (len(check) != 0):
        print('登录成功')
        push_text = push_text + '登陆成功，'
        # 获取签到所需的formhash
        getHash_url1 = 'https://bbs.binmt.cc/k_misign-sign.html'
        page_text = session.get(headers=headers, url=getHash_url1).text
        formhash1 = re.findall(formhash_ex, page_text, re.S)[0]
        # print(formhash1)
        # 模拟签到
        sign_url = 'https://bbs.binmt.cc/plugin.php?id=k_misign:sign&operation=qiandao&format=text&formhash=' + formhash1
        page_text2 = session.get(headers=headers, url=sign_url).text
        #print(page_text2)
        # 验证是否签到成功
        check = re.findall(check_ex, page_text2, re.S)
        if (len(check) != 0):
            print('签到成功')
            push_text = push_text + '签到成功'
 
        else:
            print('签到失败')
            push_text = push_text + '签到失败'
    else:
        print('登陆失败')
        push_text = push_text + '登陆失败，'
    print(push_text)
 

 
if __name__ == '__main__':
    start()
