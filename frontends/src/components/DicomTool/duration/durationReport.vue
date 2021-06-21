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
                    <span>{{project_name}} {{basedata.version}} 版本持续化测试报告</span>
                </el-header>
                <el-main>
                    <div>
                        <p class="bug-exp-step p-t-20 p-b-10"><img src="..//../../assets/img/bug-10.png">
                            <span class="bug-ex-item">Summary</span>
                            <img class="img-revers" src="..//../../assets/img/bug-10.png"></p>
                    </div>
                    <el-row>
                        <el-col style="width: 40%">
                            <el-form ref="form" :model="basedata" label-width="60%">
                                <el-row style="width: 100%" label-position="left">
                                    <el-col style="width: 50%">
                                        <el-form-item label="测试服务：" class="labelcss">
                                            <el-select  v-model="basedata.server" placeholder="请选择活动区域">
                                            </el-select>
                                        </el-form-item>
                                    </el-col>
                                    <el-col style="width: 50%" label-position="left">
                                        <el-form-item label="统计时间：" label-position="left">
                                            <el-input v-model="basedata.statistics_date"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row>
                                    <el-col style="width: 50%" label-position="left">
                                        <el-form-item label="共计发送：" label-position="left">
                                            <el-tag effect="dark" type="warning" size="150%">{{basedata.sendcount}} 笔
                                            </el-tag>
                                        </el-form-item>
                                    </el-col>
                                    <el-col style="width: 50%">
                                        <el-form-item label="共计预测：" class="labelcss">
                                            <el-tag effect="dark" type="warning" size="150%">{{basedata.AICount}} 笔
                                            </el-tag>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row>
                                    <el-col style="width: 50%" label-position="left" class="labelcss">
                                        <el-form-item label="预测成功：" label-position="left" class="label-content">
                                            <el-tag effect="dark" type="success" size="150%">{{basedata.AISuccess}} 笔
                                            </el-tag>
                                        </el-form-item>
                                    </el-col>
                                    <el-col style="width: 50%">
                                        <el-form-item label="预测失败：">
                                            <el-tag effect="dark" type="danger" size="150%">{{basedata.AIFail}} 笔
                                            </el-tag>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row>
                                    <el-col style="width: 50%" label-position="left">
                                        <el-form-item label="开始时间：" label-position="left">
                                            <el-input v-model="basedata.start_date"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col style="width: 50%">
                                        <el-form-item label="结束时间：">
                                            <el-input v-model="basedata.end_date"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row>

                                    <el-col style="width: 40%">

                                    </el-col>
                                </el-row>
                            </el-form>
                        </el-col>
                        <el-col style="width: 20%">
                            <ve-ring :data="SummaryData" :settings="SummarySettings"></ve-ring>
                        </el-col>
                        <el-col style="width: 40%">
                            <ve-ring :data="FailData" :settings="SummarySettings"></ve-ring>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col style="width: 100%">
                            <p class="bug-exp-step p-t-20 p-b-10"><img src="..//../../assets/img/bug-10.png">
                                <span class="bug-ex-item">{{diseases}} -预测时间趋势图</span><img
                                        src="..//../../assets/img/bug-10.png"></p>
                            <el-row>
                                <el-select v-model="diseases" placeholder="请选择病种"
                                           @click.native="getReport()">
                                    <el-option
                                            v-for="key in models"
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
                    <el-row>
                        <p class="bug-exp-step p-t-20 p-b-10"><img src="..//../../assets/img/bug-10.png">
                            <span class="bug-ex-item">Detailed</span>
                            <img class="img-revers" src="..//../../assets/img/bug-10.png"></p>
                        <el-col style="width: 100%">
                            <el-table
                                    :data="durationData"
                                    style="width: 100%">
                                <el-table-column
                                        label="类型"
                                >
                                    <template slot-scope="scope">
                                        <span style="margin-left: 10px">{{ scope.row.diseases }}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="发送数量"
                                >
                                    <template slot-scope="scope">
                                        <el-tag size="medium" type="warning">{{ scope.row.count }}</el-tag>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="最大预测时间"
                                >
                                    <template slot-scope="scope">
                                        <span style="margin-left: 10px">{{ scope.row.ModelMax }}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="最小预测时间"
                                >
                                    <template slot-scope="scope">
                                        <span style="margin-left: 10px">{{ scope.row.ModelMin }}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="平均预测时间"
                                >
                                    <template slot-scope="scope">
                                        <span style="margin-left: 10px">{{ scope.row.ModelAvg }}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="JOB最大时间"
                                >
                                    <template slot-scope="scope">
                                        <span style="margin-left: 10px">{{ scope.row.JobMax }}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="JOB最小时间"
                                >
                                    <template slot-scope="scope">
                                        <span style="margin-left: 10px">{{ scope.row.JobMin }}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="JOB平均时间"
                                >
                                    <template slot-scope="scope">
                                        <span style="margin-left: 10px">{{ scope.row.JobAvg }}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="预测成功"
                                >
                                    <template slot-scope="scope">
                                        <el-tag size="medium" type="success">{{ scope.row.success }}</el-tag>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="预测失败"
                                >
                                    <template slot-scope="scope">
                                        <el-popover trigger="hover" placement="top">
                                            <p>失败原因: {{ scope.row.errorinfo }}</p>
                                            <div slot="reference" class="name-wrapper">
                                                <el-tag size="medium" type="danger">{{ scope.row.fail }}</el-tag>
                                            </div>
                                        </el-popover>
                                    </template>
                                </el-table-column>
                                <el-table-column label="操作">
                                    <template slot-scope="scope">
                                        <el-button
                                                size="mini"
                                                type="danger"
                                                @click="showDetail(scope.$index, scope.row)">详情
                                        </el-button>
                                    </template>
                                </el-table-column>
                            </el-table>
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

    .labelcss.el-form-item__label {
        color: #1E90FF;
    }

    .label-content .el-form-item__content {
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
            this.project_name = localStorage.getItem("projectname"),
            this.SummaryData ={}
            this.FailData ={}
            this.chartData = {}
            this.models= []
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
                    message: '打开 Grafana 性能监控服务，  用户：admin 密码：biomind',
                    showClose: false
                });
                const start_date = this.basedata.start_date
                const end_date = this.basedata.statistics_date
                const loadserver = this.basedata.server

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

                const url = "http://192.168.1.121:3000/d/Ss3q6hSZk/server-monitor-test?orgId=1&from=" +
                    startstamp + "&to=" + endstamp + "&var-host_name=" +
                    loadserver + "&var-gpu_exporter_port=9445&var-node_exporter_port=9100&var-cadvisor_port=8080"
                const dualScreenLeft = window.screenLeft !== undefined ? window.screenLeft : screen.left
                const dualScreenTop = window.screenTop !== undefined ? window.screenTop : screen.top

                const width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width
                const height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height

                const left = ((width / 2) - (1500 / 2)) + dualScreenLeft
                const top = ((height / 2) - (800 / 2)) + dualScreenTop
                const newWindow = window.open(url, '服务监控', 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=yes, copyhistory=no, width=' + '1500' + ', height=' + '800' + ', top=' + top + ', left=' + left)

                // Puts focus on the newWindow
                if (window.focus) {
                    newWindow.focus()
                }
                // //刷新当前页面
                // window.location.reload();
            },
            ToUpdate() {
                this.$notify.success({
                    title: '刷新成功',
                    message: this.diseases + '预测时间图表已更新',
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
            // 跳转到详情页面
            showDetail(index, row) {
                this.$router.push({
                    path: '/durationData',
                    query: {
                        id: this.reportid,
                        name: row.diseases
                    }
                });
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
                        this.chartData = {"columns": data.data.model, "rows": data.data.durationLineData}
                        this.models = data.data.diseases
                        this.SummaryData = {
                            columns: ['状态', '数量'],
                            rows: [
                                {'状态': '成功', '数量': this.basedata.AISuccess},
                                {'状态': '失败', '数量': this.basedata.AIFail}
                            ]
                        }
                        this.FailData = {
                            columns: ['状态', '数量'],
                            rows: data.data.errorData
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