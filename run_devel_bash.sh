docker kill 46sp4testedupvat
docker rm 46sp4testedupvat

docker run -i -t --rm -u 0 --hostname=46sp4testedupvat --name=46sp4testedupvat -e SHIBDUSER=shibd46 -e HTTPDUSER=httpd46 --net dockernet --ip 10.1.1.46 -v 46sp4testedupvat.etc_httpd_conf:/etc/httpd/conf:Z -v 46sp4testedupvat.etc_httpd_conf.d:/etc/httpd/conf.d:Z -v 46sp4testedupvat.etc_shibboleth:/etc/shibboleth:Z -v 46sp4testedupvat.etc_shibboleth-ds:/etc/shibboleth-ds:Z -v 40pyff.var_md_feed:/opt/md_feed:ro -v 46sp4testedupvat.var_log:/var/log:Z -v 46sp4testedupvat.var_www:/var/www:Z r2h2/sp4testedupvat46 bash

