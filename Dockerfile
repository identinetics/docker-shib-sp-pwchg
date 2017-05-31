#FROM centos:centos7
#RUN yum -y install curl httpd ip lsof mod_php mod_ssl net-tools
#COPY install/security:shibboleth.repo /etc/yum.repos.d
# above command cannot be executed on a system with --storage-opt=AUFS
# therefore build shib-spbase on other system and load it:
FROM rhoerbe/shib-spbase
LABEL maintainer="Rainer Hörbe <r2h2@hoerbe.at>" \
      version="0.0.0" \
      # by default, remove all capabilities, but add those required to change the user
      capabilities='--cap-drop=all --cap-add=setuid --cap-add=setgid --cap-add=chown --cap-add=net_raw'

# allow build behind firewall
ARG HTTPS_PROXY=''

RUN echo $'export LD_LIBRARY_PATH=/opt/shibboleth/lib64:$LD_LIBRARY_PATH\n' > /etc/sysconfig/shibd \
 && chmod +x /etc/sysconfig/shibd

# Run as a non-root user, separate uids for httpd and shibd, with common group shibd.
# Allow httpd/mod_shib access to /var/run/shibboleth and /etc/shibboleth using group shibd
# Prevent yum to create default uid for shibd to control user mapping between host and container

ARG HTTPDUSER=httpd
ARG HTTPDUID=344005
ARG SHIBDGID=343005
RUN groupadd --gid $SHIBDGID shibd \
 && adduser --gid $SHIBDGID --uid $HTTPDUID $HTTPDUSER \
 && mkdir -p /var/log/httpd /run/httpd \
 && chown -R $HTTPDUID:0 /etc/httpd /var/log/httpd /run/httpd \
 && rm -rf /etc/httpd/modules /etc/httpd/logs /etc/httpd/run \
 && ln -s /usr/lib64/httpd/modules /etc/httpd/modules\
 && ln -s /var/log/httpd /etc/httpd/logs \
 && ln -s /run/httpd /etc/httpd/run


# First add user "shibd" and install shibboleth SP, then rename to "$SHIBUSER".
# Set permissions for shibd user to write to /var/cache and /var/run /var/log
ARG SHIBDUSER=shibd
ARG SHIBDUID=343005
RUN adduser --gid $SHIBDGID --uid $SHIBDUID shibd \
 && mkdir -p /var/log/shibboleth /var/run/shibboleth/ \
 && chown $SHIBDUID:$SHIBDGID /var/log/shibboleth /var/run/shibboleth/ \
 && yum -y install httpd shibboleth.x86_64 shibboleth-embedded-ds \
 && yum -y clean all \
 # key material is useless on an image -> remove!
 && rm -f /etc/shibboleth/sp-cert.pem /etc/shibboleth/sp-key.pem  \
 && chmod 700 /var/log/shibboleth \
 && chmod 750 /var/run/shibboleth/ /etc/shibboleth \
 && [ "$SHIBDUSER" == 'shibd' ] || usermod -l $SHIBDUSER shibd

RUN yum -y install epel-release
RUN yum -y install python34 wget httpd-devel python34-devel gcc python34-pip
RUN useradd wsgi
RUN pip3 install --upgrade pip setuptools
RUN pip3 install mod_wsgi \
 && cp /usr/lib64/python3.4/site-packages/mod_wsgi/server/mod_wsgi-py34.cpython-34m.so /etc/httpd/modules/mod_wsgi.so

## WARNING: This is ugly!
# we are referencing in r/w user space here because that is, where our app is now.
# TODO: docroot could not be a volume in a stable release

COPY install/requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt


COPY install/scripts/*.sh /




RUN chmod +x /*.sh \
 && mkdir /var/log/startup \
 && chmod 777 /var/log/startup  # miust be writeable by root

CMD /start.sh

VOLUME /etc/httpd/conf \
       /etc/httpd/conf.d \
       /etc/shibboleth \
       /var/log \
       /var/www
