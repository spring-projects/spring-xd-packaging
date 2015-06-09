#!/bin/sh

if [ "$1" = "0" ]; then
   # stop proc
   service spring-xd-container stop > /dev/null
   service spring-xd-admin stop > /dev/null

   # remove from chkconfig
   chkconfig --del spring-xd-container
   chkconfig --del spring-xd-admin

   rm -f /opt/pivotal/spring-xd/xd/logs/*

fi
