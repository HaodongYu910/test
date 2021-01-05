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
            <el-table-column prop="version" label="项目" min-width="12%" sortable>
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.projectname }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="version" label="版本" min-width="12%" sortable show-overflow-tooltip>
                <template slot-scope="scope">
                    <el-icon name="name"></el-icon>
                    <router-link v-if="scope.row.status" :to="{ version: '概况', params: {id: scope.row.id}}"
                                 style='text-decoration: none;color: #000000;'>
                        {{ scope.row.version }}
                    </router-link>
                    {{ !scope.row.status?scope.row.version:""}}
                </template>
            </el-table-column>
            <el-table-column prop="version" label="服务" min-width="12%" sortable>
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.loadserver }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="type" label="线程数" min-width="9%">
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.thread }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="type" label="规则" min-width="30%">
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.testdata }}</span>
                </template>
            </el-table-column>
            <el-table-column label="开始时间" min-width="16%" sortable>
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.start_date  | dateformat('YYYY-MM-DD HH:mm:SS')}}</span>
                </template>
            </el-table-column>
            <el-table-column label="结束时间" min-width="16%" sortable>
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.end_date  | dateformat('YYYY-MM-DD HH:mm:SS')}}</span>
                </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" min-width="9%">
                <template slot-scope="scope">
                    <img v-show="scope.row.status" style="width:18px;height:18px;margin-right:5px;margin-bottom:5px"
                         src="../../assets/img/qiyong.png"/>
                    <img v-show="!scope.row.status" style="width:18px;height:18px;margin-right:5px;margin-bottom:5px"
                         src="../../assets/img/fou.png"/>
                </template>
            </el-table-column>
            <el-table-column label="操作" min-width="30%">
                <template slot-scope="scope">
                    <el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)">查看</el-button>
                    <el-button type="info" size="small" @click="stressJz(scope.$index, scope.row)">基准</el-button>
                    <el-button type="primary" size="small" @click="stressRun(scope.$index, scope.row)">运行</el-button>
                    <el-button type="danger" size="small" @click="handleSave(scope.$index, scope.row)">报告</el-button>
                    <!--                    <el-button type="info" size="small" @click="handleChangeStatus(scope.$index, scope.row)">-->
                    <!--                        {{scope.row.status===false?'启用':'禁用'}}-->
                    <!--                    </el-button>-->
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

        <!--详细界面-->
        <el-dialog :visible.sync="editFormVisible" :close-on-click-modal="false"
                   style="width: 100%; left: 5.5%">
            <el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
                <el-divider>基本配置</el-divider>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="项目" prop="name">
                            <el-select v-model="editForm.projectname" placeholder="请选择">
                                <el-option key="晨曦" label="晨曦" value="晨曦"></el-option>
                                <el-option key="肺炎" label="肺炎" value="肺炎"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item label="版本" prop='version'>
                            <el-input v-model.trim="editForm.version" auto-complete="off"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="24">
                    <el-col :span="12">
                        <el-form-item label="服务器" prop='server'>
                            <el-select v-model="editForm.loadserver" placeholder="请选择服务器" @click.native="gethost()">
                                <el-option
                                        v-for="(item,index) in hosts"
                                        :key="item.host"
                                        :label="item.name"
                                        :value="item.host"
                                />
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item label="时间" prop='loop_time'>
                            <el-input v-model.trim="editForm.loop_time" auto-complete="off"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="24">
                    <el-col :span="12">
                        <el-form-item label="模型" prop='testdata'>
                            <el-select v-model="editForm.testdata" multiple placeholder="请选择" @click.native="getBase()">
                                <el-option v-for="(item,index) in model"
                                           :key="item.id"
                                           :label="item.value"
                                           :value="item.id"
                                />
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-divider>参数配置</el-divider>
                <el-row :gutter="24">
                    <el-col :span="8">
                        <el-form-item label="线程数" prop='thread'>
                            <el-input-number v-model="editForm.thread" @change="handleChange" :min="1" :max="5000"
                                             label="线程数"></el-input-number>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="循环次数" prop='loop_count'>
                            <el-input-number v-model="editForm.loop_count" @change="handleChange" :min="1" :max="5000"
                                             label="循环次数"></el-input-number>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="并发数" prop='synchroniz'>
                            <el-input-number v-model="editForm.synchroniz" @change="handleChange" :min="0" :max="5000"
                                             label="循环次数"></el-input-number>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="24">
                    <el-col :span="12">
                        <el-form-item label="ramp" prop='ramp'>
                            <el-input-number v-model="editForm.ramp" @change="handleChange" :min="0" :max="5000"
                                             label="循环次数"></el-input-number>
                        </el-form-item>
                    </el-col>
                    <el-col :span="10">
                        <el-form-item label="dicom" prop="switch">
                            <el-switch v-model="editForm.switch" active-color="#13ce66"
                                       inactive-color="#ff4949"></el-switch>
                        </el-form-item>
                    </el-col>
                </el-row>
                <i
                        class="el-icon-close"
                        @click="deleteClick(item)"
                        style=" position: absolute;top: -8px; left: 60px; cursor: pointer;"
                ></i>
                <el-row>
                    <el-divider>文件上传</el-divider>
                    <el-upload
                            class="upload-demo"
                            drag
                            action="/api/stress/upload"
                            multiple>
                        <i class="el-icon-upload"></i>
                        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                        <div class="el-upload__tip" slot="tip">只能上传jmx/.py文件</div>
                    </el-upload>
                </el-row>
                <el-divider>-</el-divider>
                <el-row>
                    <el-form-item label="基准测试" prop="switch">
                        <el-switch v-model="editForm.type" active-color="#13ce66"
                                   inactive-color="#ff4949"></el-switch>
                    </el-form-item>
                </el-row>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="editFormVisible = false">关闭</el-button>
                <el-button type="primary" @click.native="run" :loading="editLoading">运行</el-button>
                <el-button type="primary" @click.native="editSubmit" :loading="editLoading">修改</el-button>
            </div>
        </el-dialog>

        <!--新增界面-->
        <el-dialog title="新增测试" :visible.sync="addFormVisible" :close-on-click-modal="false"
                   style="width: 75%; left: 12.5%">
            <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
                <el-divider>基本配置</el-divider>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="项目" prop="name">
                            <el-select v-model="addForm.projectname" placeholder="请选择">
                                <el-option key="晨曦" label="晨曦" value="晨曦"></el-option>
                                <el-option key="肺炎" label="肺炎" value="肺炎"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="版本" prop='version'>
                            <el-input v-model.trim="addForm.version" auto-complete="off"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="24">
                    <el-col :span="12">
                        <el-form-item label="服务器" prop='server'>
                            <el-select v-model="addForm.loadserver" placeholder="请选择服务器" @click.native="gethost()">
                                <el-option
                                        v-for="(item,index) in hosts"
                                        :key="item.host"
                                        :label="item.name"
                                        :value="item.host"
                                />
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="时间" prop='loop_time' auto-complete="off">
                            <el-input v-model.trim="addForm.loop_time" auto-complete="off"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="24">
                    <el-col :span="12">
                        <el-form-item label="模型" prop='testdata'>
                            <el-select v-model="addForm.testdata" multiple placeholder="请选择" @click.native="getBase()">
                                <el-option v-for="(item,index) in model"
                                           :key="item.id"
                                           :label="item.value"
                                           :value="item.id"
                                />
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-divider>参数配置</el-divider>
                <el-row :gutter="24">
                    <el-col :span="8">
                        <el-form-item label="线程数" prop='thread'>
                            <el-input-number v-model="addForm.thread" @change="handleChange" :min="1" :max="5000"
                                             label="线程数"></el-input-number>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="循环次数" prop='loop_count'>
                            <el-input-number v-model="addForm.loop_count" @change="handleChange" :min="1" :max="5000"
                                             label="循环次数"></el-input-number>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="并发数" prop='synchroniz'>
                            <el-input-number v-model="addForm.synchroniz" @change="handleChange" :min="0" :max="5000"
                                             label="循环次数"></el-input-number>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="24">
                    <el-col :span="12">
                        <el-form-item label="ramp" prop='ramp'>
                            <el-input-number v-model="addForm.ramp" @change="handleChange" :min="0" :max="5000"
                                             label="循环次数"></el-input-number>
                        </el-form-item>
                    </el-col>
                    <el-col :span="10">
                        <el-form-item label="dicom" prop="switch">
                            <el-switch v-model="addForm.switch" active-color="#13ce66"
                                       inactive-color="#ff4949"></el-switch>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-divider>文件上传</el-divider>
                    <el-upload
                            class="upload-demo"
                            action="#"
                            :file-list="fileList"
                            :on-change="changeData"
                            :http-request="handleRequest"
                            :before-upload="beforeUpload">
                        <el-button class="btn upload-btn">上传附件</el-button>
                        <div slot="tip" class="el-upload__tip">上传文件大小不超过50M</div>
                    </el-upload>
                    <el-progress :stroke-width="16" :percentage="progressPercent"></el-progress>
