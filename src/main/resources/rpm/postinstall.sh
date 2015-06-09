#/bin/sh

if [ "$1" = "1" ]; then

   # configure chkconfig
   chkconfig --add spring-xd-admin
   chkconfig --add spring-xd-container

   ln -s /opt/pivotal/spring-xd/shell/bin/xd-shell /usr/bin/xd-shell

fi
