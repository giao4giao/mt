#!/usr/bin/env python
# encoding: utf-8
import re
from datetime import timezone, timedelta, datetime
from typing import Optional

from .sign import MtSignClass


class ParseMtClass(MtSignClass):
    """解析类"""
    mapping_dict = {
        'zero': '0',
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
    }  # 英语和数字的映射表

    html = """\
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style type="text/css">
                span{{
                    color : green;
                    font-weight: bold;
                    text-align: center;
                }}
                li{{
                    text-align: center;
                    list-style: none;
                }}
            </style>
        </head>
        <body>
        {content}
        </body>
        </html>\
    """.replace('    ', '')

    def __get_num(self, datas: list, i: int) -> str:
        """通过映射表来设置数值"""
        return ''.join(
            self.mapping_dict[i]
            for i in re.findall(
                r'<span class="(.*?)"></span>',
                datas[i]
            )
        )

    def _parse_more_data(self, text: str) -> dict:
        """解析有关的数据"""
        dic_ = {}
        many_data = re.findall(r'<b class="pics J_numpic J_animation" style=".*?">(.*?)</b>', text, re.DOTALL)
        if many_data:
            dic_['continue'] = self.__get_num(many_data, 0)  # 连续签到天数
            dic_['class'] = 'LV.' + self.__get_num(many_data, 1)  # 签到等级
            dic_['award'] = self.__get_num(many_data, 2)  # 积分奖励
            dic_['all_day'] = self.__get_num(many_data, 3)  # 签到总天数
        dates = re.findall('<div class="font">(.*?)</div>', text, re.DOTALL)
        if dates:
            dic_['num'] = dates[0].replace('\r\n', '').strip().split('：')[-1]  # 签到排名
        dates = re.findall('<div id="comiis_key".*?<span>(.*?)</span>.*?</div>', text, re.DOTALL)
        if dates:
            dic_['name'] = dates[0]  # 获取名字
        return dic_

    def _get_more_data(self, html: Optional[str] = None) -> dict:
        """获取数据"""
        html = self.sign_page() if not html else html
        return self._parse_more_data(html)

    @staticmethod
    def now_time() -> str:
        """返回北京时间"""
        sha_tz = timezone(
            timedelta(hours=8),
            name='Asia/Shanghai',
        )
        return datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(sha_tz).strftime('%Y-%m-%d %H:%M:%S')

    def read_to_html(self, dic: Optional[dict] = None) -> str:
        """返回签到的html网页"""
        dic = self._get_more_data() if dic is None else dic
        running_time = self.now_time()
        if not dic:
            content = f"""
            <li>签到失败</li>
            <li><br></li>
            <li>运行时间: <span>{running_time}</span></li>
            """.replace('\t', '')
        else:
            content = f'''\
            <li>欢迎: <span>{dic.get('name')}</span></li>
            <li><br></li>
            <li>连续签到天数: <span>{dic.get('continue')}</span></li>
            <li>签到等级: <span>{dic.get('class')}</span></li>
            <li>积分奖励: <span>{dic.get('award')}</span></li>
            <li>签到总天数: <span>{dic.get('all_day')}</span></li>
            <li>签到排名: <span>{dic.get('num')}</span></li>
            <li><br></li>
            <li>签到时间: <span>{running_time}</span></li>
            '''.replace('\t', '')
        _dic = {
            'content': content,
            'title': '自动签到成功' if dic else '自动签到失败'
        }
        return self.html.format(**_dic)


if __name__ == '__main__':
    parse = ParseMtClass()  # pragma: no cover
    # print(parse.get_more_data())
    print(parse.read_to_html())  # pragma: no cover
