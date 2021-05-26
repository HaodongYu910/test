#! /bin/bash
# 
# bash download_offline_package.sh --with-image
# bash download_offline_package.sh 

echo ""
echo "================================================================================"
echo "                          Download AI Engine package"
echo "                 Output: <engine_version> folder and zipped file"
echo "================================================================================"
echo ""
echo "Instructions:"
echo "1. this machine should have awscli, get_token installed, to download docker-images."
echo "2. to skip downloading models/images, skip entering version number" 
echo "3. if models/engine/docker-images folder already exists, it will skip downloading accordingly too" 
echo "4. enter the correct versions (models/engine/docker-images) for AI engine to start smoothly"

### export ip path

echo "######################  exporting path #######################"
export PATH=/usr/sbin:$PATH

### model version
echo "#####################  model version ########################"
model_version=$1


### date
time=$(date +%Y%m%d)
time2=$(date +%Y%m%d -d "5 day ago")


#time="20201208"

### enginer_version with nightly build and time
engine_version=$2"-nightly-"$time


### removing 5 days ago folder
oldFile="*-nightly-$time2"
echo "#################### old nighlty build $oldFile has been removed ############################"
sudo rm -rf $oldFile


### ans for downloading packages and docker_registry
ans="y"
docker_registry="biomind-registry-vpc.cn-beijing.cr.aliyuncs.com"


#### biomind stop the production 
echo "##################### stop the biomind engine ################################"
biomind stop prod master
sleep 5

if [ -z $engine_version ]; then
    echo "ERROR: engine_version cannot be empty..."
    exit 1;
fi

echo ""
echo "================================================================================"
echo ""
echo "Engine version: $engine_version"
echo "Model version: $model_version"
#echo "Docker-images version: $img_version"
echo ""

if [ ! -d "$engine_version" ]; then
    mkdir $engine_version
fi

## download models
if [ ! -d "$engine_version/models" -a ! -z $model_version ]; then
    echo "Models                                                          [ DOWNLOADING ]"
    echo "" 
    mkdir $engine_version/models
    rclone copy oss://biomind-ha-rt/biomind-model-repository/$model_version ./$engine_version/models
    #while [ $? -eq 0 ]
    #do
    #    echo "redownload again due to incomplete"
    #    rclone copy oss://biomind-ha-rt/biomind-model-repository/$model_version ./$engine_version/models
    #done
    printf "\n\n"
fi

## download engine
if [ ! -d "$engine_version/engine" -a ! -z $engine_version ]; then
    echo "Engine                                                          [ DOWNLOADING ]" 
    echo "" 
    mkdir $engine_version/engine
    rclone copy oss://biomind-ha-se/versions/$engine_version ./$engine_version/engine

    # copy setup_engine.sh
    if [ -z "./$engine_version/engine/installer/setup_engine.sh" ]; then
        echo "ERROR: setup_engine.sh not found. exiting..."
        exit 1;
    else 
        cp ./$engine_version/engine/installer/setup_engine.sh ./$engine_version/.
    fi
    printf "\n\n"
fi

## download docker-images 
if [ "$img_option" = --with-image -o "$ans" = y ] && [ ! -d "$engine_version/docker-images" ]; then
    echo "Docker-images                                                   [ DOWNLOADING ]" 
    echo "" 
    mkdir $engine_version/docker-images
    #bash ./$engine_version/engine/installer/install_docker_images.sh $img_version
    # save images 
    #images=$(sed -n '/images=(/,/)/p' ./$engine_version/engine/installer/install_docker_images.sh | grep -Ev "\(|\)" | sed '/^[[:space:]]*$/d' | awk '{$1=$1};1')
    images=$(sed -n -e 's/^.*image: ${DOCKER_REGISTRY}//p' ~/$engine_version/engine/docker-compose.yml)
    while read -r line; do
        echo $line
        line2=$docker_registry$line
        docker pull $line2
	#dname=$(sed "s/[:/]_/g" <<< "$line2")
        dname=$(sed "s/[:/]/_/g" <<< "$line2")
        #echo $dname
        echo "exporting $line2 -> ./$engine_version/docker-images/$dname.docker"
        #docker save -o ./$engine_version/docker-images/$dname.docker $line2
    done <<< "$images"
    printf "\n\n"
fi 

# download 3D env
download_3D="y"
if [ $download_3D = y ]; then
    echo "3D                                                               [ DOWNLOADING ]"
    mkdir $engine_version/3D
    
    version_3d=${engine_version:0:4}
    echo "++++++++++++++++++++++++++++++++ start download Installer-3D.zip +++++++++++++++++++++++++++++"
    rclone copy oss://biomind-ha-se/3D/$version_3d/Installer-3D.zip ./$engine_version/3D

    echo "++++++++++++++++++++++++++++++++ start download setup_install    +++++++++++++++++++++++++++++"
    rclone copy oss://biomind-ha-se/3D/$version_3d/setup_install ./$engine_version/3D
fi


## zip up
#if [ -f "$engine_version.zip" ]; then
#    echo "$engine_version.zip exists already"
#    echo "Rezipping                                                       [   ZIPPING   ]"
#    echo zip -r $engine_version.zip $engine_version 
#else 
#    echo "Zipping                                                         [   ZIPPING   ]"
#    echo zip -r $engine_version.zip $engine_version  
#fi

#printf "\n\n"
#echo "Offline package is downloaded :    $(pwd)/$engine_version"
#echo "Zipped package is downloaded  :    $(pwd)/$engine_version.zip"
#echo "Download Completed"

### rm the same version

#docker stop $(docker ps -aq)

echo "################################### installing AI Engine ###################################"
cd ~/$engine_version
bash setup_engine.sh

sleep 2

echo ""
echo "################################## install 3D modules ######################################"
### install biomind 3D
cd ~/$engine_version/engine/deps/Biomind-3D/
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
