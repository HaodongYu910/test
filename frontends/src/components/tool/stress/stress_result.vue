<template>
    <div class="app-container">

        <div class="filter-container">
            <!--工具条-->
            <el-col :span="100" class="toolbar" style="padding-bottom: 0px;">
                <aside>
                    <a href="http://192.168.2.38:3000/d/Ss3q6hSZk/docker-and-os-metrics-test?orgId=1&refresh=5s&from=now-5m&to=now&var-host_name=192.168.2.60&var-gpu_exporter_port=9445&var-node_exporter_port=9100&var-cadvisor_port=8080" target="_blank">Stress Monitor
                    </a>
                </aside>

                <!--工具条-->
                <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
                    <el-form :inline="true" :model="filters" @submit.native.prevent>
                        <el-select v-model="filters.server"  placeholder="请选择服务器" @click.native="gethost()">
                              <el-option
                                v-for="(item,index) in tags"
                                :key="item.host"
                                :label="item.name"
                                :value="item.host"
                              />
                            </el-select>
                        <el-select v-model="filters.version"  placeholder="当前版本" @click.native="getversion()">
                              <el-option
                                v-for="(item,index) in versions"
                                :key="item.version"
                                :label="item.version"
                                :value="item.version"
                              />
                            </el-select>
                        <el-select v-model="filters.checkversion"  placeholder="以前版本" @click.native="getversion()">
                              <el-option
                                v-for="(item,index) in versions"
                                :key="item.version"
                                :label="item.version"
                                :value="item.version"
                              />
                            </el-select>
                        <el-form-item>
                            <el-button type="primary" @click="getDurationlist">查询</el-button>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="handleAdd">生成报告</el-button>
                        </el-form-item>
                    </el-form>
                </el-col>
                <el-card shadow="hover" style="height:350px;">
                        <el-row :gutter="20">
                            <el-col :span="12">
                                <el-card shadow="hover">
                                    <div id='reportBar' class="mybar"
                                             style="width: 250px;height: 310px;margin:0 auto;">
                                    </div>
                                </el-card>
                            </el-col>
                        </el-row>
                    </el-card>

                <!--列表-->
                <span style="margin-left: 10px">prediction time</span>
                <el-table :data="prediction" v-loading="listLoading"
                          @selection-change="selsChange"
                          style="width: 100%;">
                    <el-table-column prop="modelname" label="modelname" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.modelname }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="prediction_count" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.count }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="avg pred time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.avg }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="median pred time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.median }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="min pred time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.min}}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="max pred time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.max }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="status" label="coef. of variation" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.coef }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="rate of success" min-width="8%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.rate }}</span>
                        </template>
                    </el-table-column>
                </el-table>

                <span style="margin-left: 10px">job time</span>
                <el-table :data="job" highlight-current-row v-loading="listLoading"
                          @selection-change="selsChange"
                          style="width: 100%;">
                    <el-table-column prop="version" label="modelname" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.modelname }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="job_count" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.count }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="avg job time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.avg }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="avg single job time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.single }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="median job time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.median }} 秒</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="min job time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.min }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="max job time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.max }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="status" label="coef. of variation" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.coef }}</span>
                        </template>
                    </el-table-column>
                </el-table>
                <span style="margin-left: 10px">Lung prediction time</span>
                <el-table :data="lung" highlight-current-row v-loading="listLoading"
                          @selection-change="selsChange"
                          style="width: 100%;">
                    <el-table-column prop="version" label="slicenumber" min-width="6%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.slicenumber }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="avg pred time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.avg }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="median pred time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.median }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="min pred time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.min }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="max pred time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.max }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="coef. of variation" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.coef }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="rate of success" min-width="8%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.rate }}</span>
                        </template>
                    </el-table-column>
                </el-table>
            </el-col>
        </div>
    </div>
</template>

