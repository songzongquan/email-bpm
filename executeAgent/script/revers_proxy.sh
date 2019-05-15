#!/bin/bash

ip=$1
domain=$2
dns1="$1\t\t\tA\t10.128.14.3"
dns2="$1\t\tA\t10.128.14.3"

cp /etc/nginx/server.d/xldc.cloudiip.com.conf /etc/nginx/server.d/$1.cloudiip.com.conf # 创建本次申请的域名配置文件，xldc.cloudiip.com.conf为模板
sleep 2
sed -ri "s/xldc/$1/g" /etc/nginx/server.d/$1.cloudiip.com.conf # 将复制的配置文件中的xldc替换为本次申请的域名
sleep 2
sed -ri "s?http://10.128.32.94?$2?g" /etc/nginx/server.d/$1.cloudiip.com.conf # 将配置文件中的proxy_pass部分替换为本次申请的内网ip
sleep 2
nginx -t
if(($?!=0));then
echo "修改配置文件失败" #此处需调用发邮件函数给运维人员发邮件
else
nginx -s reload
        if(($?!=0));then
        echo "nginx重新加载失败" #此处需调用发邮件函数给运维人员发邮件
        else
        if [ $1 -le 7 ]# 此处判断是为了文件保持对齐，如果申请的域名长度小于等于7就采用参数dns1，否则就是dns2
        then
        echo -e ${dns1} >> /etc/nginx/server.d/cloudiip.com.zone# 在文本最后添加内容，"echo -e"的"-e"能够识别参数中的tab字符
        else
        echo -e ${dns2} >> /etc/nginx/server.d/cloudiip.com.zone
        fi
        sleep 2

date=$(date "+%Y%m%d%H") # 获取当前日期，date后必有空格。%Y:当前四位年份，如“2019”，%m:当前月份，如“05”，%d:当前日期，如“15”，%H:当前小时，如”10“
a=$(awk 'NR==4 {print $1}' /etc/nginx/server.d/cloudiip.com.zone) # 获取文件第四行(NR==4)的第一个字段($1)
sleep 2
sed -ri "s/${a}/${date}/g" /etc/nginx/server.d/cloudiip.com.zone # 将从文件中获取的第四行第一个字段替换为当前时间
sleep 2
if(($?!=0));then
        echo "执行失败"
else
        rndc freeze cloudiip.com
        if(($?!=0));then
                echo "执行失败"
        else
                rndc reload cloudiip.com
                if(($?!=0));then
                        echo "执行失败"
                else
                        rndc thaw cloudiip.com
                        if(($?!=0));then
                                echo "执行失败"
                        else
                                if ping -c 1 -w 5 ${domain}.cloudiip.com&>/etc/nginx/server.d/ping.txt
                        then
                                echo "成功"
                        else
                                echo "失败"
                        fi
fi