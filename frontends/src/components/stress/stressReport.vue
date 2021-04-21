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
                                <el-col style="width: 50%" label-position="left" align="center" >
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
                        <p>预测饼图</p>
                        <ve-ring :data="stresschartData" :settings="chartSettings"></ve-ring>
                    </el-col>
                    <el-col style="width: 25%">
                        <p>Error</p>

                        <ve-ring :data="FailData" :settings="SummarySettings"></ve-ring>

                    </el-col>
                </el-row>
                <el-row style="width: 60%">
                    <el-col>
                        <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                            <span class="bug-ex-item">Result Analysis</span><img
                                    src="../../assets/img/bug-10.png"></p>
                    </el-col>
                    <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
                        <el-input type="textarea" :rows="10" v-model="basedata.summary"></el-input>
                        <el-button type="primary" @click="getSaveReport">保存更新</el-button>
                    </el-col>
                </el-row>

                <el-row>
                    <el-col style="width: 100%">
                        <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                            <span class="bug-ex-item">{{diseases}} 各个版本时间对比图</span><img
                                    src="../../assets/img/bug-10.png"></p>
                        <el-row>
                            <!--工具条-->
                            <el-form :inline="true" :model="filters" @submit.native.prevent>
                                <el-form-item>
                                    <el-select v-model="filters.type" placeholder="类型">
                                        <el-option key="jz" label="基准测试" value="jz"/>
                                        <el-option key="hh" label="混合测试" value="hh"/>
                                        <el-option key="dy" label="单一测试" value="dy"/>
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
                                <el-button type="primary" @click="ToMonitor">监控</el-button>
                                <el-button type="primary" @click="ToUpdate">发送</el-button>
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
                            <span class="bug-ex-item">Prediction Time Result</span><img
                                    src="../../assets/img/bug-10.png"></p>
                        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
                            <el-form :inline="true" :model="filters">
                                <el-select v-model="filters.type" placeholder="类型">
                                    <el-option key="jz" label="基准测试" value="jz"/>
                                    <el-option key="hh" label="混合测试" value="hh"/>
                                    <el-option key="dy" label="单一测试" value="dy"/>
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
                            <el-table-column prop="modelname" label="modelname" min-width="8%">
                                <template slot-scope="scope">
                                    <span style="margin-left: 10px">{{ scope.row.modelname }}</span>
                                </template>
                            </el-table-column>
                            <el-table-column prop="slicenumber" label="sliceThickness" min-width="8%">
                                <template slot-scope="scope">
                                    <span style="margin-left: 10px">{{ scope.row.slicenumber }}</span>
                                </template>
                            </el-table-column>
                            <el-table-column prop="type" label="prediction_count" min-width="8%">
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
                            <el-table-column label="median pred time /s" min-width="10%" >
                                <template slot-scope="scope">
                        <span style="margin-left: 10px"
                              :class="valuestatus(scope.row.median)">{{ scope.row.median }}</span>
                                </template>
                            </el-table-column>
                            <el-table-column label="min pred time /s" min-width="10%" >
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
                            <el-table-column label="预测成功率" min-width="8%">
                                <template slot-scope="scope">
                                    <div slot="reference" class="name-wrapper">
                                        <el-tag size="medium" type="success">{{ scope.row.rate }}
                                        </el-tag>
                                    </div>
                                </template>
                            </el-table-column>
                        </el-table>
                        <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                            <span class="bug-ex-item">Job Time Result</span><img src="../../assets/img/bug-10.png"></p>
                        <el-table :data="job" highlight-current-row v-loading="listLoading"
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
                            <el-table-column prop="type" label="job_count" min-width="8%">
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
                        <span style="margin-left: 10px"
                              :class="valuestatus(scope.row.single)">{{ scope.row.single }}</span>
                                </template>
                            </el-table-column>
                            <el-table-column label="median job time /s" min-width="10%">
                                <template slot-scope="scope">
                        <span style="margin-left: 10px"
                              :class="valuestatus(scope.row.median)">{{ scope.row.median }}</span>
                                </template>
                            </el-table-column>
                            <el-table-column label="min job time /s" min-width="10%">
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
                        <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                            <span class="bug-ex-item">Job - Prediction Time Result</span><img
                                    src="../../assets/img/bug-10.png"></p>
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
                            <el-table-column label="median pred time /s" min-width="10%" >
                                <template slot-scope="scope">
                        <span style="margin-left: 10px"
                              :class="valuestatus(scope.row.median)">{{ scope.row.median }}</span>
                                </template>
                            </el-table-column>
                            <el-table-column label="min pred time /s" min-width="10%" >
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
                        <el-table-column label="rate of success" min-width="8%" >
                            <template slot-scope="scope">
                                <span style="margin-left: 10px">{{ scope.row.rate }}</span>
                            </template>
                        </el-table-column>
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
        getstressversion, getstressmodel, getStressReport, getbase, getreportfigure, saveAnalysis
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
                    type: "jz",
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
        methods: {
            // 获取页面传参
            getParams() {
                this.routerParams = this.$route.query;
                this.stressId = this.routerParams.stress_id;
                this.projectName = this.routerParams.projectName
            },
            // 更新消息弹出，调用更新数据接口
            ToUpdate() {
                this.getReport();
                this.$notify.success({
                    title: '刷新成功',
                    message: '图表已更新',
                    showClose: false
                });

            },
            // 更新消息弹出，调用更新数据接口
            ToMonitor() {
                this.$notify.success({
                    title: '即将跳转到监控页面',
                    message: '即将跳转到监控页面',
                    showClose: false
                });
                this.checkExpress();
            },
            // 样式 显示
            valuestatus: function (a) {
                if (a === "匹配成功") {
                    return 'statuscssb';
                } else {
                    return 'statuscssa';
                }
            },
            // 跳转数据详情页面
            showDetail(index, row) {
                this.$router.push({
                    path: '/detail/stressId=' + this.stressId,
                });
            },
            //展示监控
            checkExpress: function () {
                if (this.basedata.start_date === null) {
                    var startstamp = new Date().getTime();
                }
                else {
                    var startdate = this.basedata.start_date.replace(/-/g, '/');
                    var startstamp = new Date(startdate).getTime();
                }
                if (this.basedata.end_date === null) {
                    var endstamp = new Date().getTime();
                }
                else {
                    var enddate = this.basedata.end_date.replace(/-/g, '/');
                    var endstamp = new Date(enddate).getTime();
                }
                {
                    window.location.href = "http://192.168.1.121:3000/d/Ss3q6hSZk/server-monitor-test?orgId=1&from=" +
                        startstamp + "&to=" + endstamp + "&var-host_name=" +
                        this.basedata.server + "&var-gpu_exporter_port=9445&var-node_exporter_port=9100&var-cadvisor_port=8080"
                }
                // //刷新当前页面
                // window.location.reload();
            },
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
            },
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
            },
            // 获取保存结论列表
            getSaveReport() {
                this.listLoading = true
                const self = this
                const params = {
                    stressid: this.stressId,
                    summary: this.summary
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
            },
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
                        this.stresschartData.rows = data.report.aiResult
                        this.basedata = data.report.basedata
                        this.prediction = data.predictionresult
                        this.job = data.jobresult
                        this.diff = data.diffresult
                        this.stressData = data.stressData
                        this.chartData = data.chartData
                        this.stressData = [{
                            strategy: '基准测试',
                            vu: this.basedata.synchroniz,
                            count: this.basedata.benchmark,
                            time: ''
                        }, {
                            strategy: '单一模型',
                            vu: this.basedata.synchroniz,
                            count:this.basedata.single,
                            time: ''
                        },{
                            strategy: '混合模型',
                            vu: this.basedata.synchroniz,
                            count: '',
                            time: this.basedata.loop_time
                        },],
                            this.FailData = {
                                columns: ['状态', '数量'],
                                rows: data.errorData
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