<template>
    <div class="app-container">
        <div class="filter-container">
            <el-main>
        <el-scrollbar>
            <el-row :gutter="20">
                <el-col :span="12" class="echarts-item">
                    <el-card>
                        <div class="content-title">饼状图示例</div>
                        <ve-pie :data="pieChartData" :settings="pieChartSettings"></ve-pie>
                    </el-card>
                </el-col>
                <el-col :span="12" class="echarts-item">
                    <el-card>
                        <div class="content-title">环形图示例</div>
                        <ve-ring :data="ringChartData" :settings="ringChartSettings"></ve-ring>
                    </el-card>
                </el-col>
                <el-col :span="12" class="echarts-item">
                    <el-card>
                        <div class="content-title">柱状图示例</div>
                        <ve-histogram :data="histogramChartData" :settings="histogramChartSettings"
                                      :mark-line="histogramChartMarkLine"></ve-histogram>
                    </el-card>
                </el-col>
                <el-col :span="12" class="echarts-item">
                    <el-card>
                        <div class="content-title">折线图示例</div>
                        <ve-line :data="lineChartData" :settings="lineChartSettings"
                                 :mark-point="lineChartMarkPoint"></ve-line>
                    </el-card>
                </el-col>
            </el-row>
        </el-scrollbar>
    </el-main>
            <el-row>
                <!--图表-->
                <el-col :span="100" class="toolbar" style="padding-bottom: 0px;">
                    <el-card shadow="hover" style="width:50%;height:600px;">
                        <el-row :gutter="50">
                            <el-col :span="30">
                                <el-card shadow="hover">
                                    <div ref='echarts' class="myLine" style="width:750px;height:500px;margin:0 auto">
                                    </div>
                                </el-card>
                            </el-col>
                        </el-row>
                    </el-card>
                </el-col>
                <el-col>
                    <el-card shadow="hover" style="width:50%;height:600px;">
                        <el-row :gutter="20">
                            <el-col :span="12">
                                <el-card shadow="hover">
                                    <div id='smokeBar' class="mybar"
                                         style="width: 750px;height: 500px;margin:0 auto;">
                                    </div>
                                </el-card>
                            </el-col>
                        </el-row>
                    </el-card>

                </el-col>
            </el-row>
            <!--工具条-->
            <el-col :span="20" class="toolbar" style="padding-bottom: 0px;">
                <el-form :inline="true" :model="filters" @submit.native.prevent>
                    <el-form-item label="服务器" prop="server">
                        <el-select v-model="filters.server" placeholder="请选择服务" @click.native="gethost()">
                            <el-option v-for="(item,index) in tags"
                                       :key="item.host"
                                       :label="item.name"
                                       :value="item.host"
                            />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="版本">
                        <el-input v-model="filters.version"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-select v-model="filters.diseases" placeholder="请选择病种类型" @click.native="getBase()">
                            <el-option v-for="(item,index) in tags"
                                       :key="item.remarks"
                                       :label="item.remarks"
                                       :value="item.remarks"
                            />
                        </el-select>
                    </el-form-item>
                    <el-select v-model="filters.status" placeholder="预测状态">
                        <el-option key="true" label="成功" value="true"/>
                        <el-option key="false" label="失败" value="false"/>
                    </el-select>
                    <el-form-item>
                        <el-button type="primary" @click="getdata">查询</el-button>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="warning" @click="smoketest">smoke测试</el-button>
                    </el-form-item>
                    <el-button type="danger" :disabled="this.sels.length===0" @click="batchdel">删除报告</el-button>
                </el-form>
            </el-col>
            <!--列表-->
            <el-table
                    v-loading="listLoading"
                    :data="stresslist"
                    highlight-current-row
                    style="width: 100%;"
                    @selection-change="selsChange">
                <el-table-column prop="ID" label="ID" min-width="4%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.id }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="服务器" label="服务器" min-width="10%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.server }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="version" label="版本" min-width="8%" sortable>
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.version }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="diseases" label="病种" min-width="8%" sortable>
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.diseases }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="studyinstanceuid" label="Studyinstanceuid" min-width="25%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.studyinstanceuid }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="sendstatus" label="预测状态" min-width="8%">
                    <template slot-scope="scope">
                        <img v-show="scope.row.status"
                             style="width:18px;height:18px;margin-right:5px;margin-bottom:5px"
                             src="../../../assets/img/qiyong.png"/>
                        <img v-show="!scope.row.status"
                             style="width:15px;height:15px;margin-right:5px;margin-bottom:5px"
                             src="../../../assets/img/shibai.png"/>
                    </template>
                </el-table-column>
                <el-table-column label="预测时间" min-width="8%" sortable>
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.time }} 秒</span>
                    </template>
                </el-table-column>
                <el-table-column label="slice" min-width="8%" sortable>
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.slicenumber }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="预测张数" min-width="5%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.imagecount }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="标准" min-width="10%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px"
                              :class="valuestatus(scope.row.report)">{{ scope.row.diagnosis }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="实际" min-width="10%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px" :class="valuestatus(scope.row.report)">{{ scope.row.aidiagnosis }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="结果" min-width="8%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px"
                              :class="valuestatus(scope.row.report)">{{ scope.row.report }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="操作" min-width="8px">
                    <template slot-scope="scope">
                        <!--          <el-button v-if=scope.row.edit  type="success"  size="small" icon="el-icon-circle-check-outline" @click="handleEdit(scope.$index, scope.row)">Ok</el-button>-->
                        <!--          <el-button v-else type="primary" size="small" icon="el-icon-edit" @click=scope.row.edit=!scope.row.edit>Edit</el-button>-->
                        <el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)">重测
                        </el-button>
                        <!--             return <el-button type="primary" size="small" @click="handle(scope.$index, scope.row)">跳转</el-button>-->
                    </template>
                </el-table-column>
            </el-table>
            <!--工具条-->
            <el-col :span="24" class="toolbar">
                <el-pagination
                        layout="prev, pager, next"
                        :page-size="20"
                        :page-count="total"
                        style="float:right;"
                        @current-change="handleCurrentChange"
                />
            </el-col>
        </div>
    </div>
</template>

<script>
    // import NProgress from 'nprogress'
    import {
        getHost, getsmokerecord, getsmokestart, getbase, getsmokefigure
    } from '@/router/api'
    import echarts from 'echarts'
    Vue.use(VCharts)
    export default {
        // components: {ElRow},
        data() {
            return {
                smokeBar: {},
                //定义表数据
                smokeBarData: [],
                filters: {
                    diseases: null,
                    slicenumber: null,
                    diseases: '',
                    server: '',
                    version: '',
                    status: ''
                },
                total: 0,
                page: 1,
                page_size: 50,
                listLoading: false,
                sels: [], // 列表选中列

                // 新增界面数据
                addForm: {
                    diseases: '',
                    server: '192.168.1.208',
                    studyinstanceuid: ''
                },
                addFormVisible: false, // 新增界面是否显示
                addLoading: false,
                addFormRules: {
                    diseases: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ]
                },
                chart: null,
                smokeBaroption: {
                    backgroundColor: '#2c343c',
                    title: {
                        text: '冒烟测试-成功/失败状态图',
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
                            name: '成功失败状态',
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
                mounted() {
                    this.getdata();
                    this.gethost();
                    this.getecharts();
                    this.drawsmokeBar();
                },
                created() {
                    this.getsmokeData();

                }, watch: {
                    //观察option的变化
                    smokeBaroption: {
                        handler(newVal, oldVal) {
                            if (this.smokeBar) {
                                if (newVal) {
                                    this.smokeBar.setOption(newVal);
                                } else {
                                    this.smokeBar.setOption(oldVal);
                                }
                            } else {
                                this.drawsmokeBar();
                            }
                        },
                        deep: true //对象内部属性的监听，关键。
                    },
                },

                methods: {
                    getsmokeData() {
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
                        getsmokefigure(headers, params).then(_data => {
                            let {code, msg, data} = _data;
                            this.smokeLineData = data.figure_list;
                            this.smokeLineoption.xAxis.data = this.smokeLineData[0];
                            this.smokeLineoption.series[0].data = this.smokeLineData[1];
                            this.smokeLineoption.series[1].data = this.smokeLineData[2];

                            this.smokeBarData = data.solution_state.sort(function (a, b) {
                                return a.value - b.value;
                            });
                            this.smokeBaroption.series[0].data = this.smokeBarData;

                        });
                    },
                    drawsmokeBar() {
                        this.smokeBar = echarts.init(document.getElementById('smokeBar'));
                        this.smokeBar.setOption(this.smokeBaroption, true);
                        setTimeout(() => {
                            window.onresize = smokeBar.resize;
                        }, 200);
                    },
                    valuestatus: function (a) {
                        if (a === "匹配成功") {
                            return 'statuscssb';
                        } else {
                            return 'statuscssa';
                        }
                    },
                    getecharts() {
                        this.chart = echarts.init(this.$refs.echarts);
                        // 使用刚指定的配置项和数据显示图表。
                        this.chart.setOption(this.option);
                    },
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
                    // 获取getBase列表
                    getBase() {
                        this.listLoading = true
                        const self = this
                        const params = {
                            selecttype: "dicom", type: "Gold",
                            status: 1
                        }
                        const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                        getbase(headers, params).then((res) => {
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
                    smoketest() {
                        this.listLoading = true
                        const self = this
                        const params = {
                            server_ip: self.filters.server,
                            diseases: self.filters.diseases,
                            version: self.filters.version
                        }
                        const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                        getsmokestart(headers, params).then((res) => {
                            self.listLoading = false
                            const {msg, code, data} = res
                            if (code === '0') {
                                self.$message.success({
                                    message: "运行中！~~~~~",
                                    center: true
                                })
                            } else {
                                self.$message.error({
                                    message: msg,
                                    center: true
                                })
                            }
                        })
                    },
                    // 获取数据列表
                    getdata() {
                        this.listLoading = true
                        const self = this
                        const params = {
                            page: self.page,
                            diseases: self.filters.diseases,
                            server: self.filters.server,
                            version: self.filters.version,
                            type: 'Gold',
                            status: self.filters.status
                        }
                        const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                        getsmokerecord(headers, params).then((res) => {
                            self.listLoading = false
                            const {msg, code, data} = res
                            if (code === '0') {
                                self.total = data.total
                                self.page = data.page
                                self.stresslist = data.data
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
                    // 批量删除
                    batchRemove: function () {
                        const ids = this.sels.map(item => item.id)
                        const self = this
                        this.$confirm('确认删除选中记录吗？', '提示', {
                            type: 'warning'
                        }).then(() => {
                            this.listLoading = true
                            // NProgress.start();
                            const self = this
                            const params = {ids: ids}
                            const header = {
                                'Content-Type': 'application/json',
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            }
                            deldicomdata(header, params).then(_data => {
                                const {msg, code, data} = _data
                                if (code === '0') {
                                    self.$message({
                                        message: '删除成功',
                                        center: true,
                                        type: 'success'
                                    })
                                } else {
                                    self.$message.error({
                                        message: msg,
                                        center: true
                                    })
                                }
                                self.getdata()
                            })
                        })
                    },
                    // 批量删除报告
                    batchDel: function () {
                        const ids = this.sels.map(item => item.id)
                        const self = this
                        this.$confirm('确认删除选中记录的报告吗？', '提示', {
                            type: 'warning'
                        }).then(() => {
                            this.listLoading = true
                            // NProgress.start();
                            const self = this
                            const params = {ids: ids}
                            const header = {
                                'Content-Type': 'application/json',
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            }
                            deldicomreport(header, params).then(_data => {
                                const {msg, code, data} = _data
                                if (code === '0') {
                                    self.$message({
                                        message: '删除成功',
                                        center: true,
                                        type: 'success'
                                    })
                                } else {
                                    self.$message.error({
                                        message: msg,
                                        center: true
                                    })
                                }
                                self.getdata()
                            })
                        })
                    }
                }
            }
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

    .simpleDemo {
        width: 600px;
        height: 400px;
        float: left;
        margin: 0 auto;
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
