<template>
    <div class="header">
        <!-- 折叠按钮 -->
        <div class="collapse-btn" @click="collapseChage">
            <img class="blogo" src="../../assets/img/logo.png"/>
        </div>
        <div class="logo">Biomind Test</div>
        <div class="logo">
                <span class="el-head-title">
                项目空间：
              </span>
            <el-dropdown  @command="handleCommand" @click.native="getProjectList">
              <span class="el-head-info">
                {{projectname}}<i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item  v-for="(item,index) in projectList"
                                   :command="item.name"
                                   >{{item.name}}</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
        </div>
        <div class="header-right">
            <div class="header-user-con">
                <!-- 全屏显示 -->
                <div class="btn-fullscreen" @click="handleFullScreen">
                    <el-tooltip effect="dark" :content="fullscreen?`取消全屏`:`全屏`" placement="bottom">
                        <i class="el-icon-rank"></i>
                    </el-tooltip>
                </div>
                <!-- 消息中心 -->
                <div class="btn-bell">
                    <el-tooltip effect="dark" :content="message?`有${message}条未读消息`:`消息中心`" placement="bottom">
                        <router-link to="/tabs">
                            <i class="el-icon-bell"></i>
                        </router-link>
                    </el-tooltip>
                    <span class="btn-bell-badge" v-if="message"></span>
                </div>
                <!-- 用户头像 -->
                <div class="user-avator"><img src="../../assets/img/aitouxiang.png"></div>
                <!-- 用户名下拉菜单 -->
                <el-dropdown class="user-name" trigger="click" @command="handleCommand">
                    <span class="el-dropdown-link">
                        {{username}} <i class="el-icon-caret-bottom"></i>
                    </span>
                    <el-dropdown-menu slot="dropdown">
                        <a href="" target="_blank">
                            <el-dropdown-item>设置</el-dropdown-item>
                        </a>
                        <el-dropdown-item divided  command="loginout">退出登录</el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
            </div>
        </div>
    </div>
</template>
<script>
    import {getProject} from '../../router/api';
    import bus from '../../utils/bus';
    export default {
        data() {
            return {
                collapse: false,
                fullscreen: false,
                projectname: '晨曦',
                message: 2,
                projectList:{},
            }
        },
        mounted() {
            this.getProjectID()
            this.getProjectList()
        },
        computed:{
            username(){
                let username = localStorage.getItem('ms_username');
                return username ? username : this.name;
            }
        },
        methods:{
            // 获取详细项目信息
            getProjectID() {
                this.listLoading = true;
                let self = this;
                let params = {name:this.projectname};
                let headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))};
                getProject(headers, params).then((res) => {
                    self.listLoading = false;
                    let {msg, code, data} = res;
                    if (code === '0') {
                        self.total = data.total;
                        self.projectData = data.data

                        localStorage.removeItem("project_id");
                        localStorage.setItem("project_id", self.projectData[0]["id"]);
                        localStorage.removeItem("projectname");
                        localStorage.setItem("projectname",this.projectname);
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }

                });
            },
            // 获取项目列表
            getProjectList() {
                this.listLoading = true;
                let self = this;
                let params = {page_size:999};
                let headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))};
                getProject(headers, params).then((res) => {
                    self.listLoading = false;
                    let {msg, code, data} = res;
                    if (code === '0') {
                        self.total = data.total;
                        self.projectList = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                })
            },
            // 用户名下拉菜单选择事件
            handleCommand(command) {
                if(command == 'loginout'){
                    localStorage.removeItem('ms_username')
                    this.$router.push('/login');
                }
                else {
                    this.projectname =command
                    this.$message('切换' + command +'项目');
                    this.getProjectID()
                }
              },
            // 侧边栏折叠
            collapseChage(){
                this.collapse = !this.collapse;
                bus.$emit('collapse', this.collapse);
            },
            // 全屏事件
            handleFullScreen(){
                let element = document.documentElement;
                if (this.fullscreen) {
                    if (document.exitFullscreen) {
                        document.exitFullscreen();
                    } else if (document.webkitCancelFullScreen) {
                        document.webkitCancelFullScreen();
                    } else if (document.mozCancelFullScreen) {
                        document.mozCancelFullScreen();
                    } else if (document.msExitFullscreen) {
                        document.msExitFullscreen();
                    }
                } else {
                    if (element.requestFullscreen) {
                        element.requestFullscreen();
                    } else if (element.webkitRequestFullScreen) {
                        element.webkitRequestFullScreen();
                    } else if (element.mozRequestFullScreen) {
                        element.mozRequestFullScreen();
                    } else if (element.msRequestFullscreen) {
                        // IE11
                        element.msRequestFullscreen();
                    }
                }
                this.fullscreen = !this.fullscreen;
            }
        },
        mounted(){
            if(document.body.clientWidth < 1500){
                this.collapseChage();
            }
        }
    }
</script>
<style scoped>
    .header {
        position: relative;
        box-sizing: border-box;
        width: 100%;
        height: 70px;
        font-size: 22px;
        color: #fff;
    }
    .collapse-btn{
        float: left;
        padding: 0 21px;
        cursor: pointer;
        line-height: 100px;
        display: table-cell;
        vertical-align: middle;
        text-align: center;
    }
    .header .logo{
        float: left;
        width:250px;
        line-height: 70px;
    }
    .blogo {
        float: left;
        width:40px;
        line-height: 40px;
        display: table-cell;
        vertical-align: middle;
        text-align: center;
        margin-top: 12.5px;
    }
    .header-right{
        float: right;
        padding-right: 50px;
    }
    .header-user-con{
        display: flex;
        height: 70px;
        align-items: center;
    }
    .btn-fullscreen{
        transform: rotate(45deg);
        margin-right: 5px;
        font-size: 24px;
    }
    .btn-bell, .btn-fullscreen{
        position: relative;
        width: 30px;
        height: 30px;
        text-align: center;
        border-radius: 15px;
        cursor: pointer;
    }
    .btn-bell-badge{
        position: absolute;
        right: 0;
        top: -2px;
        width: 8px;
        height: 8px;
        border-radius: 4px;
        background: #f56c6c;
        color: #fff;
    }
    .btn-bell .el-icon-bell{
        color: #fff;
    }
    .user-name{
        margin-left: 10px;
    }
    .user-avator{
        margin-left: 20px;
    }
    .user-avator img{
        display: block;
        width:40px;
        height:40px;
        border-radius: 50%;
    }
    .el-dropdown-link{
        color: #fff;
        cursor: pointer;
    }
    .el-head-title{

        color: #fff;
        font-size: 14px;
        font-family:"微软雅黑","PingFang SC";
        cursor: pointer;
    }
    .el-head-info{
        color: #fff;
        font-size: 12px;
        font-family:"微软雅黑","PingFang SC";
        cursor: pointer;
    }
    .el-dropdown-menu__item{
        text-align: center;
    }
    .el-dropdown-link {
        cursor: pointer;
        color: #f1f2f3;
    }
    .el-icon-arrow-down {
        font-size: 12px;
    }
</style>
