<template>
    <div class="wid-2000 " for="pc">
        <el-container style=" border: 1px solid #eee">
            <el-header style="text-align: center; color: rgb(71,62,62); font-size: 24px">
                <span :model="basedata">BioMind Stress Test Report</span>
            </el-header>
            <el-main>
                <div>
                    <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                        <span class="bug-ex-item">概述Summary</span>
                        <img class="img-revers" src="../../assets/img/bug-10.png"></p>
                </div>
                <el-row>
                    <el-col style="width: 50%">
                        <el-form ref="form" :model="basedata" label-width="50%">
                            <el-row>
                                <p></p>
                            </el-row>
                            <el-row :gutter="20">
                                <el-col style="width: 50%">
                                    <el-form-item label="测试版本:">
                                        <el-input v-model="basedata.version" style="align:left "></el-input>
                                    </el-form-item>
                                </el-col>
                                <el-col style="width: 50%">
                                    <el-form-item label="服务器：" class="labelcss">
                                        <el-select v-model="basedata.server" placeholder="请选择活动区域">
                                        </el-select>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col style="width: 50%" label-position="left" class="labelcss">
                                    <el-form-item label="共计预测：" label-position="left" class="label-content">
                                        <el-tag effect="dark" type="warning" size="150%">{{basedata.total}} 笔
                                        </el-tag>
                                    </el-form-item>
                                </el-col>
                                <el-col style="width: 50%" label-position="left" class="labelcss">
                                    <el-form-item label="" label-position="left" class="label-content">
                                        <p></p>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col style="width: 50%" label-position="left" class="labelcss">
                                    <el-form-item label="预测成功：" label-position="left" class="label-content">
                                        <el-tag effect="dark" type="success" size="150%">{{basedata.success}} 笔
                                        </el-tag>
                                    </el-form-item>
                                </el-col>
                                <el-col style="width: 50%">
                                    <el-form-item label="预测失败：">
                                        <el-tag effect="dark" type="danger" size="150%">{{basedata.fail}} 笔
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
                            <el-row label-position="left">
                                <el-col style="width: 50%" label-position="left" align="center">

                                    <el-table
                                            :data="stressData"
                                            style="width: 100%">
                                        <el-table-column
                                                label="策略"
                                        >
                                            <template slot-scope="scope">
                                                <span style="margin-left: 10px">{{ scope.row.strategy }}</span>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                                label="并发VU"
                                        >
                                            <template slot-scope="scope">
                                                <div slot="reference" class="name-wrapper">
                                                    <el-tag size="medium" type="warning">{{ scope.row.vu }}</el-tag>
                                                </div>

                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                                label="循环次数"
                                        >
                                            <template slot-scope="scope">
                                                <div slot="reference" class="name-wrapper">
                                                    <el-tag size="medium" type="success">{{ scope.row.count }}
                                                    </el-tag>
                                                </div>
                                            </template>
                                        </el-table-column>
                                        <el-table-column
                                                label="运行时间"
                                        >
                                            <template slot-scope="scope">
                                                <el-popover trigger="hover" placement="top">
                                                    <p>{{ scope.row.time }}</p>

                                                </el-popover>
                                            </template>
                                        </el-table-column>
                                    </el-table>
                                </el-col>
                                <el-col style="width: 50%" label-position="left">
                                    <el-form-item label="服务器配置" prop='serverInfo'>
                                        <el-input type="textarea" :rows="10" v-model="basedata.serverInfo"></el-input>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                        </el-form>

                    </el-col>
                    <el-col style="width: 25%">
                        <el-row>
                            <p>混合测试 - 预测结果</p>
                        </el-row>
                        <el-row>
                            <ve-ring :data="stresschartData" :settings="chartSettings"></ve-ring>
                        </el-row>
                    </el-col>
                    <el-col style="width: 25%">
                        <el-row><p>混合测试 - Error</p></el-row>
                        <el-row>
                            <ve-ring :data="FailData" :settings="SummarySettings"></ve-ring>
                        </el-row>
                    </el-col>
                </el-row>
                <el-row style="width: 70%">
                    <el-col>
                        <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                            <span class="bug-ex-item">Result Analysis</span><img
                                    src="../../assets/img/bug-10.png"></p>
                    </el-col>
                    <el-col class="toolbar" style="padding-bottom: 0px;">
                        <el-row style="width: 100%">
                            <el-col style="width: 80%">
                                <el-input type="textarea" :rows="10" v-model="basedata.summary"></el-input>
                            </el-col>
                            <el-col style="width: 20%">
                                <el-row>
                                    <el-button type="primary" @click="getSaveReport">保存更新</el-button>
                                </el-row>
                                <el-row>
                                    <el-button type="primary" @click="ToMonitor">监控</el-button>
                                </el-row>
                                <el-row>
                                    <el-button type="primary" @click="ToUpdate">发送</el-button>
                                </el-row>
                            </el-col>
                        </el-row>
                    </el-col>
                </el-row>

                <el-row>
                    <el-col style="width: 100%">
                        <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                            <span class="bug-ex-item">{{ modelName }}- 各个版本时间对比图</span><img
                                    src="../../assets/img/bug-10.png"></p>
                        <el-row>
                            <!--工具条-->
                            <el-form :inline="true" :model="filters" @submit.native.prevent>
                                <el-form-item>
                                    <el-select v-model="filters.type" placeholder="类型">
                                        <el-option key="JZ" label="基准测试" value="JZ"/>
                                        <el-option key="HH" label="混合测试" value="HH"/>
                                        <el-option key="DY" label="单一测试" value="DY"/>
                                    </el-select>
                                </el-form-item>
                                <el-select v-model="filters.models" placeholder="模型">
                                    <el-option
                                            v-for="(k,v) in basedata.models"
                                            :key="v"
                                            :label="k"
                                            :value="v"
                                    />
                                </el-select>
                                <el-button type="primary" @click="ToUpdate">更新</el-button>
                            </el-form>
                            <ve-line
                                    :set-option-opts="false"
                                    :data="chartData"
                                    :data-zoom="chartDataZoom">
                            </ve-line>
                        </el-row>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col style="width: 100%">
                        <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                            <span class="bug-ex-item">{{modelName}} -预测时间趋势图</span><img
                                    src="../../assets/img/bug-10.png"></p>
                        <el-row>
                            <el-select v-model="filters.models" placeholder="模型">
                                <el-option
                                        v-for="(k,v) in basedata.models"
                                        :key="v"
                                        :label="k"
                                        :value="v"
                                />
                            </el-select>
                            <el-button type="primary" @click="ToUpdate">更新</el-button>
                        </el-row>

                        <ve-line
                                :set-option-opts="false"
                                :data="DataChart"
                                :data-zoom="chartDataZoom">
                        </ve-line>

                    </el-col>
                </el-row>
                <el-row>
                    <el-col style="width: 100%">
                        <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                            <span class="bug-ex-item">Prediction / Job Time Result</span><img
                                    src="../../assets/img/bug-10.png"></p>
                        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
                            <el-form :inline="true" :model="filters">
                                <el-select v-model="filters.type" placeholder="类型">
                                    <el-option key="JZ" label="基准测试" value="JZ"/>
                                    <el-option key="HH" label="混合测试" value="HH"/>
                                    <el-option key="DY" label="单一测试" value="DY"/>
                                </el-select>
                                <el-select v-model="filters.checkversion" placeholder="比对版本"
                                           @click.native="getversion()">
                                    <el-option
                                            v-for="(item,index) in versions"
                                            :key="item.version"
                                            :label="item.version"
                                            :value="item.version"
                                    />
                                </el-select>
                                <el-form-item>
                                    <el-button type="primary" @click="ToUpdate">更新</el-button>
                                </el-form-item>
                            </el-form>
                        </el-col>
                        <el-table :data="prediction" v-loading="listLoading"
                                  @selection-change="selsChange"
                                  style="width: 100%;">
                            <el-table-column prop="modelname" label="模型" min-width="8%">
                                <template slot-scope="scope">
                                    <span style="margin-left: 11px;color: #07c4a8; font-family:微软雅黑">{{ scope.row.modelname }}</span>
                                </template>
                            </el-table-column>
                            <el-table-column prop="slicenumber" label="层厚" min-width="6%">
                                <template slot-scope="scope">
                                    <span style="margin-left: 10px">{{ scope.row.slicenumber }}</span>
                                </template>
                            </el-table-column>
                            <el-table-column prop="type" label="数量" min-width="6%">
                                <template slot-scope="scope">
                                    <el-row>
                                        <span style="margin-left: 10px" :class="valuestatus(scope.row.count)">{{ scope.row.count }}</span>
                                    </el-row>
                                </template>
                            </el-table-column>
                            <el-table-column prop="type" label="Avg Time /s" min-width="15%">
                                <template slot-scope="scope">
                                    <el-row>
                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Job:</span>
                                        <span style="margin-left: 10px" :class="valuestatus(scope.row.jobavg)">{{ scope.row.jobavg }}</span>
                                    </el-row>
                                    <el-row>
                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Prediction:</span>
                                        <span style="margin-left: 10px" :class="valuestatus(scope.row.avg)">{{ scope.row.avg }}</span>
                                    </el-row>
                                </template>
                            </el-table-column>
                            <el-table-column label="Median Time /s" min-width="15%">
                                <template slot-scope="scope">
                                    <el-row>
                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Job:</span>
                                        <span style="margin-left: 10px" :class="valuestatus(scope.row.jobmedian)">{{ scope.row.jobmedian }}</span>
                                    </el-row>
                                    <el-row>
                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Prediction:</span>
                                        <span style="margin-left: 10px" :class="valuestatus(scope.row.median)">{{ scope.row.median }}</span>
                                    </el-row>
                                </template>
                            </el-table-column>
                            <el-table-column label="Min Time /s" min-width="15%">
                                <template slot-scope="scope">
                                    <el-row>
                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Job:</span>
                                        <span style="margin-left: 10px" :class="valuestatus(scope.row.jobmin)">{{ scope.row.jobmin }}</span>
                                    </el-row>
                                    <el-row>
                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Prediction:</span>
                                        <span style="margin-left: 10px" :class="valuestatus(scope.row.min)">{{ scope.row.min }}</span>
                                    </el-row>
                                </template>
                            </el-table-column>
                            <el-table-column prop="type" label="Max Time /s" min-width="15%">
                                <template slot-scope="scope">
                                    <el-row>
                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Job:</span>
                                        <span style="margin-left: 10px" :class="valuestatus(scope.row.jobmax)">{{ scope.row.jobmax }}</span>
                                    </el-row>
                                    <el-row>
                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Prediction:</span>
                                        <span style="margin-left: 10px" :class="valuestatus(scope.row.max)">{{ scope.row.max }}</span>
                                    </el-row>
                                </template>
                            </el-table-column>
                            <el-table-column prop="status" label="coef.of variation" min-width="10%">
                                <template slot-scope="scope">
                                    <span style="margin-left: 10px">{{ scope.row.coef }}</span>
                                </template>
                            </el-table-column>
                            <el-table-column label="预测成功率" min-width="8%">
                                <template slot-scope="scope">
                                    <div slot="reference" class="name-wrapper">
                                        <el-tag size="medium" type="success">{{ scope.row.rate | numFilter}}%
                                        </el-tag>
                                    </div>
                                </template>
                            </el-table-column>
                            <el-table-column label="最小张数" min-width="6%">
                                <template slot-scope="scope">
                                    <span style="margin-left: 10px">{{ scope.row.minimages }}</span>
                                </template>
                            </el-table-column>
                            <el-table-column label="最大张数" min-width="6%">
                                <template slot-scope="scope">
                                    <span style="margin-left: 10px">{{ scope.row.maximages }}</span>
                                </template>
                            </el-table-column>
                            <el-table-column label="平均张数" min-width="6%">
                                <template slot-scope="scope">
                                    <span style="margin-left: 10px">{{ scope.row.avgimages }}</span>
                                </template>
                            </el-table-column>

                        </el-table>
                    </el-col>
                </el-row>
            </el-main>
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

    .word {
        color: #898888;
    }

    .statuscssa {
        color: #E61717
    }

    .statuscssb {
        color: #67c23a;
    }

    .statuscssc {
        color: #1dc5a3;
    }
