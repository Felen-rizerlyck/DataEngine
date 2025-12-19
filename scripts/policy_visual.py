import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.collections import LineCollection  # 修复后的导入
from matplotlib.patches import Patch

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False

def get_milestone_data():
    """定义政策与重大事件数据集"""
    # 颜色约定：green-支持政策, orange-调整/退坡, blue-市场大事, red-监管/危机, purple-里程碑
    milestones = [
        ("补贴政策启动", "2013-09-01", "green"),
        ("免征购置税启动", "2014-07-01", "green"),
        ("骗补大核查", "2016-01-01", "red"),
        ("双积分政策发布", "2017-09-01", "green"),
        ("特斯拉上海建厂", "2018-07-10", "blue"),
        ("补贴大幅退坡", "2019-06-25", "orange"),
        ("新冠疫情爆发", "2020-01-23", "red"),
        ("产业发展规划(2035)", "2020-11-02", "green"),
        ("国补正式退出", "2023-01-01", "orange"),
        ("以旧换新政策", "2024-04-26", "green"),
        ("月度渗透率突破50%", "2024-10-01", "purple")
    ]
    return milestones

def plot_policy_timeline():
    """绘制纯政策与事件的时间轴"""
    milestones = get_milestone_data()
    dates = [mdates.datestr2num(m[1]) for m in milestones]
    names = [m[0] for m in milestones]
    colors = [m[2] for m in milestones]

    # 创建画布，增加高度以适应大字体
    fig, ax = plt.subplots(figsize=(18, 7), constrained_layout=True)
    ax.set_title("中国新能源汽车产业关键政策与事件时间轴 (2013-2025)", fontsize=24, pad=40, fontweight='bold')

    # 1. 绘制基线
    ax.axhline(0, color="black", linewidth=3, zorder=1)

    # 2. 绘制垂直指引线（交错高度，增加视觉层次）
    levels = np.tile([-5, 5, -3, 3, -1, 1], int(np.ceil(len(dates)/6)))[:len(dates)]
    ax.vlines(dates, 0, levels, color="darkgrey", linestyle="-", linewidth=1.5, alpha=0.6)
    
    # 3. 绘制时间节点圆点
    ax.scatter(dates, np.zeros_like(dates), c=colors, s=200, zorder=3, edgecolors='white', linewidth=2)
    
    # 4. 标注文本
    for i, (date, name, level) in enumerate(zip(dates, names, levels)):
        ax.annotate(name, xy=(date, level),
                    xytext=(0, 12 if level > 0 else -12), 
                    textcoords="offset points",
                    ha="center", va="bottom" if level > 0 else "top",
                    fontsize=14, fontweight='bold', color=colors[i],
                    bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=colors[i], alpha=0.1))

    # 5. 格式化坐标轴
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    plt.xticks(fontsize=14, fontweight='bold')
    ax.get_yaxis().set_visible(False)
    for s in ["left", "top", "right"]: ax.spines[s].set_visible(False)

    # 6. 添加颜色图例
    legend_elements = [
        Patch(facecolor='green', label='支持/激励政策'),
        Patch(facecolor='orange', label='补贴退坡/调整'),
        Patch(facecolor='blue', label='行业重大事件'),
        Patch(facecolor='red', label='监管核查/外部危机'),
        Patch(facecolor='purple', label='行业里程碑点')
    ]
    ax.legend(handles=legend_elements, loc='best', title="分类图例", 
              fontsize=12, title_fontsize=14, frameon=True, shadow=True, borderpad=1)
    
    plt.savefig('policy_timeline_v3.png', dpi=300)
    print("已生成：policy_timeline_v3.png")

def plot_data_with_policy(csv_path):
    """绘制政策与产销叠加图（修正数据类型）"""
    df = pd.read_csv(csv_path)
    df['日期'] = pd.to_datetime(df['日期'], format='%b-%y')
    df = df.sort_values('日期')
    
    # 使用 np.nan 确保绘图兼容性
    df['NEV总销量'] = df['NEV总销量'].replace(0, np.nan).astype(float)
    df['NEV总产量'] = df['NEV总产量'].replace(0, np.nan).astype(float)

    fig, ax1 = plt.subplots(figsize=(16, 9))

    # 绘制曲线
    ax1.plot(df['日期'], df['NEV总销量'], label='月度总销量', color='skyblue', linewidth=1.5, zorder=3)
    ax1.fill_between(df['日期'], df['NEV总销量'].fillna(0), color='lightskyblue', alpha=0.2)
    ax1.plot(df['日期'], df['NEV总产量'], label='月度总产量', color='sandybrown', linestyle='--', alpha=0.7, zorder=2)
    
    ax1.set_ylabel('数量 (辆)', fontsize=16, fontweight='bold')
    ax1.tick_params(axis='both', labelsize=13)

    # 标注政策
    milestones = get_milestone_data()
    for name, date_str, color in milestones:
        dt = pd.to_datetime(date_str)
        if dt >= df['日期'].min() and dt <= df['日期'].max():
            valid_df = df.dropna(subset=['NEV总销量'])
            idx = (valid_df['日期'] - dt).abs().idxmin()
            y_val = valid_df.loc[idx, 'NEV总销量']

            ax1.axvline(dt, color=color, linestyle='-', alpha=0.4, linewidth=1.2)
            ax1.annotate(name, xy=(dt, y_val), xytext=(15, 40),
                         textcoords='offset points', rotation=30,
                         fontsize=11, color=color, fontweight='bold',
                         arrowprops=dict(arrowstyle='->', color=color, alpha=0.6, connectionstyle="arc3,rad=.2"))

    plt.title("中国新能源汽车产销走势与关键政策节点关联分析 (2015-2025)", fontsize=22, pad=25, fontweight='bold')
    plt.grid(True, axis='y', linestyle='--', alpha=0.4)
    ax1.legend(loc='upper left', fontsize=14, shadow=True)
    
    plt.tight_layout()
    plt.savefig('sales_policy_combined_v3.png', dpi=300)
    print("已生成：sales_policy_combined_v3.png")

if __name__ == "__main__":
    data_path = '../data/China_NEV_Sales_Trend_2013_2025.csv'
    try:
        plot_policy_timeline()
        plot_data_with_policy(data_path)
    except Exception as e:
        import traceback
        print(f"绘图过程中出现错误: {e}")
        traceback.print_exc()