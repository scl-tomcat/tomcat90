# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%{?scl:%scl_package tomcat}
%{!?scl:%global pkg_name %{name}}

%global jspspec 2.2
%global major_version 7
%global minor_version 0
%global micro_version 82
%global packdname apache-tomcat-%{version}-src
%global servletspec 3.0
%global elspec 2.2
%global tcuid 91

# FHS 2.3 compliant tree structure - http://www.pathname.com/fhs/2.3/
%global basedir %{_localstatedir}/lib/%{pkg_name}
%global appdir %{basedir}/webapps
%global homedir %{_datadir}/%{pkg_name}
%global bindir %{homedir}/bin
%global confdir %{_sysconfdir}/%{pkg_name}
%global libdir %{_datadir}/java/%{pkg_name}
%global logdir %{_localstatedir}/log/%{pkg_name}
%global cachedir %{_localstatedir}/cache/%{pkg_name}
%global tempdir %{cachedir}/temp
%global workdir %{cachedir}/work
%global _initrddir %{_sysconfdir}/init.d
%global _systemddir %{_lib}/systemd/system

Name:          %{?scl_prefix}tomcat
Epoch:         0
Version:       %{major_version}.%{minor_version}.%{micro_version}
Release:       1%{?dist}
Summary:       Apache Servlet/JSP Engine, RI for Servlet %{servletspec}/JSP %{jspspec} API

Group:         System Environment/Daemons
License:       ASL 2.0
URL:           http://tomcat.apache.org/
Source0:       http://www.apache.org/dist/tomcat/tomcat-%{major_version}/v%{version}/src/%{packdname}.tar.gz
Source1:       %{pkg_name}.conf
Source3:       %{pkg_name}.sysconfig
Source4:       %{pkg_name}.wrapper
Source5:       %{pkg_name}.logrotate
Source6:       %{pkg_name}-digest.script
Source7:       %{pkg_name}-tool-wrapper.script
Source10:      %{pkg_name}-log4j.properties
Source11:      %{pkg_name}.service
Source20:      %{pkg_name}-jsvc.service
Source21:      tomcat-functions
Source22:      tomcat-preamble
Source23:      tomcat-server
Source24:      tomcat-named.service
Source25:      http://www.apache.org/dist/tomcat/tomcat-%{major_version}/v%{version}/bin/extras/tomcat-juli-adapters.jar
Source26:      http://www.apache.org/dist/tomcat/tomcat-%{major_version}/v%{version}/bin/extras/tomcat-juli.jar

BuildArch:     noarch

BuildRequires: ant
#BuildRequires: ant-nodeps
BuildRequires: ecj >= 1:4.2.1
BuildRequires: findutils
BuildRequires: apache-commons-daemon
BuildRequires: apache-commons-dbcp
BuildRequires: apache-commons-pool
BuildRequires: jakarta-taglibs-standard
BuildRequires: java-devel >= 1:1.6.0
BuildRequires: jpackage-utils >= 0:1.7.0
BuildRequires: junit
BuildRequires: log4j
BuildRequires: geronimo-jaxrpc
BuildRequires: wsdl4j
BuildRequires: systemd-units
BuildRequires: scl-utils-build
Requires:      apache-commons-daemon
Requires:      apache-commons-logging
Requires:      apache-commons-dbcp
Requires:      apache-commons-pool
Requires:      java >= 1:1.6.0
Requires:      procps
Requires:      %{?scl_prefix}%{pkg_name}-lib = %{epoch}:%{version}-%{release}
Requires(pre):    shadow-utils
Requires(post):   chkconfig
Requires(preun):  chkconfig
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
%{?scl:Requires: %scl_runtime}

%description
Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.

Tomcat is developed in an open and participatory environment and
released under the Apache Software License version 2.0. Tomcat is intended
to be a collaboration of the best-of-breed developers from around the world.

%package admin-webapps
Group: Applications/System
Summary: The host-manager and manager web applications for Apache Tomcat
Requires: %{?scl_prefix}%{pkg_name} = %{epoch}:%{version}-%{release}

%description admin-webapps
The host-manager and manager web applications for Apache Tomcat.

%package docs-webapp
Group: Applications/Text
Summary: The docs web application for Apache Tomcat
Requires: %{?scl_prefix}%{pkg_name} = %{epoch}:%{version}-%{release}

%description docs-webapp
The docs web application for Apache Tomcat.

%package javadoc
Group: Documentation
Summary: Javadoc generated documentation for Apache Tomcat
Requires: jpackage-utils

%description javadoc
Javadoc generated documentation for Apache Tomcat.

%package jsvc
Group: System Environment/Daemons
Summary: Apache jsvc wrapper for Apache Tomcat as separate service
Requires: %{?scl_prefix}%{pkg_name} = %{epoch}:%{version}-%{release}
Requires: apache-commons-daemon-jsvc

%description jsvc
Systemd service and wrapper scripts to start tomcat with jsvc,
which allows tomcat to perform some privileged operations
(e.g. bind to a port < 1024) and then switch identity to a non-privileged user.

%package jsp-%{jspspec}-api
Group: Development/Libraries
Summary: Apache Tomcat JSP API implementation classes
Provides: jsp = %{jspspec}
Provides: jsp22
Requires: %{?scl_prefix}%{pkg_name}-servlet-%{servletspec}-api = %{epoch}:%{version}-%{release}
Requires(post): chkconfig
Requires(postun): chkconfig

