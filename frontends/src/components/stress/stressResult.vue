<template>
    <div class="app-container">

        <div class="filter-container">
            <!--工具条-->
            <el-row>
                <el-col style="width: 100%">
                    <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                        <span class="bug-ex-item">{{diseases}} 各个版本时间对比图</span><img
                                src="../../assets/img/bug-10.png"></p>
                    <el-row>
                        <!--工具条-->
                        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
                            <el-form :inline="true" :model="filters" @submit.native.prevent>
                                <el-form-item>
                                    <el-select v-model="filters.type" placeholder="类型">
                                        <el-option key="jz" label="基准测试" value="jz"/>
                                        <el-option key="hh" label="混合测试" value="hh"/>
                                        <el-option key="dy" label="单一测试" value="dy"/>
                                    </el-select>
                                </el-form-item>
                                <el-form-item>
                                    <el-cascader
                                            :options="diseasesoptions"
                                            :props="props"
                                            clearable v-model="filters.diseases"
                                            @click.native="stressmodel()"></el-cascader>
                                </el-form-item>
                                <el-form-item>
                                    <el-button type="primary" @click="ToUpdate">更新</el-button>
                                </el-form-item>
                                <!--                                <el-form-item>-->
                                <!--                                    <el-button type="warning" @click="handleAdd">监控</el-button>-->
                                <!--                                </el-form-item>-->
                            </el-form>
                        </el-col>

                    </el-row>

                    <ve-line
                            :set-option-opts="false"
                            :data="chartData"
                            :data-zoom="chartDataZoom">
                    </ve-line>

                </el-col>
            </el-row>

            <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
                <el-form :inline="true" :model="filters" @click.native="getreportData()">
                    <el-select v-model="filters.type" placeholder="类型">
                        <el-option key="jz" label="基准测试" value="jz"/>
                        <el-option key="hh" label="混合测试" value="hh"/>
                        <el-option key="dy" label="单一测试" value="dy"/>
                    </el-select>
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
                        <el-button type="primary" @click="getstresslist">查询</el-button>
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
                        <span style="margin-left: 10px"
                              :class="valuestatus(scope.row.median)">{{ scope.row.median }}</span>
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
                        <span style="margin-left: 10px"
                              :class="valuestatus(scope.row.single)">{{ scope.row.single }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="median job time /s" min-width="10%" sortable>
                    <template slot-scope="scope">
                        <span style="margin-left: 10px"
                              :class="valuestatus(scope.row.median)">{{ scope.row.median }}</span>
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
                        <span style="margin-left: 10px"
                              :class="valuestatus(scope.row.median)">{{ scope.row.median }}</span>
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
        </div>
    </div>
</template>

<script>
    // import NProgress from 'nprogress'

    import {
        getstressversion, getstressresult, getHost, getreportfigure, getstressmodel
    } from '@/router/api';
    import echarts from "echarts";

    export default {
        // import ElRow from "element-ui/packages/row/src/row";
        // components: {ElRow},
        data() {
            this.chartDataZoom = [{type: 'slider'}]
            return {
                props: {multiple: false}, // 控制级联选择 是否允许多选
                filters: {
                    server: '192.168.1.208',
                    diseases: '',
                    type: "jz"
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
                        value: '2.18.1',
                        label: '2.18.1',
                        children: [{
                            value: 'Brain',
                            label: 'Brain'
                        }]
                    }, {
                        value: 1,
                        label: 'Brain'
                    }, {
                        value: 13,
                        label: 'SWI'
                    }]
                }, {
                    value: 'Gold',
                    label: 'Gold',
                    children: [{
                        value: 1,
                        label: 'Lung'
                    }, {
                        value: 1,
                        label: 'Brain'
                    }, {
                        value: 13,
                        label: 'SWI'
                    }]
                }],
                durationlist: [],
                total: 0,
                page: 1,
                listLoading: false,
                sels: [], // 列表选中列
                host: [],
                //定义表
                series: []
            }
        },
        components: {},
        mounted() {
            this.gethost();
            this.getBase();
        },
        created() {
            this.getreportData();
        },
        methods: {
            ToUpdate() {
                this.getreportData();
                this.$notify.success({
                    title: '刷新成功',
                    message: '图表已更新',
                    showClose: false
                });

            },
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
                        self.diseasesoptions = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
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
                const params = {
                    page_size: 100
                }
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
            getstresslist() {
                this.listLoading = true
                const self = this
                const params = {
                    version: this.filters.version,
                    checkversion: this.filters.checkversion,
                    type: this.filters.type
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
                    "type": this.filters.type,
                    "diseases": this.filters.diseases
                };
                let headers = {
                    "Content-Type": "application/json"
                };
                getreportfigure(headers, params).then(_data => {
                    let {code, msg, data} = _data;
                    this.chartData = data.chartData;
                });
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
