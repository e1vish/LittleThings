import json
import os
from requests import request
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

base_path = 'dicts/'
dict_base_url = {
    '城市信息': 'https://pinyin.sogou.com/dict/cate/index/360/default/%s',
    '自然科学': 'https://pinyin.sogou.com/dict/cate/index/1/default/%s',
    '社会科学': 'https://pinyin.sogou.com/dict/cate/index/76/default/%s',
    '工程应用': 'https://pinyin.sogou.com/dict/cate/index/96/default/%s',
    '农林鱼畜': 'https://pinyin.sogou.com/dict/cate/index/127/default/%s',
    '医学医药': 'https://pinyin.sogou.com/dict/cate/index/132/default/%s',
    '电子游戏': 'https://pinyin.sogou.com/dict/cate/index/436/default/%s',
    '艺术设计': 'https://pinyin.sogou.com/dict/cate/index/154/default/%s',
    '生活百科': 'https://pinyin.sogou.com/dict/cate/index/154/default/%s',
    '运动休闲': 'https://pinyin.sogou.com/dict/cate/index/367/default/%s',
    '人文科学': 'https://pinyin.sogou.com/dict/cate/index/31/default/%s',
    '娱乐休闲': 'https://pinyin.sogou.com/dict/cate/index/403/default/%s'
}
dict_category_url = {}
dict_category_dl_url = {}


def get_soup(url):
    response = request('GET', url, headers=headers)
    response.encoding = 'UTF-8'
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    return soup


def get_category_page_size(url):
    soup = get_soup(url % str(1))
    dict_page_list = soup.find_all(id="dict_page_list")
    if dict_page_list:
        dict_page_list = dict_page_list[0].find_all('li')
        if dict_page_list:
            dict_page_size = int(dict_page_list[-2].text)
        else:
            dict_page_size = 1
    return dict_page_size


def get_categories(url, parent_category_name):
    soup = get_soup(url % str(1))
    soup = [s.extract() for s in soup('table')]
    tds = soup[0].find_all('td')
    for category in tds:
        if category.a:
            category_name = category.a.get_text().split('(')[0]
            category_url = 'https://pinyin.sogou.com' + category.a['href'] + '/default/%s'
            dict_category_url[parent_category_name][category_name] = category_url
    return


def get_city_list(url, parent_category_name):
    soup = get_soup(url % str(1))
    if soup:
        citylist = soup.findAll(class_="citylist")
        if citylist:
            for city in citylist:
                if city:
                    city_name = city.get_text()
                    city_url = 'https://pinyin.sogou.com' + city['href'] + '/default/%s'
                    dict_category_url[parent_category_name][city_name] = city_url
    return


def get_dict_dl_url(url, parent_category_name, second_category_name):
    dict_page_size = get_category_page_size(url)
    for i in range(1, dict_page_size + 1):
        soup = get_soup(url % str(i))
        dict_items = soup.find_all(class_="dict_detail_block")
        for dict in dict_items:
            detail_title = dict.find_all(class_="detail_title")[0]
            dict_name = detail_title.text
            dict_name = dict_name.replace(' ', '、')
            dict_name = dict_name.replace('_', '')
            dict_name = dict_name.replace('/', '')
            dict_dl_btn = dict.find_all(class_="dict_dl_btn")[0]
            dict_dl_url = dict_dl_btn.a.attrs['href']
            dict_category_dl_url[parent_category_name][second_category_name][dict_name] = dict_dl_url


def get_dict_file(dict_url, dict_name, path):
    response = request('GET', dict_url, stream=True, headers=headers)
    with open(path + dict_name + '.scel', 'wb') as f:
        for chunk in response.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
    print(dict_name + ' download successfully.')
    return


def get_all_files():
    print('---Get All Files---')
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    for i in dict_category_dl_url:
        if not os.path.exists(base_path + i):
            os.mkdir(base_path + i)
        for j in dict_category_dl_url[i]:
            if not os.path.exists(base_path + i + '/' + j):
                os.mkdir(base_path + i + '/' + j)
            for k in dict_category_dl_url[i][j]:
                get_dict_file(dict_category_dl_url[i][j][k], k, base_path + i + '/' + j + '/')
    print('---Get All Files Done---')


def get_all_categories():
    print('---Get All Categories---')
    for i in dict_base_url:
        dict_category_url[i] = {}
        get_categories(dict_base_url[i], i)
        get_city_list(dict_base_url['城市信息'], '城市信息')
    print('---Get All Categories Done---')


def get_all_url():
    print('---Get All URL---')
    for i in dict_category_url:
        dict_category_dl_url[i] = {}
        for j in dict_category_url[i]:
            dict_category_dl_url[i][j] = {}
            get_dict_dl_url(dict_category_url[i][j], i, j)
    print('---Get All URL Done---')


def save_to_json(dict, filename):
    print('---Save to Json Files---')
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    with open(base_path + filename, 'w') as f:
        f.write(json.dumps(dict, ensure_ascii=False, indent=2))
    print('---Save to Json Files Done---')


def read_from_json(filename):
    print('---Read From Json Files---')
    if not os.path.exists(base_path + filename):
        print('---No Json Files---')
        return {}
    else:
        with open(base_path + filename, 'r') as f:
            dict_json = json.load(f)
        print('---Read From Json Files Done---')
        return dict_json


def main():
    # Get all category and dicts url, then save to json files
    get_all_categories()
    get_all_url()
    save_to_json(dict_base_url, "dict_base_url.json")
    save_to_json(dict_category_url, "dict_category_url.json")
    save_to_json(dict_category_dl_url, "dict_category_dl_url.json")

    # Read dicts from json files
    # global dict_category_dl_url
    # dict_category_dl_url = read_from_json("dict_category_dl_url.json")

    # Download all dicts files
    if dict_category_dl_url:
        get_all_files()


if __name__ == '__main__':
    main()
