#! /bin/bash

version=$1
versions="2.18.4-istroke 2.19.1-radiology 2.19.0-radiology 2.18.4-radiology 2.18.3-radiology 2.18.3-istroke 2.18.2-radiology 2.18.1-radiology 2.18.5-radiology 2.18.6-radiology 2.18.7-radiology 2.19.2-radiology 2.19.3-radiology 2.19.4-radiology 2.19.5-radiology 2.19.6-radiology"

echo ""
echo "================================================================================"
echo "                          Download AI Engine"
echo "                          Install: <engine_version>: "
echo "================================================================================"
echo ""
echo "Instructions:"

###  version
echo "#####################$version ########################"

if [[ $versions == *$version* ]];then
  name="${version}.zip"
  echo "包含 ${name}"
else
  name="${version}.tgz"
  echo "不包含 ${name}"
fi

### removing ago folder
echo "#################### old build has been removed ############################"
sudo rm -rf $version $name
mkdir QInstall
### ans for downloading packages and docker_registry

my_var=`rclone ls oss://biomind-ha-se/versions/$name`

echo $my_var

echo "#################### rclone download $version ############################"
rclone copy -P oss://biomind-ha-se/versions/$name /home/biomind/ --transfers=8


echo "#################### tar|| zip - $name   ############################"
if [[ $versions == *$version* ]];then
    echo "unzip -o ${version}.zip"
    unzip -o "${version}.zip"
else
    echo "tar -zxvf ${version}.tgz"
    tar -zxvf "${version}.tgz"
fi

echo "################################### installing $version AI Engine ###################################"
cd ~/$version
sshpass -p biomind bash setup_engine.sh

sleep 2

#echo ""
#echo "################################## install 3D modules ######################################"
#### install biomind 3D
#cd ~/$version/engine/deps/Biomind-3D/
#bash setup_install prod master
#sleep 2
#
#### set the permission
##sudo chown biomind:biomind -R ~/.biomind/var/biomind/*

echo ""
echo "################################### fixed permission ###########################################"
echo " "
### fixed permssion
bash ~/.biomind/lib/current/installer/biomind.sh install
sleep 3
echo ""
echo "################################### cache config ###########################################"
echo ""
echo "rm -rf QInstall"
sudo rm -rf /home/biomind/QInstall
echo "mv -b -f /home/biomind/orthanc.json /home/biomind/.biomind/var/biomind/orthanc/orthanc.json"
mv -b -f /home/biomind/orthanc.json /home/biomind/.biomind/var/biomind/orthanc/orthanc.json
echo "mv -b -f /home/biomind/cache/ /home/biomind/.biomind/var/biomind/"
mv -b -f /home/biomind/cache/ /home/biomind/.biomind/var/biomind/

### report
#biomind report prod master
#echo ""
#echo "fixed permission"
### fixed permssion
#bash ~/.biomind/lib/current/installer/biomind.sh install
echo "##################################### installation has been done #############################"
