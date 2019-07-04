#!/bin/bash

CONF_PATH="Conf/config.ini"

read -p "请输入请求地址: （参考http://xxxxxxxxx） " url
echo 请求地址为$url

read -p "请输入账号：" username
echo 用户名为$username

read -p "请输入密码: " password

sed -i "/^common_url/ccommon_url = ${url}:18888" $CONF_PATH

sed -i "/^username/cusername = ${username}" $CONF_PATH

sed -i "/^password/cpassword = ${password}" $CONF_PATH

echo "修改配置完成"

CURRENT_PATH=`pwd`

echo $CURRENT_PATH

PYTHON3PATH=${CURRENT_PATH%/*}'/Python-3.7.1/bin/python3.7'

$PYTHON3PATH run.py -N
