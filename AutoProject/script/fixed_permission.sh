#!/bin/bash

### report
biomind report prod master
sleep 10

echo ""
echo "fixed permission"
### fixed permssion
bash ~/.biomind/lib/current/installer/biomind.sh install
sleep 5

echo ""
echo "restart AI-engine"
biomind stop
sleep 10

cp config .biomind/

biomind start
sleep 10

echo "restart finished"
