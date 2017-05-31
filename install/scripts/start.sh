#!/bin/bash

function main {
    # transition from root to daemon user is handled by shibd/httpd; must start as root
    if [ $(id -u) -ne 0 ]; then
        echo "must start shibd and httpd as root"
        exit 1
    fi
    cleanup_and_prep
    start_shibd
    start_httpd
}


function cleanup_and_prep {

    # correct ownership (docker run will reset the ownership of volumes to the uis passed with -u).
    # Only a problem with /etc/shibboleth, where mod_shib needs to have access with the httpd id
    chown -R $SHIBDUSER:shibd  /etc/shibboleth

    # Make sure we're not confused by old, incompletely-shutdown shibd or httpd
    # context after restarting the container. httpd and shibd won't start correctly                                                                                                                                                        # if thinking it is already running.
    rm -rf /var/lock/subsys/shibd  \
           /run/httpd/*
    su - $SHIBDUSER  -c '[ -e /run/shibboleth/shibd.sock ] && rm /run/shibboleth/shibd.*'
}


function start_shibd {
    /usr/sbin/shibd -u $SHIBDUSER -g root -p /var/run/shibboleth/shib.pid > /var/log/startup/start.log 2>&1
}


function start_httpd {
    # do not start with root to avoid permission conflicts on log files
    chown $HTTPDUSER:root /run/httpd/
    su - $HTTPDUSER  -c 'httpd -DFOREGROUND -d /etc/httpd/ -f conf/httpd.conf'  >> /var/log/startup/start.log 2>&1
}


main
