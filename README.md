### 安装说明 ###
前端：vue cil 3.0 
后端框架： django rest framework
数据库： mysql
python 3.6版本以上

## 本地开发-安装步骤 ##
git@git.biomind.com.cn:QA/Biomind_Test_Platform.git      // 下载到本地

## pipenv // 管理虚拟环境
pip3 install pipenv // 安装 pipenv
pipenv install --three   // 项目所在目录下运行,安装虚拟环境以及项目所需的依赖包
pipenv shell  // 进入虚拟环境

## 手动创建虚拟环境
pip install virtualenv  // 为一个工程创建一个虚拟环境：
$ virtualenv -p /usr/bin/python3.6 project_env  // venv为虚拟环境目录名，目录名自定义
$ source env/bin/activate // 要开始使用虚拟环境，其需要被激活
$ deactivate //停用虚拟环境 
pip freeze > requirements.txt    //生成
pip install -r requirements.txt  //导入

## 同步数据库 ## 
python manage.py makemigrations
python manage.py migrate

## 创建超级用户 ## 
python manage.py createsuperuser

## 本地开发 ##
python3 manage.py runserver 0.0.0.0:8000 // 起django服务 

## 构建生产 ##
# uwsgi配置
pip install uwsgi     // 安装uwsgi
uwsgi.ini             // 创建文件 参考test.ini
uwsgi --ini test.ini  // 启动uwsgi
killall -9 uwsgi      // 关闭
# 测试 uwsgi --http :8000 --home=/usr/project_env  --wsgi-file test.py

# nginx 启动
sudo service nginx reload 
sudo service nginx restart 
/path/to/nginx -s reload

#nginx授权
chown :www-data /usr/project_env/platform/test/
chown :www-data /usr/project_env/platform/test/uwsgi.sock
chmod g+rw /usr/project_env/platform/test/uwsgi.sock
# crontab定时任务处理
$ python manage.py crontab add     // 添加
$ python manage.py crontab show    // 展示
$ python manage.py crontab remove  // 移除

python manage.py collectstatic     //后台样式

## 使用说明 ##

### AutoTest ###
settings.py // 配置文件
urls.py     //总路由文件

### AutoUI ###
基于unittest框架 编写的ui自动化管理
### frontends ###
前端代码
### TestPlatform ###
api    // 接口
common // 公共方法
serializer.py //序列化
# 序列化：将程序中的一个数据结构类型转换为其他格式（JSON、XML等），例如：将Django中的模型类对象装换为JSON字符串，这个转换过程我们称为序列化。简单来说：对象 -> 字典 -> json
# 反序列化：将其他格式（JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象，这个过程我们称为反序列化。简单来说：json -> 字典 -> 对象

### models 说明用法 ###
Django ORM model 常用过滤属性
常用的过滤属性
属性	SQL元
__exact	like 'aaa'
__iexact	忽略大小写 ilike 'aaa
__contains	包含 like '%aaa%'
__icontains	包含 忽略大小写 ilike '%aaa%'
__gt	大于
__gte	大于等于
__lt	小于
__lte	小于等于
__in	存在于一个list范围内
__startswith	以...开头
__istartswith	以...开头 忽略大小写
__endswith	以...结尾
__iendswith	以...结尾，忽略大小写
__range	在...范围内
__year	日期字段的年份
__month	日期字段的月份
__day	日期字段的日
__isnull	True/False
__isnull	True 与 __exact=None的区别

## docker 建立方式 ##
  cd Biomind_Test_platform
  
  docker build -f dockerfile -t qa:{current_tag} .
  
  docker save -o qa:{current_tag}.tar qa:{current_tag}
  
  sh qa_platform.sh install qa:{current_tag}.tar
  
  qa start


## 其他注意事项 ##
python-ldap出现编译错误解决方法：
sudo apt-get install libldap2-dev
sudo apt-get install libsasl2-dev

## 项目截图 ##







