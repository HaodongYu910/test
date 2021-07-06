#! /bin/bash

echo ""
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "+"
echo "+                       Running server Monitor setup"
echo "+"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo ""

sudo grep &> /dev/null

print () {
    printf "$1"
}

step=1;
print_check() {
    printf "\n| Step - %2d | $1\n\n" "$step"
    step=$((step + 1));
}

print_ok() { 
    print "\n[     OK    ]\n\n"
}

print_warn() {
    print "\n[   WARN    ]: $1\n\n"
}

throw_error() {
    print "\n[   ERROR   ]: $1\n\n"
    exit 1;
}

# Get zipped monitor installer package from nextcloud.
get_dependencies() {
    if [ ! -d ./monitor ]; then
        # Download
        if [ ! -f ./monitor.zip ]; then
            sudo wget https://ifileserver.biomind.com.cn/index.php/s/4dMqo7F2meb4cTp/download -O ./monitor.zip --no-check-certificate
            if [ $? -ne 0 ]; then
                exit 1;
            fi
        fi
        sudo unzip ./monitor.zip
        if [ $? -ne 0 ]; then
            exit 2;
        fi
    fi
}

#==============================================================================
# Remove UseDNS option to speedup ssh login
#==============================================================================
print_check "Check sshd_config"
if [ -f /etc/ssh/sshd_config ]; then
    sudo grep -Fxq "#UseDNS yes" /etc/ssh/sshd_config
    if [ $? -eq 0 ]; then
        sudo sed -i 's/#UseDNS yes/UseDNS no/' /etc/ssh/sshd_config
        sudo systemctl restart sshd
        print 'sshd_config removed UseDNS\n\n'
    fi
    print_ok
else
    print_warn "/etc/ssh/sshd_config file not found"
fi

#==============================================================================
# Check LFS 
#==============================================================================
print_check "Check lfs"
if [ ! -d /lfs ]; then
    throw_error "/lfs not mounted"
else
    print_ok
fi

#==============================================================================
# Check for monitor files
#==============================================================================
print_check "Checking monitor.zip"
get_dependencies
if [ $? -ne 0 ]; then
    if [ $? -eq 1 ]; then
        throw_error "Failed to download monitor.zip"
    elif [ $? -eq 2 ]; then
        throw_error "Failed to unzip monitor.zip"
    fi
else
    # Create local yum repo
    repo=/etc/yum.repos.d/bmlocal.repo
    print "Create local yum repo $repo"
    echo "[bmlocal.repo]" | sudo tee $repo
    echo "name=bmlocal.repo" | sudo tee -a $repo
    echo "baseurl=file://$PWD/monitor/yum" | sudo tee -a $repo
    echo "enabled=1" | sudo tee -a $repo
    echo "gpgcheck=0" | sudo tee -a $repo
    print_ok
fi


#==============================================================================
# Install and update GPU packages
#==============================================================================
print_check "Install and update GPU packages"
sudo rpm -ivh ./monitor/datacenter-gpu-manager-1.7.2-1.x86_64.rpm
sudo cp ./monitor/dcgm/dcgm-exporter /usr/local/bin/ 
sudo cp ./monitor/dcgm/node_exporter /usr/local/bin/
sudo cp ./monitor/dcgm/prometheus-dcgm.service  /etc/systemd/system/
sudo cp ./monitor/dcgm/prometheus-node-exporter.service  /etc/systemd/system/
sudo systemctl enable dcgm.service
sudo systemctl start dcgm.service
sudo systemctl daemon-reload
sudo systemctl enable prometheus-dcgm.service
sudo systemctl enable prometheus-node-exporter.service
sudo systemctl start prometheus-dcgm.service
sudo systemctl start prometheus-node-exporter.service

if [ $? -ne 0 ]; then
    throw_error "GPU packages install error"
else
    print_ok
fi

#==============================================================================
# Open firewall port
#==============================================================================

print_check "Open firewall port"
sudo firewall-cmd --permanent --zone=public --add-port=9100/tcp
sudo firewall-cmd --permanent --zone=public --add-port=9209/tcp
sudo firewall-cmd --permanent --zone=public --add-port=9187/tcp
sudo firewall-cmd --reload
if [ $? -ne 0 ]; then
    sudo firewall-cmd --reload
    print "added $USER to firewall trusted zone\n\n"
fi
print_ok

#==============================================================================
# Install docker postgres 鐩戞帶
#==============================================================================
# Add /lfs/docker directory as docker image path
print_check "Install docker "
# 查看进程是否存在
# exist=`docker inspect --format '{{.State.Running}}' google/cadvisor`
# if [ "${exist}" != "true" ]; then
sudo docker load -i ./monitor/cadvisor.tar
sudo docker run --volume=/:/rootfs:ro  --volume=/var/run:/var/run:ro --volume=/sys:/sys:ro --volume=/var/lib/docker/:/var/lib/docker:ro --volume=/dev/disk/:/dev/disk:ro --volume=/cgroup:/cgroup:ro --privileged=true --publish=8080:8080 --detach=true --name=cadvisor google/cadvisor
sudo docker load -i ./monitor/postgres.tar
sudo docker run -itd --name postgres_exporter -p 9187:9187 -e DATA_SOURCE_NAME="postgresql://postgres:4a53e4f5c42fd5a31890860b204472c5@localhost:5432/orthanc?sslmode=disable" wrouesnel/postgres_exporter
#记录日志
echo "${now} 重启docker容器，容器名称：google/cadvisor"


if [ $? -ne 0 ]; then
    throw_error "GPU packages install error"
else
    print_ok
fi

#
# Complete
#
print "\nSetup Completed\n\n"

#==============================================================================
# Install and update  PM2 packages
#==============================================================================
print_check "Install and update PM2 packages"
sudo tar -xvf ./monitor/node-v12.4.0-linux-x64.tar.gz
sudo cp -r ./monitor/node-v12.4.0-linux-x64 /var/local/node-v12.4.0-linux-x64
sudo rm -rf /usr/bin/node
sudo rm -rf /usr/bin/npm
sudo rm -rf /usr/bin/pm2
sudo ln -s /var/local/node-v12.4.0-linux-x64/bin/node /usr/bin/node
sudo ln -s /var/local/node-v12.4.0-linux-x64/bin/npm /usr/bin/npm
sudo ln -s /var/local/node-v12.4.0-linux-x64/bin/pm2 /usr/bin/pm2
sudo npm install -g pm2
sudo pm2 install pm2-metrics
sudo npm install
sudo cp -r ./monitor/pm2-prometheus-exporter /var/local/pm2-prometheus-exporter
sudo pm2 start /var/local/pm2-prometheus-exporter/exporter.js --name pm2-metrics

if [ $? -ne 0 ]; then
    throw_error "pm2 install error"
else
    print_ok
fi