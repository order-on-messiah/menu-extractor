import os
import io
from bs4 import BeautifulSoup
import requests
import pandas as pd
from flask import Flask, request
from flask import send_file
app = Flask(__name__)

@app.route('/download')
def downloadFile ():
    restaurant_url = request.args.get('restaurant_url')
    file_name = get_menu(restaurant_url)
    path = os.getcwd() + "/" + file_name
    return_data = io.BytesIO()
    with open(path, 'rb') as fo:
        return_data.write(fo.read())
    return_data.seek(0)
    os.remove(path)
    return send_file(return_data, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     attachment_filename=file_name)


def get_menu (restaurant_url):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    restaurant_name = '_'.join(restaurant_url.split('/')[-2:])
    restaurant_name = restaurant_name[:30]
    response=requests.get(restaurant_url,headers=headers)

    soup=BeautifulSoup(response.content,'lxml')
    link = soup.select_one('.sc-1s0saks-15')
    next_md_headlines = link.find_all_next("h4", {"class": "sc-1s0saks-15"})
    food_len = len(next_md_headlines) + 1
    #print(soup.select('[data-lid]'))
    i=0
    ls_dict = []
    for item in soup.select('.sc-fEUNkw'):
        for food in range(food_len):
            print(i)
            print(item)
            data = {}
            data = {'sr_no': str(i + 1), 'food': item.select('.sc-1s0saks-15')[i].get_text().strip(),'price': item.select('.sc-17hyc2s-1')[i].get_text().strip(), 'description': item.select('.sc-1s0saks-12')[i].get_text().strip()}
            i = i + 1
            ls_dict.append(data)
        
    df = pd.DataFrame(ls_dict)
    file_name = restaurant_name + '.xlsx'
    writer = pd.ExcelWriter(restaurant_name + '.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name=restaurant_name, index=False)
    writer.close()
    return file_name


@app.route('/hello')
def hello ():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(port=8666,debug=True) 