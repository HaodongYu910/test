<template>
    <section>
        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
            <el-form :inline="true" :model="filters" @submit.native.prevent>
                <el-form-item>
                    <el-input v-model="filters.name" placeholder="名称" @keyup.enter.native="stresslistList"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="stresslistList">查询</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleAdd">创建测试</el-button>
                </el-form-item>
            </el-form>

        </el-col>

        <!--列表-->
        <el-table :data="project" highlight-current-row v-loading="listLoading" @selection-change="selsChange"
                  style="width: 100%;">
            <el-table-column type="selection" min-width="5%">
            </el-table-column>
            <el-table-column prop="version" label="版本-名称" min-width="15%"  sortable>
                    <template slot-scope="scope">
                        <router-link v-if="scope.row.version" :to="{ name: 'stressDetail', query: {stressid: scope.row.stressid}}"
                                     style='text-decoration: none;color: #0000ff;'>
                            <span style="margin-left: 10px">{{ scope.row.version }}-{{ scope.row.name }}</span>
                        </router-link>
                    </template>
                </el-table-column>
            <el-table-column prop="version" label="服务" min-width="12%">
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.loadserver }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="type" label="线程数" min-width="9%">
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.thread }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="type" label="规则" min-width="20%" show-overflow-tooltip>
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.testdata }}</span>
                </template>
            </el-table-column>
            <el-table-column label="状态" min-width="12%">
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.teststatus }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="status" label="" min-width="8%" show-overflow-tooltip>
                <template slot-scope="scope">
                    <img v-show="scope.row.status" style="width:18px;height:18px;margin-right:5px;margin-bottom:5px"
                         src="../../assets/img/qiyong.png"/>
                    <img v-show="!scope.row.status" style="width:18px;height:18px;margin-right:5px;margin-bottom:5px"
                         src="../../assets/img/fou.png"/>
                </template>
            </el-table-column>
            <el-table-column label="操作" min-width="25%">
                <template slot-scope="scope">
                    <el-row>
                        <el-button type="info" size="small"
                                   @click="checkExpress(scope.row.start_date,scope.row.end_date, scope.row.loadserver)">
                            监控
                        </el-button>
                        <el-button type="warning" size="small" @click="showReport(scope.$index, scope.row)">报告
                        </el-button>
                        <el-button :type="typeStatus(scope.row.status)" size="small"
                                       @click="handleChangeStatus(scope.$index, scope.row)">
                                {{scope.row.status===false?'启用':'停用'}}
                            </el-button>
                    </el-row>
                </template>
            </el-table-column>
        </el-table>

        <!--工具条-->
        <el-col :span="24" class="toolbar">
            <el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button>
            <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20"
                           :page-count="total" style="float:right;">
            </el-pagination>
        </el-col>


        <!--新增界面-->
        <el-dialog title="新增测试" :visible.sync="addFormVisible" :close-on-click-modal="false"

                   style="width: 120%; right: 0.5%">
            <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
                <el-row :gutter="18">
                    <el-col :span="6">
                        <el-form-item label="版本&名称" prop="name">
                            <el-select v-model="addForm.version" placeholder="请选择"
                                                   @click.native="getversion()">
                                            <el-option
                                                    v-for="(item,index) in VersionInfo"
                                                    :key="item.id"
                                                    :label="item.version"
                                                    :value="item.id"
                                            />
                                        </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="3">
                        <el-input v-model.trim="addForm.name" auto-complete="off"></el-input>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item label="Jmeter" prop='server'>
                            <el-select @click.native="getuploadList()" placeholder="请选择"
                                               v-model="addForm.uploadID">
                                        <el-option
                                                :key="item.id"
                                                :label="item.filename"
                                                :value="item.id"
                                                v-for="(item,index) in jmeterList"
                                        />
                                    </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="24">
                    <el-col :span="8">
                        <el-form-item label="服务器" prop='server'>
                            <el-select v-model="addForm.Host" placeholder="请选择服务器" @click.native="gethost()">
                                <el-option
                                        v-for="(item,index) in hosts"
                                        :key="item.id"
                                        :label="item.name"
                                        :value="item.id"
                                />
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="模型" prop='testdata'>
                            <el-select v-model="addForm.testdata" multiple placeholder="请选择" @click.native="Dictionary()">
                                <el-option v-for="(item,index) in model"
                                           :key="item.id"
                                           :label="item.value"
                                           :value="item.id"
                                />
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="24">
                    <el-col :span="8">
                        <el-card>
                            <el-divider>基准-配置</el-divider>

                            <el-form-item label="循环次数" prop='benchmark'>
                                <el-input-number v-model="addForm.benchmark" @change="handleChange" :min="1" :max="5000"
                                                 label="基准循环次数"></el-input-number>
                            </el-form-item>

                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card>
                            <el-divider>单一-配置</el-divider>

                            <el-form-item label="任务数量" prop='single'>
                                <el-input-number v-model="addForm.single" @change="handleChange" :min="1" :max="2000"
                                                 label="单一循环"></el-input-number>
                                笔
                            </el-form-item>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card>
                            <el-divider>混合-配置</el-divider>
                            <!--                            <el-form-item label="发送数量" prop='loop_count'>-->
                            <!--                                <el-input-number v-model="addForm.loop_count" @change="handleChange" :min="1"-->
                            <!--                                                 :max="5000"-->
                            <!--                                                 label="发送数量"></el-input-number>-->
                            <!--                            </el-form-item>-->
                            <el-form-item label="持续时间" prop='thread'>
                                <el-input-number v-model="addForm.duration" @change="handleChange" :min="1" :max="200"
                                                 label="持续时间"></el-input-number>
                                时
                            </el-form-item>
                        </el-card>
                    </el-col>
                </el-row>
                <el-row :gutter="24">
                    <el-col :span="16">
                        <el-card>
                            <el-divider>Jmeter-配置</el-divider>
                            <el-row :gutter="24">
                                <el-col :span="12">
                                    <el-form-item label="线程数" prop='thread'>
                                        <el-input-number v-model="addForm.thread" @change="handleChange" :min="1"
                                                         :max="100"
                                                         label="线程数"></el-input-number>
                                    </el-form-item>
                                </el-col>
                                <el-col :span="12">
                                    <el-form-item label="Ramp-Up" prop='ramp'>
                                        <el-input-number v-model="addForm.ramp" @change="handleChange" :min="0"
                                                         :max="5000"
                                                         label="Ramp-Up"></el-input-number>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="12">
                                    <el-form-item label="并发数" prop='synchroniz'>
                                        <el-input-number v-model="addForm.synchroniz" @change="handleChange" :min="0"
                                                         :max="100"
                                                         label="并发数"></el-input-number>
                                    </el-form-item>
                                </el-col>

                                <el-col :span="12">
                                    <el-form-item label="持续时间" prop='single'>
                                        <el-input-number v-model="addForm.loop_time" @change="handleChange" :min="0"
                                                         :max="1000000"
                                                         label="持续时间"></el-input-number>
                                        秒
                                    </el-form-item>

                                </el-col>
                            </el-row>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-divider>Jmeter-文件上传</el-divider>
                        <el-upload
                                class="upload-demo"
                                action="#"
                                :file-list="fileList"
                                :on-change="changeData"
                                multiple
                                :http-request="handleRequest"
                                :before-upload="beforeUpload"
                                :on-remove="handleRemove"
                                :before-remove="beforeRemove">

                            <el-button class="btn upload-btn">上传附件</el-button>
                            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                            <div slot="tip" class="el-upload__tip">只能上传jmx/.py文件</div>
                        </el-upload>
                        <el-progress :stroke-width="16" :percentage="100"></el-progress>

                    </el-col>
                </el-row>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="addFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="addSubmit" :loading="addLoading">保存</el-button>
            </div>
        </el-dialog>

    </section>
