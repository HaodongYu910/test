<template>
    <div class="wid-2000 " for="pc">
        <el-container style="height: 2000px; border: 1px solid #eee">
            <el-container>
                <el-header style="text-align: center; color: rgb(71,62,62); font-size: 24px">
                    <el-dropdown>
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item>查看</el-dropdown-item>
                            <el-dropdown-item>新增</el-dropdown-item>
                            <el-dropdown-item>删除</el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                    <span>BioMind 持续化 Test Report</span>
                </el-header>
                <el-main>
                    <div>
                        <p class="bug-exp-step p-t-20 p-b-10"><img src="..//../../assets/img/bug-10.png">
                            <span class="bug-ex-item">Summary</span>
                            <img class="img-revers" src="..//../../assets/img/bug-10.png"></p>
                    </div>
                    <el-row>
                        <el-col style="width: 80%">
                            <el-table :data="basedata" border>
                                <el-table-column style="width: 6%"
                                                 prop="version"
                                                 label="测试版本">
                                </el-table-column>
                                <el-table-column
                                        prop="sendcount"
                                        label="共计发送(个)">
                                </el-table-column>
                                <el-table-column
                                        prop="AICount"
                                        label="共计预测(个)"
                                        class=statuscssa>
                                </el-table-column>
                                <el-table-column
                                        prop="AISuccess"
                                        label="AI预测成功"
                                        class=statuscssa>
                                </el-table-column>
                                <el-table-column
                                        prop="AIFail"
                                        label="AI预测失败">
                                </el-table-column>
                                <el-table-column
                                        prop="start_date"
                                        label="持续化开始日期">
                                </el-table-column>
                                <el-table-column
                                        prop="end_date"
                                        label="统计截至日期">
                                </el-table-column>
                                <el-table-column
                                        prop="end_date"
                                        label="持续化结束日期">
                                </el-table-column>
                            </el-table>
                        </el-col>
                        <el-col style="width: 20%">
                            <ve-ring :data="SummaryData" :settings="SummarySettings"></ve-ring>
                        </el-col>
                    </el-row>
                    <el-row>
                        <p class="bug-exp-step p-t-20 p-b-10"><img src="..//../../assets/img/bug-10.png">
                            <span class="bug-ex-item">Detailed</span>
                            <img class="img-revers" src="..//../../assets/img/bug-10.png"></p>
                        <el-col style="width: 60%">
                            <el-table :data="durationData" border style="width: 100%" row-key="id" border
                                      default-expand-all
                                      :tree-props="{children: 'children', hasChildren: 'hasChildren'}">
                                <el-table-column
                                        prop="diseases"
                                        label="类型">
                                </el-table-column>
                                <el-table-column
                                        prop="count"
                                        label="发送数量">
                                </el-table-column>
                                <el-table-column
                                        prop="ModelAvg"
                                        label="平均预测时间">
                                </el-table-column>
                                <el-table-column
                                        prop="ModelMin"
                                        label="最小预测时间"
                                >
                                </el-table-column>
                                <el-table-column
                                        prop="ModelMax"
                                        label="最大预测时间">
                                </el-table-column>
                                <el-table-column
                                        prop="success"
                                        label="成功数量">
                                </el-table-column>
                                <el-table-column
                                        prop="fail"
                                        label="失败数量"
                                >
                                </el-table-column>
                                <el-table-column
                                        prop="rate"
                                        label="成功率">
                                </el-table-column>
                            </el-table>
                        </el-col>
                        <el-col style="width: 40%">
                            <ve-ring :data="SummaryData" :settings="SummarySettings"></ve-ring>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col style="width: 100%">
                            <p class="bug-exp-step p-t-20 p-b-10"><img src="..//../../assets/img/bug-10.png">
                                <span class="bug-ex-item">预测时间趋势图</span><img src="..//../../assets/img/bug-10.png"></p>
                            <!--                                                        <ve-line :data="durationLineData" :settings="DurationSettings" :extend="extend"></ve-line>-->

                            <ve-line
                                    :set-option-opts="false"
                                    :data="chartData"
                                    :data-zoom="chartDataZoom">
                            </ve-line>
                            <button @click="change">change</button>
                            <div :id="id" :class="className" :style="{height:height,width:width}"/>

                        </el-col>
                    </el-row>
                </el-main>

            </el-container>
        </el-container>

    </div>
