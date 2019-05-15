#!/bin/bash

ip=$1
domain=$2
dns1="$1\t\t\tA\t10.128.14.3"
dns2="$1\t\tA\t10.128.14.3"

cp /etc/nginx/server.d/xldc.cloudiip.com.conf /etc/nginx/server.d/$1.cloudiip.com.conf # ����������������������ļ���xldc.cloudiip.com.confΪģ��
sleep 2
sed -ri "s/xldc/$1/g" /etc/nginx/server.d/$1.cloudiip.com.conf # �����Ƶ������ļ��е�xldc�滻Ϊ�������������
sleep 2
sed -ri "s?http://10.128.32.94?$2?g" /etc/nginx/server.d/$1.cloudiip.com.conf # �������ļ��е�proxy_pass�����滻Ϊ�������������ip
sleep 2
nginx -t
if(($?!=0));then
echo "�޸������ļ�ʧ��" #�˴�����÷��ʼ���������ά��Ա���ʼ�
else
nginx -s reload
        if(($?!=0));then
        echo "nginx���¼���ʧ��" #�˴�����÷��ʼ���������ά��Ա���ʼ�
        else
        if [ $1 -le 7 ]# �˴��ж���Ϊ���ļ����ֶ��룬����������������С�ڵ���7�Ͳ��ò���dns1���������dns2
        then
        echo -e ${dns1} >> /etc/nginx/server.d/cloudiip.com.zone# ���ı����������ݣ�"echo -e"��"-e"�ܹ�ʶ������е�tab�ַ�
        else
        echo -e ${dns2} >> /etc/nginx/server.d/cloudiip.com.zone
        fi
        sleep 2

date=$(date "+%Y%m%d%H") # ��ȡ��ǰ���ڣ�date����пո�%Y:��ǰ��λ��ݣ��硰2019����%m:��ǰ�·ݣ��硰05����%d:��ǰ���ڣ��硰15����%H:��ǰСʱ���硱10��
a=$(awk 'NR==4 {print $1}' /etc/nginx/server.d/cloudiip.com.zone) # ��ȡ�ļ�������(NR==4)�ĵ�һ���ֶ�($1)
sleep 2
sed -ri "s/${a}/${date}/g" /etc/nginx/server.d/cloudiip.com.zone # �����ļ��л�ȡ�ĵ����е�һ���ֶ��滻Ϊ��ǰʱ��
sleep 2
if(($?!=0));then
        echo "ִ��ʧ��"
else
        rndc freeze cloudiip.com
        if(($?!=0));then
                echo "ִ��ʧ��"
        else
                rndc reload cloudiip.com
                if(($?!=0));then
                        echo "ִ��ʧ��"
                else
                        rndc thaw cloudiip.com
                        if(($?!=0));then
                                echo "ִ��ʧ��"
                        else
                                if ping -c 1 -w 5 ${domain}.cloudiip.com&>/etc/nginx/server.d/ping.txt
                        then
                                echo "�ɹ�"
                        else
                                echo "ʧ��"
                        fi
fi