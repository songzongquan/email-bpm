#!/bin/bash
#公网域名申请

domain=$1
ip=$2
dns1="$1\t\t\tA\t10.128.14.3"
dns2="$1\t\tA\t10.128.14.3"

cp /etc/nginx/server.d/xldc.cloudiip.com.conf /etc/nginx/server.d/$1.cloudiip.com.conf # 创建本次申请的域名配置文件，xldc.cloudiip.com.conf为模板
sed -ri "s/xldc/$1/g" /etc/nginx/server.d/$1.cloudiip.com.conf # 将复制的配置文件中的xldc替换为本次申请的域名
sed -ri "s?http://10.128.32.94?$2?g" /etc/nginx/server.d/$1.cloudiip.com.conf # 将配置文件中的proxy_pass部分替换为本次申请的内网ip
(nginx -t;)>&/root/output.txt
if (($?==0));then

    nginx -s reload
    if (($?==0));then

        if [ ${#domain} -le 7 ];then  # 此处判断是为了文件保持对齐，如果申请的域名长度小于等于7就采用参数dns1，否则就是dns2

            echo -e ${dns1} >> /var/named/cloudiip.com.zone   # 在文本最后添加内容，"echo -e"的"-e"能够识别参数中的tab字符
            date=$(date "+%Y%m%d%H") # 获取当前日期，date后必有空格。%Y:当前四位年份，如“2019”，%m:当前月份，如“05”，%d:当前日期，如“15”，%H:当前小时，如”10“
            a=$(awk 'NR==4 {print $1}' /var/named/cloudiip.com.zone) # 获取文件第四行(NR==4)的第一个字段($1)
            sed -ri "s/${a}/${date}/g" /var/named/cloudiip.com.zone # 将从文件中获取的第四行第一个字段替换为当前时间

                if (($?==0));then

                    rndc freeze cloudiip.com

                        if (($?==0));then

                            (rndc reload cloudiip.com;)>>/root/output.txt

                                if (($?==0));then

                                    (rndc thaw cloudiip.com;)>>/root/output.txt

                                        if (($?==0));then

                                            if ping -c 1 -w 5 ${domain}.cloudiip.com&>>/root/output.txt;then

                                                echo "反向代理工作已完成！"

                                            else

                                                echo "域名ping不通，请联系运维人员！"
                                            fi

                                        else

                                            echo "rndc thaw cloudiip.com命令执行失败，请联系运维人员！"
                                        fi

                                else

                                    echo "rndc reload cloudiip.com命令执行失败，请联系运维人员！"
                                fi

                        else

                            echo "rndc frezze cloudiip.com命令执行失败，请联系运维人员！"
                        fi

                else

                    echo "域名解析文件修改失败，请联系运维人员！"
                fi

        else

            echo -e ${dns2} >> /var/named/cloudiip.com.zone
            date=$(date "+%Y%m%d%H") # 获取当前日期，date后必有空格。%Y:当前四位年份，如“2019”，%m:当前月份，如“05”，%d:当前日期，如“15”，%H:当前小时，如”10“
            a=$(awk 'NR==4 {print $1}' /var/named/cloudiip.com.zone) # 获取文件第四行(NR==4)的第一个字段($1)
            sed -ri "s/${a}/${date}/g" /var/named/cloudiip.com.zone # 将从文件中获取的第四行第一个字段替换为当前时间

                if (($?==0));then

                    rndc freeze cloudiip.com

                        if (($?==0));then

                            (rndc reload cloudiip.com;)>>/root/output.txt

                                if (($?==0));then

                                    (rndc thaw cloudiip.com;)>>/root/output.txt

                                        if (($?==0));then

                                            if ping -c 1 -w 5 ${domain}.cloudiip.com&>>/root/output.txt;then

                                                echo "反向代理工作已完成！"

                                            else

                                                echo "域名ping不通，请联系运维人员！"
                                            fi

                                        else

                                            echo "rndc thaw cloudiip.com命令执行失败，请联系运维人员！"
                                        fi

                                else

                                    echo "rndc reload cloudiip.com命令执行失败，请联系运维人员！"
                                fi

                        else

                            echo "rndc frezze cloudiip.com命令执行失败，请联系运维人员！"
                        fi

                else

                    echo "域名解析文件修改失败，请联系运维人员！"
                fi

        fi

    else

        echo "nginx重新加载失败，请联系运维人员！"
    fi

else

    "nginx配置文件修改失败，请联系运维人员！"
fi
