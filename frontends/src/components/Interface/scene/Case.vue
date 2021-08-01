<template>
    <div class="app-container">
        <div class="filter-container">
            <el-row>
                <el-page-header @back="goBack" content="详情页面">
            </el-page-header>
                <!--工具条-->
                <el-col :span="30" class="toolbar" style="padding-bottom: 0px;">
                    <el-form :inline="true" :model="filters" @submit.native.prevent>
                        <el-form-item label="版本/名称" prop="version">
                            <el-input placeholder="请输入内容" v-model="CaseForm.name">
                                <template slot="prepend">{{CaseForm.version}}</template>
                            </el-input>

                        </el-form-item>
                        <el-form-item label="服务器" prop="server">
                            <el-select @click.native="gethost()" placeholder="请选择服务" v-model="CaseForm.loadserver">
                                <el-option key="" label="" value=""></el-option>
                                <el-option :key="item.id"
                                           :label="item.name"
                                           :value="item.id"
                                           v-for="(item,index) in Host"
                                />
                            </el-select>
                        </el-form-item>

                        <el-form-item>
                            <el-button @click="editSubmit" type="primary">修改</el-button>
                        </el-form-item>
                        <el-form-item>
                            <el-button @click="stressStop" type="danger">停止</el-button>
                        </el-form-item>
                        <el-form-item>
                            <el-button @click="showReport" type="warning">报告</el-button>
                        </el-form-item>
                    </el-form>
                </el-col>
            </el-row>
            <!--列表-->
            <el-row>
                <el-form :model="CaseForm" :rules="CaseFormRules" label-width="80px" ref="addForm">
                    <el-card>
                        <el-divider>基础配置</el-divider>
                        <el-row :gutter="24">
                            <el-col span="8">
                                <el-form-item label="用例ID" prop='id'>
                                    <el-input id="用例ID" v-model="CaseForm.id" placeholder=""/>
                                </el-form-item>
                            </el-col>
                            <el-col span="8">
                                <el-form-item label="用例名称" prop='casename'>
                                    <el-input id="用例名称" v-model="CaseForm.casename" placeholder=""/>
                                </el-form-item>
                            </el-col>
                            <el-col span="8">
                                <el-form-item label="场景组" prop='casename'>
                                    <el-input id="场景组" v-model="CaseForm.group" placeholder=""/>
                                </el-form-item>
                            </el-col>
                        </el-row>
                        <el-row :gutter="24">
                            <el-col span="8">
                                <el-form-item label="用例等级" prop='level'>
                                    <el-input id="用例等级" v-model="CaseForm.level" placeholder=""/>
                                </el-form-item>
                            </el-col>
                            <el-col span="8">
                                <el-form-item label="修改用户" prop='casename'>
                                    <el-input id="修改用户" v-model="CaseForm.user" placeholder=""/>
                                </el-form-item>
                            </el-col>
                            <el-col span="8">
                                <el-form-item label="修改时间" prop='benchmarkstart'>
                                    <el-input
                                            placeholder="请选择日期"
                                            suffix-icon="el-icon-date"
                                            v-model="CaseForm.start_date">
                                    </el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>
                        <el-row :gutter="24">
                            <el-col span="8">
                                <el-form-item label="状态" prop='status'>
                                    <el-input id="status" v-model="CaseForm.status" placeholder="status"/>
                                </el-form-item>
                            </el-col>
                            <el-col span="8">
                                <el-form-item label="描述" prop='status'>
                                    <el-input id="remask" v-model="CaseForm.remask" placeholder="remask"/>
                                </el-form-item>
                            </el-col>
                        </el-row>

                    </el-card>
                    <el-row>
                        <el-card>
                            <el-divider>场景配置</el-divider>
                            <el-row :gutter="24">
                                <el-col :span="12">
                                    <el-button @click="stressRun('')" type="primary"
                                    >修改
                                    </el-button>
                                </el-col>
                            </el-row>
                        </el-card>
                    </el-row>
                    <el-card>
                        <el-table :data="CaseDetail" @selection-change="selsChange"
                                  style="width: 100%;"
                                  v-loading="listLoading">
                            <el-table-column label="接口名称" min-width="8%" prop="modelname">
                                <template slot-scope="scope">
                                    <span style="margin-left: 11px;color: #07c4a8; font-family:微软雅黑">{{ scope.row.modelname }}_{{ scope.row.slicenumber }}</span>
                                </template>
                            </el-table-column>
                            <el-table-column label="接口" min-width="12%" prop="type">
                                <template slot-scope="scope">
                                    <el-row>
                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Job:</span>
                                        <span :class="valuestatus(scope.row.jobavg)"
                                              style="margin-left: 10px">{{ scope.row.jobavg }}</span>
                                    </el-row>
                                </template>
                            </el-table-column>
                            <el-table-column label="入参" min-width="10%">
                                <template slot-scope="scope">
                                    <el-row>
                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Job:</span>
                                        <span :class="valuestatus(scope.row.jobmedian)"
                                              style="margin-left: 10px">{{ scope.row.jobmedian }}</span>
                                    </el-row>
                                </template>
                            </el-table-column>
                            <el-table-column label="返回状态码" min-width="12%">
                                <template slot-scope="scope">
                                    <el-row>
                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Job:</span>
                                        <span :class="valuestatus(scope.row.jobmin)"
                                              style="margin-left: 10px">{{ scope.row.jobmin }}</span>
                                    </el-row>
                                </template>
                            </el-table-column>
                            <el-table-column label="返回值断言" min-width="12%">
                                <template slot-scope="scope">
                                    <el-row>
                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Job:</span>
                                        <span :class="valuestatus(scope.row.jobmin)"
                                              style="margin-left: 10px">{{ scope.row.jobmin }}</span>
                                    </el-row>
                                </template>
                            </el-table-column>
                            <el-table-column label="提取返回值" min-width="12%" prop="type">
                                <template slot-scope="scope">
                                    <el-row>
                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Job:</span>
                                        <span :class="valuestatus(scope.row.jobmax)"
                                              style="margin-left: 10px">{{ scope.row.jobmax }}</span>
                                    </el-row>
                                    <el-row>
                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Prediction:</span>
                                        <span :class="valuestatus(scope.row.max)"
                                              style="margin-left: 10px">{{ scope.row.max }}</span>
                                    </el-row>
                                </template>
                            </el-table-column>
                            <el-table-column label="操作" min-width="12%" prop="type">
                                <template slot-scope="scope">
                                    <el-row>
                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Job:</span>
                                        <span :class="valuestatus(scope.row.jobmax)"
                                              style="margin-left: 10px">{{ scope.row.jobmax }}</span>
                                    </el-row>
                                    <el-row>
                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Prediction:</span>
                                        <span :class="valuestatus(scope.row.max)"
                                              style="margin-left: 10px">{{ scope.row.max }}</span>
                                    </el-row>
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-card>
                </el-form>

            </el-row>

            <!--工具条-->
            <el-col :span="24" class="toolbar">
            </el-col>
            <!--编辑界面-->
            <el-dialog title="修改" :visible.sync="editFormVisible" :close-on-click-modal="false"
                       style="width: 100%; left: 7.5%">
                <el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
                    <el-divider>基本配置</el-divider>

                    <el-row :gutter="24">
                        <el-col :span="12">
                            <el-form-item label="每日发送" prop='sendcount'>
                                <el-input-number v-model="editForm.sendcount" :min="0"
                                                 :max="100000"
                                                 label="每日发送"></el-input-number>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="结束时间">
                                <el-date-picker v-model="editForm.end_time" type="datetime"
                                                placeholder="选择日期" value-format="yyyy-MM-dd HH:mm:ss"></el-date-picker>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click.native="editFormVisible = false">取消</el-button>
                    <el-button type="primary" @click.native="editSubmit" :loading="editLoading">保存</el-button>
                </div>
            </el-dialog>

            <!--新增界面-->
            <el-dialog :close-on-click-modal="false" :visible.sync="addFormVisible" style="width: 100%; left: 10%"
                       title="新增">
                <el-form :model="addForm" :rules="CaseFormRules" label-width="120" ref="addForm">
                    <el-row :gutter="24">
                        <el-card>
                            <el-divider>基本-配置</el-divider>
                            <el-row :gutter="24">
                                <el-col :span="12">
                                    <el-form-item label="Jmeter文件" prop="name">
                                        <el-select @click.native="getuploadList()" placeholder="请选择"
                                                   v-model="CaseForm.filename">
                                            <el-option
                                                    :key="item.filename"
                                                    :label="item.filename"
                                                    :value="item.filename"
                                                    v-for="(item,index) in jmeterList"
                                            />
                                        </el-select>
                                    </el-form-item>
                                </el-col>
                                <el-col :span="12">
                                    <el-form-item label="Jmeter文件" prop="name">
                                        <el-select @click.native="getuploadList()" placeholder="请选择"
                                                   v-model="CaseForm.filename">
                                            <el-option
                                                    :key="item.filename"
                                                    :label="item.filename"
                                                    :value="item.filename"
                                                    v-for="(item,index) in jmeterList"
                                            />
                                        </el-select>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                            <el-divider>Jmeter-配置</el-divider>
                            <el-row :gutter="24">
                                <el-col :span="12">
                                    <el-form-item label="线程数" prop='thread'>
                                        <el-input-number :max="100"
                                                         :min="1"
                                                         label="线程数"
                                                         v-model="CaseForm.thread"></el-input-number>
                                    </el-form-item>
                                </el-col>
                                <el-col :span="12">
                                    <el-form-item label="Ramp-Up" prop='ramp'>
                                        <el-input-number :max="5000"
                                                         :min="0"
                                                         label="Ramp-Up"
                                                         v-model="CaseForm.ramp"></el-input-number>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="12">
                                    <el-form-item label="并发数" prop='synchroniz'>
                                        <el-input-number :max="100"
                                                         :min="0"
                                                         label="并发数"
                                                         v-model="CaseForm.synchroniz"></el-input-number>
                                    </el-form-item>
                                </el-col>

                                <el-col :span="12">
                                    <el-form-item label="持续时间" prop='single'>
                                        <el-input-number :max="1000000"
                                                         :min="0"
                                                         label="持续时间"
                                                         v-model="CaseForm.loop_time"></el-input-number>
                                        秒
                                    </el-form-item>

                                </el-col>
                            </el-row>
                        </el-card>
                    </el-row>
                    <el-row :gutter="24">
                        <el-card>
                            <el-divider>Jmeter-文件更新</el-divider>
                            <el-upload
                                    :before-remove="beforeRemove"
                                    :before-upload="beforeUpload"
                                    :file-list="fileList"
                                    :http-request="handleRequest"
                                    :on-change="changeData"
                                    :on-remove="handleRemove"
                                    action="#"
                                    class="upload-demo"
                                    multiple>

                                <el-button class="btn upload-btn" type="primary">更新附件</el-button>
                                <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                                <div class="el-upload__tip" slot="tip">只能上传jmx/.py文件</div>
                            </el-upload>
                        </el-card>
                    </el-row>
                </el-form>

                <div class="dialog-footer" slot="footer">
                    <el-button @click.native="addFormVisible = false">取消</el-button>
                    <el-button :loading="addLoading" @click.native="addSubmit" type="primary">保存</el-button>
                </div>
            </el-dialog>

        </div>
    </div>
