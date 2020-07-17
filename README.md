Linux环境
pipenv 管理虚拟环境
安装 pipenv：pip3 install pipenv
下载代码之后，进入项目运行 pipenv install --three--安装虚拟环境以及项目所需的依赖包
进入虚拟环境：pipenv shell 
手动创建
pip install virtualenv
为一个工程创建一个虚拟环境：
$ virtualenv -p /usr/bin/python3.6 project_env  #venv为虚拟环境目录名，目录名自定义
要开始使用虚拟环境，其需要被激活：
$ source env/bin/activate

python-ldap出现编译错误解决方法：
sudo apt-get install libldap2-dev
sudo apt-get install libsasl2-dev

生成pip freeze > requirements.txt
导入pip install -r requirements.txt
停用虚拟环境 deactivate

# 同步数据库
# python manage.py makemigrations
# python manage.py migrate
# python服务 python3 manage.py runserver 0.0.0.0:8000

uwsgi配置
# pip install uwsgi
# 创建uwsgi.ini文件 见test.ini

启动uwsgi
uwsgi --ini test.ini
# 测试 uwsgi --http :8000 --home=/usr/project_env  --wsgi-file test.py
# killall -9 uwsgi 关闭

1.pip install https://github.com/darklow/django-suit/tarball/v2
2.安装VUE环境，下载node.js并配置环境，下载npm包管理器，安装vue脚手架用于生成vue工程模板
npm install --global vue-cli
3.cmd进入frontend目录下，运行npm install安装相关依赖包
4.打包 npm run build
5.起本地服务 npm run serve


#nginx
sudo service nginx reload 或 sudo service nginx restart 或 /path/to/nginx -s reload

#nginx授权
chown :www-data /usr/project_env/platform/test/
chown :www-data /usr/project_env/platform/test/uwsgi.sock
chmod g+rw /usr/project_env/platform/test/uwsgi.sock


