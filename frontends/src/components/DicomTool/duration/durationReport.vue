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
                        <el-col style="width: 60%">
                            <el-form ref="form" :model="basedata" label-width="60%">
                                <el-row>
                                    <el-divider></el-divider>
                                </el-row>
                                <el-row>
                                    <el-col style="width: 40%" label-position ="left">

                                    <el-form-item  label="测试版本：" label-position ="left">
                                        <el-input v-model="basedata.version" ></el-input>
                                    </el-form-item>
                                        </el-col>
                                    <el-col style="width: 40%">
                                    <el-form-item label="测试服务：" class="labelcss">
                                        <el-select v-model="basedata.server" placeholder="请选择活动区域">
                                        </el-select>
                                    </el-form-item>
                                        </el-col>
                                </el-row>
                                <el-row>
                                    <el-col style="width: 40%" label-position ="left">
                                    <el-form-item  label="共计发送（个）：" label-position ="left">
                                        <el-tag effect="dark" type="warning" size ="150%">{{basedata.sendcount}} 笔</el-tag>
                                    </el-form-item>
                                        </el-col>
                                    <el-col style="width: 40%">
                                    <el-form-item label="共计预测：" class="labelcss">
                                        <el-tag effect="dark" type="warning" size ="150%">{{basedata.AICount}} 笔</el-tag>
                                    </el-form-item>
                                        </el-col>
                                </el-row>
                                <el-row>
                                    <el-col style="width: 40%" label-position ="left" class="labelcss">
                                    <el-form-item  label="预测成功：" label-position ="left" class="label-content">
                                        <el-tag effect="dark" type="success" size ="150%">{{basedata.AISuccess}} 笔</el-tag>
                                    </el-form-item>
                                        </el-col>
                                    <el-col style="width: 40%">
                                    <el-form-item label="预测失败：">
                                        <el-tag effect="dark" type="danger" size ="150%">{{basedata.AIFail}} 笔</el-tag>
                                    </el-form-item>
                                        </el-col>
                                </el-row>
                                <el-row>
                                    <el-col style="width: 40%" label-position ="left">
                                    <el-form-item  label="开始时间：" label-position ="left">
                                        <el-input v-model="basedata.start_date"></el-input>
                                    </el-form-item>
                                        </el-col>
                                    <el-col style="width: 40%">
                                    <el-form-item label="结束时间：">
                                        <el-input v-model="basedata.end_date"></el-input>
                                    </el-form-item>
                                        </el-col>
                                </el-row>
                                <el-row>
                                    <el-col style="width: 40%" label-position ="left">
                                    <el-form-item  label="统计时间：" label-position ="left">
                                        <el-input v-model="basedata.statistics_date"></el-input>
                                    </el-form-item>
                                        </el-col>
                                    <el-col style="width: 40%">

                                        </el-col>
                                </el-row>
                            </el-form>
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
                                        label="成功数量"
                                        style="color: #67c23a">
                                </el-table-column>
                                <el-table-column
                                        prop="fail"
                                        label="失败数量"
                                        style="background: #990000"
                                >
                                </el-table-column>
                                <el-table-column
                                        prop="rate"
                                        label="成功率">
                                </el-table-column>
                            </el-table>
                        </el-col>
                        <el-col style="width: 40%">
                            <ve-ring :data="FailData" :settings="SummarySettings"></ve-ring>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col style="width: 100%">
                            <p class="bug-exp-step p-t-20 p-b-10"><img src="..//../../assets/img/bug-10.png">
                                <span class="bug-ex-item">{{diseases}} -模型预测时间趋势图</span><img
                                        src="..//../../assets/img/bug-10.png"></p>
                            <el-row>
                                <el-select v-model="diseases" placeholder="请选择病种"
                                           @click.native="getReport()">
                                    <el-option
                                            v-for="key in model"
                                            :key="key"
                                            :label="key"
                                            :value="key"
                                    />
                                </el-select>
                                <el-button
                                        plain
                                        @click="ToUpdate()">
                                    更新
                                </el-button>
                                <el-button
                                        plain
                                        @click="SaveReport()">
                                    保存报告
                                </el-button>
                                <el-button
                                        plain
                                        @click="checkExpress()">
                                    服务监控
                                </el-button>
                            </el-row>

                            <ve-line
                                    :set-option-opts="false"
                                    :data="chartData"
                                    :data-zoom="chartDataZoom">
                            </ve-line>

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
    .labelcss.el-form-item__label{
        color: #1E90FF;
    }
    .label-content .el-form-item__content{
        font-size: 20px;
        color: #aaaa33;
    }