<script>
    // import NProgress from 'nprogress'

    import {
        getstressversion,getstressresult, getHost,getreportfigure
    } from '@/router/api';
    import echarts from "echarts";
  export default {
    // import ElRow from "element-ui/packages/row/src/row";
        // components: {ElRow},
        data() {
            return {
                filters: {
                    diseases: ''
                },
                durationlist: [],
                total: 0,
                page: 1,
                listLoading: false,
                sels: [], // 列表选中列

                //定义表
                reportBar: {},
                reportLine: {},
                coinnessBar: {},
                coinnessLine: {},
                //定义表数据
                reportBarData: [],
                reportLineData: [],
                coinnessBarData: [],
                coinnessLineData: [],
                twoData: [],
                //定义表数据对应的option数据
                reportBaroption: {
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
                reportLineoption: {
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
            this.drawreportBar();
            this.drawCoinNessBar();
            this.drawreportLine();
            this.drawCoinNessLine();
        },
        computed: {
            role() {
                return this.name === 'admin' ? '超级管理员' : '普通用户';
            }
        },
        created() {
            this.getreportData();
            //'CoinNess-App-缺陷'
            this.getCoinnessData();
            this.getData();

        },
        watch: {
            //观察option的变化
            reportBaroption: {
                handler(newVal, oldVal) {
                    if (this.reportBar) {
                        if (newVal) {
                            this.reportBar.setOption(newVal);
                        } else {
                            this.reportBar.setOption(oldVal);
                        }
                    } else {
                        this.drawreportBar();
                    }
                },
                deep: true //对象内部属性的监听，关键。
            },
            reportLineoption: {
                handler(newVal, oldVal) {
                    if (this.reportBar) {
                        if (newVal) {
                            this.reportLine.setOption(newVal);
                        } else {
                            this.reportLine.setOption(oldVal);
                        }
                    } else {
                        this.drawreportLine();
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
        mounted() {
            this.getDurationlist()
            this.gethost()
            this.getBase()
        },
        methods: {
            // 压测版本
            getversion() {
                this.listLoading = true
                const self = this
                const params = {}
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getstressversion(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total
                        self.list = data.data
                        var json = JSON.stringify(self.list)
                        this.versions = JSON.parse(json)
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },

            // 获取host数据列表
            gethost() {
                this.listLoading = true
                const self = this
                const params = {}
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getHost(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total
                        self.list = data.data
                        var json = JSON.stringify(self.list)
                        this.tags = JSON.parse(json)
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            // 获取数据列表
            getDurationlist() {
                this.listLoading = true
                const self = this
                const params = {
                    version: this.filters.version,
                    checkversion: this.filters.checkversion,
                    server: this.filters.server
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getstressresult(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.prediction = data.predictionresult
                        self.job =data.jobresult
                        self.lung =data.lungresult
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            selsChange: function (sels) {
                this.sels = sels
            },
        //     //获取由路由传递过来的参数
        //     getParams(){
        //         this.routerParams=this.$route.query;
        //     },
            getreportData() {
                let params = {
                    "checkversion": "BUG",
                    "version": "Boimind"
                };
                let headers = {
                    "Content-Type": "application/json"
                };
                getreportfigure(headers, params).then(_data => {
                    let {code, msg, data} = _data;
                    this.reportLineData = data.figure_list;
                    this.reportLineoption.xAxis.data = this.reportLineData[0];
                    this.reportLineoption.series[0].data = this.reportLineData[1];
                    this.reportLineoption.series[1].data = this.reportLineData[2];

                    this.reportBarData = data.solution_state.sort(function (a, b) {
                        return a.value - b.value;
                    });
                    this.reportBaroption.series[0].data = this.reportBarData;

                });
            },
            getCoinnessData() {
                let params = {
                    "checkversion": "BUG",
                    "version": "Boimind"
                };
                let headers = {
                    "Content-Type": "application/json"
                };
                getreportfigure(headers, params).then(_data => {
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
            drawreportBar() {
                this.reportBar = echarts.init(document.getElementById('reportBar'));
                this.reportBar.setOption(this.reportBaroption, true);
                setTimeout(() => {
                    window.onresize = reportBar.resize;
                }, 200);
            },
            drawCoinNessBar() {
                this.coinnessBar = echarts.init(document.getElementById('coinnessBar'));
                this.coinnessBar.setOption(this.coinnessBaroption, true);
                setTimeout(() => {
                    window.onresize = coinnessBar.resize;
                }, 200);
            },
            drawreportLine() {
                this.reportLine = echarts.init(document.getElementById('reportLine'));
                this.reportLine.setOption(this.reportLineoption);
                setTimeout(() => {
                    window.onresize = reportLine.resize;
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
    .edit-input {
        padding-right: 100px;
    }

    .cancel-btn {
        position: absolute;
        right: 15px;
        top: 10px;
    }
    .view-png {
        width:15px;
        height:15px;
        margin-right:3px;
        margin-bottom:5px
    }
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
