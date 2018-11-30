import requests
import json
from jsonpath import jsonpath
from pandas import DataFrame
from time import sleep


# 处理url
def handler_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    return response


# 获取json数据
def handler_json(response):
    json_str = response.text
    # 首先将json格式数据转化为python对象
    obj = json.loads(json_str)

    # 获取公司，职位，薪资
    company = jsonpath(obj,'$..company.name')
    job = jsonpath(obj,'$..jobName')
    salary = jsonpath(obj,'$..salary')
    # 封装起来
    total = list(zip(company,job,salary))
    return total


# 写入csv文件
def main():
    city = input("请输入城市：")
    job = input("请输入岗位：")
    page = input("请输入起始页：")
    page2 = input("请输入终止页：")
    start = 60 * (int(page) - 1)

    for i in range(int(page),int(page2)+1):
        # 这个url是json链接
        url = 'https://fe-api.zhaopin.com/c/i/sou?start={}&pageSize=60&cityId={}&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={}&kt=3&lastUrlQuery=%7B%22p%22:{},%22pageSize%22:%2260%22,%22jl%22:%22530%22,%22kw%22:%22python%22,%22kt%22:%223%22%7D'.format(start, city, job, i)
        start += 60
        response = handler_url(url)
        response = handler_url(url)
        total = handler_json(response)
        test = DataFrame(data=total)
        test.to_csv('./jobs.csv', encoding="utf_8_sig", mode="a", index=False, header=False)
        sleep(2)


if __name__ == '__main__':
    main()
