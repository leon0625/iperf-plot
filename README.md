# iperf-plot
使用iperf3跑流输出的json数据绘制吞吐量折线图    
使用python3 iperf3运行良好.  
支持多个json文件生成在一张图上,便于观察流量之间的影响  
举例:  
```  
python3 iperf-plot.py other_stream.json web_stream.json
```  

![示例](./example.png)  
