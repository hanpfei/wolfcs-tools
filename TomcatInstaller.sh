#!/bin/bash

## Step Two.

groupId=`id -g "tomcat"`

if [ $groupId -ne 0 ]; then
  echo "Group exists"
else
  groupadd tomcat
fi 

userId=`id -u "tomcat"`

if [ $userId -ne 0 ]; then
  echo "User exists"
else
  useradd -s /bin/false -g tomcat -d /opt/tomcat tomcat
fi

## Step Three.

cd /tmp

url=http://archive.apache.org/dist/tomcat/tomcat-8/v8.0.32/bin/apache-tomcat-8.0.32.tar.gz
filename=`basename $url`

# echo "filename "
# echo $filename

if [ ! -f $filename ]; then 
  curl -O $url
else
  echo "$filename File exists"
fi

if [ $? -ne 0 ]; then
  echo "Download failed!!!"
  exit 1
fi

if [ -d "/opt/tomcat" ]; then
  mv /opt/tomcat /opt/tomcat_bak
fi

mkdir /opt/tomcat

if [ $? -ne 0 ]; then
  echo "mkdir /opt/tomcat failed!!!"
  exit 1
fi

tar xzf apache-tomcat-8*tar.gz -C /opt/tomcat --strip-components=1

if [ $? -ne 0 ]; then
  echo "mkdir /opt/tomcat failed!!!"
  exit 1
fi

## Step Four.

cd /opt/tomcat

chown -R tomcat:tomcat .

chgrp -R tomcat /opt/tomcat

chmod -R g+r conf

chmod g+x conf

chown -R tomcat webapps/ work/ temp/ logs/

