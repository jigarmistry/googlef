import os
import json
import calendar
from datetime import datetime

from gfdata import get_finance_data_phantom, get_finance_data_requests, get_news_data

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))


def calculate_day_range(last, high, low):
    try:
        if float(last) >= 0.995 * float(high):
            return "HIGH", 1
        else:
            if float(last) <= 1.005 * float(low):
                return "LOW", 2
            else:
                return "", 3
    except Exception as e:
        return "", 3


def format_date_time(timestamp):
    date_time = datetime.fromtimestamp(int(timestamp))
    nmonth = calendar.month_abbr[date_time.month]
    nday = date_time.day
    curr_date = datetime.now()
    diff = curr_date - date_time
    ndate = ""
    ntime = ""
    if diff.days < 2:
        ndate = str(nday) + "-" + str(nmonth)
        ntime = str(format(date_time.hour, '02d')) + ":" + \
            str(format(date_time.minute, '02d'))
    return ndate, ntime


def get_finance_data(pid):
    nav_filter_list, pos_filter_list = get_finance_data_phantom(pid)

    with open(os.path.join(__location__, 'data.json'), 'r') as data_file:
        json_data = json.load(data_file)

    dict_nav = {}
    dict_pos = {}

    for i, n in enumerate(nav_filter_list):
        dict_nav[n[1]] = i + 1
        try:
            json_news = get_news_data(n[1])
            if json_news != []:
                ndate, ntime = format_date_time(json_news[0]["tt"])
                if ndate != "":
                    n.append({"title": json_news[0][
                             "t"], "date": ndate, "time": ntime, "link": json_news[0]["u"]})
                else:
                    n.append({"title": "", "date": "", "time": "", "link": ""})
            else:
                n.append({"title": "", "date": "", "time": "", "link": ""})
            if n[1] in json_data["nav"].keys() and json_data["nav"][n[1]] > i + 1:
                n.append("YES")
            else:
                n.append("NO")
        except Exception as e:
            n.append({"title": "", "date": "", "time": "", "link": ""})
            n.append("NO")

    for i, p in enumerate(pos_filter_list):
        dict_pos[p[1]] = i + 1
        try:
            json_news = get_news_data(p[1])
            if json_news != []:
                ndate, ntime = format_date_time(json_news[0]["tt"])
                if ndate != "":
                    p.append({"title": json_news[0][
                             "t"], "date": ndate, "time": ntime, "link": json_news[0]["u"]})
                else:
                    p.append({"title": "", "date": "", "time": "", "link": ""})
            else:
                p.append({"title": "", "date": "", "time": "", "link": ""})
            if p[1] in json_data["pos"].keys() and json_data["pos"][p[1]] > i + 1:
                p.append("YES")
            else:
                p.append("NO")
        except Exception as e:
            p.append({"title": "", "date": "", "time": "", "link": ""})
            p.append("NO")

    dict_data = {"nav": dict_nav, "pos": dict_pos}
    with open(os.path.join(__location__, 'data.json'), 'w') as jsonfile:
        json.dump(dict_data, jsonfile)

    return nav_filter_list, pos_filter_list


def format_api_response(item_list):
    ret_list = []
    for nl in item_list:
        item = {}
        item["symbol"] = nl[1]
        item["last_price"] = nl[2]
        item["change"] = nl[3]
        item["open"] = nl[6]
        item["net_change"] = str(nl[10]) + "%"
        item["high"] = nl[7]
        item["low"] = nl[8]
        value, st = calculate_day_range(nl[2], nl[7], nl[8])
        item["day_range"] = {"value": value, "st": st}
        item["news"] = nl[11]
        item["is_rank"] = nl[12]
        ret_list.append(item)
    return ret_list


def generate_api_response(pid):
    nav_list, pos_list = get_finance_data(pid)
    json_response = {}
    json_response["nav"] = format_api_response(nav_list)
    json_response["pos"] = format_api_response(pos_list)

    return json_response


