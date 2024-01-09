def get_html(url, requests=None):
    try:
        r = requests.get(url)             # 使用get来获取网页数据
        r.raise_for_status()              # 如果返回参数不为200，抛出异常
        r.encoding = r.apparent_encoding  # 获取网页编码方式
        return r.text                     # 返回获取的内容
    except:
        return '错误'
def main():
    url = 'https://www.bilibili.com/v/popular/rank/bangumi'    # 网址
    html = get_html(url)                                       # 获取返回值
    print(html)                                              # 打印
if __name__ == '__main__':                        #入口
    main()
