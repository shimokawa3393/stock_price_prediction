import copy
import os

from flask import Flask
from flask import request, render_template

import growth_rate
import scraping
import stock_price
import shaping
import prediction


app = Flask(__name__)


new_Scraping = scraping.Scraping()

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/result", methods= ["GET"])
def result():    
    word = request.args.get('input_company')
    obj = new_Scraping.search(word) # dictか、"error"が返ってくる
    num = 0
        
    if obj != None and obj != "error":
        num = len(obj)
        
    return render_template('result.html', num = num, obj = obj)
        
    
@app.route('/prediction/<int:company_code>/<string:company_name>')
def performance(company_code, company_name):
    bs_performance_page = new_Scraping.bsInstance(company_code)
    
    # 業績データタプルを取得
    settlement = new_Scraping.getSettlement(bs_performance_page)
    settlement_t_head = list(settlement[0])
    settlement_t_body = list(settlement[1])
    settlement_len = len(settlement_t_body[0])

    settlement_copy = copy.deepcopy(settlement_t_body)
    for row in settlement_copy:
        row.pop(0)
        
    finance = new_Scraping.getFinance(bs_performance_page)
    finance_t_head = list(finance[0])
    finance_t_body = list(finance[1])
    finance_len = len(finance_t_body[0])
    
    profitability = new_Scraping.getProfitability(bs_performance_page)
    profitability_t_head = list(profitability[0])
    profitability_t_body = list(profitability[1])
    profitability_len = len(profitability_t_body[0])

    # 株価の平均リストを取得
    new_StockPrice = stock_price.StockPrice(new_Scraping.date, company_code)
    stock_price_list = new_StockPrice.getStockPrice()
    length = new_StockPrice.length

    # 成長率と整形した決算リストを取得
    new_Shaping = shaping.Shaping()
    new_GrowthRate = growth_rate.GrowthRate()
    growth_rate_list = []
    settlement_num = []

    settlement_copy = new_Shaping.replaceList(settlement_copy)

    for item in settlement_copy:
        item = new_Shaping.changeNum(item)
        settlement_num.append(new_Shaping.shapePerformance(length, item))
        result_growth_rate = new_GrowthRate.calGrowthRate(item)
        if result_growth_rate != 0:
            growth_rate_list.append(result_growth_rate)
            
    df_income = new_Shaping.createDF(settlement_num)

    new_Prediction = prediction.Prediction()
    new_Prediction.predict(new_StockPrice.df_stock_price, df_income, growth_rate_list)
    predicted_list = list(new_Prediction.getValues())
    predicted_list[0] = float('{:.3f}'.format(predicted_list[0]))
    
    return render_template('prediction.html',
                           company_code=company_code,
                           company_name=company_name,
                           settlement_t_head=settlement_t_head,
                           settlement_t_body=settlement_t_body,
                           settlement_len=settlement_len,
                           finance_t_head=finance_t_head,
                           finance_t_body=finance_t_body,
                           finance_len=finance_len,
                           profitability_t_head=profitability_t_head,
                           profitability_t_body=profitability_t_body,
                           profitability_len=profitability_len,
                           stock_price_list=stock_price_list,
                           predicted_list=predicted_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))