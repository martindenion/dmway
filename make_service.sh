#!/bin/bash

if [ $# -ne 4 ]
then
echo "dmway service enabled and ready to be used"
exit 1
fi

NAME=$1
SCRIPT_FILE=$2
AFTER=$3
REMAIN_AFTER_EXIT=$4

SERVICE_FILE="/etc/systemd/system/$1.service"
echo "[Unit]" >$SERVICE_FILE
echo "Description=Service basique pour lancer $SCRIPT_FILE" >>$SERVICE_FILE
echo "After=$AFTER" >>$SERVICE_FILE
echo "Requires=$AFTER" >>$SERVICE_FILE
echo "[Service]"  >>$SERVICE_FILE
if [ "$REMAIN_AFTER_EXIT" == "no" ]
then echo "Type=simple" >>$SERVICE_FILE;
else echo "Type=forking" >>$SERVICE_FILE; fi
echo "ExecStart=/usr/bin/python3 $SCRIPT_FILE" >>$SERVICE_FILE
echo "TimeoutSec=0" >>$SERVICE_FILE
echo "RemainAfterExit=$REMAIN_AFTER_EXIT" >>$SERVICE_FILE
echo "SysVStartPriority=99" >>$SERVICE_FILE
echo "RestartSec=5" >>$SERVICE_FILE
echo "Restart=on-failure" >>$SERVICE_FILE
echo "[Install]" >>$SERVICE_FILE
echo "WantedBy=multi-user.target" >>$SERVICE_FILE
chmod 755 $SCRIPT_FILE
systemctl -q enable $NAME
