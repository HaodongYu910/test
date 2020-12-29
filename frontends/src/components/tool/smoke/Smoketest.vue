<template>
    <ve-histogram :data="HistogramData" :settings="Histogramchart"></ve-histogram>
</template>

<script>
    import {
        getsmokefigure, getHost
    } from '@/router/api';

    export default {
        data() {
            this.Histogramchart = {
                stack: {'版本': ['匹配成功', '匹配失败', '预测失败']}
            }
            return {
                total: 0,
                page: 1,
                listLoading: false,
                sels: [], // 列表选中列
                host: [],
                //定义表
                HistogramData: {
                    columns: ['版本', '匹配成功', '匹配失败', '预测失败'],
                    rows: []
                },
                //定义表数据
                goldrows: [],
                goldcolumns: [],
                twoData: [],
                //定义表数据对应的option数据

            }
        },
        components: {},
        mounted() {
            this.gethost();
            this.getBase();
            this.smokefigure();
        },
        created() {
            this.smokefigure();
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
            smokefigure() {
                this.listLoading = true
                const self = this
                const params = {
                    version: '1'
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getsmokefigure(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        // self.chartData.columns= data.goldcolumns
                        self.HistogramData.rows = data.goldrows
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
                                data: this.predictionLineData[(i + 1)],
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
                                data: this.jobLineData[(i + 1)],
                                markPoint: {
                                    data: [
                                        {type: 'max', name: '最大值'},
                                        {type: 'min', name: '最小值'}
                                    ]
                                },
                            }
                        );
                    }
                    ;
                    // lung 数据j
                    for (var j = 0; j < this.lungLineData.length; j++) {
                        this.lungLineoption.series.push({
                                name: this.lungLineoption.legend.data[j],
                                type: 'line',
                                data: this.lungLineData[(j + 1)],
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
                                data: this.lungLineData[(j + 1)],
                                markPoint: {
                                    data: [
                                        {type: 'max', name: '最大值'},
                                        {type: 'min', name: '最小值'}
                                    ]
                                },
                            }
                        );
                    }
                    ;


                    console.log(this.lungjobLineoption)
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