</template>

<script>
    //import NProgress from 'nprogress'
    import {
        stresslist, delStress, disableStress, enableStress,getVersionInfo,
         addStress, getHost, getDictionary, stressTool, addupload, delupload, getupload
    } from '../../router/api';
    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                project_id:localStorage.getItem("project_id"),
                filters: {
                    name: ''
                },
                jmeterList:{},
                fileList: {},
                filedict: {},
                VersionInfo: {},
                total: 0,
                page: 1,
                project:{},
                hosts:{},
                model:{},
                progressPercent:100,
                listLoading: false,
                sels: [],//列表选中列
                editFormVisible: false,//编辑界面是否显示
                editLoading: false,
                options: [{label: "Web", value: "Web"}, {label: "App", value: "App"}],
                editFormRules: {
                    name: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ],
                    version: [
                        {required: true, message: '请输入版本号', trigger: 'change'},
                        // {pattern: /^\d+\.\d+\.\d+$/, message: '请输入合法的版本号（x.x.x）'}
                    ]
                },
                //编辑界面数据
                editForm: {
                    name: '',
                    version: '',
                    thread: 1,
                    type: false
                },

                addFormVisible: false,//新增界面是否显示
                addLoading: false,
                addFormRules: {
                    name: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ],
                    testdata: [
                        {required: true, message: '请选择模型类型', trigger: 'blur'}
                    ],
                    version: [
                        {required: true, message: '请输入版本号', trigger: 'change'},
                        // {pattern: /^\d+\.\d+\.\d+$/, message: '请输入合法的版本号（x.x.x）'}
                    ]
                },
                //新增界面数据
                addForm: {
                    name: '晨曦',
                    version: '',
                    type: '',
                    jmeterstatus: false,
                    uploadID:""
                }
            }
        },
        methods: {
            // 按钮状态判断
            typeStatus: function (i) {
                if (i === true) {
                    return 'danger'
                } else {
                    return 'primary'
                }

            },
            showReport(index, row) {
                this.$router.push({
                    path: '/stressReport',
                    query: {
                        stress_id: row.stressid,
                        name: row.name
                    }
                });
            },
            //展示监控
            checkExpress: function (start_date, end_date, loadserver) {
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
                const url = "http://10.10.10.2:8084/d/MTWM-LW7z/qa-jian-kong-zhan-shi-kan-ban?from="+
                            startstamp + "&to=" + endstamp + "&var-interval=$__auto_interval_interval&var-env=&var-name=&var-node="
                            +loadserver +" &var-maxmount=&var-node_port=9100&var-cadvisor_port=8080&gpu_port=9445"

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
            //上传前对文件大小进行校验
            beforeUpload(file) {
                const isLt2M = file.size / 1024 / 1024 < 100;
                if (!isLt2M) {
                    this.$message.error('上传文件大小大小不能超过 100MB!');
                    return isLt2M;
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
            handleRemove(file, fileList) {
                console.log(file)
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
                    for (var i in this.jmeterList) {
                        if (i["filename"] === this.detailForm.filename) {
                            this.jmeterData = i
                        }
                    }
                })
            },
            showdetail(index, row) {
                this.$router.push({
                    path: '/stressdetail',
                    query: {
                        stressid: row.stressid,
                        name: row.name
                    }
                });
            },
            // 获取版本列表
            getversion() {
                this.listLoading = true
                let self = this;
                const params = {
                    page_size: 999,
                    project_id:this.project_id
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getVersionInfo(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.VersionInfo = data.data
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
                    page_size: 100,
                    project_id:this.project_id
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getHost(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.total = data.total
                        this.list = data.data
                        var json = JSON.stringify(this.list)
                        this.hosts = JSON.parse(json)
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            // 获取getDictionary列表
            Dictionary() {
                this.listLoading = true
                const self = this
                const params = {
                    status: 1,
                    type: 'model'
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getDictionary(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total
                        self.list = data.data
                        var json = JSON.stringify(self.list)
                        this.model = JSON.parse(json)
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            stressTest: function (index,row) {
                let self = this;
                this.$confirm('执行全部测试?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {
                        ids: row.id,
                        type: "type"
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
                        self.stresslistList()
                    });
                })
            },
            // 运行压力测试
            stressRun: function (index, row) {
                this.$confirm('确认执行混合场景测试?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {
                        stressid: row.stressid,
                        type: "test"
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
                        self.stresslistList()
                    });
                })
            },
            // 获取项目列表
            stresslistList() {
                this.listLoading = true;
                let self = this;
                let params = {
                    page: self.page,
                    name: self.filters.name,
                    type: "",
                    project_id:this.project_id
                };
                let headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))};
                stresslist(headers, params).then((res) => {
                    self.listLoading = false;
                    let {msg, code, data} = res;
                    if (code === '0') {
                        self.total = data.total;
                        self.project = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                })
            },
            //删除
            handleDel: function (index, row) {
                this.$confirm('确认删除该记录吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {ids: [row.stressid,]};
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    };
                    delProject(header, params).then(_data => {
                        let {msg, code, data} = _data;
                        if (code === '0') {
                            self.$message({
                                message: '删除成功',
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
            handleChange(value) {
                console.log(value);
            },
            // 改变项目状态
            handleChangeStatus: function (index, row) {
                let self = this;
                this.listLoading = true;
                let params = {
                    stressid: row.stressid,
                    type: "test"
                };
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                if (row.status) {
                    disableStress(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        self.listLoading = false;
                        if (code === '0') {
                            self.$message({
                                message: '禁用成功',
                                center: true,
                                type: 'success'
                            });
                            row.status = !row.status;
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                    });
                } else {
                    enableStress(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        self.listLoading = false;
                        if (code === '0') {
                            self.$message({
                                message: '启用成功',
                                center: true,
                                type: 'success'
                            });
                            row.status = !row.status;
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                    });
                }
            },
            handleCurrentChange(val) {
                this.page = val;
                this.stresslistList()
            },
            // 运行详情页面
            handleLook: function (index, row) {
                this.$router.push({
                    path: '/stressDetail',
                    query: {
                        id: row.id
                    }
                });
            },
            //显示编辑界面
            handleEdit: function (index, row) {
                this.editFormVisible = true;
                this.editForm = Object.assign({}, row);
            },
            //显示新增界面
            handleAdd: function () {
                this.addFormVisible = true;
                this.addForm = {
                    version: null,
                    name: "",
                    thread: 1,
                    synchroniz: 1,
                    benchmark: 5,
                    single: 1,
                    ramp: 0,
                    loop_count: 1,
                    duration: 1,
                    loop_time: 3600,
                    uploadID:""
                };
            },
            //新增
            addSubmit: function () {
                this.$refs.addForm.validate((valid) => {
                    if (valid) {
                        let self = this;
                        this.$confirm('确认保存吗？', '提示', {}).then(() => {
                            self.addLoading = true;
                            //NProgress.start();
                            let params = JSON.stringify({
                                name: self.addForm.name,
                                version: self.addForm.version,
                                testdata: self.addForm.testdata,
                                thread: this.addForm.thread,
                                synchroniz: this.addForm.synchroniz,
                                ramp: this.addForm.ramp,
                                loop_count: this.addForm.loop_count,
                                loop_time: this.addForm.loop_time,
                                benchmark: this.addForm.benchmark,
                                single: this.addForm.single,
                                duration: this.addForm.duration,
                                jmeterstatus: false,
                                filedict: this.filedict,
                                Host: this.addForm.Host,
                                project:this.project_id,
                                uploadID: this.addForm.uploadID,
                                status: false,
                            });
                            let header = {
                                "Content-Type": "application/json",
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            };
                            addStress(header, params).then(_data => {
                                let {msg, code, data} = _data;
                                self.addLoading = false;
                                if (code === '0') {
                                    self.$message({
                                        message: '添加成功',
                                        center: true,
                                        type: 'success'
                                    });
                                    self.$refs['addForm'].resetFields();
                                    self.addFormVisible = false;
                                    self.stresslistList()
                                } else if (code === '999997') {
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    })
                                } else {
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    });
                                    self.$refs['addForm'].resetFields();
                                    self.addFormVisible = false;
                                    self.stresslistList()
                                }
                            })
                        });
                    }
                });
            },
            selsChange: function (sels) {
                this.sels = sels;
            },
            //批量删除
            batchRemove: function () {
                let ids = this.sels.map(item => item.stressid);
                let self = this;
                this.$confirm('确认删除选中记录吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {ids: ids};
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    };
                    delStress(header, params).then(_data => {
                        let {msg, code, data} = _data;
                        if (code === '0') {
                            self.$message({
                                message: '删除成功',
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
            }
        },
        mounted() {
            this.stresslistList();
        }
    }

</script>

<style>

</style>