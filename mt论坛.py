import time

import requests
import os
import re
# print(os.environ)
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]

dic = {
    'zero':'0',
    'one':'1',
    'two':'2',
    'three':'3',
    'four':'4',
    'five':'5',
    'six':'6',
    'seven':'7',
    'eight':'8',
    'nine':'9',
}

def get_more_data(text):
    def get_num(i):
        num = ''
        for i in re.findall('<span class="(.*?)"></span>',dates[i]):
            num+=dic[i]
        return num
    # with open('a.html','w',encoding='utf-8')as f:
    #     f.write(text)
    dic_ = {}
    dates = re.findall('<b class="pics J_numpic J_animation" style=".*?">(.*?)</b>', text, re.DOTALL)
    if dates !=[]:
        dic_['continue'] = get_num(0) # 连续签到天数
        dic_['class'] = 'LV.'+get_num(1) # 签到等级
        dic_['award'] = get_num(2) # 积分奖励
        dic_['all_day'] = get_num(3) # 签到总天数
    dates = re.findall('<div class="font">(.*?)</div>', text, re.DOTALL)
    if dates != []:
        dic_['num'] =dates[0].replace('\r\n','').strip().split('：')[-1] # 签到排名
    dates = re.findall('<div id="comiis_key".*?<span>(.*?)</span>.*?</div>', text, re.DOTALL)
    if dates != []:
        dic_['name'] = dates[0]  # 获取名字
    return dic_


def start():
    session = requests.Session()
    push_text = 'mt论坛：'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }
    # 获取登陆所需loginhash和formhash
    getHash_url = 'https://bbs.binmt.cc/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login'
    session.get(headers=headers, url=getHash_url)
    time.sleep(10)
    session.get(headers=headers, url=getHash_url)
    time.sleep(10)
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
    # print(page_text1)
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
        # 模拟签到
        sign_url = 'https://bbs.binmt.cc/plugin.php?id=k_misign:sign&operation=qiandao&format=text&formhash=' + formhash1
        page_text2 = session.get(headers=headers, url=sign_url).text
        # 验证是否签到成功
        check = re.findall(check_ex, page_text2, re.S)
        if (len(check) != 0):
            print('签到成功')
            push_text = push_text + '签到成功'
            print(push_text)
            return get_more_data(session.get(headers=headers, url=getHash_url1).text)
        else:
            print('签到失败')
            push_text = push_text + '签到失败'
    else:
        print('登陆失败')
        push_text = push_text + '登陆失败，'
    print(push_text)
 

 
if __name__ == '__main__':
    from read_file_to_html import read_to_html
    from mail_to import Mail
    data = start()
    html = read_to_html(data)
    mail = Mail()
    mail.send(html)