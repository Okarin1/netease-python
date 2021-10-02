# encoding：utf-8
import time


def generate_time_name():
    # time.strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}').format(y='年', m='月', d='日', h='时', f='分', s='秒')
    now = time.strftime('%H{h}%M{f}').format(y='年', m='月', d='日', h='時', f='分', s='秒')
    return now
