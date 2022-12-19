import requests

from bs4 import BeautifulSoup


class Scraping():
    
    def __init__(self):
        self.date = [] # 株価取得に使用する日時

    # wordを元に、企業コードと企業名を取得
    def search(self, word):
        word = word

        # 検索結果ページを取得
        try:
            # 検索ワード次第で、個別企業ページに行くか、候補リストページに行くかに別れる
            search_page = requests.get(f'https://minkabu.jp/stock/find?tag={word}')
            bs_search_page = BeautifulSoup(search_page.text, "html.parser")

            # 企業コードと企業名を取得
            num = bs_search_page.find('table', class_='md_table').find_all(
                'div', class_='md_sub')
            company = bs_search_page.find(
                'table', class_='md_table').find_all('div', class_='fwb')

            dic = {}
            for (n, c) in (zip(num, company)):
                dic[n.text.strip('\n ')] = c.text.strip('\n ')

            if len(dic) == 0:
                # 企業コードを取得してリターンする
                company_page = requests.get(
                    f'https://minkabu.jp/stock/find?tag={word}')
                bs_company_page = BeautifulSoup(company_page.text, "html.parser")

                title = bs_company_page.find('title').text
                ls = title.split(' ')

                name = None
                for i, x in enumerate(ls):
                    if i == 0:
                        name = x

                    if i == 1:
                        x = x.strip('()')
                        company_code = x
                        dic[company_code] = name
                        break
            return dic

        except Exception as e:
            err = 'error'
            print(e)
            return err


    # 業績ページでインスタンス化
    def bsInstance(self, company_code):
        performance_page = requests.get(
            f'https://minkabu.jp/stock/{company_code}/settlement')
        bs_performance_page = BeautifulSoup(performance_page.text, "html.parser")

        return bs_performance_page


    # テーブルのカラム名を取得
    def getThead(self, table):
        t_head = table.find('thead').text.strip('\n')
        t_head = t_head.split('\n')
        
        return t_head


    # 決算や財務の内容を取得
    def getTbody(self, table):
        t_body = table.find('tbody').text
        t_body = t_body.split('\n')
        
        return t_body
    
    
    # 余分な空文字を削除する
    def delEmpty(self, ls):
        ls_new = []
        
        for word in ls:
            if word == '':
                continue
            ls_new.append(word)
            
        return ls_new
    
    
    # t_bodyを二次元リストに変換
    def createList(self, t_body):
        new_t_body = []
        row_len = int(len(t_body) / 4)
        
        for i in range(1, len(t_body) + 1):
            if i % row_len == 0:
                new_t_body.append(t_body[i-row_len: i])
        
        return new_t_body
    
    
    # 各テーブルからデータを取得
    def getData(self, table):
        t_head = self.getThead(table)
        t_body = self.getTbody(table)
        t_body = self.delEmpty(t_body)
        t_body = self.createList(t_body)
        
        return t_head, t_body
    

    # 決算情報のテーブルからデータを取得
    def getSettlement(self, bs_performance_page): 
        table = bs_performance_page.find('table', class_='data_table md_table is_fix')
        table_data = self.getData(table)
                                    
        for item in table_data[1]:
            date = item[0]
            
            if len(date) == 20:
                year = date[9:13]
                month = date[14:16]
                day = date[17:19]
            else:
                year = date[10:14]
                month = date[15:17]
                day = date[18:20]
                
            self.date.append(year + month + day) 
        
        return table_data


    # 財務情報のテーブルからデータを取得
    def getFinance(self, bs_performance_page):
        table = bs_performance_page.find('table', class_='data_table md_table')
        table_data = self.getData(table)

        return table_data


    # 収益性のテーブルからデータを取得
    def getProfitability(self, bs_performance_page):
        table = bs_performance_page.find('div', class_='ly_col ly_colsize_6')
        table_data = self.getData(table)

        return table_data