%description jsp-%{jspspec}-api
Apache Tomcat JSP API implementation classes.

%package lib
Group: Development/Libraries
Summary: Libraries needed to run the Tomcat Web container
Requires: %{?scl_prefix}%{pkg_name}-jsp-%{jspspec}-api = %{epoch}:%{version}-%{release}
Requires: %{?scl_prefix}%{pkg_name}-servlet-%{servletspec}-api = %{epoch}:%{version}-%{release}
Requires: %{?scl_prefix}%{pkg_name}-el-%{elspec}-api = %{epoch}:%{version}-%{release}
Requires: ecj >= 1:4.2.1
Requires: apache-commons-dbcp
Requires: apache-commons-pool
Requires(preun): coreutils

%description lib
Libraries needed to run the Tomcat Web container.

%package servlet-%{servletspec}-api
Group: Development/Libraries
Summary: Apache Tomcat Servlet API implementation classes
Provides: servlet = %{servletspec}
Provides: servlet6
Provides: servlet3
Requires(post): chkconfig
Requires(postun): chkconfig

%description servlet-%{servletspec}-api
Apache Tomcat Servlet API implementation classes.

%package el-%{elspec}-api
Group: Development/Libraries
Summary: Expression Language v%{elspec} API
Provides: el_1_0_api = %{epoch}:%{version}-%{release}
Provides: el_api = %{elspec}
Requires(post): chkconfig
Requires(postun): chkconfig

%description el-%{elspec}-api
Expression Language %{elspec}.

%package webapps
Group: Applications/Internet
Summary: The ROOT and examples web applications for Apache Tomcat
Requires: %{?scl_prefix}%{pkg_name} = %{epoch}:%{version}-%{release}
Requires: jakarta-taglibs-standard >= 0:1.1

%description webapps
The ROOT and examples web applications for Apache Tomcat.

%prep
%setup -q -n %{packdname}
# remove pre-built binaries and windows files
find . -type f \( -name "*.bat" -o -name "*.class" -o -name Thumbs.db -o -name "*.gz" -o \
   -name "*.jar" -o -name "*.war" -o -name "*.zip" \) -delete

%{__ln_s} $(build-classpath jakarta-taglibs-core) webapps/examples/WEB-INF/lib/jstl.jar
%{__ln_s} $(build-classpath jakarta-taglibs-standard) webapps/examples/WEB-INF/lib/standard.jar

%{__sed} -e "s|/etc/tomcat|%_sysconfdir/tomcat|g" \
         -e "s|/etc/sysconfig/tomcat|%_sysconfdir/sysconfig/tomcat|g"\
         -e "s|/usr/libexec/tomcat|%_libexecdir/tomcat|g"\
         -e "s|/var/lib/tomcats|%_localstatedir/lib/tomcats|g"\
         -e "s|/var/cache/tomcat|%_localstatedir/cache/tomcat|g"\
         -e "s|/var/run/jsvc-tomcat|/var/run/%{?scl_prefix}jsvc-tomcat|g"\
         -i %{SOURCE1} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE10} %{SOURCE11} %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24}

sed -i 's/failonwarning="true"//g' build.xml

%build
export OPT_JAR_LIST="xalan-j2-serializer"

   # we don't care about the tarballs and we're going to replace
   # tomcat-dbcp.jar with apache-commons-{collections,dbcp,pool}-tomcat5.jar
   # so just create a dummy file for later removal
   touch HACK
   %{__mkdir_p} HACKDIR
   touch HACKDIR/build.xml
   # who needs a build.properties file anyway
   %{ant} -Dbase.path="." \
      -Dbuild.compiler="modern" \
      -Dcommons-daemon.jar="$(build-classpath apache-commons-daemon)" \
      -Dcommons-daemon.native.src.tgz="HACK" \
      -Djasper-jdt.jar="$(build-classpath ecj)" \
      -Djdt.jar="$(build-classpath ecj)" \
      -Dtomcat-dbcp.jar="$(build-classpath apache-commons-dbcp)" \
      -Dtomcat-native.tar.gz="HACK" \
      -Dtomcat-native.home="." \
      -Dcommons-daemon.native.win.mgr.exe="HACK" \
      -Dnsis.exe="HACK" \
      -Djaxrpc-lib.jar="$(build-classpath jaxrpc)" \
      -Dwsdl4j-lib.jar="$(build-classpath wsdl4j)" \
      -Dcommons-pool.home="HACKDIR" \
      -Dcommons-dbcp.home="HACKDIR" \
      -Dno.build.dbcp=true \
      -Dversion="%{version}" \
      -Dversion.build="%{micro_version}" \
      -Djava.7.home=/usr/lib/jvm/java-1.7.0/ \
      deploy dist-prepare dist-source javadoc

    # remove some jars that we'll replace with symlinks later
   %{__rm} output/build/bin/commons-daemon.jar \
           output/build/lib/ecj.jar \
           output/build/lib/apache-commons-dbcp.jar

    # remove the cruft we created
   %{__rm} output/build/bin/tomcat-native.tar.gz