def generate_report(nav_list, pos_list):
    """['Name', 'Symbol', 'Last price', 'Change', 'Mkt cap', 'Volume', 'Open', 'High', 'Low', "Day's gain"]"""

    strHtml = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8" /><title>Report</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
        <style>td {height:8px;text-align: center;}
        th{text-align: center;} tbody { height: 80px;width:100%;} </style> </head><body style="margin-left:20px;">"""

    strPosTableHtml = """<table border="1"><caption class="text-center">Positive Values</caption><thead><tr>
    <th> Symbol </th><th> Last Price </th><th> Change </th><th> Open </th>
    <th> % Net Change </th><th> High </th><th> Low </th><th> Day's Range </th>
    <th> News </th></tr></thead><tbody>"""

    for prow in pos_list:
        if prow[11] == "YES":
            strProw = """<tr style="background-color:#ede980">"""
        else:
            strProw = """<tr>"""
        strProw = strProw + "<td style='color:#1893f2'>" + prow[1] + "</td><td>" + prow[
            2] + "</td><td style='color:#3fc151'>" + prow[3] + "</td><td>" + prow[6] + "</td>"
        strProw = strProw + "<td>" + \
            format(((float(prow[2]) - float(prow[6])) /
                    float(prow[6])) * 100, '.2f') + "%</td>"
        strProw = strProw + "<td>" + prow[7] + "</td><td>" + prow[8] + "</td>"
        value, st = calculate_day_range(prow[2], prow[7], prow[8])
        if st == 1:
            strProw = strProw + "<td style='background-color:#99e5a2;color:green'>" + value + "</td>"
        elif st == 2:
            strProw = strProw + "<td style='background-color:#ef8b8b;color:red'>" + value + "</td>"
        else:
            strProw = strProw + "<td></td>"
        strProw = strProw + "<td style='text-align:left;'>" + \
            prow[10] + "</td>"
        strProw = strProw + "</tr>"
        strPosTableHtml = strPosTableHtml + strProw
    strPosTableHtml = strPosTableHtml + "</tbody></table>"
    strHtml = strHtml + strPosTableHtml

    strNavTableHtml = """<table border="1"><caption class="text-center">Nagative Values</caption><thead><tr>
    <th> Symbol </th><th> Last Price </th><th> Change </th><th> Open </th>
    <th> % Net Change </th><th> High </th><th> Low </th><th> Day's Range </th>
    <th> News </th></tr></thead><tbody>"""

    for nrow in nav_list:
        if nrow[11] == "YES":
            strNrow = """<tr style="background-color:#ede980">"""
        else:
            strNrow = """<tr>"""
        strNrow = strNrow + "<td style='color:#1893f2'>" + nrow[1] + "</td><td>" + nrow[
            2] + "</td><td style='color:#ed5353'>" + nrow[3] + "</td><td>" + nrow[6] + "</td>"
        strNrow = strNrow + "<td>" + \
            format(((float(nrow[2]) - float(nrow[6])) /
                    float(nrow[6])) * 100, '.2f') + "%</td>"
        strNrow = strNrow + "<td>" + nrow[7] + "</td><td>" + nrow[8] + "</td>"
        value, st = calculate_day_range(nrow[2], nrow[7], nrow[8])
        if st == 1:
            strNrow = strNrow + "<td style='background-color:#99e5a2;color:green'>" + value + "</td>"
        elif st == 2:
            strNrow = strNrow + "<td style='background-color:#ef8b8b;color:red'>" + value + "</td>"
        else:
            strNrow = strNrow + "<td></td>"
        strNrow = strNrow + "<td style='text-align:left;'>" + \
            nrow[10] + "</td>"
        strNrow = strNrow + "</tr>"
        strNavTableHtml = strNavTableHtml + strNrow
    strNavTableHtml = strNavTableHtml + "</tbody></table><br>"
    strHtml = strHtml + strNavTableHtml

    strHtml = strHtml + "</body></html>"
    html_file = open(os.path.join(__location__, 'report.html'), 'w')
    html_file.write(str(strHtml))


if __name__ == "__main__":
    nav_list, pos_list = get_finance_data()
    generate_report(nav_list, pos_list)
