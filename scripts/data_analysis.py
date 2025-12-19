import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 设置中文字体（根据环境调整，如 'SimHei' 或 'Heiti TC'）
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style="whitegrid", font='SimHei')

# 读取数据
df = pd.read_csv('../data/China_NEV_Sales_Trend_2013_2025.csv')

# 日期转换与排序
df['日期'] = pd.to_datetime(df['日期'], format='%b-%y')
df = df.sort_values('日期')

# 处理 0 或空值：将 0 替换为 NaN，方便绘图时跳过或插值
df.replace(0, np.nan, inplace=True)

plt.figure(figsize=(12, 6))
plt.plot(df['日期'], df['NEV总销量'], label='新能源汽车总销量', color='#2ecc71', lw=3)
plt.fill_between(df['日期'], df['NEV总销量'], color='#2ecc71', alpha=0.1)

# 标注关键节点（示例）
plt.annotate('特斯拉国产化/补贴调整', xy=(pd.to_datetime('2019-12-01'), 100000), 
             xytext=(pd.to_datetime('2017-01-01'), 400000),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.title('2013-2025年中国新能源汽车月度销量走势', fontsize=16)
plt.ylabel('销量 (辆)')
plt.legend()
plt.tight_layout()
plt.show()

# 准备堆叠数据（处理缺失值以便绘图）
plot_df = df.dropna(subset=['BEV销量', 'PHEV销量'])

plt.figure(figsize=(12, 6))
plt.stackplot(plot_df['日期'], plot_df['BEV销量'], plot_df['PHEV销量'], 
              labels=['纯电动 (BEV)', '插电混动 (PHEV)'], 
              colors=['#3498db', '#e67e22'], alpha=0.8)

plt.title('中国新能源汽车市场构成演变 (BEV vs PHEV)', fontsize=16)
plt.ylabel('销量 (辆)')
plt.legend(loc='upper left')
plt.show()

# 提取年份和月份
df['Year'] = df['日期'].dt.year
df['Month'] = df['日期'].dt.month

# 创建透视表
heatmap_data = df.pivot_table(index='Year', columns='Month', values='NEV总产量')

plt.figure(figsize=(14, 8))
sns.heatmap(heatmap_data, annot=False, cmap='YlOrRd', cbar_kws={'label': '月产量'})
plt.title('新能源汽车产量季节性热力图 (年份 vs 月份)', fontsize=16)
plt.xlabel('月份')
plt.ylabel('年份')
plt.show()

# 计算环比增长率
df['MoM_Growth'] = df['NEV总销量'].pct_change() * 100

plt.figure(figsize=(12, 5))
plt.bar(df['日期'], df['MoM_Growth'], color=np.where(df['MoM_Growth'] > 0, '#e74c3c', '#95a5a6'), alpha=0.6)
plt.axhline(0, color='black', lw=1)
plt.title('月度销量环比增长率 (%)', fontsize=14)
plt.ylabel('增长率')
plt.ylim(-100, 100) # 限制范围以防异常值干扰视线
plt.show()