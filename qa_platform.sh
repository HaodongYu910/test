#!/bin/bash
set -e
# all parameters passed to script
command=$1
image_tar=$2

source ~/.bashrc
echo "Current QA_Platform_HOME: $QA_Platform_HOME"

bash_profile=~/.bashrc

#get image:tag
get_image_tag(){
    source ~/.bashrc
    cd $QA_Platform_HOME
    image_tag="qa:$QA_Platform_TAG"

}

if [[ $command = install ]]; then
    PROJECTDIR=$(pwd)
    echo $PROJECTDIR
    # load image
    res=$(docker load -i $image_tar)
    # get tag
    tag=$(sed -e 's/.*://' <<< $res)
    echo $tag

    sudo cp ./qa_platform.sh /usr/local/bin/qa
    sudo chmod +x /usr/local/bin/qa

    echo "Setting QA Platform home path"
    echo "export QA_Platform_HOME=${PROJECTDIR}" >> $bash_profile
    echo "export QA_Platform_TAG=${tag}" >> $bash_profile

    source $bash_profile

    echo "Done"

    echo "Current QA_Platform_HOME: $QA_Platform_HOME"
elif [[ $command = start ]]; then
    # source ~/.bashrc
    cd $QA_Platform_HOME
    image_tag="qa:$QA_Platform_TAG"

    if docker ps -a  | grep -w -q -i "qa"; then
        docker ps -a  | grep "qa" | awk '{print $1}' | xargs docker rm -f 
    fi
    docker run --restart always -d --net="host" -it --name 'qa' -p 9000:9000 -v `pwd`:/usr/src/Biomind_Test_Platform $image_tag
    echo "biomind test platform start success"
fi
