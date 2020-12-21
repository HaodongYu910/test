<template>
    <div class="app-container">

        <div class="filter-container">
            <!--工具条-->
            <el-col :span="100" class="toolbar" style="padding-bottom: 0px;">
                <el-card shadow="hover" style="width:100%;height:600px;">
                    <el-row :gutter="50">
                        <el-col :span="30">
                            <el-card shadow="hover">
                                <div id='predictionLine' class="myLine" style="width:1500px;height:500px;margin:0 auto">
                                </div>
                            </el-card>
                        </el-col>
                    </el-row>
                </el-card>
                <el-card shadow="hover" style="width:100%;height:600px;">
                    <el-row :gutter="50">
                        <el-col :span="30">
                            <el-card shadow="hover">
                                <div id='jobLine' class="myLine" style="width:1500px;height:500px;margin:0 auto">
                                </div>
                            </el-card>
                        </el-col>
                    </el-row>
                </el-card>
                <el-card shadow="hover" style="width:100%;height:100%;">
                    <el-row :gutter="50">
                        <el-col :span="30">
                            <el-card shadow="hover">
                                <div id='lungLine' class="myLine" style="width:700px;height:600px;margin:0 auto">
                                </div>
                            </el-card>
                        </el-col>
                        <el-col :span="30">
                            <el-card shadow="hover">
                                <div id='lungjobLine' class="myLine" style="width:700px;height:600px;margin:0 auto">
                                </div>
                            </el-card>
                        </el-col>
                    </el-row>
                </el-card>
                <!--工具条-->
                <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
                    <el-form :inline="true" :model="filters" @submit.native.prevent>
                        <el-select v-model="filters.version" placeholder="当前版本" @click.native="getversion()">
                            <el-option
                                    v-for="(item,index) in versions"
                                    :key="item.version"
                                    :label="item.version"
                                    :value="item.version"
                            />
                        </el-select>
                        <el-select v-model="filters.checkversion" placeholder="以前版本" @click.native="getversion()">
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
                <!--列表-->
                <span style="margin-left: 15px" class="title">Prediction Time</span>
                <el-table :data="prediction" v-loading="listLoading"
                          @selection-change="selsChange"
                          style="width: 100%;">
                    <el-table-column prop="modelname" label="modelname" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.modelname }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="version" label="sliceThickness" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.slicenumber }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="prediction_count" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.count }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="avg pred time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px"
                                  :class="valuestatus(scope.row.avg)">{{ scope.row.avg }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="median pred time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.median)">{{ scope.row.median }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="min pred time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px"
                                  :class="valuestatus(scope.row.min)">{{ scope.row.min}}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="max pred time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px"
                                  :class="valuestatus(scope.row.max)">{{ scope.row.max }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="status" label="coef. of variation" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.coef }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="min images" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.minimages }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="max images" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.maximages }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="avg images" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.avgimages }}</span>
                        </template>
                    </el-table-column>
                </el-table>
                <el-table-column label="rate of success" min-width="8%" sortable>
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.rate }}</span>
                    </template>
                </el-table-column>
                <span style="margin-left: 15px" class="title">Job Time</span>
                <el-table :data="job" highlight-current-row v-loading="listLoading"
                          @selection-change="selsChange"
                          style="width: 100%;">
                    <el-table-column prop="version" label="modelname" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.modelname }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="sliceThickness" label="sliceThickness" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.slicenumber }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="job_count" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.count }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="avg job time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px"
                                  :class="valuestatus(scope.row.avg)">{{ scope.row.avg }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="avg single job time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.single)">{{ scope.row.single }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="median job time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.median)">{{ scope.row.median }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="min job time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px"
                                  :class="valuestatus(scope.row.min)">{{ scope.row.min }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="max job time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px"
                                  :class="valuestatus(scope.row.max)">{{ scope.row.max }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="min images" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.minimages }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="max images" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.maximages }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="avg images" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.avgimages }}</span>
                        </template>
                    </el-table-column>
                </el-table>
                <el-table-column prop="status" label="coef. of variation" min-width="10%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.coef }}</span>
                    </template>
                </el-table-column>
                <span style="margin-left: 15px" class="title">Job - Prediction Time</span>
                <el-table :data="diff" v-loading="listLoading"
                          @selection-change="selsChange"
                          style="width: 100%;">
                    <el-table-column prop="modelname" label="modelname" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.modelname }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="sliceThickness" label="sliceThickness" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.slicenumber }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="avg" label="avg pred time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px"
                                  :class="valuestatus(scope.row.avg)">{{ scope.row.avg }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="median pred time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.median)">{{ scope.row.median }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="min pred time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px"
                                  :class="valuestatus(scope.row.min)">{{ scope.row.min}}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="max" label="max pred time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px"
                                  :class="valuestatus(scope.row.max)">{{ scope.row.max }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="min images" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.minimages }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="max images" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.maximages }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="avg images" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.avgimages }}</span>
                        </template>
                    </el-table-column>
                </el-table>
                <el-table-column label="rate of success" min-width="8%" sortable>
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.rate }}</span>
                    </template>
                </el-table-column>
            </el-col>
        </div>
    </div>