</template>
<script>
    // import NProgress from 'nprogress'

    import {
        getupload, addJmeter, updateJmeter, delJmeter, JmeterList,
        getVersionInfo, StressDetail, StrategyDetail,
        updateStress, stresssave, getHost, getDictionary, stressTool, addupload, delupload

    } from '@/router/api'

    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                fileList: [],
                filedict: {},
                statistics: {}, // 数量统计
                progress: {}, // 策略进度
                JmeterData: [], //jmeter 脚本选择
                CaseDetail: [], //策略模型详情
                modelID: "",
                activeName: 'SceneConfiguration',
                customColors: [
                    {color: '#f5ce6c', percentage: 20},
                    {color: '#3ccde6', percentage: 40},
                    {color: '#1989fa', percentage: 60},
                    {color: '#6f7ad3', percentage: 80},
                    {color: '#03fa54', percentage: 100},
                ],
                Host: {},
                StartDate: "",
                EndDate: "",
                jmeterList: {},
                props: {multiple: true},
                form: {
                    server_ip: '',
                    fuzzy: '是',
                    testtype: 'PatientID',
                    deldata: ''
                },
                rules: {
                    server_ip: [
                        {required: true, message: '请输入测试服务器', trigger: 'blur'}
                    ],
                    version: [
                        {required: true, message: '请输入版本号', trigger: 'change'}
                    ]
                },
                filters: {
                    diseases: '',
                    server: ''
                },
                CaseForm: {},
                total: 0,
                page: 1,
                page_size: 10,
                listLoading: true,
                sels: [], // 列表选中列

                editFormVisible: false, // 编辑界面是否显示
                editLoading: false,
                editFormRules: {
                    diseases: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ],
                    type: [
                        {required: true, message: '请选择类型', trigger: 'blur'}
                    ]
                },
                editLoading: false,
                editForm: {},
                addForm: {
                    port: '4242',
                    type: '匿名',
                    sendcount: 0,
                    end_time: null

                },
                addFormVisible: false, // 新增界面是否显示
                addLoading: false,
                CaseFormRules: {
                    diseases: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ],
                    type: [
                        {required: true, message: '请选择类型', trigger: 'blur'}
                    ],
                    version: [
                        {required: true, message: '请输入版本号', trigger: 'change'},
                    ]
                }
            }
        },
        mounted() {
        },
        methods: {
            // 返回上级页面
            goBack() {
                 this.$router.push({
                    path: '/scene',
                });
                console.log('go back');
            },
            // 样式 显示
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
            //展示监控
            checkExpress: function (start_date, end_date) {
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
                const url = "http://10.10.10.2:8084/d/MTWM-LW7z/qa-jian-kong-zhan-shi-kan-ban?from=" +
                    startstamp + "&to=" + endstamp + "&var-interval=$__auto_interval_interval&var-env=&var-name=&var-node="
                    + this.CaseForm.loadserver + " &var-maxmount=&var-node_port=9100&var-cadvisor_port=8080&gpu_port=9445"

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
            },
            changeData(file, fileList) {
                // 数据小于0.1M的时候按KB显示
                const size = file.size / 1024 / 1024 > 0.1 ? `(${(file.size / 1024 / 1024).toFixed(1)}M)` : `(${(file.size / 1024).toFixed(1)}KB)`
                file.name.indexOf('M') > -1 || file.name.indexOf('KB') > -1 ? file.name : file.name += size
            },
            beforeRemove(file) {
                const isLt2M = file.size / 1024 / 1024 < 100;
                if (!isLt2M) {
                    this.$message.info('文件删除中 ！!');
                    return isLt2M;
                }
            },
            handleRequest(data) {
                let params = new FormData()
                params.append('file', data.file)
                params.append('type', "stress")
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                addupload(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        var filename = data.filename
                        this.filedict[filename] = data.fileid;
                        this.$set(this.filedict, data.filename, data.fileid)
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            //上传前对文件大小进行校验
            beforeUpload(file) {
                const isLt2M = file.size / 1024 / 1024 < 100;
                if (!isLt2M) {
                    this.$message.error('上传文件大小大小不能超过 100MB!');
                    return isLt2M;
                }
            },
            handleRemove(file, fileList) {
                var id = this.filedict[file.raw.name]
                let params = {"id": id, "filename": file.raw.name}
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                delupload(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code} = res
                    if (code === '0') {
                        self.$message.info({
                            message: msg,
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
            handleClick(tab, event) {
                this.StressStrategyDetail();
            },
            // 获取host数据列表
            Installversion() {
                this.listLoading = true
                let self = this;
                const params = {
                    page_size: 100
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getInstallersion(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.versionlist = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            typestatus: function (i) {
                if (i === true) {
                    return 'danger'
                } else {
                    return 'primary'
                }

            },
            showReport() {
                this.$router.push({
                    path: '/stressReport',
                    query: {
                        stress_id: this.stressid,
                        strategy: self.activeName
                    }
                });
            },
            JmeterDel: function (row) {
                let self = this;
                this.$confirm('删除改jmeter?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {
                        id: row.id
                    };
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    };
                    delJmeter(header, params).then(_data => {
                        let {msg, code, data} = _data;
                        if (code === '0') {
                            self.$message({
                                message: '已删除',
                                center: true,
                                type: 'success'
                            })
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                        self.stresslistList()
                    });
                })
            },
            getuploadList() {
                const params = {
                    page_size: "999999",
                    type: "stress"
                }
                const headers = {
                    'Content-Type': 'application/json'
                }
                getupload(headers, params).then(_data => {
                    const {msg, code, data} = _data
                    if (code != '0') {
                        this.$message.error(msg)
                        return
                    }
                    // 请求正确时执行的代码
                    this.jmeterList = data.data
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
                        this.Host = JSON.parse(json)
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            // 获取性能数据列表
            StressDetaillist() {
                this.listLoading = true
                const self = this
                const params = {
                    stressid: self.stressid
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                StressDetail(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total
                        self.CaseForm = data.data[0]
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            // 运行压力测试
            stressRun: function (modelID) {
                this.$confirm('开始测试?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {
                        stressid: this.stressid,
                        type: this.activeName,
                        modelId: modelID
                    };
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    };
                    stressTool(header, params).then(_data => {
                        let {msg, code, data} = _data;
                        if (code === '0') {
                            self.$message({
                                message: '成功',
                                center: true,
                                type: 'success'
                            })
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                    });
                })
            },
            stressStop: function () {
                let self = this;
                this.$confirm('停止测试?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {
                        id: this.stressid
                    };
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    };
                    stressStop(header, params).then(_data => {
                        let {msg, code, data} = _data;
                        if (code === '0') {
                            self.$message({
                                message: '已停止',
                                center: true,
                                type: 'success'
                            })
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                        self.stresslistList()
                    });
                })
            },
            // 获取性能数据列表
            StressStrategyDetail() {
                this.listLoading = true
                const self = this
                const params = {
                    stressid: self.stressid,
                    strategy: self.activeName
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                StrategyDetail(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.progress = data.progress
                        this.CaseDetail = data.CaseDetail
                        self.JmeterData = data.JmeterData
                        console.log(this.JmeterData[0])
                        self.statistics = data.statistics.length ? data.statistics[0] : {}
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            //保存同步测试结果
            handleSave: function () {
                this.$confirm('同步测试结果?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {
                        stressid: this.stressid,
                        strategy: this.activeName
                    };
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    };
                    stresssave(header, params).then(_data => {
                        let {msg, code, data} = _data;
                        if (code === '0') {
                            this.listLoading = false;
                            self.$message({
                                message: '成功',
                                center: true,
                                type: 'success'
                            })
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                        self.stresslistList()
                    });
                })
            },
            // 删除
            handleDel: function (index, row) {
                this.$confirm('确认删除该记录吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true
                    // NProgress.start();
                    const self = this
                    const params = {ids: [row.id]}
                    const header = {
                        'Content-Type': 'application/json',
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    }

                    delduration(header, params).then(_data => {
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
                        self.StressDetaillist()
                    })
                })
            }
            ,
            // 改变状态
            handleChangeStatus: function (index, row) {
                let self = this;
                this.listLoading = true;
                let params = {id: row.id};
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                if (row.sendstatus) {
                    disable_duration(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        self.listLoading = false;
                        if (code === '0') {
                            self.$message({
                                message: '停止成功',
                                center: true,
                                type: 'success'
                            });
                            row.sendstatus = !row.sendstatus;
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                    });
                } else {
                    enable_duration(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        self.listLoading = false;
                        if (code === '0') {
                            self.$message({
                                message: '启用成功',
                                center: true,
                                type: 'success'
                            });
                            row.sendstatus = !row.sendstatus;
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                    });
                }
            }
            ,
            // 显示编辑界面
            handleEdit: function (index, row) {
                this.editFormVisible = true
                this.editForm = Object.assign({}, row)

            }
            ,
            // 显示新增界面
            handleAdd: function () {
                this.addFormVisible = true
                this.addForm = {
                    server: null,
                    port: 4242,
                    loop_time: '',
                    keyword: null,
                    dicom: null,
                    dds: null,
                    sendstatus: false,
                    status: false,
                    sleepcount: null,
                    sleeptime: 0,
                    sendcount: 0,
                    type: '匿名',
                    series: false,
                    end_time: null
                }
            }
            ,
            // 编辑
            editSubmit: function () {
                const self = this
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.editLoading = true
                            // NProgress.start();
                            const params = {
                                id: self.editForm.id,
                                dicom: this.editForm.senddata,
                                sendcount: this.editForm.sendcount,
                                end_time: this.editForm.end_time
                            }
                            const header = {
                                'Content-Type': 'application/json',
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            }
                            updateduration(header, params).then(_data => {
                                const {msg, code, data} = _data
                                self.editLoading = false
                                if (code === '0') {
                                    self.$message({
                                        message: '修改成功',
                                        center: true,
                                        type: 'success'
                                    })
                                    self.$refs['editForm'].resetFields()
                                    self.editFormVisible = false
                                    self.getDurationlist()
                                } else if (code === '999997') {
                                    self.$message.error({
                                        message: msg,
                                        center: true
                                    })
                                } else {
                                    self.$message.error({
                                        message: msg,
                                        center: true
                                    })
                                }
                            })
                        })
                    }
                })
            }
            ,
            // 新增
            addSubmit: function () {
                this.$refs.addForm.validate((valid) => {
                    if (valid) {
                        const self = this
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.addLoading = true
                            // NProgress.start();
                            const params = JSON.stringify({
                                port: self.addForm.port,
                                version: self.addForm.version,
                                loop_time: self.addForm.loop_time,
                                patientname: 'duration',
                                patientid: '',
                                dicom: this.addForm.senddata,
                                sendcount: this.addForm.sendcount,
                                end_time: this.addForm.end_time,
                                type: '持续化',
                                sendstatus: false,
                                status: false,
                                Host: this.addForm.Host,
                                project: this.project_id
                            })
                            const header = {
                                'Content-Type': 'application/json',
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            }
                            addduration(header, params).then(_data => {
                                const {msg, code, data} = _data
                                self.addLoading = false
                                if (code === '0') {
                                    self.$message({
                                        message: '添加成功',
                                        center: true,
                                        type: 'success'
                                    })
                                    self.$refs['addForm'].resetFields()
                                    self.addFormVisible = false
                                    self.getDurationlist()
                                } else if (code === '999997') {
                                    self.$message.error({
                                        message: msg,
                                        center: true
                                    })
                                } else {
                                    self.$message.error({
                                        message: msg,
                                        center: true
                                    })
                                    self.$refs['addForm'].resetFields()
                                    self.addFormVisible = false
                                    self.getDurationlist()
                                }
                            })
                        })
                    }
                })
            }
            ,
            selsChange: function (sels) {
                this.sels = sels
            }
            ,
            cancelEdit(row) {
                row.title = row.originalTitle
                row.edit = false
                this.$message({
                    message: 'The title has been restored to the original value',
                    type: 'warning'
                })
            }
            ,
            confirmEdit(row) {
                row.edit = false
                row.originalTitle = row.title
                this.$message({
                    message: 'The title has been edited',
                    type: 'success'
                })
            }
            ,
            // 批量删除
            batchRemove: function () {
                const ids = this.sels.map(item => item.id)
                console.log(ids)
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
                    delduration(header, params).then(_data => {
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
                        self.StressDetaillist()
                    })
                })
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
        width: 15px;
        height: 15px;
        margin-right: 3px;
        margin-bottom: 5px
    }

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