</style>

<script>
    import {
        getdurationReport
    } from '@/router/api'

    export default {
        data() {
            this.chartDataZoom = [{type: 'slider'}]
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
                basedata: [],
                durationData: [],
                diseases: 'CT'

            }
        },
        created() {
            this.getParams();
        },
        mounted() {
            this.getParams()
            this.getReport()
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
            checkExpress: function () {
                this.$notify.success({
                    title: '提示',
                    type: 'warning',
                    message: '5秒后跳转到 Grafana 性能监控服务，  用户：admin 密码：biomind',
                    showClose: false
                });
                const start_date = this.basedata[0].start_date
                const end_date = this.basedata[0].statistics_date
                const loadserver = this.basedata[0].server

                if (start_date === null) {
                    var startstamp = new Date().getTime();
                } else {
                    var startdate = start_date.replace(/-/g, '/');
                    var startstamp = new Date(startdate).getTime();
                }
                if (end_date === null) {
                    var endstamp = new Date().getTime();
                } else {
                    var enddate = end_date.replace(/-/g, '/');
                    var endstamp = new Date(enddate).getTime();
                }
                this.timer = setTimeout(() => {   //设置延迟执行
                    {
                        window.location.href = "http://192.168.1.121:3000/d/Ss3q6hSZk/server-monitor-test?orgId=1&from=" +
                            startstamp + "&to=" + endstamp + "&var-host_name=" +
                            loadserver + "&var-gpu_exporter_port=9445&var-node_exporter_port=9100&var-cadvisor_port=8080"
                    }
                    ;
                }, 5000);

                // //刷新当前页面
                // window.location.reload();
            },
            ToUpdate() {
                this.$notify.success({
                    title: '刷新成功',
                    message: this.diseases + '模型预测时间图表已更新',
                    showClose: false
                });
                this.getReport()
            },
            SaveReport() {
                this.$notify.success({
                    title: '保存报告成功',
                    message: '保存报告成功：请在fileServer ： 下载',
                    showClose: false
                });
                this.getReport()
            },
            getParams() {
                this.routerParams = this.$route.query;
                this.reportid = this.$route.params.reportid
            },
            // 获取数据列表
            getReport() {
                this.listLoading = true
                const self = this
                const params = {
                    id: this.reportid,
                    diseases: this.diseases
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getdurationReport(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.basedata = data.data.basedata
                        this.durationData = data.data.durationData
                        const chartData = {"columns": [], "rows": []}
                        chartData.rows = data.data.durationLineData
                        this.model = data.data.diseases
                        chartData.columns = data.data.model
                        this.chartData = chartData
                        this.SummaryData= {
                            columns: ['状态', '数量'],
                            rows: [
                                {'状态': '成功', '数量':this.basedata.AISuccess},
                                {'状态': '失败', '数量':this.basedata.AIFail }
                            ]
                        }
                        this.FailData= {
                            columns: ['状态', '数量'],
                            rows: [
                                {'状态': '系统错误', '数量':this.basedata.AISuccess},
                                {'状态': '预测超时', '数量':this.basedata.AIFail },
                                {'状态': '序列错误', '数量':this.basedata.AIFail }

                            ]
                        }
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

        }
    }
</script>