#!/bin/bash
set -ex
docker build -t rpmbuilder .test/
docker run --cap-add=SYS_ADMIN -w /root/rpmbuild/SOURCES/ -it -v `pwd`:/root/rpmbuild/SOURCES/ rpmbuilder
