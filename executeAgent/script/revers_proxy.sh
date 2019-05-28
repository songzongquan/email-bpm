#!/bin/bash
#������������

domain=$1
ip=$2
dns1="$1\t\t\tA\t10.128.14.3"
dns2="$1\t\tA\t10.128.14.3"

cp /etc/nginx/server.d/xldc.cloudiip.com.conf /etc/nginx/server.d/$1.cloudiip.com.conf # ����������������������ļ���xldc.cloudiip.com.confΪģ��
sed -ri "s/xldc/$1/g" /etc/nginx/server.d/$1.cloudiip.com.conf # �����Ƶ������ļ��е�xldc�滻Ϊ�������������
sed -ri "s?http://10.128.32.94?$2?g" /etc/nginx/server.d/$1.cloudiip.com.conf # �������ļ��е�proxy_pass�����滻Ϊ�������������ip
(nginx -t;)>&/root/output.txt
if (($?==0));then

    nginx -s reload
    if (($?==0));then

        if [ ${#domain} -le 7 ];then  # �˴��ж���Ϊ���ļ����ֶ��룬����������������С�ڵ���7�Ͳ��ò���dns1���������dns2

            echo -e ${dns1} >> /var/named/cloudiip.com.zone   # ���ı����������ݣ�"echo -e"��"-e"�ܹ�ʶ������е�tab�ַ�
            date=$(date "+%Y%m%d%H") # ��ȡ��ǰ���ڣ�date����пո�%Y:��ǰ��λ��ݣ��硰2019����%m:��ǰ�·ݣ��硰05����%d:��ǰ���ڣ��硰15����%H:��ǰСʱ���硱10��
            a=$(awk 'NR==4 {print $1}' /var/named/cloudiip.com.zone) # ��ȡ�ļ�������(NR==4)�ĵ�һ���ֶ�($1)
            sed -ri "s/${a}/${date}/g" /var/named/cloudiip.com.zone # �����ļ��л�ȡ�ĵ����е�һ���ֶ��滻Ϊ��ǰʱ��

                if (($?==0));then

                    rndc freeze cloudiip.com

                        if (($?==0));then

                            (rndc reload cloudiip.com;)>>/root/output.txt

                                if (($?==0));then

                                    (rndc thaw cloudiip.com;)>>/root/output.txt

                                        if (($?==0));then

                                            if ping -c 1 -w 5 ${domain}.cloudiip.com&>>/root/output.txt;then

                                                echo "�������������ɣ�"

                                            else

                                                echo "����ping��ͨ������ϵ��ά��Ա��"
                                            fi

                                        else

                                            echo "rndc thaw cloudiip.com����ִ��ʧ�ܣ�����ϵ��ά��Ա��"
                                        fi

                                else

                                    echo "rndc reload cloudiip.com����ִ��ʧ�ܣ�����ϵ��ά��Ա��"
                                fi

                        else

                            echo "rndc frezze cloudiip.com����ִ��ʧ�ܣ�����ϵ��ά��Ա��"
                        fi

                else

                    echo "���������ļ��޸�ʧ�ܣ�����ϵ��ά��Ա��"
                fi

        else

            echo -e ${dns2} >> /var/named/cloudiip.com.zone
            date=$(date "+%Y%m%d%H") # ��ȡ��ǰ���ڣ�date����пո�%Y:��ǰ��λ��ݣ��硰2019����%m:��ǰ�·ݣ��硰05����%d:��ǰ���ڣ��硰15����%H:��ǰСʱ���硱10��
            a=$(awk 'NR==4 {print $1}' /var/named/cloudiip.com.zone) # ��ȡ�ļ�������(NR==4)�ĵ�һ���ֶ�($1)
            sed -ri "s/${a}/${date}/g" /var/named/cloudiip.com.zone # �����ļ��л�ȡ�ĵ����е�һ���ֶ��滻Ϊ��ǰʱ��

                if (($?==0));then

                    rndc freeze cloudiip.com

                        if (($?==0));then

                            (rndc reload cloudiip.com;)>>/root/output.txt

                                if (($?==0));then

                                    (rndc thaw cloudiip.com;)>>/root/output.txt

                                        if (($?==0));then

                                            if ping -c 1 -w 5 ${domain}.cloudiip.com&>>/root/output.txt;then

                                                echo "�������������ɣ�"

                                            else

                                                echo "����ping��ͨ������ϵ��ά��Ա��"
                                            fi

                                        else

                                            echo "rndc thaw cloudiip.com����ִ��ʧ�ܣ�����ϵ��ά��Ա��"
                                        fi

                                else

                                    echo "rndc reload cloudiip.com����ִ��ʧ�ܣ�����ϵ��ά��Ա��"
                                fi

                        else

                            echo "rndc frezze cloudiip.com����ִ��ʧ�ܣ�����ϵ��ά��Ա��"
                        fi

                else

                    echo "���������ļ��޸�ʧ�ܣ�����ϵ��ά��Ա��"
                fi

        fi

    else

        echo "nginx���¼���ʧ�ܣ�����ϵ��ά��Ա��"
    fi

else

    "nginx�����ļ��޸�ʧ�ܣ�����ϵ��ά��Ա��"
fi
