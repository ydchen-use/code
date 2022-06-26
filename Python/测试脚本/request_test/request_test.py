import re
import requests

from bs4 import BeautifulSoup

r = requests.get("https://www.baidu.com")
data = r.text
r_code = r.status_code
print(r_code)

# 利用BeautifulSoup获取所有链接
soup = BeautifulSoup(data, "lxml")
link_list = []
for a in soup.find_all("a"):
    link_list.append(a["href"])

# 利用正则获取所有链接
# link_list = re.findall(r"href\=\"(http\:\/\/[a-zA-Z0-9\.\/]+)\"", data)

print(link_list)
for url in link_list:
    url = [url]
    length = len(url)
    url_success = []
    url_failed = []
    for i in range(0, length):
        try:
            response = requests.get(url[i].strip(), verify=False, allow_redirects=True, timeout=5)
            if response.status_code != 200:
                raise requests.RequestException(u"Status code error : {}".format(response.status_code))  # 引出请求时出现歧义异常
        except requests.RequestException as e:
            url_failed.append(url[i])
            result_failed_len = len(url_failed)
            for j in range(0, result_failed_len):
                print("URL --> %s" % url_failed[j].strip() + " --> 死链接")
            continue
        url_success.append(url[i])

    url_success_len = len(url_success)
    for j in range(0, url_success_len):
        print("URL --> %s" % url_success[j].strip() + " --> 活链接")
