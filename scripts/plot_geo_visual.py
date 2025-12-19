import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform

def set_chinese_font():
    """根据操作系统自动设置中文字体"""
    system = platform.system()
    if system == "Windows":
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    elif system == "Darwin":  # macOS
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC']
    else:  # Linux
        plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 核心数据：各省公共充电桩TOP10 (数据来源：中国充电联盟 2024-2025预测)
data = {
    '省份': ['广东', '浙江', '江苏', '上海', '湖北', '山东', '北京', '安徽', '河南', '福建'],
    '公共充电桩数量(万个)': [62.5, 31.2, 28.5, 19.8, 18.5, 17.6, 15.2, 14.8, 12.5, 11.2],
    '同比增长(%)': [25.4, 28.1, 22.3, 15.6, 32.1, 30.5, 12.8, 35.2, 40.1, 28.9]
}

def plot_geo_infrastructure(data_dict):
    set_chinese_font()
    df_geo = pd.DataFrame(data_dict)
    
    # 设置绘图风格
    sns.set_context("talk")
    fig, ax1 = plt.subplots(figsize=(15, 8))
    
    # 1. 绘制柱状图（保有量）
    # 使用调色盘展现地域差异感
    colors = sns.color_palette("Blues_r", len(df_geo))
    bars = ax1.bar(df_geo['省份'], df_geo['公共充电桩数量(万个)'], color=colors, label='充电桩保有量')
    
    ax1.set_title('2025年中国各省公共充电桩分布及增长率 (TOP10)', fontsize=22, pad=30, fontweight='bold')
    ax1.set_ylabel('公共充电桩保有量 (万个)', fontsize=16, fontweight='bold')
    ax1.set_xlabel('省份', fontsize=16)
    ax1.tick_params(axis='both', labelsize=13)

    # 2. 绘制折线图（同比增长率）
    ax2 = ax1.twinx()
    line = ax2.plot(df_geo['省份'], df_geo['同比增长(%)'], marker='o', color='#e74c3c', 
                    linewidth=3, markersize=10, label='同比增长率 (%)')
    ax2.set_ylabel('同比增长率 (%)', fontsize=16, color='#e74c3c', fontweight='bold')
    ax2.set_ylim(0, 50)
    ax2.tick_params(axis='y', colors='#e74c3c', labelsize=13)
    
    # 3. 添加数值标注
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                 f'{height}', ha='center', va='bottom', fontsize=12, fontweight='bold')

    # 4. 图例整合
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper right', fontsize=12, shadow=True)

    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig('geo_infrastructure.png', dpi=300)
    print("已生成图像：geo_infrastructure.png")

if __name__ == "__main__":
    plot_geo_infrastructure(data)