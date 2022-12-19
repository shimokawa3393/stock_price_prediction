import numpy as np
from sklearn import linear_model


class Prediction():
    
    def __init__(self):
        self.score_list = []
        self.min_list = []
        self.max_list = []
    
    # 予測する
    def predict(self, df_stock_price, df_income, growth_rate):
        growth_rate = np.array(growth_rate)
        
        for column in df_income:
            x = df_income[column]
            y = df_stock_price['Avg']
                                    
            x = np.array(x)
            x = np.reshape(x, (-1, 1))
            
            model = linear_model.LinearRegression() # LinearRegressionクラスをインスタンス化
            model.fit(x, y) # fit() -- 線形回帰分析を行う
            
            # y = ax + b の a と b を求める
            # print(f'----------{column}------------')
            # print("回帰係数:", model.coef_) # x
            # print("切片    :", model.intercept_) # -y
            # print("決定係数:", model.score(x, y)) # 相関の信頼度
            
            self.score_list.append(model.score(x, y))
            
            mn = df_income[column][0] * np.min(growth_rate)
            mx = df_income[column][0] * np.max(growth_rate)
            
            mn = np.array(mn)
            mn = np.reshape(mn, (-1, 1))
            mx = np.array(mx)
            mx = np.reshape(mx, (-1, 1))
                    
            # predict = model.predict(mn)
            # print(f'predict_min:{predict}')
            
            self.min_list.append(model.predict(mn))
            
            # predict = model.predict(mx)
            # print(f'predict_max:{predict}')
            
            self.max_list.append(model.predict(mx))
    
    
    # 決定係数と予測最小値と予測最大値を取得
    def getValues(self):
        score = np.mean(self.score_list)
        mn = int(np.mean(self.min_list))
        mx = int(np.mean(self.max_list))
        if mn > mx:
            escape = mn
            mn = mx
            mx = escape
        return score, mn, mx

        
        