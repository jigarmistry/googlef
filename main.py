import os
import json

from gfdata import get_finance_data_phantom, get_finance_data_requests, get_news_data

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def calculate_day_range(last, high, low):
    if float(last) >= 0.995*float(high):
        return "HIGH",1
    else:
        if float(last) <= 1.005*float(low):
            return "LOW",2
        else:
            return "",3


def get_finance_data():
    nav_filter_list, pos_filter_list = get_finance_data_phantom()

    with open(os.path.join(__location__, 'data.json'), 'r') as data_file:
        json_data = json.load(data_file)

    dict_nav = {}
    dict_pos = {}

    for i, n in enumerate(nav_filter_list):
        dict_nav[n[1]] = i + 1
        try:
            json_news = get_news_data(n[1])
            if json_news != []:
                n.append(json_news[0]["t"])
            else:
                n.append("")
            if n[1] in json_data["nav"].keys() and json_data["nav"][n[1]] > i + 1:
                n.append("YES")
            else:
                n.append("NO")
        except e:
            n.append("")
            n.append("NO")

    for i, p in enumerate(pos_filter_list):
        dict_pos[p[1]] = i + 1
        try:
            json_news = get_news_data(p[1])
            if json_news != []:
                p.append(json_news[0]["t"])
            else:
                p.append("")
            if p[1] in json_data["pos"].keys() and json_data["pos"][p[1]] > i + 1:
                p.append("YES")
            else:
                p.append("NO")
        except e:
            p.append("")
            p.append("NO")

    dict_data = {"nav":dict_nav, "pos":dict_pos}
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
        item["net_change"] = format(((float(nl[2])-float(nl[6]))/float(nl[6]))*100, '.2f')
        item["high"] = nl[7]
        item["low"] = nl[8]
        value,st = calculate_day_range(nl[2], nl[7], nl[8])
        item["day_range"] = {"value":value, "st":st}
        item["news"] = nl[10]
        item["is_rank"] = nl[11]
        ret_list.append(item)
    return ret_list


