#! /bin/bash

version=$1
package_name=$2
path=$3



echo ""
echo "================================================================================"
echo "                          Download AI Engine"
echo "                          Install: <engine_version>: "
echo "================================================================================"
echo ""
echo "Instructions:"

###  version
echo "#####################$version ########################"
echo $package_name
echo $path
### removing ago folder
echo "#################### old build has been removed ############################"
sudo rm -rf $version
sudo rm -rf $package_name

mkdir QInstall
### ans for downloading packages and docker_registry

my_var=`rclone ls $path`

echo $my_var

echo "#################### rclone download $version ############################"
rclone copy -P $path /home/biomind/ --transfers=8


echo "#################### tar|| zip - $name   ############################"
if [[ ${$package_name##*.} == "zip" ]];then
    echo "unzip -o $package_name"
    unzip -o $package_name
else
    echo "tar -zxvf $package_name"
    tar -zxvf $package_name
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
