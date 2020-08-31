<template>
    <div>
        <el-row :gutter="20">
            <el-col :span="9">
                <el-card shadow="hover" class="mgb20" style="height:252px;">
                    <div class="user-info">
                        <img src="../../assets/img/img.jpg" class="user-avator" alt="">
                        <div class="user-info-cont">
                            <div class="user-info-name">{{name}}</div>
                            <div>{{role}}</div>
                        </div>
                    </div>
                    <div class="user-info-list">上次登录时间：<span style="margin-left: 10px">{{ date_joined  | dateformat('YYYY-MM-DD HH:mm:ss')}}</span></div>
                    <div class="user-info-list">上次登录地点：<span>北京</span></div>
                </el-card>
                <el-card shadow="hover" style="height:350px;">
                    <el-row :gutter="20">
                        <el-col :span="12">
                            <el-card shadow="hover">
                                <div id='bishijieBar' class="mybar"
                                     style="width: 250px;height: 310px;margin:0 auto;">
                                </div>
                            </el-card>
                        </el-col>
                    </el-row>
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
                                    <div>待处理Bug</div>
                                    <div class="grid-num">{{bug}}</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{padding: '0px'}">
                            <div class="grid-content grid-con-2">
                                <i class="el-icon-lx-text grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">{{todo}}</div>
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
                                    <div class="grid-num">{{online}}</div>
                                    <div>待处理线上问题</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
                <el-card shadow="hover">
                    <div id='bishijieLine' class="myLine" style="width:100%;height:350px;margin:0 auto">
                    </div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    import echarts from 'echarts';
    import {loadFigure} from "../../router/api";
    import {loadtodo} from "../../router/api";

    export default {
        name: 'dashboard',
        date_joined: '2019-06-06',
        data() {
            return {
                name: localStorage.getItem('ms_username'),
                date_joined: localStorage.getItem('date_joined'),
                //定义表
                bishijieBar: {},
                bishijieLine: {},
                coinnessBar: {},
                coinnessLine: {},
                //定义表数据
                bishijieBarData: [],
                bishijieLineData: [],
                coinnessBarData: [],
                coinnessLineData: [],
                twoData: [],
                //定义表数据对应的option数据
                bishijieBaroption: {
                    backgroundColor: '#2c343c',
                    title: {
                        text: 'Boimind-Bug解决数量状态图',
                        left: 'center',
                        top: 20,
                        textStyle: {
                            color: '#ccc'
                        }
                    },
                    tooltip: {
                        trigger: 'item',
                        formatter: "{a} <br/>{b} : {c} ({d}%)"
                    },
                    series: [
                        {
                            name: 'Bug状态',
                            type: 'pie',
                            radius: '55%',
                            center: ['50%', '60%'],
                            data: [],
                            itemStyle: {
                                emphasis: {
                                    shadowBlur: 10,
                                    shadowOffsetX: 0,
                                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                                },
                                normal: {
                                    label: {
                                        show: function (value) {
                                            if (value == 0.00) return false;
                                        }(),
                                        formatter: '{b} : {c} ({d}%)'
                                    },
                                    labelLine: {
                                        show: function (value) {
                                            if (value == 0.00) return false;
                                        }()
                                    }
                                }
                            }
                        }
                    ]
                },
                coinnessBaroption: {
                    backgroundColor: '#2c343c',
                    title: {
                        text: 'CoinNess-Bug解决数量状态图',
                        left: 'center',
                        top: 20,
                        textStyle: {
                            color: '#ccc'
                        }
                    },
                    tooltip: {
                        trigger: 'item',
                        formatter: "{a} <br/>{b} : {c} ({d}%)"
                    },
                    series: [
                        {
                            name: 'Bug状态',
                            type: 'pie',
                            radius: '55%',
                            center: ['50%', '60%'],
                            data: [],
                            itemStyle: {
                                emphasis: {
                                    shadowBlur: 10,
                                    shadowOffsetX: 0,
                                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                                },
                                normal: {
                                    label: {
                                        show: function (value) {
                                            if (value == 0.00) return false;
                                        }(),
                                        formatter: '{b} : {c} ({d}%)'
                                    },
                                    labelLine: {
                                        show: function (value) {
                                            if (value == 0.00) return false;
                                        }()
                                    }
                                }
                            }
                        }
                    ]
                },
                bishijieLineoption: {
                    title: {
                        text: 'Boimind-创建与解决问题对比图'
                    },
                    tooltip: {
                        trigger: 'axis',
                        padding: 25
                    },
                    legend: {
                        data: ['创建问题', '解决问题'],
                        padding: 25
                    },
                    toolbox: {
                        show: true,
                        feature: {
                            dataZoom: {
                                yAxisIndex: 'none'
                            },
                            dataView: {readOnly: true},
                            magicType: {type: ['line', 'bar']},
                            restore: {},
                            saveAsImage: {}
                        }
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: []
                    },
                    yAxis: {
                        type: 'value',
                        axisLabel: {
                            formatter: '{value} 个'
                        }
                    },
                    series: [
                        {
                            name: '创建问题',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: '解决问题',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        }
                    ]
                },
                coinnessLineoption: {
                    title: {
                        text: 'CoinNess-创建与解决问题对比图'
                    },
                    tooltip: {
                        trigger: 'axis',
                        padding: 25
                    },
                    legend: {
                        data: ['创建问题', '解决问题'],
                        padding: 25
                    },
                    toolbox: {
                        show: true,
                        feature: {
                            dataZoom: {
                                yAxisIndex: 'none'
                            },
                            dataView: {readOnly: true},
                            magicType: {type: ['line', 'bar']},
                            restore: {},
                            saveAsImage: {}
                        }
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: []
                    },
                    yAxis: {
                        type: 'value',
                        axisLabel: {
                            formatter: '{value} 个'
                        }
                    },
                    series: [
                        {
                            name: '创建问题',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: '解决问题',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        }
                    ]
                }
            }
        },
        components: {},
        mounted() {
            this.drawbishijieBar();
            this.drawCoinNessBar();
            this.drawbishijieLine();
            this.drawCoinNessLine();
        },
        computed: {
            role() {
                return this.name === 'admin' ? '超级管理员' : '普通用户';
            }
        },
        created() {
            this.getbishijieData();
            //'CoinNess-App-缺陷'
            this.getCoinnessData();
            this.getData();

        },
        watch: {
            //观察option的变化
            bishijieBaroption: {
                handler(newVal, oldVal) {
                    if (this.bishijieBar) {
                        if (newVal) {
                            this.bishijieBar.setOption(newVal);
                        } else {
                            this.bishijieBar.setOption(oldVal);
                        }
                    } else {
                        this.drawbishijieBar();
                    }
                },
                deep: true //对象内部属性的监听，关键。
            },
            bishijieLineoption: {
                handler(newVal, oldVal) {
                    if (this.bishijieBar) {
                        if (newVal) {
                            this.bishijieLine.setOption(newVal);
                        } else {
                            this.bishijieLine.setOption(oldVal);
                        }
                    } else {
                        this.drawbishijieLine();
                    }
                },
                deep: true //对象内部属性的监听，关键。
            },
            coinnessBaroption: {
                handler(newVal, oldVal) {
                    if (this.coinnessBar) {
                        if (newVal) {
                            this.coinnessBar.setOption(newVal);
                        } else {
                            this.coinnessBar.setOption(oldVal);
                        }
                    } else {
                        this.drawCoinNessBar();
                    }
                },
                deep: true //对象内部属性的监听，关键。
            },
            coinnessLineoption: {
                handler(newVal, oldVal) {
                    if (this.coinnessBar) {
                        if (newVal) {
                            this.coinnessLine.setOption(newVal);
                        } else {
                            this.coinnessLine.setOption(oldVal);
                        }
                    } else {
                        this.drawCoinNessLine();
                    }
                },
                deep: true //对象内部属性的监听，关键。
            }
        },
       todoData:[],

        methods: {
            //初始化数据
            getData(){
                let params ={
                    user:'yinhang'
                };
                let headers= {
                    'Content-Type': 'application/x-www-form-urlencoded'
                };
                loadtodo(headers,params).then(_data=>{
                    let {code, msg, data} = _data;
                    if(_data.length==0) {
                        this.todoData=null;
                        return;
                    }

                    this.totalData = data.total;
                    this.bug = this.totalData[0];
                    this.todo = this.totalData[1];
                    this.online = this.totalData[2];
                    console.log(this.bug);
                });
            },
        //     //获取由路由传递过来的参数
        //     getParams(){
        //         this.routerParams=this.$route.query;
        //     },
            getbishijieData() {
                let params = {
                    "project": "BUG",
                    "service": "Boimind-APP-缺陷",
                    "sprint_version": "",
                    "starttime": "",
                    "days": 7,
                    "status": "",
                    "component": "",
                    "priority": ""
                };
                let headers = {
                    "Content-Type": "application/json"
                };
                loadFigure(headers, params).then(_data => {
                    let {code, msg, data} = _data;
                    this.bishijieLineData = data.figure_list;
                    this.bishijieLineoption.xAxis.data = this.bishijieLineData[0];
                    this.bishijieLineoption.series[0].data = this.bishijieLineData[1];
                    this.bishijieLineoption.series[1].data = this.bishijieLineData[2];

                    this.bishijieBarData = data.solution_state.sort(function (a, b) {
                        return a.value - b.value;
                    });
                    this.bishijieBaroption.series[0].data = this.bishijieBarData;

                });
            },
            getCoinnessData() {
                let params = {
                    "project": "BUG",
                    "service": "CoinNess-APP-缺陷",
                    "sprint_version": "",
                    "starttime": "",
                    "days": 7,
                    "status": "",
                    "component": "",
                    "priority": ""
                };
                let headers = {
                    "Content-Type": "application/json"
                };
                loadFigure(headers, params).then(_data => {
                    let {code, msg, data} = _data;
                    this.coinnessLineData = data.figure_list;
                    this.coinnessLineoption.xAxis.data = this.coinnessLineData[0];
                    this.coinnessLineoption.series[0].data = this.coinnessLineData[1];
                    this.coinnessLineoption.series[1].data = this.coinnessLineData[2];
                    this.coinnessBarData = data.solution_state.sort(function (a, b) {
                        return a.value - b.value;
                    });
                    this.coinnessBaroption.series[0].data = this.coinnessBarData;
                });
            },
            drawbishijieBar() {
                this.bishijieBar = echarts.init(document.getElementById('bishijieBar'));
                this.bishijieBar.setOption(this.bishijieBaroption, true);
                setTimeout(() => {
                    window.onresize = bishijieBar.resize;
                }, 200);
            },
            drawCoinNessBar() {
                this.coinnessBar = echarts.init(document.getElementById('coinnessBar'));
                this.coinnessBar.setOption(this.coinnessBaroption, true);
                setTimeout(() => {
                    window.onresize = coinnessBar.resize;
                }, 200);
            },
            drawbishijieLine() {
                this.bishijieLine = echarts.init(document.getElementById('bishijieLine'));
                this.bishijieLine.setOption(this.bishijieLineoption);
                setTimeout(() => {
                    window.onresize = bishijieLine.resize;
                }, 200);
            },
            drawCoinNessLine() {
                this.coinnessLine = echarts.init(document.getElementById('coinnessLine'));
                this.coinnessLine.setOption(this.coinnessLineoption);
                setTimeout(() => {
                    window.onresize = coinnessLine.resize;
                }, 200);
            },
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