</template>

<script>
    // import NProgress from 'nprogress'

    import {
        getstressversion, getstressresult, getHost, getreportfigure
    } from '@/router/api';
    import echarts from "echarts";

    export default {
        // import ElRow from "element-ui/packages/row/src/row";
        // components: {ElRow},
        data() {
            return {
                filters: {
                    server:'192.168.1.208',
                    diseases: ''
                },
                durationlist: [],
                total: 0,
                page: 1,
                listLoading: false,
                sels: [], // 列表选中列
                host:[],
                //定义表
                predictionLine: {},
                jobLine: {},
                lungLine: {},
                lungjobLine: {},
                //定义表数据
                predictionLineData: [],
                jobLineData: [],
                lungData: [],
                twoData: [],
                //定义表数据对应的option数据
                predictionLineoption: {
                    title: {
                        text: '模型预测时间对比图'
                    },
                    tooltip: {
                        trigger: 'axis',
                        padding: 25
                    },
                    legend: {
                        data: [],
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
                            formatter: '{value} 秒'
                        }
                    },
                    series: []
                },
                jobLineoption: {
                    title: {
                        text: 'Job时间对比图'
                    },
                    tooltip: {
                        trigger: 'axis',
                        padding: 25
                    },
                    legend: {
                        data: [],
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
                            formatter: '{value} 秒'
                        }
                    },
                    series: []
                },
                lungLineoption: {
                    title: {
                        text: 'Lung 模型预测时间对比'
                    },
                    tooltip: {
                        trigger: 'axis',
                        padding: 25
                    },
                    legend: {
                        data: [],
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
                            formatter: '{value} 秒'
                        }
                    },
                    series: []
                },
                lungjobLineoption: {
                    title: {
                        text: 'Lung Job预测时间对比'
                    },
                    tooltip: {
                        trigger: 'axis',
                        padding: 25
                    },
                    legend: {
                        data: [],
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
                            formatter: '{value} 秒'
                        }
                    },
                    series: []
                }
            }
        },
        components: {},
        mounted() {
            this.drawpredictionLine();
            this.drawjobLine();
            this.drawlungLine();
            this.drawlungjobLine();
            this.gethost();
            this.getBase();
        },
        created() {
            this.getreportData();
        },
        watch: {
            //观察option的变化
            predictionLineoption: {
                handler(newVal, oldVal) {
                    if (this.reportBar) {
                        if (newVal) {
                            this.predictionLine.setOption(newVal);
                        } else {
                            this.predictionLine.setOption(oldVal);
                        }
                    } else {
                        this.drawpredictionLine();
                    }
                },
                deep: true //对象内部属性的监听，关键。
            },
            jobLineoption: {
                handler(newVal, oldVal) {
                    if (this.coinnessBar) {
                        if (newVal) {
                            this.jobLine.setOption(newVal);
                        } else {
                            this.jobLine.setOption(oldVal);
                        }
                    } else {
                        this.drawjobLine();
                    }
                },
                deep: true //对象内部属性的监听，关键。
            },
            lungLineoption: {
                handler(newVal, oldVal) {
                    this.drawlungLine();
                },
                deep: true //对象内部属性的监听，关键。
            },
            lungjobLineoption: {
                handler(newVal, oldVal) {
                    this.drawlungjobLine();
                },
                deep: true //对象内部属性的监听，关键。
            }
        },
        methods: {
            valuestatus: function (i) {
                if (!/-/g.test(i)) {
                    i = 0
                } else if (!/\+/g.test(i)) {
                    i = 1
                } else {
                    i = 2
                }
                switch (i) {
                    case 0:
                        return 'statuscssa';
                    case 1:
                        return 'statuscssb';
                    case 2:
                        return 'statuscssc';
                }

            },
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
                        this.hosts = JSON.parse(json)
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
                        self.job = data.jobresult
                        self.diff = data.diffresult
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

            getreportData() {
                let params = {
                    "version": "Boimind",
                    "type": "prediction"
                };
                let headers = {
                    "Content-Type": "application/json"
                };
                getreportfigure(headers, params).then(_data => {
                    let {code, msg, data} = _data;
                    this.predictionLineData = data.predictionFigure;
                    this.jobLineData = data.jobFigure;
                    this.lungLineData = data.lungFigure;
                    this.lungjobLineData = data.lungjobFigure;
                    this.predictionLineoption.legend.data = data.modlename;
                    this.jobLineoption.legend.data = data.modlename;
                    this.lungLineoption.legend.data = data.lungname;
                    this.lungjobLineoption.legend.data = data.lungname;

                    this.predictionLineoption.xAxis.data = this.predictionLineData[0];
                    this.jobLineoption.xAxis.data = this.jobLineData[0];
                    this.lungLineoption.xAxis.data = this.lungLineData[0];
                    this.lungjobLineoption.xAxis.data = this.lungjobLineData[0];

                    for (var i = 0; i < this.predictionLineData.length; i++) {
                        this.predictionLineoption.series.push({
                                name: this.predictionLineoption.legend.data[i],
                                type: 'line',
                                data:  this.predictionLineData[(i + 1)],
                                markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                                },
                            }
                            );
                        this.jobLineoption.series.push({
                                name: this.jobLineoption.legend.data[i],
                                type: 'line',
                                data:  this.jobLineData[(i + 1)],
                                markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                                },
                            }
                            );
                    };
                     // lung 数据j
                    for (var j = 0; j < this.lungLineData.length; j++) {
                        this.lungLineoption.series.push({
                                name: this.lungLineoption.legend.data[j],
                                type: 'line',
                                data:  this.lungLineData[(j + 1)],
                                markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                                },
                            }
                            );
                         // job lung
                        this.lungjobLineoption.series.push({
                                name: this.lungjobLineoption.legend.data[j],
                                type: 'line',
                                data:  this.lungLineData[(j + 1)],
                                markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                                },
                            }
                            );
                    };


                    console.log( this.lungjobLineoption)
                    this.reportBarData = data.solution_state.sort(function (a, b) {
                        return a.value - b.value;
                    });
                    this.reportBaroption.series[0].data = this.reportBarData;
                });
            },
            drawreportBar() {
                this.reportBar = echarts.init(document.getElementById('reportBar'));
                this.reportBar.setOption(this.reportBaroption, true);
                setTimeout(() => {
                    window.onresize = reportBar.resize;
                }, 200);
            },
            drawpredictionLine() {
                this.predictionLine = echarts.init(document.getElementById('predictionLine'));
                this.predictionLine.setOption(this.predictionLineoption);
                setTimeout(() => {
                    window.onresize = predictionLine.resize;
                }, 200);
            },
            drawjobLine() {
                this.jobLine = echarts.init(document.getElementById('jobLine'));
                this.jobLine.setOption(this.jobLineoption);
                setTimeout(() => {
                    window.onresize = jobLine.resize;
                }, 200);
            },
            drawlungLine() {
                this.lungLine = echarts.init(document.getElementById('lungLine'));
                this.lungLine.setOption(this.lungLineoption);
                setTimeout(() => {
                    window.onresize = lungLine.resize;
                }, 200);
            },
            drawlungjobLine() {
                this.lungjobLine = echarts.init(document.getElementById('lungjobLine'));
                this.lungjobLine.setOption(this.lungjobLineoption);
                setTimeout(() => {
                    window.onresize = lungjobLine.resize;
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
        width: 15px;
        height: 15px;
        margin-right: 3px;
        margin-bottom: 5px
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

    .statuscssa {
        color: #E61717
    }

    .statuscssb {
        color: #67c23a;
    }

    .statuscssc {
        color: #666666;
    }
    .title {
        position: relative;
        box-sizing: border-box;
        width: 100%;
        height: 70px;
        font-size: 22px;
        color: #000000;
    }
</style>