<!--                    <el-upload-->
<!--                            class="upload-demo"-->
<!--                            drag-->
<!--                            action="/api/stress/upload"-->
<!--                            multiple v-model="addForm.upload">-->
<!--                        <i class="el-icon-upload"></i>-->
<!--                        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>-->
<!--                        <div class="el-upload__tip" slot="tip">只能上传jmx/.py文件</div>-->

<!--                        &lt;!&ndash;                            <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">&ndash;&gt;-->
<!--                        &lt;!&ndash;                                上传到服务器&ndash;&gt;-->
<!--                        &lt;!&ndash;                            </el-button>&ndash;&gt;-->
<!--                    </el-upload>-->
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
        stresslist, delStress, disableStress, enableStress,
        updateStress, addStress, stresssave, getHost, getDictionary, stressTool,getupload
    } from '../../router/api';
    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                filters: {
                    name: ''
                },
                project: [],
                total: 0,
                page: 1,
                listLoading: false,
                sels: [],//列表选中列

                editFormVisible: false,//编辑界面是否显示
                editLoading: false,
                options: [{label: "Web", value: "Web"}, {label: "App", value: "App"}],
                editFormRules: {
                    projectname: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ],
                    testdata: [
                        {required: true, message: '请选择模型', trigger: 'blur'}
                    ],
                    version: [
                        {required: true, message: '请输入版本号', trigger: 'change'},
                        {pattern: /^\d+\.\d+\.\d+$/, message: '请输入合法的版本号（x.x.x）'}
                    ]
                },
                //编辑界面数据
                editForm: {
                    projectname: '',
                    version: '',
                    thread: 1,
                    type: false
                },

                addFormVisible: false,//新增界面是否显示
                addLoading: false,
                addFormRules: {
                    projectname: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ],
                    testdata: [
                        {required: true, message: '请选择模型类型', trigger: 'blur'}
                    ],
                    version: [
                        {required: true, message: '请输入版本号', trigger: 'change'},
                        {pattern: /^\d+\.\d+\.\d+$/, message: '请输入合法的版本号（x.x.x）'}
                    ]
                },
                //新增界面数据
                addForm: {
                    projectname: '晨曦',
                    loadserver: '192.168.1.208',
                    version: '',
                    type: '',
                    jmeterstatus: false
                }
            }
        },
        methods: {
            //展示风险项
            //上传前对文件大小进行校验
            beforeUpload(file) {
                const isLt2M = file.size / 1024 / 1024 < 50;
                if (!isLt2M) {
                    this.$message.error('上传文件大小大小不能超过 50MB!');
                    return isLt2M;
                }
            },
            changeData(file, fileList) {
                // 数据小于0.1M的时候按KB显示
                const size = file.size / 1024 / 1024 > 0.1 ? `(${(file.size / 1024 / 1024).toFixed(1)}M)` : `(${(file.size / 1024).toFixed(1)}KB)`
                file.name.indexOf('M') > -1 || file.name.indexOf('KB') > -1 ? file.name : file.name += size
            },
            handleRequest(data) {
                let params = new FormData()
                params.append('file', data.file)
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getupload(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.data = data.data
                        var json = JSON.stringify(this.data)
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            showdetail(index, row) {
                this.$router.push({
                    path: '/stressdetail',
                    query: {
                        id: row.id,
                        name: row.name
                    }
                });
            },
            // 获取host数据列表
            gethost() {
                this.listLoading = true
                let self = this;
                const params = {}
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
            // 获取getBase列表
            getBase() {
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
            stressJz: function (index, row) {
                this.$confirm('确认执行测试?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {
                        id: row.id,
                        type: true
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
                this.$confirm('确认执行测试?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {
                        id: row.id,
                        type: false
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
                    type: ""
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
            //保存
            handleSave: function (index, row) {
                this.$confirm('确认测试完成了吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {id: row.id};
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    };
                    stresssave(header, params).then(_data => {
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
            //删除
            handleDel: function (index, row) {
                this.$confirm('确认删除该记录吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {ids: [row.id,]};
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
                let params = {project_id: row.id};
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
                    projectname: "晨曦",
                    loadserver: '192.168.1.208',
                    thread: 1,
                    synchroniz: 0,
                    ramp: 0,
                    loop_count: 1
                };
            },
            //run 性能测试
            run: function () {
                let self = this;
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认执行？', '提示', {}).then(() => {
                            self.editLoading = true;
                            //NProgress.start();
                            let params = {
                                id: self.editForm.id,
                                type: self.editForm.type
                            };
                            let header = {
                                "Content-Type": "application/json",
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            };
                            stressTool(header, params).then(_data => {
                                let {msg, code, data} = _data;
                                self.editLoading = false;
                                if (code === '0') {
                                    self.$message({
                                        message: '已执行',
                                        center: true,
                                        type: 'success'
                                    });
                                    self.$refs['editForm'].resetFields();
                                    self.editFormVisible = false;
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
                                    })
                                }
                            });
                        });
                    }
                });
            },
            //编辑修改
            editSubmit: function () {
                let self = this;
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认保存吗？', '提示', {}).then(() => {
                            self.editLoading = true;
                            //NProgress.start();
                            let params = {
                                id: self.editForm.id,
                                projectname: self.editForm.projectname,
                                loadserver: self.editForm.loadserver,
                                version: self.editForm.version,
                                testdata: self.editForm.testdata,
                                thread: this.editForm.thread,
                                synchroniz: this.editForm.synchroniz,
                                ramp: this.editForm.ramp,
                                loop_count: this.editForm.loop_count,
                                loop_time: this.editForm.loop_time,
                                status: true,
                                jmeterstatus: false,
                            };
                            let header = {
                                "Content-Type": "application/json",
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            };
                            updateStress(header, params).then(_data => {
                                let {msg, code, data} = _data;
                                self.editLoading = false;
                                if (code === '0') {
                                    self.$message({
                                        message: '修改成功',
                                        center: true,
                                        type: 'success'
                                    });
                                    self.$refs['editForm'].resetFields();
                                    self.editFormVisible = false;
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
                                    })
                                }
                            });
                        });
                    }
                });
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
                                projectname: self.addForm.projectname,
                                loadserver: self.addForm.loadserver,
                                version: self.addForm.version,
                                testdata: self.addForm.testdata,
                                thread: this.addForm.thread,
                                synchroniz: this.addForm.synchroniz,
                                ramp: this.addForm.ramp,
                                loop_count: this.addForm.loop_count,
                                loop_time: this.addForm.loop_time,
                                jmeterstatus: false,
                                status: true,
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
                let ids = this.sels.map(item => item.id);
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