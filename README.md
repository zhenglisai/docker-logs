# docker-logs
##############################################################  
背景说明：  
需求：  
1，收集每个docker的日志。  
2，日志搜集程序必须运行在docker中，不能运行在主机上。  
3，日志搜集程序不能占用大量服务器资源。  
4，收集和存储的日志方便使用grafana展示。  
开源方案：  
1，ELK方案。将主机的/var/lib/docker/containers目录挂在到容器中，然后使用logstash抓取日志，发送到elasticsearch中，最后使用kibana或者grafana展示。  
分析：理想很好，实际操作发现elasticsearch占用大量内存，影响线上业务  
结论：不实用  
2，fluentd。配置docker的log-driver，将日志直接输出到fluentd中。  
分析：fluentd只是一个收集工具，日志还是需要存储在一个地方，还是需要elk系统协助才能存储和展示。  
结论：不实用  
3，logstash。将主机的/var/lib/docker/containers目录挂在到容器中，然后使用logstash抓取日志，通过influxdb输出插件输出到influxdb中。  
分析：研究了一天的logstash的influxdb输出插件和filter过滤插件，发现将logs中的内容重组成influxdb所需的格式太困难。  
结论：放弃  
自研方案：  
1，使用python获取日志内容，发送到influxdb  
分析：这个方案的难点在于python怎么实时获取每个日志的最新文件，而不重复。python中有很多日志监控模块可以用，但是考虑到大并发的时候这个操作方式有可能太耗费资源。  
结论：放弃  
2，使用python监听udp端口，docker使用logs-driver将日志主动发送到udp中。python接受到消息后，重新解析拼接，发送给influxdb  
分析：这个方案解决了需要自己监控日志变化的问题，只需要被动接受消息就行了,采用udp是减少docker主机发送日志压力。  
结论：可行  
####################################################  
本程序使用方式  
####################################################  
1，修改logs.py中influxdb的地址为你自己的influxdb服务器地址和端口  
2，修改本地监听端口，默认为6015  
3，根据自己需要修改要传入的field和tag  
4，使用dockerfile生成docker  
5，运行docker  
docker run -d \  
-p 6015:6015/udp \  
--name docker-logs \  
docker-logs  
6，被记录日志的docker启动时添加三个参数  
docker run -d \  
--log-driver gelf \  
--log-opt gelf-address=udp://<DOCKER_LOGS_IP>:6015 \  
--log-opt gelf-compression-type=none \  
alpine
  
