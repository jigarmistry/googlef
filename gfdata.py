import csv
import time
import json
import demjson
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from operator import itemgetter


browser = webdriver.PhantomJS("/usr/local/lib/phantomjs/bin/phantomjs", service_args=[
                              '--ssl-protocol=any', '--ignore-ssl-errors=true', '--load-images=no'])

browser.set_window_size(1600, 900)

url_login = "https://accounts.google.com/ServiceLogin?service=finance"
url_auth = "https://accounts.google.com/ServiceLoginAuth"
url_finance_data = "https://www.google.com/finance/portfolio?pid=3&output=csv&action=view&pview=sview&ei=FUQ9WIjWGoavuATfq5LQAw&authuser=0"
google_username = "parasdoshipu@gmail.com"
google_password = "algoforme12"


class SessionGoogle:

    def __init__(self, url_login, url_auth, login, pwd):
        self.ses = requests.session()
        login_html = self.ses.get(url_login)
        soup_login = BeautifulSoup(login_html.content, "lxml").find(
            'form').find_all('input')
        my_dict = {}
        for u in soup_login:
            if u.has_attr('value'):
                my_dict[u['name']] = u['value']
        my_dict['Email'] = login
        my_dict['Passwd'] = pwd
        self.ses.post(url_auth, data=my_dict)

    def get(self, URL):
        return self.ses.get(URL, stream=True, timeout=None).text


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def get_news_data(symbol):
    news_url = 'http://www.google.com/finance/company_news?output=json&q=' + \
        symbol + '&start=0&num=1'
    r = requests.get(news_url)
    article_json = []
    if r.status_code == 200:
        content_json = demjson.decode(json.loads(json.dumps(r.text)))
        if content_json['clusters']:
            news_json = content_json['clusters']
            for cluster in news_json:
                for article in cluster:
                    if article == 'a':
                        article_json.extend(cluster[article])
    return article_json


def get_browser(pid):
    global browser
    browser.get(url_login)
    try:
        passwordElem = browser.find_element_by_id('Passwd')
        passwordElem.send_keys(google_password)
        signinButton = browser.find_element_by_id('signIn')
        signinButton.click()
    except Exception as e:
        emailElem = browser.find_element_by_id('Email')
        emailElem.send_keys(google_username)
        nextButton = browser.find_element_by_id('next')
        nextButton.click()
        time.sleep(2)
        passwordElem = browser.find_element_by_id('Passwd')
        passwordElem.send_keys(google_password)
        signinButton = browser.find_element_by_id('signIn')
        signinButton.click()

        # Only Needed for first time
        # btns =  browser.find_elements_by_xpath("//*[@type='submit']")
        # btns[0].click()
        # remailElem = browser.find_element_by_name('email')
        # remailElem.send_keys("stockforindia@gmail.com")
        # rsigninButton = browser.find_element_by_id('submit')
        # rsigninButton.click()
        # print browser.page_source

    purl = 'https://www.google.com/finance/portfolio?action=view&pid=' + \
        pid + '&authuser=2&ei=sAg8WLn-MYviugSQ_4WQBA?pview=sview'
    browser.get(purl)


def get_finance_fund_data_phantom():
    global browser
    link = browser.find_element_by_link_text('Fundamentals')
    link.click()
    html_data = browser.find_element_by_class_name(
        "gf-table").get_attribute('innerHTML')
    table_data = [[cell.text for cell in row(
        "td")] for row in BeautifulSoup(html_data, "lxml")("tr")]
    fdata = {}
    for row in table_data:
        if len(row) == 11:
            fdata[row[2]] = {"avg_vol": row[5],
                             "52wkhigh": row[6], "52wklow": row[7]}
    return fdata


def format_data_per_change(fdata):
    cfdata = []
    for d in fdata:
        e = d[3]
        if e[0] != "-":
            try:
                d.append(format(((float(d[2].replace(
                    ',', '')) - float(d[8].replace(',', ''))) / float(d[8].replace(',', ''))) * 100, '.2f'))
            except Exception as e:
                d.append('0')
        elif e[0] == "-":
            try:
                d.append(format(((float(d[2].replace(
                    ',', '')) - float(d[7].replace(',', ''))) / float(d[7].replace(',', ''))) * 100, '.2f'))
            except Exception as e:
                d.append('0')
        else:
            d.append('0')
        cfdata.append(d)
    return cfdata


def get_finance_data_phantom(pid):
    global browser
    get_browser(pid)
    link = browser.find_element_by_link_text('Overview')
    link.click()

    html_data = browser.find_element_by_class_name(
        "gf-table").get_attribute('innerHTML')
    table_data = [[cell.text for cell in row(
        "td")] for row in BeautifulSoup(html_data, "html.parser")("tr")]

    fdata = []
    for row in table_data:
        if len(row) == 11 and row[4].strip() != "":
            i_list = []
            for i, v in enumerate(row):
                if i == 0:
                    continue
                if i == 4:
                    v = find_between(row[4], "(", "%")
                i_list.append(v)
            fdata.append(i_list)

    cfdata = format_data_per_change(fdata)

    cfdata.sort(key=lambda row: float(row[10]))
    nav_filter_list = cfdata[0:15]
    temp = cfdata[-15:]
    pos_filter_list = temp[::-1]

    # dict_fund_data = get_finance_fund_data_phantom()

    return nav_filter_list, pos_filter_list


def get_finance_data_requests():
    session = SessionGoogle(url_login, url_auth,
                            google_username, google_password)
    download_data = session.get(url_finance_data)
    csv_data = list(csv.reader(download_data.splitlines(), delimiter=','))
    filter_list = [row for row in csv_data[
        1:] if row[0] != "" and row[9] != ""]
    filter_list.sort(key=lambda row: float(row[9]))
    nav_filter_list = filter_list[0:15]
    pos_filter_list = sorted(
        filter_list[-15:], key=itemgetter(9), reverse=True)

    return nav_filter_list, pos_filter_list
