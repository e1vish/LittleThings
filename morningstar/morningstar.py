from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from requests import request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
}


def get_morningstar_index():
    response = request('GET', 'http://cn.morningstar.com/index/default.aspx', headers=header)
    response.encoding = 'UTF-8'
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    table = soup.table
    table_trs = table.find_all("tr")
    table_ths = table.find_all('th')
    data_columns = []
    for table_th in table_ths:
        data_columns.append(table_th.get_text())
    table_data = []
    for table_tr in table_trs:
        table_tds = table_tr.find_all('td')
        if table_tds:
            table_text = []
            for table_td in table_tds:
                table_text.append(table_td.get_text().replace(',', ''))
            table_data.append(table_text)
    db_data_columns=['region', 'category', 'name', 'close', 'change', 'percent', 'date']
    morningstar_index = pd.DataFrame(data=table_data, columns=data_columns)
    db_morningstar_index = pd.DataFrame(data=table_data, columns=db_data_columns)
    engine = create_engine("postgresql+psycopg2://username:password@127.0.0.1/morningstar")
    db = scoped_session(sessionmaker(bind=engine))
    for index, row in db_morningstar_index.iterrows():
        db_date = db.execute("SELECT date from morningstar_index WHERE name = :name ORDER BY date DESC",
                   {"name": row['name']}).fetchone()
        db_morningstar_index_date = datetime.date(datetime.strptime(row['date'], "%Y-%m-%d"))
        if (db_date is None) or (db_morningstar_index_date != db_date[0]):
            db.execute("INSERT INTO morningstar_index (region, category, name, close, change, percent, date) "
                       "VALUES (:region, :category, :name, :close, :change, :percent, :date)",
                       {"region": row['region'], "category": row['category'], "name": row['name'],
                        "close": row['close'], "change": row['change'], "percent": row['percent'],
                    "date": row['date']})
            print(f"Added {row['name']}, date: {row['date']}.")
    db.commit()
    # output morningstar index to csv file.
    # if you want to do this, remove comment below.
    # csv_name = "morningstar_index_" + datetime.now().strftime("%Y-%m-%d") + ".csv"
    # morningstar_index.to_csv(csv_name)
    return


def main():
    get_morningstar_index()


if __name__ == '__main__':
    main()
