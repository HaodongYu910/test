

## remove all docker images
docker rmi -f $(docker images -qa)
sleep 1

docker system prune --all --force
sleep 1

### remove the files and folders

sudo rm -rf ~/$engine_version
sleep 1

sudo rm -rf /lfs/docker/volumes/*
sleep 1

sudo rm -rf /lfs/biomind
sleep 1

sudo rm -rf /lfs/Biomind-3DServer
sleep 1

sudo rm -rf ~/.biomind/lib/versions
sudo rm -rf ~/.biomind/lib/biomind-model-repository
sudo rm -rf ~/.biomind/lib/current
sudo rm -rf ~/.biomind/lib/installer
sleep 1

sudo rm -rf ~/.biomind/var

sudo rm -rf ~/.3D-biomind
sleep 1

sudo rm -rf /etc/yum.repos.d/3dlocal.repo
sleep 1
