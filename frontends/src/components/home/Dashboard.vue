<template>
    <div>
        <el-row :gutter="20">
            <el-col :span="9">
                <el-card shadow="hover" class="mgb20" style="height:252px;">
                    <div class="user-info">
                        <img src="../../assets/img/aitouxiang.png" class="user-avator" alt="">
                        <div class="user-info-cont">
                            <div class="user-info-name">{{name}}</div>
                            <div>{{role}}</div>
                        </div>
                    </div>
                    <div class="user-info-list">上次登录时间：<span style="margin-left: 10px">{{ date_joined  | dateformat('YYYY-MM-DD HH:mm:ss')}}</span>
                    </div>
                    <div class="user-info-list">上次登录地点：<span>北京</span></div>
                </el-card>
                <el-card shadow="hover" style="height:350px;">

                </el-card>
                <!--版本下载-->
            </el-col>
            <el-col :span="15">
                <!--用户访问量、系统消息、数量-->
                <el-row :gutter="20" class="mgb20">
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{padding: '0px'}">
                            <div class="grid-content grid-con-1">
                                <i class="el-icon-lx-read grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">10</div>
                                    <div>当前任务</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{padding: '0px'}">
                            <div class="grid-content grid-con-2">
                                <i class="el-icon-lx-text grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">12</div>
                                    <div>待处理任务</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{padding: '0px'}">
                            <div class="grid-content grid-con-3">
                                <i class="el-icon-lx-warn grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">5</div>
                                    <div>已完成任务</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
                <div>
                    <ve-line
                            :set-option-opts="false"
                            :data="chartData"
                            :data-zoom="chartDataZoom">
                    </ve-line>

                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    export default {
        name: 'dashboard',
        date_joined: '2019-06-06',
        data() {

            this.chartDataZoom = [{type: 'slider'}]
            return {
                name: localStorage.getItem('ms_username'),
                date_joined: localStorage.getItem('date_joined'),
                chartData: {
                    columns: ["日期", "创建问题", "解决问题"],
                    rows: [
                        {日期: "1/1", 创建问题: 13, 解决问题: 10, 解决率: 0.32},
                        {日期: "1/2", 创建问题: 35, 解决问题: 32, 解决率: 0.26},
                        {日期: "1/3", 创建问题: 29, 解决问题: 26, 解决率: 0.76},
                        {日期: "1/4", 创建问题: 17, 解决问题: 14, 解决率: 0.49},
                        {日期: "1/5", 创建问题: 37, 解决问题: 34, 解决率: 0.323},
                        {日期: "1/6", 创建问题: 45, 解决问题: 42, 解决率: 0.78}
                    ]
                },
            }
        },
        components: {},
        mounted() {
        },
        computed: {
            role() {
                return this.name === 'admin' ? '超级管理员' : '普通用户';
            }
        },
        created() {

        },
        methods: {
            change() {
                this.chartData.rows.push({
                    '日期': '1/1',
                    '访问用户': Math.random() * 1000,
                    '下单用户': Math.random() * 1000
                })
            },
            //初始化数据
            getData() {
                let params = {
                    user: 'yinhang'
                };
                let headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                };
                loadtodo(headers, params).then(_data => {
                    let {code, msg, data} = _data;
                    if (_data.length == 0) {
                        this.todoData = null;
                        return;
                    }

                });
            },
            //     //获取由路由传递过来的参数
            //     getParams(){
            //         this.routerParams=this.$route.query;
            //     },

        }
    }

</script>


<style scoped>
    .el-row {
        margin-bottom: 20px;
    }

    .grid-content {
        display: flex;
        align-items: center;
        height: 100px;
    }

    .grid-cont-right {
        flex: 1;
        text-align: center;
        font-size: 14px;
        color: #999;
    }

    .grid-num {
        font-size: 30px;
        font-weight: bold;
    }

    .grid-con-icon {
        font-size: 50px;
        width: 100px;
        height: 100px;
        text-align: center;
        line-height: 100px;
        color: #fff;
    }

    .grid-con-1 .grid-con-icon {
        background: rgb(45, 140, 240);
    }

    .grid-con-1 .grid-num {
        color: rgb(45, 140, 240);
    }

    .grid-con-2 .grid-con-icon {
        background: rgb(100, 213, 114);
    }

    .grid-con-2 .grid-num {
        color: rgb(45, 140, 240);
    }

    .grid-con-3 .grid-con-icon {
        background: rgb(242, 94, 67);
    }

    .grid-con-3 .grid-num {
        color: rgb(242, 94, 67);
    }

    .user-info {
        display: flex;
        align-items: center;
        padding-bottom: 20px;
        border-bottom: 2px solid #ccc;
        margin-bottom: 20px;
    }

    .user-avator {
        width: 120px;
        height: 120px;
        border-radius: 50%;
    }

    .user-info-cont {
        padding-left: 50px;
        flex: 1;
        font-size: 14px;
        color: #999;
    }

    .user-info-cont div:first-child {
        font-size: 30px;
        color: #222;
    }

    .user-info-list {
        font-size: 14px;
        color: #999;
        line-height: 25px;
    }

    .user-info-list span {
        margin-left: 70px;
    }

    .mgb20 {
        margin-bottom: 20px;
    }


</style>
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             