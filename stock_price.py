import datetime
import pandas_datareader


class StockPrice():
    
    def __init__(self, date, company_code):
        self.date = date
        self.company_code = company_code
        self.df_stock_price = None
        self.length = 0


    # 単純平均線用
    def createSma(self, df, num):
        df[f'Sma{num}'] =df['Avg'].rolling(window=num).mean().shift(-num)
        sma_list = list(df[f'Sma{num}'].values)
        
        for i, x in enumerate(reversed(sma_list)):
            i += 1
            x = None
            sma_list[-i] = x
            
            if i == num:
                break
                
        return sma_list
        
        
    # 指定期間の株価の平均を返す
    def getStockPrice(self):        
        symbol = f'{self.company_code}.JP'
        data_source = 'stooq' # もしくは yahoo
        start = self.date[-1] # 古い日付
        end = self.date[0] # 新しい日付
        
        # 相関関係調査用
        df_stock_price = pandas_datareader.data.DataReader(symbol, data_source, start, end)   
        df_plus = df_stock_price.copy()
        df_plus['Avg'] = (df_stock_price['Open'] + df_stock_price['Close']) / 2
                
        # predict.py用
        self.df_stock_price = df_plus
        self.length = len(self.df_stock_price)
        
        # グラフ生成用
        today = datetime.datetime.now()
        four_years_ago = today- datetime.timedelta(days=365*4+1)
        start = four_years_ago.strftime("%Y%m%d")

        df_stock_price = pandas_datareader.data.DataReader(symbol, data_source, start)
        df_plus = df_stock_price.copy()
        df_plus['Avg'] = (df_stock_price['Open'] + df_stock_price['Close']) / 2

        avg_list = list(df_plus['Avg'].values)
        sma75_list = self.createSma(df_plus, 75)
        sma200_list = self.createSma(df_plus, 200)
                                                
        return avg_list, sma75_list, sma200_list
        