</template>

<style>
    .el-header {
        background-color: #B3C0D1;
        color: #333;
        line-height: 60px;
    }

    .el-aside {
        color: #333;
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
</style>

<script>
    import {
        getHost, getdurationReport, getbase
    } from '@/router/api'
    import echarts from 'echarts'
    import resize from '../../../utils/resize'

    export default {
        mixins: [resize],
        props: {
            className: {
                type: String,
                default: 'durationmonitor-chart'
            },
            id: {
                type: String,
                default: 'durationmonitor-chart'
            },
            width: {
                type: String,
                default: '100%'
            },
            height: {
                type: String,
                default: '600px'
            }
        },
        data() {
            chart:null,
                this.chartDataZoom = [{type: 'slider'}],
                chartData = {
                    columns: ["日期", "访问用户", "下单用户"],
                    rows: [
                        {日期: "1/1", 访问用户: 1391, 下单用户: 1093, 下单率: 0.32},
                        {日期: "1/2", 访问用户: 3530, 下单用户: 3230, 下单率: 0.26},
                        {日期: "1/3", 访问用户: 2923, 下单用户: 2623, 下单率: 0.76},
                        {日期: "1/4", 访问用户: 1723, 下单用户: 1423, 下单率: 0.49},
                        {日期: "1/5", 访问用户: 3792, 下单用户: 3492, 下单率: 0.323},
                        {日期: "1/6", 访问用户: 4593, 下单用户: 4293, 下单率: 0.78}
                    ]
                },
                this.SummarySettings = {
                    roseType: 'radius'
                }
            this.DurationSettings = {
                axisSite: {right: ['成功率']},
                yAxisType: ['KMB', 'percent'],
                yAxisName: ['预测时长/秒', '成功率']
            }
            this.extend = {
                'xAxis.0.axisLabel.rotate': 45
            }
            return {
                durationLineData: {
                    columns: ['日期', 'CTA', 'BrainCT', '成功率'],
                    rows: [
                        {'日期': '1/1', 'CTA': 1393, 'BrainCT': 1093, '成功率': 0.32},
                        {'日期': '1/2', 'CTA': 3530, 'BrainCT': 3230, '成功率': 0.26},
                        {'日期': '1/3', 'CTA': 2923, 'BrainCT': 2623, '成功率': 0.76},
                        {'日期': '1/4', 'CTA': 1723, 'BrainCT': 1423, '成功率': 0.49},
                        {'日期': '1/5', 'CTA': 3792, 'BrainCT': 3492, '成功率': 0.323},
                        {'日期': '1/6', 'CTA': 4593, 'BrainCT': 4293, '成功率': 0.78}
                    ]
                },
                SummaryData: {
                    columns: ['状态', '数量'],
                    rows: [
                        {'状态': '成功', '数量': 0},
                        {'状态': '失败', '数量': 0}
                    ]
                },
                basedata: [],
                durationData: [],

            }
        },
        created() {
            this.getParams();
        },
        mounted() {
            this.getParams()
            this.getReport()
            this.initChart()
        },
        activated() {
            this.getParams();
        },

        beforeDestroy() {
            if (!this.chart) {
                return
            }
            this.chart.dispose()
            this.chart = null
        },
        methods: {
            change() {
                this.chartData.rows.push({
                    '日期': '1/1',
                    '访问用户': Math.random() * 1000,
                    '下单用户': Math.random() * 1000
                })
            },
            getParams() {
                this.routerParams = this.$route.query;
                this.reportid = this.$route.params.reportid
            },
            valuestatus: function (a) {
                if (a === "匹配成功") {
                    return 'statuscssb';
                } else {
                    return 'statuscssa';
                }
            },
            // 获取数据列表
            getReport() {
                this.listLoading = true
                const self = this
                const params = {
                    id: this.reportid
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getdurationReport(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.basedata = data.data.basedata
                        this.durationData = data.data.durationData
                        this.durationLineData = data.data.durationLineData
                        this.diseases = data.data.diseases
                        this.datedata = data.data.datedata
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            handleCurrentChange(val) {
                this.page = val
                this.getdata()
            },
            selsChange: function (sels) {
                this.sels = sels
            },
            initChart() {
                this.chart = echarts.init(document.getElementById(this.id))
                const xData = (function () {
                    console.log(this.datedata)
                    const datedata = this.datedata

                    return datedata
                }())
                this.chart.setOption({
                    backgroundColor: '#eeeeef',
                    title: {
                        text: '预测时间趋势图',
                        x: '20',
                        top: '20',
                        textStyle: {
                            color: '#0e0e0e',
                            fontSize: '22'
                        },
                        subtextStyle: {
                            color: '#90979c',
                            fontSize: '16'
                        }
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            textStyle: {
                                color: '#fff'
                            }
                        }
                    },
                    grid: {
                        left: '5%',
                        right: '5%',
                        borderWidth: 0,
                        top: 150,
                        bottom: 95,
                        textStyle: {
                            color: '#fff'
                        }
                    },
                    legend: {
                        x: '5%',
                        top: '10%',
                        textStyle: {
                            color: '#90979c'
                        },
                        //左上角示例图对应数据
                        data: this.diseases
                    },
                    calculable: true,
                    xAxis: [{
                        type: 'category',
                        axisLine: {
                            lineStyle: {
                                color: '#3c3c58'
                            }
                        },
                        splitLine: {
                            show: false
                        },
                        axisTick: {
                            show: false
                        },
                        splitArea: {
                            show: false
                        },
                        axisLabel: {
                            interval: 0
                        },
                        data: xData
                    }],
                    yAxis: [{
                        type: 'value',
                        splitLine: {
                            show: false
                        },
                        axisLine: {
                            lineStyle: {
                                color: '#111111'
                            }
                        },
                        axisTick: {
                            show: false
                        },
                        axisLabel: {
                            interval: 0
                        },
                        splitArea: {
                            show: false
                        }
                    }],
                    dataZoom: [{
                        show: true,
                        height: 30,
                        xAxisIndex: [
                            0
                        ],
                        bottom: 30,
                        start: 10,
                        end: 80,
                        handleIcon: 'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
                        handleSize: '100%',
                        handleStyle: {
                            color: '#d3dee5'
                        },
                        textStyle: {
                            color: '#fff'
                        },
                        borderColor: '#90979c'
                    }, {
                        type: 'inside',
                        show: true,
                        height: 15,
                        start: 1,
                        end: 35
                    }],
                    series: [{
                        //失败数据
                        name: 'fail',
                        type: 'bar',
                        stack: 'total',
                        barMaxWidth: 35,
                        barGap: '10%',
                        itemStyle: {
                            normal: {
                                color: 'rgba(255,144,128,1)',
                                label: {
                                    show: true,
                                    textStyle: {
                                        color: '#fff'
                                    },
                                    position: 'insideTop',
                                    formatter(p) {
                                        return p.value > 0 ? p.value : ''
                                    }
                                }
                            }
                        },
                        data: []
                    },
                        {
                            //成功数据
                            name: 'success',
                            type: 'bar',
                            stack: 'total',
                            itemStyle: {
                                normal: {
                                    color: 'rgba(0,191,183,1)',
                                    barBorderRadius: 0,
                                    label: {
                                        show: true,
                                        position: 'top',
                                        formatter(p) {
                                            return p.value > 0 ? p.value : ''
                                        }
                                    }
                                }
                            },
                            data: []
                        },
                        {
                            //影响张数
                            name: 'CTA',
                            type: 'line',
                            stack: 'total',
                            symbolSize: 10,
                            symbol: 'circle',
                            itemStyle: {
                                normal: {
                                    color: 'rgba(252,230,48,1)',
                                    barBorderRadius: 0,
                                    label: {
                                        show: true,
                                        position: 'top',
                                        formatter(p) {
                                            return p.value > 0 ? p.value : ''
                                        }
                                    }
                                }
                            },
                            data: [
                                103,
                                369,
                                296,
                                381,
                                251,
                                191,
                                174,
                                467,
                                620,
                                432,
                                286,
                                429
                            ]
                        }
                    ]
                })
            }

        }
    }
</script>