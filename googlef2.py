import csv
import json
import demjson
import requests
from bs4 import BeautifulSoup
from operator import itemgetter

from napi import getNews

url_login = "https://accounts.google.com/ServiceLogin?service=finance"
url_auth = "https://accounts.google.com/ServiceLoginAuth"
url_finance_data = "https://www.google.com/finance/portfolio?pid=3&output=csv&action=view&pview=sview&ei=FUQ9WIjWGoavuATfq5LQAw&authuser=0"
google_username = "parasdoshipu@gmail.com"
google_password = "algoforme12"

nav_filter_list_old = []
pos_filter_list_old = []


class SessionGoogle:
    def __init__(self, url_login, url_auth, login, pwd):
        self.ses = requests.session()
        login_html = self.ses.get(url_login)
        soup_login = BeautifulSoup(login_html.content,"lxml").find('form').find_all('input')
        my_dict = {}
        for u in soup_login:
            if u.has_attr('value'):
                my_dict[u['name']] = u['value']
        my_dict['Email'] = login
        my_dict['Passwd'] = pwd
        self.ses.post(url_auth, data=my_dict)

    def get(self, URL):
        return self.ses.get(URL,stream=True,timeout=None).text


def get_news_data(symbol):
    news_url = 'http://www.google.com/finance/company_news?output=json&q=' + symbol + '&start=0&num=1'
    r = requests.get(news_url)
    content_json = demjson.decode(json.loads(json.dumps(r.text)))
    article_json = []
    news_json = content_json['clusters']
    for cluster in news_json:
        for article in cluster:
            if article == 'a':
                article_json.extend(cluster[article])
    return article_json


def get_finance_data():
    session = SessionGoogle(url_login, url_auth, google_username, google_password)
    download_data  = session.get(url_finance_data)
    csv_data = list(csv.reader(download_data.splitlines(), delimiter=','))
    header_data = csv_data[0]
    filter_list = [row for row in csv_data[1:] if row[0]!="" and row[9]!=""]
    filter_list.sort(key = lambda row: float(row[9]))
    nav_filter_list = filter_list[0:15]
    pos_filter_list = sorted(filter_list[-15:], key = itemgetter(9) ,reverse=True)

    for n in nav_filter_list:
        json_news = get_news_data(n[1])
        n.append(json_news[0]["t"])

    for p in pos_filter_list:
        json_news = get_news_data(p[1])
        p.append(json_news[0]["t"])

    return header_data, nav_filter_list, pos_filter_list


def calculate_day_range(last, high, low):
    if float(last) >= 0.995*float(high):
        return "HIGH",1
    else:
        if float(last) <= 1.005*float(low):
            return "LOW",2
        else:
            return "",3


def generate_report(header_data, nav_list, pos_list):
    """['Name', 'Symbol', 'Last price', 'Change', 'Mkt cap', 'Volume', 'Open', 'High', 'Low', "Day's gain"]"""

    strHtml = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8" /><title>Report</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
        <style>td {height:10px;text-align: center;}
        th{text-align: center;} tbody { height: 80px;width:100%;} </style> </head><body>"""

    strPosTableHtml = """<table border="1"><caption class="text-center">Positive Values</caption><thead><tr>
    <th>Symbol</th><th>Last Price</th><th>Change</th><th>Open</th>
    <th>% Net Change</th><th>High</th><th>Low</th><th>Day's Range</th><th>News</th></tr></thead><tbody>"""
    for prow in pos_list:
        strProw = """<tr>"""
        strProw = strProw + "<td style='color:#1893f2'>"+prow[1]+"</td><td>"+prow[2]+"</td><td style='color:#3fc151'>"+prow[3]+"</td><td>"+prow[6]+"</td>"
        strProw = strProw + "<td>"+format((float(prow[2])-float(prow[6]))/float(prow[6]), '.4f')+"%</td>"
        strProw = strProw + "<td>"+prow[7]+"</td><td>"+prow[8]+"</td>"
        value,st = calculate_day_range(prow[2], prow[7], prow[8])
        if st == 1:
            strProw = strProw + "<td style='background-color:#99e5a2;color:green'>"+value+"</td>"
        elif st == 2:
            strProw = strProw + "<td style='background-color:#ef8b8b;color:red'>"+value+"</td>"
        else:
            strProw = strProw + "<td></td>"
        strProw = strProw + "<td style='text-align:left;'>"+prow[10]+"</td>"
        strProw = strProw + "</tr>"
        strPosTableHtml = strPosTableHtml + strProw
    strPosTableHtml = strPosTableHtml + "</tbody></table>"
    strHtml = strHtml + strPosTableHtml

    strNavTableHtml = """<table border="1"><caption class="text-center">Nagative Values</caption><thead><tr>
    <th>Symbol</th><th>Last Price</th><th>Change</th><th>Open</th>
    <th>% Net Change</th><th>High</th><th>Low</th><th>Day's Range</th><th>News</th></tr></thead>"""
    for nrow in nav_list:
        strNrow = """<tr>"""
        strNrow = strNrow + "<td style='color:#1893f2'>"+nrow[1]+"</td><td>"+nrow[2]+"</td><td style='color:#ed5353'>"+nrow[3]+"</td><td>"+nrow[6]+"</td>"
        strNrow = strNrow + "<td>"+format((float(nrow[2])-float(nrow[6]))/float(nrow[6]), '.4f')+"%</td>"
        strNrow = strNrow + "<td>"+nrow[7]+"</td><td>"+nrow[8]+"</td>"
        value,st = calculate_day_range(nrow[2], nrow[7], nrow[8])
        if st == 1:
            strNrow = strNrow + "<td style='background-color:#99e5a2;color:green'>"+value+"</td>"
        elif st == 2:
            strNrow = strNrow + "<td style='background-color:#ef8b8b;color:red'>"+value+"</td>"
        else:
            strNrow = strNrow + "<td></td>"
        strNrow = strNrow + "<td style='text-align:left;'>"+nrow[10]+"</td>"
        strNrow = strNrow + "</tr>"
        strNavTableHtml = strNavTableHtml + strNrow
    strNavTableHtml = strNavTableHtml + "</tbody></table>"
    strHtml = strHtml + strNavTableHtml

    strHtml = strHtml + "</body></html>"
    html_file = open("report.html","w")
    html_file.write(str(strHtml))


if __name__ == "__main__":
    header_data, nav_list, pos_list = get_finance_data()
    generate_report(header_data, nav_list, pos_list)