</style>

<script>
    import {
        getstressversion, getstressmodel, getStressReport, saveAnalysis
    } from '@/router/api'

    export default {

        data() {
            this.chartDataZoom = [{type: 'slider'}]

            this.chartSettings = {
                roseType: 'radius'
            }
            this.SummarySettings = {
                roseType: 'radius'
            }
            return {
                props: {multiple: false}, // 控制级联选择 是否允许多选
                versions: {},
                filters: {

                    type: "JZ",
                    models: 1
                },
                chartData: {
                    "columns": ['version', 'Prediction', 'Job'],
                    "rows": [{
                        "version": "demo",
                        "Prediction": "194.36", "Job": "209.58"
                    }, {
                        "version": "demo1",
                        "Job": "73.02",
                        "Prediction": "68.9"
                    }]
                },
                DataChart: {
                    "columns": ['date', 'Prediction', 'Job'],
                    "rows": [{
                        "version": "demo",
                        "Prediction": "194.36", "Job": "209.58"
                    }, {
                        "version": "demo1",
                        "Job": "73.02",
                        "Prediction": "68.9"
                    }]
                },
                modeloptions: [{
                    value: '晨曦',
                    label: '晨曦',
                    children: [{
                        value: 'brain_predictor',
                        label: 'brain_predictor',
                    }]
                }],
                stresschartData: {
                    columns: ['状态', '数量'],
                    rows: [
                        {'状态': '成功', '数量': 0},
                        {'状态': '失败', '数量': 0}
                    ]
                },
                FailData: {
                    columns: ['状态', '数量'],
                    rows: [
                        {'状态': '成功', '数量': 0},
                        {'状态': '失败', '数量': 0}
                    ]
                },
                basedata: [],
                stressData: [],

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

        filters: {
            numFilter(value) {
                let realVal = ''
                if (!isNaN(value) && value !== '') {
                    // 截取当前数据到小数点后两位
                    realVal = parseFloat(value).toFixed(2)
                } else {
                    realVal = '--'
                }
                return realVal
            }
        },
        methods: {
            // 获取页面传参
            getParams() {
                this.routerParams = this.$route.query;
                this.stressId = this.routerParams.stress_id;
                this.projectName = this.routerParams.projectName
            }
            ,
            // 更新消息弹出，调用更新数据接口
            ToUpdate() {
                this.getReport();
                this.$notify.success({
                    title: '刷新成功',
                    message: '图表已更新',
                    showClose: false
                });
            }
            ,
            // 更新消息弹出，调用更新数据接口
            ToMonitor() {
                this.$notify.success({
                    title: '即将跳转到监控页面',
                    message: '即将跳转到监控页面',
                    showClose: false
                });
                this.checkExpress();
            }
            ,
            // 样式 显示
            valuestatus: function (i) {
                if (!/-/g.test(i)) {
                    console.log("2")
                    i = 0
                } else if (!/\+/g.test(i)) {
                    i = 1
                } else {
                    console.log("1")
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
            // 跳转数据详情页面
            showDetail(index, row) {
                this.$router.push({
                    path: '/detail/stressId=' + this.stressId,
                });
            }
            ,
            //展示监控
            checkExpress: function () {
                if (this.basedata.start_date === null) {
                    var startstamp = new Date().getTime();
                } else {
                    var startdate = this.basedata.start_date.replace(/-/g, '/');
                    var startstamp = new Date(startdate).getTime();
                }
                if (this.basedata.end_date === null) {
                    var endstamp = new Date().getTime();
                } else {
                    var enddate = this.basedata.end_date.replace(/-/g, '/');
                    var endstamp = new Date(enddate).getTime();
                }
                const url = "http://10.10.10.2:8084/d/Ss3q6hSZk/server-monitor-test?orgId=1&from=" +
                    startstamp + "&to=" + endstamp + "&var-host_name=" +
                    this.basedata.server + "&var-gpu_exporter_port=9445&var-node_exporter_port=9100&var-cadvisor_port=8080"

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
            }
            ,

            // 压测项目模型
            stressmodel() {
                this.listLoading = true
                const self = this
                const params = {}
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getstressmodel(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.modeloptions = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            }
            ,
            // 获取压测版本
            getversion() {
                this.listLoading = true
                const self = this
                const params = {
                    projectName: this.projectName
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getstressversion(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        var json = JSON.stringify(data.data)
                        this.versions = JSON.parse(json)
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            }
            ,

            // 获取保存结论列表
            getSaveReport() {
                this.listLoading = true
                const self = this
                const params = {
                    stressid: this.stressId,
                    summary: this.basedata.summary
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                saveAnalysis(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.summary = data.summary
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            }
            ,
            // 获取数据列表
            getReport() {
                this.listLoading = true
                const self = this
                const params = {
                    stressId: this.stressId,
                    type: this.filters.type,
                    checkversion: this.filters.checkversion,
                    models: this.filters.models
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getStressReport(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.reportdata = data
                        this.modelName = data.modelsName  // 模型名
                        this.stresschartData.rows = data.report.aiResult  //
                        this.basedata = data.report.basedata  // 基础数据信息
                        this.prediction = data.result// 预测 结果数据
                        this.job = data.jobresult  // job 结果数据
                        this.diff = data.diffresult  // job 数据 - 预测数据 结果
                        this.chartData = data.chartData  // 各个版本预测时间对比
                        this.DataChart.rows = data.LineData  // 预测时间

                        this.stressData = [{
                            strategy: '基准测试',
                            vu: this.basedata.synchroniz,
                            count: this.basedata.benchmark,
                            time: ''
                        }, {
                            strategy: '单一模型',
                            vu: this.basedata.synchroniz,
                            count: this.basedata.single,
                            time: ''
                        }, {
                            strategy: '混合模型',
                            vu: this.basedata.synchroniz,
                            count: '',
                            time: this.basedata.loop_time
                        },],
                            // 错误数据 图表
                            this.FailData = {
                                columns: ['状态', '数量'],
                                rows: data.report.errorData

                            }
                    }
                    else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            }
            ,
            handleCurrentChange(val) {
                this.page = val
                this.getdata()
            }
            ,
            selsChange: function (sels) {
                this.sels = sels
            }
            ,
        }
    }
</script>