class GrowthRate():
    
    # 決算データの一項目ごとの成長率を算出する(年平均成長率)
    def calGrowthRate(self, item):
        try:
            cagr = (item[0] / item[-1]) ** (1 / len(item))
        except Exception:
            cagr = 0
            
        return cagr
        
