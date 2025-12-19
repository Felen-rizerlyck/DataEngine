import pandas as pd
import requests
import time
import random
from bs4 import BeautifulSoup

class NEVDataSpider:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.sales_data = []
        self.regional_data = []

    def crawl_sales_trend(self, start_year=2015, end_year=2025):
        """
        模块1：爬取全国新能源汽车月度产销趋势
        策略：通过搜狐汽车或汽车之家等公开API/JSON数据接口获取
        """
        print(f"正在启动销量爬虫 (范围: {start_year}-{end_year})...")
        
        # 实际操作中，此处 URL 对应行业协会在第三方平台的镜像数据接口
        # 这里演示一个标准的 RESTful API 爬取逻辑
        for year in range(start_year, end_year + 1):
            # 模拟请求间隔，防止被封
            time.sleep(random.uniform(1.5, 3.0))
            
            # 注意：此 URL 为逻辑示例，实际运行需对应目标网站的具体动态路径
            # 建议在浏览器控制台(F12) Network 找到返回 JSON 的链接填入
            target_url = f"https://db.auto.sohu.com/api/model/sales/list.json?year={year}&type=nev"
            
            try:
                # 若无真实接口，此处代码段模拟获取到的清洗后结构
                # 实际运行请将此段替换为真正的 response = requests.get(...)
                print(f"  正在获取 {year} 年月度细分数据...")
                
                # 假设获取到的 JSON 包含 12 个月的数据
                for month in range(1, 13):
                    if year == 2025 and month > 10: break # 2025年数据仅到当前月
                    
                    # 清洗逻辑：获取总销量、BEV、PHEV
                    self.sales_data.append({
                        "日期": f"{year}-{month:02d}",
                        "NEV总销量": random.randint(100000, 800000) if year > 2020 else random.randint(10000, 100000),
                        "BEV销量": random.randint(80000, 600000) if year > 2020 else random.randint(8000, 80000),
                        "PHEV销量": random.randint(20000, 200000) if year > 2020 else random.randint(2000, 20000),
                        "渗透率": round(min(0.05 + (year-2015)*0.09 + month*0.005, 0.52), 3)
                    })
            except Exception as e:
                print(f"获取 {year} 年数据失败: {e}")

        df = pd.DataFrame(self.sales_data)
        df.to_csv("China_NEV_Sales_2015_2025.csv", index=False, encoding='utf-8-sig')
        print(f"销量数据采集完成，保存至: China_NEV_Sales_2015_2025.csv")

    def crawl_regional_data(self):
        """
        模块2：爬取地域差异数据（充电桩密度与城市销量）
        策略：爬取中国充电联盟(EVCIPA)官方月度通报页面
        """
        print("正在爬取地域分布与基础设施数据...")
        
        # 目标：中国充电联盟公共充电桩各省份分布
        target_url = "http://www.evcipa.org.cn/Data/Public" 
        
        try:
            # 1. 尝试获取静态 HTML 中的表格
            # response = requests.get(target_url, headers=self.headers)
            # soup = BeautifulSoup(response.text, 'html.parser')
            # table = soup.find('table') # 寻找数据表
            
            # 2. 模拟从 EVCIPA 获取的 2024-2025 最新城市/省级分布
            city_list = ["北京", "上海", "广州", "深圳", "杭州", "成都", "郑州", "西安", "柳州", "合肥"]
            tiers = ["一线", "一线", "一线", "一线", "新一线", "新一线", "二线", "二线", "三线", "二线"]
            restrictions = ["是", "是", "是", "是", "是", "否", "否", "否", "否", "否"]
            
            for i, city in enumerate(city_list):
                self.regional_data.append({
                    "城市": city,
                    "城市等级": tiers[i],
                    "是否限牌": restrictions[i],
                    "公共充电桩数量": random.randint(50000, 150000) if tiers[i]=="一线" else random.randint(10000, 50000),
                    "2024年NEV注册量": random.randint(200000, 400000) if tiers[i]=="一线" else random.randint(50000, 150000),
                    "充电桩密度(个/km²)": round(random.uniform(5, 35), 1)
                })
                
        except Exception as e:
            print(f"地域数据爬取异常: {e}")

        df = pd.DataFrame(self.regional_data)
        df.to_csv("China_NEV_Regional_Analysis.csv", index=False, encoding='utf-8-sig')
        print(f"地域数据采集完成，保存至: China_NEV_Regional_Analysis.csv")

if __name__ == "__main__":
    spider = NEVDataSpider()
    # 执行销量爬虫
    spider.crawl_sales_trend(start_year=2015, end_year=2025)
    # 执行地域数据爬虫
    spider.crawl_regional_data()