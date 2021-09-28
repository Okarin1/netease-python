import re
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from utils import name
from requests_html import HTMLSession  # 用于数据请求、数据提取、相较于其他库更加简洁方便

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.111 Safari/537.36 '
}  # 请求头

session = HTMLSession()


def login(u, p):
    url = 'https://netease-cloud-music-api-okarin1.vercel.app/login/cellphone'  # 网易云手机登录接口

    data = {
        'phone': u,
        'password': p
    }
    res = session.get(url, headers=headers, params=data)
    return res.text


def upload_name_job(prefix):
    url = 'https://netease-cloud-music-api-okarin1.vercel.app/user/update?nickname='  # 网易云更换名字接口
    upname = prefix + name.generate_time_name()
    print(upname)
    namecode = session.get(str(url + upname), headers=headers)

    """
    更改名字接口仅在登录后生效
    更改成功返回值为：code:200
    """

    code = namecode.json()  # 将返回值转换为字典
    if code['code'] == 200:
        print("Succeed")
    else:
        print("fail")


def main():
    u = input('请输入手机号: ')
    p = input('请输入密码: ')
    prefix = input('请输入前缀：')  # 网易云不允许重复名字

    userInfo = login(u, p)
    oldname = re.findall('"nickname":"(.*?)",', str(userInfo))  # 正则表达式获取名字
    print(oldname)
    print('starting...')

    scheduler = BlockingScheduler()  # 定时任务
    now = datetime.now()
    scheduler.add_job(
        upload_name_job,
        'interval',
        minutes=1,
        args=[prefix],  # 不能使用upload_name_job(prefix)传递参数
        start_date=now.replace(second=0, microsecond=0),
    )
    scheduler.start()


if __name__ == '__main__':
    main()
