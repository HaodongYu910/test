<template>
    <div class="details">
        <div class="top">
            <div class="title">
                <div class="title-left">
                    <span>神外-30-test</span>
                    <span class="mode">web前端</span>
                    <span class="mode">
            <i class="el-icon-suitcase"></i>
            测试</span
                    >
                </div>
                <div class="title-right">
                    <el-button type="primary" icon="el-icon-orange">构建</el-button>
                    <el-button icon="el-icon-edit">编辑</el-button>
                    <el-button type="danger" icon="el-icon-delete-solid">删除</el-button>
                </div>
            </div>
            <div class="status">
                <span>状态：</span>
                <span>打包成功</span>
            </div>
        </div>
        <div class="build bg-color">
            <el-steps
                    :active="stepActive"
                    finish-status="success"
                    class="build-step"
                    align-center
            >
                <el-step
                        title="更新源码"
                        :icon="stepActive === 0 ? 'el-icon-loading' : 'el-icon-refresh'"
                ></el-step>
                <el-step
                        title="依赖集成"
                        :icon="stepActive === 1 ? 'el-icon-loading' : 'el-icon-sold-out'"
                ></el-step>
                <el-step
                        title="打包"
                        :icon="stepActive === 2 ? 'el-icon-loading' : 'el-icon-s-cooperation'"
                ></el-step>
                <el-step
                        title="打包成功"
                        :icon="stepActive === 3 ? 'el-icon-loading' : 'el-icon-finished'"
                ></el-step>
            </el-steps>
            <div class="build-title">构建历史</div>
            <div class="build-list">
                <div class="build-item build-item-title">
                    <span>构建序号</span>
                    <span>构建分支</span>
                    <span>状态</span>
                    <span>发起人</span>
                    <span>开始时间</span>
                    <span>操作</span>
                </div>
                <div class="build-item" v-for="(item, index) in buildList" :key="index">
                    <span>{{ item.job }}</span>
                    <span>{{ item.branch }}</span>
                    <span>{{ item.service }}</span>
                    <span>{{ item.user }}</span>
                    <span>{{ item.create_time }}</span>
                    <span class="highlight">
            <el-button type="text" class="operation-item"
                       @click="checkExpress(item)"> 查看日志
                            </el-button>

            </span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {
        getBuildDetail,
        submitPublishAddTaskService,
        submitPublishUpdateTaskService,
        submitPublishDeleteTaskService,
        PublishEnableTaskService,
        PublishDisableTaskService,
        queryGitBranchService,
        queryGit,
        getHost
    } from "./../../router/api";

    export default {
        name: "publishDetail",
        // el-icon-loading
        data() {
            return {
                buildList: [],
                stepActive: 1,
            };
        },
        created() {
            this.getParams();
        },
        activated() {
            this.getParams();
        },
        methods: {
            //获取由路由传递过来的参数
            getParams() {
                this.build_id = this.$route.query.id;
                this.jenkins_job= this.$route.query.jenkins_job;
                this.jenkins_view= this.$route.query.jenkins_view;
                this.BuildDetail();
            },
            // 获取数据列表
            BuildDetail() {
                this.listLoading = true
                const self = this
                const params = {
                    build_id: this.build_id,
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getBuildDetail(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.buildList = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            //展示监控
            checkExpress: function (item) {

                const url = "http://10.10.10.2:8095/view/" + this.jenkins_view + "/job/" + this.jenkins_job +"/"+ item.job + "/consoleText"
                const dualScreenLeft = window.screenLeft !== undefined ? window.screenLeft : screen.left
                const dualScreenTop = window.screenTop !== undefined ? window.screenTop : screen.top

                const width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width
                const height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height

                const left = ((width / 2) - (1500 / 2)) + dualScreenLeft
                const top = ((height / 2) - (800 / 2)) + dualScreenTop
                const newWindow = window.open(url, '集成日志', 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=yes, copyhistory=no, width=' + '1500' + ', height=' + '800' + ', top=' + top + ', left=' + left)

                // Puts focus on the newWindow
                if (window.focus) {
                    newWindow.focus()
                }
            },
            handleCurrentChange(val) {
                this.page = val
                this.getDurationlist()
            },

            selsChange: function (sels) {
                this.sels = sels
            }
        }
    };

</script>

<style lang="scss" scoped>
    .details {
        width: 100%;
        height: 100%;
        font-size: 15px;
        color: #333;
        display: flex;
        flex-direction: column;

        .top {
            background-color: #fff;
            padding: 15px;
            margin-bottom: 10px;
        }

        .title {
            display: flex;
            width: 100%;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 10px;
            background-color: #fff;

            &-left {
                > span {
                    display: inline-block;
                    margin-right: 20px;

                    &:first-child {
                        font-size: 16px;
                        font-weight: bold;
                    }
                }
            }
        }

        .bg-color {
            background-color: #fff;
        }

        .build {
            flex: 1;
            background-color: #fff;

            &-title {
                font-weight: 500;
                margin-bottom: 10px;
                padding: 15px;
            }

            &-list {
                width: 100%;
            }

            &-item {
                width: 100%;
                display: flex;
                align-items: center;
                font-size: 13px;
                height: 40px;
                border-bottom: 1px solid #f0f0f0;

                > span {
                    flex: 1;
                    text-align: center;
                }

                &-title {
                    font-weight: 500;

                    background-color: #fafafa;
                    display: flex;
                    align-items: center;
                    font-size: 13px;
                    font-weight: 500;

                    > span {
                        flex: 1;
                        text-align: center;
                        position: relative;

                        &::after {
                            position: absolute;
                            right: 0;
                            top: 10%;
                            content: "";
                            display: block;
                            background-color: #ddd;
                            width: 1px;
                            height: 80%;
                        }
                    }
                }

                .highlight {
                    color: #1890ff;
                    cursor: pointer;
                }
            }

            &-step {
                padding-top: 20px;
            }

            .el-step__icon.is-icon {
                color: #1890ff;
            }

            .is-wait {
                font-size: 13px !important;
                font-weight: 500;
            }
        }
    }
</style>