pushd output/dist/src/webapps/docs/appdev/sample/src
%{__mkdir_p} ../web/WEB-INF/classes
%{javac} -cp ../../../../../../../../output/build/lib/servlet-api.jar -d ../web/WEB-INF/classes mypackage/Hello.java
pushd ../web
%{jar} cf ../../../../../../../../output/build/webapps/docs/appdev/sample/sample.war *
popd
popd


%install
# build initial path structure
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_bindir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_sbindir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_javadocdir}/%{pkg_name}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_initrddir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_systemddir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{appdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{bindir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{confdir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{confdir}/Catalina/localhost
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{confdir}/conf.d
/bin/echo "Place your custom *.conf files here. Shell expansion is supported." > ${RPM_BUILD_ROOT}%{confdir}/conf.d/README
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{libdir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{logdir}
/bin/touch ${RPM_BUILD_ROOT}%{logdir}/catalina.out
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{_localstatedir}/lib/tomcats
/bin/echo "%{pkg_name}-%{major_version}.%{minor_version}.%{micro_version} RPM installed" >> ${RPM_BUILD_ROOT}%{logdir}/catalina.out
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{homedir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{tempdir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{workdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_unitdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_libexecdir}/%{pkg_name}

# move things into place
# First copy supporting libs to tomcat lib
pushd output/build
    %{__cp} -a bin/*.{jar,xml} ${RPM_BUILD_ROOT}%{bindir}
    %{__cp} %{SOURCE10} conf/log4j.properties
    %{__cp} -a conf/*.{policy,properties,xml} ${RPM_BUILD_ROOT}%{confdir}
    %{__cp} -a lib/*.jar ${RPM_BUILD_ROOT}%{libdir}
    %{__cp} -a webapps/* ${RPM_BUILD_ROOT}%{appdir}
popd
# javadoc
%{__cp} -a output/dist/webapps/docs/api/* ${RPM_BUILD_ROOT}%{_javadocdir}/%{pkg_name}

%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE1} \
    > ${RPM_BUILD_ROOT}%{confdir}/%{pkg_name}.conf
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE3} \
    > ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/%{pkg_name}
%{__install} -m 0644 %{SOURCE4} \
    ${RPM_BUILD_ROOT}%{_sbindir}/%{pkg_name}
%{__install} -m 0644 %{SOURCE11} \
    ${RPM_BUILD_ROOT}%{_unitdir}/%{?scl_prefix}%{pkg_name}.service
%{__install} -m 0644 %{SOURCE20} \
    ${RPM_BUILD_ROOT}%{_unitdir}/%{?scl_prefix}%{pkg_name}-jsvc.service
# %{__ln_s} %{pkg_name} ${RPM_BUILD_ROOT}%{_sbindir}/d%{pkg_name}
%{__sed} -e "s|\@\@\@TCLOG\@\@\@|%{logdir}|g" %{SOURCE5} \
    > ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{pkg_name}
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE6} \
    > ${RPM_BUILD_ROOT}%{_bindir}/%{pkg_name}-digest
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE7} \
    > ${RPM_BUILD_ROOT}%{_bindir}/%{pkg_name}-tool-wrapper

%{__install} -m 0644 %{SOURCE21} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/%{pkg_name}/functions         
%{__install} -m 0755 %{SOURCE22} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/%{pkg_name}/preamble          
%{__install} -m 0755 %{SOURCE23} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/%{pkg_name}/server            
%{__install} -m 0644 %{SOURCE24} \
    ${RPM_BUILD_ROOT}%{_unitdir}/%{?scl_prefix}%{pkg_name}@.service 

# create jsp and servlet API symlinks
pushd ${RPM_BUILD_ROOT}%{_javadir}
   %{__mv} %{pkg_name}/jsp-api.jar %{pkg_name}-jsp-%{jspspec}-api.jar
   %{__ln_s} %{pkg_name}-jsp-%{jspspec}-api.jar %{pkg_name}-jsp-api.jar
   %{__mv} %{pkg_name}/servlet-api.jar %{pkg_name}-servlet-%{servletspec}-api.jar
   %{__ln_s} %{pkg_name}-servlet-%{servletspec}-api.jar %{pkg_name}-servlet-api.jar
   %{__mv} %{pkg_name}/el-api.jar %{pkg_name}-el-%{elspec}-api.jar
   %{__ln_s} %{pkg_name}-el-%{elspec}-api.jar %{pkg_name}-el-api.jar
popd

pushd output/build
    /usr/bin/build-jar-repository lib apache-commons-dbcp apache-commons-pool ecj 2>&1
    # need to use -p here with b-j-r otherwise the examples webapp fails to
    # load with a java.io.IOException
    /usr/bin/build-jar-repository -p webapps/examples/WEB-INF/lib \
    taglibs-core.jar taglibs-standard.jar 2>&1
popd

pushd ${RPM_BUILD_ROOT}%{libdir}
    # symlink JSP and servlet API jars
    %{__ln_s} ../%{pkg_name}-jsp-%{jspspec}-api.jar .
    %{__ln_s} ../%{pkg_name}-servlet-%{servletspec}-api.jar .
    %{__ln_s} ../%{pkg_name}-el-%{elspec}-api.jar .
    %{__ln_s} $(build-classpath apache-commons-dbcp) commons-dbcp.jar
    %{__ln_s} $(build-classpath apache-commons-pool) commons-pool.jar
    %{__ln_s} $(build-classpath log4j) log4j.jar
    %{__ln_s} $(build-classpath ecj) jasper-jdt.jar

    # Temporary copy the juli jar here from /usr/share/java/tomcat (for maven depmap)
    %{__cp} -a ${RPM_BUILD_ROOT}%{bindir}/tomcat-juli.jar ./

    # Add extras JULI jars
    %{__mkdir} extras
    pushd extras
        %{__cp} -p %{SOURCE25} .
        %{__cp} -p %{SOURCE26} .
    popd
popd

# symlink to the FHS locations where we've installed things
pushd ${RPM_BUILD_ROOT}%{homedir}
    %{__ln_s} %{appdir} webapps
    %{__ln_s} %{confdir} conf
    %{__ln_s} %{libdir} lib
    %{__ln_s} %{logdir} logs
    %{__ln_s} %{tempdir} temp
    %{__ln_s} %{workdir} work
popd

# install sample webapp
%{__mkdir_p} ${RPM_BUILD_ROOT}%{appdir}/sample
pushd ${RPM_BUILD_ROOT}%{appdir}/sample
%{jar} xf ${RPM_BUILD_ROOT}%{appdir}/docs/appdev/sample/sample.war
popd
%{__rm} ${RPM_BUILD_ROOT}%{appdir}/docs/appdev/sample/sample.war

# Allow linking for example webapp
%{__mkdir_p} ${RPM_BUILD_ROOT}%{appdir}/examples/META-INF
pushd ${RPM_BUILD_ROOT}%{appdir}/examples/META-INF
echo '<?xml version="1.0" encoding="UTF-8"?>'>context.xml
echo '<Context allowLinking="true"/>'>>context.xml
popd

pushd ${RPM_BUILD_ROOT}%{appdir}/examples/WEB-INF/lib
%{__ln_s} -f $(build-classpath jakarta-taglibs-core) jstl.jar
%{__ln_s} -f $(build-classpath jakarta-taglibs-standard) standard.jar
popd


# Install the maven metadata
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_mavenpomdir}
pushd output/dist/src/res/maven
for pom in *.pom; do
    # fix-up version in all pom files
    sed -i 's/@MAVEN.DEPLOY.VERSION@/%{version}/g' $pom
done

# we won't install dbcp, juli-adapters and juli-extras pom files
for libname in annotations-api catalina jasper-el jasper catalina-ha; do
    %{__cp} -a %{pkg_name}-$libname.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{pkg_name}-$libname.pom
    %add_maven_depmap JPP.%{pkg_name}-$libname.pom %{pkg_name}/$libname.jar
done

# servlet-api jsp-api and el-api are not in tomcat subdir, since they are widely re-used elsewhere
%{__cp} -a tomcat-jsp-api.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP-tomcat-jsp-api.pom
%add_maven_depmap JPP-tomcat-jsp-api.pom tomcat-jsp-api.jar -f "tomcat-jsp-api" -a "javax.servlet.jsp:javax.servlet.jsp-api,javax.servlet:jsp-api,org.eclipse.jetty.orbit:javax.servlet.jsp"

%{__cp} -a tomcat-el-api.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP-tomcat-el-api.pom
%add_maven_depmap JPP-tomcat-el-api.pom tomcat-el-api.jar -f "tomcat-el-api" -a "javax.el:javax.el-api,javax.el:el-api,org.eclipse.jetty.orbit:javax.el"

%{__cp} -a tomcat-servlet-api.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP-tomcat-servlet-api.pom
# Generate a depmap fragment javax.servlet:servlet-api pointing to
# tomcat-servlet-3.0-api for backwards compatibility
# also provide jetty depmap (originally in jetty package, but it's cleaner to have it here
%add_maven_depmap JPP-tomcat-servlet-api.pom tomcat-servlet-api.jar -f "tomcat-servlet-api" -a "javax.servlet:servlet-api,javax.servlet:javax.servlet-api,org.mortbay.jetty:servlet-api,org.eclipse.jetty.orbit:javax.servlet"

# two special pom where jar files have different names
%{__cp} -a tomcat-tribes.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{pkg_name}-catalina-tribes.pom
%add_maven_depmap JPP.%{pkg_name}-catalina-tribes.pom %{pkg_name}/catalina-tribes.jar

%{__cp} -a tomcat-coyote.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{pkg_name}-tomcat-coyote.pom
%add_maven_depmap JPP.%{pkg_name}-tomcat-coyote.pom %{pkg_name}/tomcat-coyote.jar

%{__cp} -a tomcat-juli.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{pkg_name}-tomcat-juli.pom
%add_maven_depmap JPP.%{pkg_name}-tomcat-juli.pom %{pkg_name}/tomcat-juli.jar

%{__cp} -a tomcat-api.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{pkg_name}-tomcat-api.pom
%add_maven_depmap JPP.%{pkg_name}-tomcat-api.pom %{pkg_name}/tomcat-api.jar

%{__cp} -a tomcat-util.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{pkg_name}-tomcat-util.pom
%add_maven_depmap JPP.%{pkg_name}-tomcat-util.pom %{pkg_name}/tomcat-util.jar

# replace temporary copy with link
%{__ln_s} -f %{bindir}/tomcat-juli.jar ${RPM_BUILD_ROOT}%{libdir}/


%pre
# add the tomcat user and group
%{_root_sbindir}/groupadd -g %{tcuid} -r tomcat 2>/dev/null || :
%{_root_sbindir}/useradd -c "Apache Tomcat" -u %{tcuid} -g tomcat \
    -s /sbin/nologin -r -d %{homedir} tomcat 2>/dev/null || :

%post
# install but don't activate
%systemd_post %{?scl_prefix}%{pkg_name}.service

%post jsp-%{jspspec}-api
%{_root_sbindir}/update-alternatives --install %{_javadir}/jsp.jar jsp \
    %{_javadir}/%{pkg_name}-jsp-%{jspspec}-api.jar 20200

%post servlet-%{servletspec}-api
%{_root_sbindir}/update-alternatives --install %{_javadir}/servlet.jar servlet \
    %{_javadir}/%{pkg_name}-servlet-%{servletspec}-api.jar 30000

%post el-%{elspec}-api
%{_root_sbindir}/update-alternatives --install %{_javadir}/elspec.jar elspec \
   %{_javadir}/%{pkg_name}-el-%{elspec}-api.jar 20300

%preun
# clean tempdir and workdir on removal or upgrade
%{__rm} -rf %{workdir}/* %{tempdir}/*
%systemd_preun %{?scl_prefix}%{pkg_name}.service

%postun
%systemd_postun_with_restart %{?scl_prefix}%{pkg_name}.service 

%postun jsp-%{jspspec}-api
if [ "$1" = "0" ]; then
    %{_root_sbindir}/update-alternatives --remove jsp \
        %{_javadir}/%{pkg_name}-jsp-%{jspspec}-api.jar
fi

%postun servlet-%{servletspec}-api
if [ "$1" = "0" ]; then
    %{_root_sbindir}/update-alternatives --remove servlet \
        %{_javadir}/%{pkg_name}-servlet-%{servletspec}-api.jar
fi

%postun el-%{elspec}-api
if [ "$1" = "0" ]; then
    %{_root_sbindir}/update-alternatives --remove elspec \
        %{_javadir}/%{pkg_name}-el-%{elspec}-api.jar
fi

%triggerun -- %{?scl_prefix}tomcat < 0:7.0.22-2
/usr/bin/systemd-sysv-convert -- save %{?scl_prefix}tomcat > /dev/null 2>&1 || :
# Run these becasue the SysV package being removed won't do them
/sbin/chkconfig --del %{?scl_prefix}tomcat > /dev/null 2>&1 || :
/bin/systemctl try-restart %{?scl_prefix}tomcat.service > /dev/null 2>&1 || :

%files
%defattr(0664,root,tomcat,0755)
%doc {LICENSE,NOTICE,RELEASE*}
%attr(0755,root,root) %{_bindir}/%{pkg_name}-digest
%attr(0755,root,root) %{_bindir}/%{pkg_name}-tool-wrapper
%attr(0755,root,root) %{_sbindir}/%{pkg_name}
%attr(0644,root,root) %{_unitdir}/%{?scl_prefix}%{pkg_name}.service
%attr(0644,root,root) %{_unitdir}/%{?scl_prefix}%{pkg_name}@.service
%attr(0755,root,root) %dir %{_libexecdir}/%{pkg_name}
%attr(0755,root,root) %dir %{_localstatedir}/lib/tomcats
%attr(0644,root,root) %{_libexecdir}/%{pkg_name}/functions
%attr(0755,root,root) %{_libexecdir}/%{pkg_name}/preamble
%attr(0755,root,root) %{_libexecdir}/%{pkg_name}/server
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{pkg_name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{pkg_name}
%attr(0755,root,tomcat) %dir %{basedir}
%attr(0755,root,tomcat) %dir %{confdir}

%defattr(0664,tomcat,root,0770)
%attr(0770,tomcat,root) %dir %{logdir}

%defattr(0664,root,tomcat,0770)
%attr(0660,tomcat,tomcat) %verify(not size md5 mtime) %{logdir}/catalina.out
%attr(0770,root,tomcat) %dir %{cachedir}
%attr(0770,root,tomcat) %dir %{tempdir}
%attr(0770,root,tomcat) %dir %{workdir}

%defattr(0644,root,tomcat,0775)
%attr(0775,root,tomcat) %dir %{appdir}
%attr(0775,root,tomcat) %dir %{confdir}/Catalina
%attr(0775,root,tomcat) %dir %{confdir}/Catalina/localhost
%attr(0755,root,tomcat) %dir %{confdir}/conf.d
%{confdir}/conf.d/README
%config(noreplace) %{confdir}/%{pkg_name}.conf
%config(noreplace) %{confdir}/*.policy
%config(noreplace) %{confdir}/*.properties
%config(noreplace) %{confdir}/*.xml
%attr(0640,root,tomcat) %config(noreplace) %{confdir}/tomcat-users.xml
%config(noreplace) %{confdir}/web.xml
%dir %{homedir}
%{bindir}/bootstrap.jar
%{bindir}/catalina-tasks.xml
%{homedir}/lib
%{homedir}/temp
%{homedir}/webapps
%{homedir}/work
%{homedir}/logs
%{homedir}/conf

%files admin-webapps
%defattr(0664,root,tomcat,0755)
%{appdir}/host-manager
%{appdir}/manager
%config(noreplace) %{appdir}/manager/WEB-INF/web.xml
%config(noreplace) %{appdir}/host-manager/WEB-INF/web.xml

%files docs-webapp
%defattr(-,root,root,-)
%{appdir}/docs

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{pkg_name}

%files jsp-%{jspspec}-api
%defattr(-,root,root,-)
%{_javadir}/%{pkg_name}-jsp-%{jspspec}*.jar
%{_javadir}/%{pkg_name}-jsp-api.jar
%{_mavenpomdir}/JPP-%{pkg_name}-jsp-api.pom
%{_mavendepmapfragdir}/%{pkg_name}-tomcat-jsp-api

%files lib
%defattr(-,root,root,-)
%{libdir}
%{bindir}/tomcat-juli.jar
%{_mavendepmapfragdir}/%{pkg_name}
%{_mavenpomdir}/JPP.%{pkg_name}-annotations-api.pom
%{_mavenpomdir}/JPP.%{pkg_name}-catalina-ha.pom
%{_mavenpomdir}/JPP.%{pkg_name}-catalina-tribes.pom
%{_mavenpomdir}/JPP.%{pkg_name}-catalina.pom
%{_mavenpomdir}/JPP.%{pkg_name}-jasper-el.pom
%{_mavenpomdir}/JPP.%{pkg_name}-jasper.pom
%{_mavenpomdir}/JPP.%{pkg_name}-tomcat-api.pom
%{_mavenpomdir}/JPP.%{pkg_name}-tomcat-juli.pom
%{_mavenpomdir}/JPP.%{pkg_name}-tomcat-coyote.pom
%{_mavenpomdir}/JPP.%{pkg_name}-tomcat-util.pom

%exclude %{libdir}/%{pkg_name}-el-%{elspec}-api.jar

%files servlet-%{servletspec}-api
%defattr(-,root,root,-)
%doc LICENSE
%{_javadir}/%{pkg_name}-servlet-%{servletspec}*.jar
%{_javadir}/%{pkg_name}-servlet-api.jar
%{_mavendepmapfragdir}/%{pkg_name}-tomcat-servlet-api
%{_mavenpomdir}/JPP-%{pkg_name}-servlet-api.pom

%files el-%{elspec}-api
%defattr(-,root,root,-)
%doc LICENSE
%{_javadir}/%{pkg_name}-el-%{elspec}-api.jar
%{_javadir}/%{pkg_name}-el-api.jar
%{libdir}/%{pkg_name}-el-%{elspec}-api.jar
%{_mavenpomdir}/JPP-%{pkg_name}-el-api.pom
%{_mavendepmapfragdir}/%{pkg_name}-tomcat-el-api


%files webapps
%defattr(0644,tomcat,tomcat,0755)
%{appdir}/ROOT
%{appdir}/examples
%{appdir}/sample

%files jsvc
%defattr(755,root,root,0755)
%attr(0644,root,root) %{_unitdir}/%{?scl_prefix}%{pkg_name}-jsvc.service

%changelog
* Mon Oct 09 2017 Romain Philibert <Filirom1@gmail.com> 7.0.82-1
- new package built with tito

* Thu Jun 08 2017 Coty Sutherland <csutherl@redhat.com> 0:7.0.76-2
- Resolves: rhbz#1459747 CVE-2017-5664 tomcat: Security constrained bypass in error page mechanism
- Resolves: rhbz#1441481 CVE-2017-5647 tomcat: Incorrect handling of pipelined requests when send file was used

* Wed Mar 29 2017 Coty Sutherland <csutherl@redhat.com> - 0:7.0.76-1
- Resolves: rhbz#1414895 Rebase tomcat to the current release

* Thu Aug 25 2016 Coty Sutherland <csutherl@redhat.com> - 0:7.0.69-10
- Related: rhbz#1368122

* Tue Aug 23 2016 Coty Sutherland <csutherl@redhat.com> - 0:7.0.69-9
- Resolves: rhbz#1362213 Tomcat: CGI sets environmental variable based on user supplied Proxy request header
- Resolves: rhbz#1368122

* Wed Aug 03 2016 Coty Sutherland <csutherl@redhat.com> - 0:7.0.69-7
- Resolves: rhbz#1362545

* Fri Jul 08 2016 Coty Sutherland <csutherl@redhat.com> - 0:7.0.69-6
- Related: rhbz#1201409 Added /etc/sysconfig/tomcat to the systemd unit for tomcat-jsvc.service

* Fri Jul 01 2016 Coty Sutherland <csutherl@redhat.com> - 0:7.0.69-5
- Resolves: rhbz#1347860 The systemd service unit does not allow tomcat to shut down gracefully

* Mon Jun 27 2016 Coty Sutherland <csutherl@redhat.com> - 0:7.0.69-4
- Resolves: rhbz#1350438 CVE-2016-3092 tomcat: Usage of vulnerable FileUpload package can result in denial of service

* Fri Jun 17 2016 Coty Sutherland <csutherl@redhat.com> - 0:7.0.69-3
- Resolves: rhbz#1347774 The security manager doesn't work correctly (JSPs cannot be compiled)

* Tue Jun 07 2016 Coty Sutherland <csutherl@redhat.com> - 0:7.0.69-2
- Rebase Resolves: rhbz#1311622 Getting NoSuchElementException while handling attributes with empty string value in tomcat
- Rebase Resolves: rhbz#1320853 Add HSTS support
- Rebase Resolves: rhbz#1293292 CVE-2014-7810 tomcat: Tomcat/JBossWeb: security manager bypass via EL expressions
- Rebase Resolves: rhbz#1347144 CVE-2016-0706 tomcat: security manager bypass via StatusManagerServlet
- Rebase Resolves: rhbz#1347139 CVE-2015-5346 tomcat: Session fixation
- Rebase Resolves: rhbz#1347136 CVE-2015-5345 tomcat: directory disclosure
- Rebase Resolves: rhbz#1347129 CVE-2015-5174 tomcat: URL Normalization issue
- Rebase Resolves: rhbz#1347146 CVE-2016-0763 tomcat: security manager bypass via setGlobalContext()
- Rebase Resolves: rhbz#1347142 CVE-2016-0714 tomcat: Security Manager bypass via persistence mechanisms
- Rebase Resolves: rhbz#1347133 CVE-2015-5351 tomcat: CSRF token leak

* Mon Jun 06 2016 Coty Sutherland <csutherl@redhat.com> - 0:7.0.69-1
- Resolves: rhbz#1287928 Rebase to tomcat 7.0.69
- Resolves: rhbz#1327326 rpm -V tomcat fails on /var/log/tomcat/catalina.out
- Resolves: rhbz#1277197 tomcat user has non-existing default shell set
- Resolves: rhbz#1240279 The command tomcat-digest doesn't work with RHEL 7
- Resolves: rhbz#1229476 Tomcat startup ONLY options
- Resolves: rhbz#1133070 Need to include full implementation of tomcat-juli.jar and tomcat-juli-adapters.jar
- Resolves: rhbz#1201409 Fix the broken tomcat-jsvc service unit
- Resolves: rhbz#1221896 tomcat.service loads /etc/sysconfig/tomcat without shell expansion
- Resolves: rhbz#1208402 Mark web.xml in tomcat-admin-webapps as config file

* Tue Mar 24 2015 David Knox <dknox@redhat.com> - 0:7.0.54-2
- Resolves: CVE-2014-0227

* Wed Sep 17 2014 David Knox <dknox@redhat.com> - 0:7.0.54-1
- Resolves: rhbz#1141372 - Remove systemv artifacts. Add new systemd 
- artifacts. Rebase on 7.0.54.

* Wed Jun 18 2014 David Knox <dknox@redhat.com> - 0:7.0.43-6
- Resolves: CVE-2014-0099
- Resolves: CVE-2014-0096
- Resolves: CVE-2014-0075

* Wed Apr 16 2014 David Knox <dknox@redhat.com> - 0:7.0.42-5
- Related: CVE-2013-4286
- Related: CVE-2013-4322
- Related: CVE-2014-0050
- revisit patches for above. 

* Thu Mar 20 2014 David Knox <dknox@redhat.com> - 0:7.0.42-4
- Related: rhbz#1056696 correct packaging for sbin tomcat

* Thu Mar 20 2014 David Knox <dknox@redhat.com> - 0:7.0.42-3
- Related: CVE-2013-4286. increment build number. missed doing
- it. 
- Resolves: rhbz#1038183 remove BR for ant-nodeps. it's
- no long used.

* Wed Jan 22 2014 David Knox <dknox@redhat.com> - 0:7.0.42-2
- Resolves: rhbz#1056673 Invocation of useradd with shell
- other than sbin nologin
- Resolves: rhbz#1056677 preun systemv scriptlet unconditionally
- stops service
- Resolves: rhbz#1056696 init.d tomcat does not conform to RHEL7
- systemd rules. systemv subpackage is removed.
- Resolves: CVE-2013-4286
- Resolves: CVE-2013-4322
- Resolves: CVE-2014-0050
- Built for rhel-7 RC

* Tue Jan 21 2014 David Knox <dknox@redhat.com> - 0:7.0.42-1
- Resolves: rhbz#1051657 update to 7.0.42. Ant-nodeps is
- deprecated.

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 07.0.40-3
- Mass rebuild 2013-12-27

* Sat May 11 2013 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.40-1
- Updated to 7.0.40
- Resolves: rhbz 956569 added missing commons-pool link

* Mon Mar  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:7.0.37-2
- Add depmaps for org.eclipse.jetty.orbit
- Resolves: rhbz#917626

* Wed Feb 20 2013 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.39-1
- Updated to 7.0.39

* Wed Feb 20 2013 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.37-1
- Updated to 7.0.37

* Mon Feb 4 2013 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.35-1
- Updated to 7.0.35
- systemd SuccessExitStatus=143 for proper stop exit code processing

* Mon Dec 24 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.34-1
- Updated to 7.0.34
- ecj >= 4.2.1 now required
- Resolves: rhbz 889395 concat classpath correctly; chdir to $CATALINA_HOME

* Fri Dec 7 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.33-2
- Resolves: rhbz 883806 refix logdir ownership 

* Sun Dec 2 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.33-1
- Updated to 7.0.33
- Resolves: rhbz 873620 need chkconfig for update-alternatives

* Wed Oct 17 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.32-1
- Updated to 7.0.32
- Resolves: rhbz 842620 symlinks to taglibs

* Fri Aug 24 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.29-1
- Updated to 7.0.29
- Add pidfile as tmpfile
- Use systemd for running as unprivileged user
- Resolves: rhbz 847751 upgrade path was broken
- Resolves: rhbz 850343 use new systemd-rpm macros

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:7.0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 2 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.28-1
- Updated to 7.0.28
- Resolves: rhbz 820119 Remove bundled apache-commons-dbcp
- Resolves: rhbz 814900 Added tomcat-coyote POM
- Resolves: rhbz 810775 Remove systemv stuff from %post scriptlet
- Remove redhat-lsb R 

* Mon Apr 9 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.27-2
- Fixed native download hack

* Sat Apr 7 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.27-1
- Updated to 7.0.27
- Fixed jakarta-taglibs-standard BR and R

* Wed Mar 21 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:7.0.26-2
- Add more depmaps to J2EE apis to help jetty/glassfish updates

* Wed Mar 14 2012 Juan Hernandez <juan.hernandez@redhat.com> 0:7.0.26-2
- Added the POM files for tomcat-api and tomcat-util (#803495)

* Wed Feb 22 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.26-1
- Updated to 7.0.26
- Bug 790334: Change ownership of logdir for logrotate

* Thu Feb 16 2012 Krzysztof Daniel <kdaniel@redhat.com> 0:7.0.25-4
- Bug 790694: Priorities of jsp, servlet and el packages updated.

* Wed Feb 8 2012 Krzysztof Daniel <kdaniel@redhat.com> 0:7.0.25-3
- Dropped indirect dependecy to tomcat 5

* Sun Jan 22 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.25-2
- Added hack for maven depmap of tomcat-juli absolute link [ -f ] pass correctly

* Sat Jan 21 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.25-1
- Updated to 7.0.25
- Removed EntityResolver patch (changes already in upstream sources)
- Place poms and depmaps in the same package as jars
- Added javax.servlet.descriptor to export-package of servlet-api
- Move several chkconfig actions and reqs to systemv subpackage
- New maven depmaps generation method
- Add patch to support java7. (patch sent upstream).
- Require java >= 1:1.6.0

* Fri Jan 13 2012 Krzysztof Daniel <kdaniel@redhat.com> 0:7.0.23-5
- Exported javax.servlet.* packages in version 3.0 as 2.6 to make
  servlet-api compatible with Eclipse.

* Thu Jan 12 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.23-4
- Move jsvc support to subpackage

* Wed Jan 11 2012 Alexander Kurtakov <akurtako@redhat.com> 0:7.0.23-2
- Add EntityResolver setter patch to jasper for jetty's need. (patch sent upstream).

* Mon Dec 12 2011 Joseph D. Wagner <joe@josephdwagner.info> 0:7.0.23-3
- Added support to /usr/sbin/tomcat-sysd and /usr/sbin/tomcat for
  starting tomcat with jsvc, which allows tomcat to perform some
  privileged operations (e.g. bind to a port < 1024) and then switch
  identity to a non-privileged user. Must add USE_JSVC="true" to
  /etc/tomcat/tomcat.conf or /etc/sysconfig/tomcat.

* Mon Nov 28 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.23-1
- Updated to 7.0.23

* Fri Nov 11 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.22-2
- Move tomcat-juli.jar to lib package
- Drop %%update_maven_depmap as in tomcat6
- Provide native systemd unit file ported from tomcat6

* Thu Oct 6 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.22-1
- Updated to 7.0.22

* Mon Oct 03 2011 Rex Dieter <rdieter@fedoraproject.org> - 0:7.0.21-3.1
- rebuild (java), rel-eng#4932

* Mon Sep 26 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.21-3
- Fix basedir mode

* Tue Sep 20 2011 Roland Grunberg <rgrunber@redhat.com> 0:7.0.21-2
- Add manifests for el-api, jasper-el, jasper, tomcat, and tomcat-juli.

* Thu Sep 8 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.21-1
- Updated to 7.0.21

* Mon Aug 15 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.20-3
- Require java = 1:1.6.0

* Mon Aug 15 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.20-2
- Require java < 1.7.0

* Mon Aug 15 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.20-1
- Updated to 7.0.20

* Tue Jul 26 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.19-1
- Updated to 7.0.19

* Tue Jun 21 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.16-1
- Updated to 7.0.16

* Mon Jun 6 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.14-3
- Added initial systemd service
- Fix some paths

* Sat May 21 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.14-2
- Fixed http source link
- Securify some permissions
- Added licenses for el-api and servlet-api
- Added dependency on jpackage-utils for the javadoc subpackage

* Sat May 14 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.14-1
- Updated to 7.0.14

* Thu May 5 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.12-4
- Provided local paths for libs
- Fixed dependencies
- Fixed update temp/work cleanup

* Mon May 2 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.12-3
- Fixed package groups
- Fixed some permissions
- Fixed some links
- Removed old tomcat6 crap

* Thu Apr 28 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.12-2
- Package now named just tomcat instead of tomcat7
- Removed Provides:  %{pkg_name}-log4j
- Switched to apache-commons-* names instead of jakarta-commons-* .
- Remove the old changelog
- BR/R java >= 1:1.6.0 , same for java-devel
- Removed old tomcat6 crap

* Wed Apr 27 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.12-1
- Tomcat7
