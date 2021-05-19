#! /bin/bash
#
echo ""
echo "================================================================================"
echo "                          Download AI Engine"
echo "                          Install: <engine_version>: "
echo "================================================================================"
echo ""
echo "Instructions:"


###  version
echo "#####################   version ########################"
version=$1


### removing ago folder
echo "#################### old build has been removed ############################"
sudo rm -rf $version

### ans for downloading packages and docker_registry

my_var=`rclone ls oss://biomind-ha-se/versions/$version.tgz`

echo $my_var

echo "#################### rclone download $version ############################"
rclone copy -P oss://biomind-ha-se/versions/$version.tgz /home/biomind/ --transfers=8


echo "#################### pigz -p 8 -d $version.tgz  ############################"
pigz -p 8 -d $version.tgz
tar -xvf $version.tar

echo "################################### installing $version AI Engine ###################################"
cd ~/$version
bash setup_engine.sh

sleep 2

echo ""
echo "################################## install 3D modules ######################################"
### install biomind 3D
cd ~/$version/engine/deps/Biomind-3D/
bash setup_install prod master
sleep 2

### set the permission
#sudo chown biomind:biomind -R ~/.biomind/var/biomind/*

echo ""
echo "################################### fixed permission ###########################################"
echo " "
### fixed permssion
bash ~/.biomind/lib/current/installer/biomind.sh install
sleep 5

echo ""
echo "################################### config ###########################################"
echo " "
### fixed permssion
mv orthanc.json /home/biomind/.biomind/var/biomind/orthanc/orthanc.json
mv cache /home/biomind/.biomind/var/biomind/cache

### report
#biomind report prod master

#echo ""
#echo "fixed permission"
### fixed permssion
#bash ~/.biomind/lib/current/installer/biomind.sh install


echo "##################################### installation has been done #############################"
