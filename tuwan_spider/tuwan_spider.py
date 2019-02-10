import requests
import re
from base64 import b64decode, b64encode


class Tuwan_spider:
    def __init__(self, start, end, dl_path):
        self.ids = (start, end)
        self.path = dl_path

    @staticmethod
    def url_gen(start, stop):
        step = 1 if start <= stop else -1
        url_head = 'https://api.tuwan.com/apps/Welfare/detail?id='
        for pid in range(start, stop + 1, step):
            yield url_head + str(pid), str(pid)

    @staticmethod
    def pic_size_transform(pic_url):
        # 1.切片  2.修改1,2切片 3.重新组装  3.返回新图片地址
        def b64_pic_size_transform(b64_size: str):
            # NTMwNCwxNTgsMTU4LDksMywxLC0xLE5PTkUsLCw5MA==
            # ['1e45', '158', '158', '9', '3', '1', '-1', 'NONE', '', '', '90']
            # 修改为 ['1e45', '0', '0', '9', '3', '1', '-1', 'NONE', '', '', '90']
            # b64encode返回 NTMwNCwwLDAsOSwzLDEsLTEsTk9ORSwsLDkw
            b64_decode_str: str = b64decode(b64_size).decode()
            b64_decode_list: list = b64_decode_str.split(',')
            b64_decode_list[1:3] = [0, 0]
            s = ','.join([str(i) for i in b64_decode_list])

            return b64encode(s.encode())

        pic_url_list = pic_url.split('/')
        pic_url_list[6] = b64_pic_size_transform(pic_url_list[6]).decode()
        return '/'.join(pic_url_list)

    def get_pic_url(self, url):
        pattern = re.compile('''"thumb".*"times"''')
        pst = self.pic_size_transform

        def get_response(url):
            response = requests.get(url)
            ori_match = pattern.search(response.content.decode('unicode_escape'))
            if ori_match:
                ori_match = ori_match.group()
            else:
                return
            match_list = ori_match.split(',')
            if match_list:
                for pic_url in match_list:
                    if pic_url.startswith('''"http''') and pic_url.endswith(('jpg', 'jpeg', 'png')):
                        pic_url = pic_url.replace('\\', '')
                        yield pst(pic_url)

        return get_response(url)

    def start(self):
        ug = self.url_gen(*self.ids)
        with open('tuwan_pic.txt', 'w') as f:
            for i, pid in ug:
                print(pid)
                for p in self.get_pic_url(i):
                    f.write(pid + ' ' + p + '\n')


if __name__ == '__main__':
    Tuwan_spider(1500, 1, 'qwer').start()
