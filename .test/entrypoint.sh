#!/bin/bash -ex

echo "Build SRPM"
spectool -g -R *.spec
chown root. *
rpmbuild -bs *.spec

echo "Build RPM"
/usr/bin/mock /root/rpmbuild/SRPMS/*.src.rpm

echo "Install RPM"
yum install -y /var/lib/mock/epel-7-x86_64/result/*.rpm

echo "Start Tomcat"
/usr/libexec/tomcat/server start &

echo "Wait for Tomcat to be ready"
wait-for-it.sh localhost:8080 -- echo "Tomcat is up"

curl -s -I -L localhost:8080/examples/servlets |grep 200
curl -s -I -L localhost:8080/examples/jsp |grep 200
curl -s -I -L localhost:8080/examples/websocket |grep 200