def generate_api_response():
    # nav_list, pos_list = get_finance_data()
    nav_list = [['Direxion Shares...', 'ERY', '10.10', '-15.27', '78.99M', '', '10.72', '10.72', '9.775', '-1.82', 'Direxion Shares Exchange Traded Fund Trust (JNUG): The Potential &#39;Gold Trigger ...', 'NO'], ['American Eagle Outfitter...', 'AEO', '16.56', '-12.43', '3.09B', '', '16.87', '16.98', '16.05', '-2.35', 'American Eagle Outfitters appoints Bob Madore as EVP, Chief Financial Officer', 'NO'], ['Direxion Daily S&P...', 'LABU', '37.96', '-8.57', '235.42M', '', '42.22', '42.22', '37.83', '-3.56', 'Direxion Daily S&amp;P Biotech Bull 3X Shares', 'NO'], ['Valeant Pharmaceuticals...', 'VRX', '15.79', '-7.98', '5.30B', '', '17.02', '17.08', '15.25', '-1.37', 'Live Stock Coverage: Valeant Pharmaceuticals Intl Inc Stock Is At 52-Week Low Now', 'NO'], ['Integrated Device Tech...', 'IDTI', '23.40', '-6.70', '3.11B', '', '25.08', '25.08', '23.39', '-1.68', 'Price Change to Note: Is Integrated Device Technology Inc&#39;s Fuel Running Low ...', 'NO'], ['Sarepta Therapeutics Inc', 'SRPT', '34.26', '-6.70', '1.89B', '', '36.75', '36.9397', '34.08', '-2.46', 'Price Action Alert: Could Sarepta Therapeutics Inc Gain Strenght? The Stock ...', 'NO'], ['bluebird bio Inc', 'BLUE', '60.35', '-6.29', '2.39B', '', '64.5', '67.05', '60.3', '-4.05', 'Notable Reporting: Today bluebird bio Inc Stock Crashes', 'NO'], ['Horizon Pharma PLC', 'HZNP', '19.81', '-5.89', '3.19B', '', '21.3', '21.32', '19.3', '-1.24', 'A New Kind of Stock Chart: Horizon Pharma plc (NASDAQ:HZNP) Critical Pivot Points', 'NO'], ['Ionis Pharmaceuticals...', 'IONS', '43.76', '-5.42', '5.36B', '', '45.78', '46.27', '43.49', '-2.51', 'Price Change to Note: A Reversal for Ionis Pharmaceuticals Inc Is Not Near ...', 'NO'], ['BofI Holding, Inc.', 'BOFI', '23.63', '-5.40', '1.51B', '', '25.45', '25.49', '23.55', '-1.35', 'Live Price Coverage: BofI Holding, Inc. Just Recorded A Sigfniciant Decline', 'NO'], ['Juno Therapeutics Inc', 'JUNO', '20.05', '-5.11', '2.03B', '', '21.1', '21.12', '20', '-1.08', 'Price Action to Note: What&#39;s in Juno Therapeutics Inc After Today&#39;s ...', 'NO'], ['Quintiles IMS Holdings...', 'Q', '76.83', '-5.05', '19.18B', '', '81.18', '81.18', '76.5', '-4.09', 'Noteworthy Price Action: A Reversal for Quintiles IMS Holdings Inc Is Not Near ...', 'NO'], ['PBF Energy Inc', 'PBF', '23.99', '-4.84', '2.49B', '', '25.35', '25.965', '23.46', '-1.22', 'PBF Energy Inc. (PBF) Upgrade to Hold by The Zacks Investment Research', 'NO'], ['Vertex Pharmaceuticals...', 'VRTX', '81.60', '-4.73', '19.95B', '', '85.86', '86.91', '81.59', '-4.05', 'BMO Reiterates Vertex Pharmaceuticals Incorporated (VRTX) at Market Perform On ...', 'NO'], ['Select Medical Hldgs...', 'SEM', '12.15', '-4.71', '1.61B', '', '12.8', '12.8', '12.075', '-0.60', 'Notable Price Action: What&#39;s Select Medical Holdings Corporation Downside ...', 'NO']]

    pos_list = [['California Resources...', 'CRC', '17.40', '44.40', '662.22M', '', '15.59', '17.56', '13.8201', '+5.35', 'Stock Mover of The Day: What&#39;s Propelling California Resources Corp to ...', 'NO'], ['Oasis Petroleum Inc.', 'OAS', '14.97', '27.73', '3.48B', '', '13.59', '15.02', '13.47', '+3.25', 'Market Runner: Could Oasis Petroleum Inc. Lose its Strength? The Stock Reaches ...', 'NO'], ['WPX Energy Inc', 'WPX', '15.54', '27.59', '5.11B', '', '13.71', '15.63', '13.71', '+3.36', 'Notable Price Action: WPX Energy Inc Sets 52-Week High; Strong Momentum for ...', 'NO'], ['SM Energy Co', 'SM', '39.86', '24.91', '3.34B', '', '37.25', '40.02', '36.8', '+7.95', 'Strategy To YieldBoost SM From 0.3% To 13.5% Using Options', 'NO'], ['Continental Resources...', 'CLR', '58.01', '22.88', '20.80B', '', '52.37', '58.859', '52.37', '+10.80', 'Noteworthy Analyst Evaluations of Stocks: Freeport-McMoRan Inc. (NYSE:FCX ...', 'NO'], ['Nabors Industries Ltd.', 'NBR', '16.10', '22.25', '4.45B', '', '14.21', '16.5', '14.21', '+2.93', 'Here&#39;s Why Nabors Industries Ltd., Patterson-UTI Energy, Inc., and Precision ...', 'NO'], ['Callon Petroleum Company', 'CPE', '17.64', '22.08', '2.72B', '', '16.61', '17.975', '16.28', '+3.19', 'Callon Petroleum Company Risk Points versus Energy', 'NO'], ['Marathon Oil Corporation', 'MRO', '18.06', '20.80', '14.72B', '', '16.38', '18.55', '16.38', '+3.11', 'Budget 2016: Mr Jaitley, when the weak state offers asylum to black money ...', 'NO'], ['Carrizo Oil & Gas Inc', 'CRZO', '42.35', '20.42', '2.68B', '', '39.23', '42.435', '38.03', '+7.18', 'Stock of The Day: What&#39;s Propelling Carrizo Oil &amp; Gas Inc to Increase So Much?', 'NO'], ['Superior Energy...', 'SPN', '17.24', '18.65', '2.52B', '', '15.74', '17.36', '15.66', '+2.71', 'Stock On Watch: What Will Happen to Superior Energy Services, Inc. Next? The ...', 'NO'], ['Matador Resources Co', 'MTDR', '26.64', '17.46', '2.38B', '', '24.62', '27.3', '24.62', '+3.96', 'Stock Mover of the Day: Matador Resources Co on Focus After Raising In Today&#39;s ...', 'NO'], ['Transocean LTD', 'RIG', '12.90', '17.06', '4.56B', '', '11.82', '13.2752', '11.82', '+1.88', 'Price Action Don&#39;t Lie: Could Transocean LTD Lose Strenght? The Stock ...', 'NO'], ['Energen Corporation', 'EGN', '62.07', '16.45', '5.83B', '', '60.17', '62.22', '57.58', '+8.77', 'Notable Price Action: Energen Corporation Increases Again; Strong Momentum for ...', 'NO'], ['Patterson-UTI Energy...', 'PTEN', '26.67', '16.16', '3.83B', '', '24.64', '27.34', '24.415', '+3.71', 'Here&#39;s Why Nabors Industries Ltd., Patterson-UTI Energy, Inc., and Precision ...', 'NO'], ['Laredo Petroleum Inc', 'LPI', '15.99', '15.95', '3.81B', '', '15.28', '16.33', '15.14', '+2.20', 'Today&#39;s Stock Alert: After Today&#39;s Big Increase, Is Laredo Petroleum Inc&#39;s ...', 'NO']]

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
        strProw = strProw + "<td style='color:#1893f2'>"+prow[1]+"</td><td>"+prow[2]+"</td><td style='color:#3fc151'>"+prow[3]+"</td><td>"+prow[6]+"</td>"
        strProw = strProw + "<td>"+format(((float(prow[2])-float(prow[6]))/float(prow[6]))*100, '.2f')+"%</td>"
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
    <th> Symbol </th><th> Last Price </th><th> Change </th><th> Open </th>
    <th> % Net Change </th><th> High </th><th> Low </th><th> Day's Range </th>
    <th> News </th></tr></thead><tbody>"""

    for nrow in nav_list:
        if nrow[11] == "YES":
            strNrow = """<tr style="background-color:#ede980">"""
        else:
            strNrow = """<tr>"""
        strNrow = strNrow + "<td style='color:#1893f2'>"+nrow[1]+"</td><td>"+nrow[2]+"</td><td style='color:#ed5353'>"+nrow[3]+"</td><td>"+nrow[6]+"</td>"
        strNrow = strNrow + "<td>"+format(((float(nrow[2])-float(nrow[6]))/float(nrow[6]))*100, '.2f')+"%</td>"
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
    strNavTableHtml = strNavTableHtml + "</tbody></table><br>"
    strHtml = strHtml + strNavTableHtml

    strHtml = strHtml + "</body></html>"
    html_file = open(os.path.join(__location__, 'report.html'),'w')
    html_file.write(str(strHtml))


if __name__ == "__main__":
    nav_list, pos_list = get_finance_data()
    generate_report(nav_list, pos_list)
