<template>
    <div class="app-container">

        <div class="filter-container">
            <!--工具条-->
            <el-col :span="100" class="toolbar" style="padding-bottom: 0px;">
                <aside>
                    <a href="http://192.168.2.38:3000/d/Ss3q6hSZk/docker-and-os-metrics-test?orgId=1&refresh=5s&from=now-5m&to=now&var-host_name=192.168.2.60&var-gpu_exporter_port=9445&var-node_exporter_port=9100&var-cadvisor_port=8080" target="_blank">Stress Monitor
                    </a>
                </aside>
                <el-form ref="form" :model="form" status-icon :rules="rules" label-width="100px">
                    <el-row>
                        <el-col :span="3">
                            <el-form-item label="服务器" prop="hostid">
                            <el-select v-model="form.hostid"  placeholder="请选择" @click.native="gethost()">
                              <el-option
                                v-for="(item,index) in tags"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id"
                              />
                            </el-select>
                          </el-form-item>
                        </el-col>
                        <el-col :span="3">
                        <el-form-item label="测试版本" prop="version">
                          <el-input id="version" v-model="form.version" placeholder="测试版本" />
                        </el-form-item>
                      </el-col>
                        <el-col :span="3">
                              <el-form-item label="压测时间" prop="loop_time">
                                <el-input id="loop_time" v-model="form.loop_time" placeholder="测试小时" />
                              </el-form-item>
                            </el-col>
                        <el-col :span="3">
                            <el-form-item label="线程数" prop="loop_time">
                                <el-input id="thread" v-model="form.thread" placeholder="个" />
                              </el-form-item>
                            </el-col>
                            <el-col :span="3">
                              <el-form-item label="循环次数" prop="loop">
                                <el-input id="loop" v-model="form.loop" placeholder="个" />
                              </el-form-item>
                            </el-col>
                        <el-col :span="3">
                              <el-form-item label="并发" prop="synchronizing">
                                <el-input id="synchronizing" v-model="form.synchronizing" placeholder="个" />
                              </el-form-item>
                            </el-col>
                        <el-col :span="4">
                            <el-form-item>
                                <el-button type="primary" @click="stressrun('form')">执行</el-button>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form>
                    <el-row>
                            <el-checkbox-group v-model="form.testdata" size="small">
                              <el-checkbox-button v-for="(item,index) in dibase" :label="item.remarks" :key="item.remarks">{{item.remarks}}</el-checkbox-button>
                            </el-checkbox-group>
                    </el-row>

                <aside>
                    <a href="http://192.168.2.38:9000/" target="_blank">测试结果
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
        getstressversion,getstressresult, getHost,getbase,stressTool
    } from '@/router/api'
    import {addbaseData} from "../../router/api";
  export default {
    // import ElRow from "element-ui/packages/row/src/row";
        // components: {ElRow},
        data() {
            return {
                cities: ['lung','swi','svd'],
                form: {
                    version: '',
                    loadserver: '',
                    loop_time: '',
                    thread:4,
                    synchronizing:0,
                    testdata:['Lung','Brain','SWI','SVD','Tumor','Heart','Hematoma','CTA','CTP'],
                    switch:false
                },
                rules: {
                    server: [
                        {required: true, message: '请输入测试服务器', trigger: 'blur'}
                    ],
                    version: [
                        {required: true, message: '请输入测试版本', trigger: 'blur'}
                    ]
                },
                filters: {
                    diseases: ''
                },
                durationlist: [],
                total: 0,
                page: 1,
                listLoading: false,
                sels: [], // 列表选中列

                editFormVisible: false, // 编辑界面是否显示
                editLoading: false,
                options: [{label: 'Web', value: 'Web'}, {label: 'App', value: 'App'}],
                editFormRules: {
                    diseases: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ],
                    type: [
                        {required: true, message: '请选择类型', trigger: 'blur'}
                    ],
                    version: [
                        {required: true, message: '请输入版本号', trigger: 'change'},
                        {pattern: /^\d+\.\d+\.\d+$/, message: '请输入合法的版本号（x.x.x）'}
                    ],
                    description: [
                        {required: false, message: '请输入描述', trigger: 'blur'},
                        {max: 1024, message: '不能超过1024个字符', trigger: 'blur'}
                    ]
                },
                // 编辑界面数据
                filters: {
                    checkversion: '2.11.0',
                    version: '2.10.0RC9',
                    server: '192.168.1.208'
                },
                // 新增界面数据
                addForm: {
                    diseases: '',
                    version: '',
                    type: '',
                    description: ''
                }

            }
        },
        mounted() {
            this.getDurationlist()
            this.gethost()
            this.getBase()
        },
        methods: {
            // 执行压测
            stressrun(formName) {
                let self = this;
                this.tableData = null
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        let params = JSON.stringify({
                            version: this.form.version,
                            loadserver: this.form.loadserver,
                            loop_time: this.form.loop_time,
                            thread:this.form.thread,
                            testdata: this.form.testdata,
                            switch: this.form.switch,
                            loop: this.form.loop,
                            hostid:this.form.hostid,
                            synchronizing:this.form.synchronizing
                        });
                        let header = {
                            "Content-Type": "application/json",
                            Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                        };
                        stressTool(header, params).then(_data => {
                            let {msg, code,data } = _data;
                            console.log(code);
                            if (code === '0') {
                                self.$message({
                                    message: '执行成功',
                                    center: true,
                                    type: 'Success'
                                });
                            } else {
                                self.$message.error({
                                        message: msg,
                                        center: true,
                                    });
                            }
                        })
                    }
                })
            },
            getversion() {
                let self = this;
                this.listLoading = true
                const params = {}
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getstressversion(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.total = data.total
                        this.list = data.data
                        var json = JSON.stringify(this.list)
                        this.versions = JSON.parse(json)
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
                let self = this;
                this.listLoading = true
                const params = {selecttype:"dicom",status:1}
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getbase(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.total = data.total
                        this.list = data.data
                        var json = JSON.stringify(this.list)
                        this.dibase = JSON.parse(json)
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
                let self = this;
                const params = {
                    page_size:100
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getHost(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.total = data.total
                        this.list = data.data
                        var json = JSON.stringify(this.list)
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
                let self = this;
                const params = {
                    version: this.filters.version,
                    checkversion: this.filters.checkversion,
                    server: this.filters.server
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getstressresult(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.prediction = data.predictionresult
                        this.job =data.jobresult
                        this.lung =data.lungresult
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
    .view-png {
        width:15px;
        height:15px;
        margin-right:3px;
        margin-bottom:5px
    }
</style>
