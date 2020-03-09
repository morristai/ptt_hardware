# -*- coding: utf-8 -*
import requests
import re
from bs4 import BeautifulSoup

proxies = {
    "http": "http://proxy-chain.intel.com:912",
    "https": "http://proxy-chain.intel.com:912",
}
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
    "sec-fetch-user": "?1",
    "dnt": "1",
    # Can't place "br", otherwise need to install other decoder
    "accept-encoding": "gzip, deflate",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "cookie": "__cfduid=d5bf85bc78cd75c30beabfc2c14e52e5f1567955601; _ga=GA1.2.410818996.1567955602; _gid=GA1.2.1223439128.1582700194; _gat=1",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "upgrade-insecure-requests": "1",
}


class Hardware:
    def __int__(self):
        pass

    def get_data(self, url=None, get_first=False, proxy=False):
        if get_first:
            if proxy:
                resp = requests.get(
                    "https://www.ptt.cc/bbs/HardwareSale/index.html",
                    headers=header,
                    verify=True,
                    timeout=3,
                    proxies=proxies)
            else:
                resp = requests.get(
                    "https://www.ptt.cc/bbs/HardwareSale/index.html",
                    headers=header,
                    verify=True,
                    timeout=3)
        else:
            if proxy:
                resp = requests.get(
                    url=url,
                    headers=header,
                    verify=True,
                    timeout=3,
                    proxies=proxies)
            else:
                resp = requests.get(
                    url,
                    headers=header,
                    verify=True,
                    timeout=3)

        return resp

    def data_processing(self, resp, words, rollback, proxy=False):
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')
        latest = str(soup.find_all("a", string="‹ 上頁")[0])
        latest = int(re.search(r'\d{4}', latest).group(0))
        # TODO
        found = {}
        for i in range(0, rollback):
            next_url = f"https://www.ptt.cc/bbs/HardwareSale/index{latest-i}.html"
            result = self.get_data(url=next_url, get_first=False, proxy=proxy)
            soup = BeautifulSoup(result.text, 'html.parser')
            found.update(self.search_word(soup, words=words))
        return found

    # soup.find_all("div", {"class": "title"})
    @staticmethod
    def search_word(soup, words):
        temp = {}
        if words is None:
            words = []
        for item in soup.select('.title'):
            try:
                title = item.select_one('a').text
            except BaseException:
                continue
            for key in words:
                if bool(re.match(f".*賣.*{key}.*", title)):
                    product_url = f"https://www.ptt.cc/{item.find('a').get('href')}"
                    temp[title] = product_url
        return temp