#! /bin/bash

version=$1
package_name=$2
path=$3
passwd=$4
reset=$5


echo ""
echo "================================================================================"
echo "                          Download AI Engine $version"
echo "                          Install: <engine_version>: $version"
echo "================================================================================"
echo ""
echo "Instructions:"


echo "##################### stop old version  ########################"
sshpass -p $passwd biomind stop
###  version

### removing ago folder
echo "#################### old build has been removed ############################"
sudo rm -rf $version
sudo rm -rf $package_name

echo "#################### backups old version orthanc.json and  cache ############################"
cp -rf /home/biomind/.biomind/var/biomind/orthanc/orthanc.json /home/biomind/orthanc.json
cp -rf /home/biomind/.biomind/var/biomind/cache/ /home/biomind/cache

if [ $? -eq 0 ]; then
     echo "backups succeed"
else
     echo "backups failed"
fi

### ans for downloading packages and docker_registry
echo "##################### rclone download $version  ########################"
echo $package_name
echo $path
my_var=`rclone ls $path`

echo $my_var

rclone copy -P $path /home/biomind/ --transfers=8


echo "#################### tar|| zip - $name   ############################"
if [[ ${package_name##*.} == "zip" ]];then
    echo "unzip -o $package_name"
    unzip -o $package_name
else
    echo "tar -zxvf $package_name"
    tar -zxvf $package_name
fi

echo "################################### installing $version AI Engine ###################################"
cd ~/$version

sshpass -p biomind bash setup_engine.sh

#echo ""
#echo "################################### fixed permission ###########################################"
#echo " "
### fixed permssion
# bash ~/.biomind/lib/current/installer/biomind.sh install
#sleep 3
#echo ""
if [ $reset = y ]; then
  echo "################################### cache config ###########################################"
  echo "mv -b -f /home/biomind/orthanc.json /home/biomind/.biomind/var/biomind/orthanc/orthanc.json"
  cp -rf /home/biomind/orthanc.json /home/biomind/.biomind/var/biomind/orthanc/orthanc.json
  echo "mv -b -f /home/biomind/cache/ /home/biomind/.biomind/var/biomind/"
  cp -rf /home/biomind/cache/ /home/biomind/.biomind/var/biomind/
fi
### report
#biomind report prod master
#echo ""
#echo "fixed permission"
### fixed permssion
#bash ~/.biomind/lib/current/installer/biomind.sh install
echo "##################################### installation has been done #############################"
