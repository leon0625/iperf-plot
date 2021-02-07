import json
import matplotlib.pyplot as plt
import sys
import argparse
import time

# 根据iperf3跑流输出的json结果,生成流量图
# 支持多个文件生成在一张图上,便于观察流量之间的影响
# python3 iperf3_plot.py web.json other.json

def getSumName(data):
    protocol = data['start']['test_start']['protocol']
    if protocol == 'UDP':
        return 'sum'
    else:
        return 'sum_sent'

# 根据开始时间,结束时间计算所有跑流结果的时间范围
# 返回的timeRange存储的unix时间
def calcTimeRange(files):
    minStartTime = 0xffffffff
    maxEndTime = 0
    for n in files:
        with open(n) as f:
            data = json.load(f)
            sum = getSumName(data)
            startTime = data["start"]["timestamp"]["timesecs"]
            endTime = startTime + data["end"][sum]["seconds"]
            if startTime < minStartTime:
                minStartTime = startTime
            if endTime > maxEndTime:
                maxEndTime = endTime
    
    timeRange = []
    for i in range(minStartTime, int(maxEndTime)):
        timeRange.append(i)

    return timeRange
    

# 根据数据文件绘图
def chart(files, timeRange):
    for n in files:
        with open(n) as f:
            data = json.load(f)
            sum = getSumName(data)
            startTime = data["start"]["timestamp"]["timesecs"]
            endTime = startTime + data["end"][sum]["seconds"]
            endTime = int(endTime)
            debit = []

            headTime = timeRange[0]
            tailTime = timeRange[len(timeRange)-1]

            # 没有吞吐量时间的部分填充0
            if startTime > headTime:
                for i in range(0, startTime - headTime):
                    debit.append(0)

            intervals = data['intervals']
            for i in intervals:
                debit.append(i['sum']['bits_per_second']/1024/1024) # Mbit单位换算
            
            # 没有吞吐量时间的部分填充0
            if endTime < tailTime:
                for i in range(endTime-headTime,tailTime-headTime):
                    debit.append(0)

            plt.plot(debit, label=n)

            
    plt.ylabel('Mbit/s')
    plt.xlabel('Time sec')
    plt.title("Throughput") 
    plt.legend()    # 显示图例
    plt.grid(axis='y', linestyle='--')  # 显示y轴网格
    plt.show()

def main(argv):
    timeRange=calcTimeRange(argv)
    chart(argv,timeRange)

if __name__ == '__main__':
    main(sys.argv[1:])
