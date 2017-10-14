FROM centos

RUN yum install -y epel-release \
 && yum install -y tito \
 && yum clean all

RUN git config --global user.name "Filirom1-bot" \
 && git config --global user.email Filirom1@gmail.com

ENTRYPOINT ["tito"]
