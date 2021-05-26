<template>
    <section>
        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
            <el-form :inline="true" :model="filters" @submit.native.prevent>
                <el-form-item>
                    <el-select v-model="filters.type" placeholder="类型" @click.native="getfile()">
                                    <el-option v-for="(item,index) in filetype"
                                               :key="item.value"
                                               :label="item.value"
                                               :value="item.value"
                                    />
                                </el-select>
                </el-form-item>
                <el-form-item>
                    <el-select v-model="filters.content" placeholder="请选择病种名称" @click.native="getbaseList()">
                        <el-option v-for="(item,index) in baseData"
                                   :key="item.remarks"
                                   :label="item.remarks"
                                   :value="item.remarks"
                        />
                    </el-select>
                </el-form-item>
                <el-form-item label="服务器" prop="server">
                    <el-select v-model="filters.server" placeholder="请选择服务" @click.native="gethost()">
                        <el-option v-for="(item,index) in tags"
                                   :key="item.id"
                                   :label="item.name"
                                   :value="item.id"
                        />
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="getbaseList">查询</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleAdd">新增病种</el-button>
                </el-form-item>
<!--                <el-button type="warning" :disabled="this.sels.length===0" @click="batchSend">发送数据</el-button>-->
            </el-form>
        </el-col>

        <!--列表-->
        <el-table :data="baseData" highlight-current-row v-loading="listLoading" @selection-change="selsChange"
                  style="width: 100%;">
            <el-table-column type="selection" min-width="5%">
            </el-table-column>

            <el-table-column prop="select_type" label="ID" min-width="6%" sortable>
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.id }}</span>
                </template>
            </el-table-column>
            <el-table-column label="名称" min-width="16%" sortable>
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.remarks }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="content" label="路径" min-width="25%">
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.content }}</span>
                </template>
            </el-table-column>
            <el-table-column label="模型" min-width="16%" sortable>
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.predictor }}</span>
                </template>
            </el-table-column>
            <el-table-column label="类型" min-width="16%" sortable>
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.type }}</span>
                </template>
            </el-table-column>
            <el-table-column label="数量" min-width="16%" sortable>
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.other }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" min-width="9%">
                <template slot-scope="scope">
                    <img v-show="scope.row.status" style="width:18px;height:18px;margin-right:5px;margin-bottom:5px" src="../../../assets/img/qiyong.png"/>
                    <img v-show="!scope.row.status" style="width:18px;height:18px;margin-right:5px;margin-bottom:5px" src="../../../assets/img/fou.png"/>
                </template>
            </el-table-column>
            <el-table-column label="修改时间" min-width="16%" sortable>
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.updatetime  | dateformat('YYYY-MM-DD ')}}</span>
                </template>
            </el-table-column>
            <el-table-column label="操作" min-width="50px">
                <template slot-scope="scope">
                    <el-button type ="primary" size="small" @click="handleEdit(scope.$index, scope.row)">编辑病种</el-button>
                    <el-button type="primary" size="small" @click="handleSupplement(scope.$index, scope.row)">补充病人数据</el-button>
                    <el-button type="info" size="small" @click="handleChangeStatus(scope.$index, scope.row)">
                        {{scope.row.status===false?'启用':'禁用'}}
                    </el-button>
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

        <!--编辑界面-->
        <el-dialog title="编辑病种" :visible.sync="editFormVisible" :close-on-click-modal="false"
                   style="width: 75%; left: 12.5%">
            <el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
                <el-form-item label="文件路径">
                    <el-input v-model="editForm.content" :disabled="true"></el-input>
                </el-form-item>
                <el-row :gutter="24">
                    <el-col :span="12">
                        <el-form-item label="分类" prop='type'>
                            <el-select v-model="editForm.type" placeholder="请选择" auto-complete="off" :disabled="true">
                                <el-option v-for="item in options" :key="item.value" :label="item.label"
                                           :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="类型">
                            <el-input v-model="editForm.select_type" :disabled="true" auto-complete="off"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="模型" prop='predictor'>
                            <el-select v-model="editForm.predictor" placeholder="请选择" @click.native="getDict()">
                                <el-option v-for="(item,index) in model"
                                           :key="item.id"
                                           :label="item.value"
                                           :value="item.id"
                                />
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-form-item label="名称">
                    <el-input v-model="editForm.remarks"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="editFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
            </div>
        </el-dialog>

        <!--新增界面-->
        <el-dialog title="新增病种" :visible.sync="addFormVisible" :close-on-click-modal="false"
                   style="width: 75%; left: 12.5%">
            <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="病种名称" prop='remarks'>
                            <el-input v-model.trim="addForm.remarks" auto-complete="off" style="width: 215px;height:32px;"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="文件路径" prop='content'>
                            <el-input v-model.trim="addForm.content" auto-complete="off" style="width: 215px;height:32px;"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="数据类型" prop='type'>
                                <el-select v-model="addForm.type" placeholder="请选择" @click.native="getfile()">
                                    <el-option v-for="(item,index) in filetype"
                                               :key="item.value"
                                               :label="item.remarks"
                                               :value="item.value"
                                    />
                                </el-select>
                        </el-form-item>
                    </el-col>
                        <el-col :span="12">
                            <el-form-item label="模型类型" prop='predictor'>
                                <el-select v-model="addForm.predictor" placeholder="请选择" @click.native="getDict()">
                                    <el-option v-for="(item,index) in model"
                                               :key="item.id"
                                               :label="item.value"
                                               :value="item.id"
                                    />
                                </el-select>
                            </el-form-item>
                        </el-col>
                </el-row>
                <el-alert title="使用帮助" type="success">
                    <template slot='title'>
                        <div class="iconSize">使用帮助:</div>
                        <div class="iconSize">1、病种名称:测试部自定义病种名称，一个病种下可以有多个病人数据,此处是新增病种，如已有该病种，请在列表处直接添加病人数据</div>
                        <div class="iconSize">2、文件路径:该病种（N）个病人数据所在文件夹</div>
                        <div class="iconSize">3、数据类型:测试用途不同，需要不同的类型数据</div>
                        <div class="iconSize">4、模型类型:开发部定义，该病种使用哪种模型算法进行智能分析</div>
                        <div class="iconSize">5、上传数据:点击后，数据将自动上传测试服务器，下一步请到Dicom发送中选择发送到哪个被测服务器上</div>
                    </template>
                </el-alert>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="addFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="addSubmit" :loading="addLoading">上传数据</el-button>
            </div>
        </el-dialog>

        <!--补充病人数据界面-->
        <el-dialog title="补充病人数据" :visible.sync="supplementVisible" :close-on-click-modal="false"
                   style="width: 75%; left: 12.5%">
            <el-form :model="supplemenForm" label-width="80px" ref="supplementForm" enctype="multipart/form-data">
                <el-form-item label="文件路径">
                    <el-input v-model="supplemenForm.content" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item label="文件id">
                    <el-input v-model="supplemenForm.id" :disabled="true"></el-input>
                </el-form-item>

                <el-form-item label="名称" :disabled="true">
                     <el-upload
                      class="upload-demo"
                      ref="upload"
                      :limit="1"
                      action="FakeAction"
                      :on-preview="handlePreview"
                      :on-exceed="handleExceed"
                      :on-change="handleChange"
                      :file-list="fileList"
                      :show-file-list="showFileName"

                      :auto-upload="false">
                      <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
                      <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload()" :disabled=dataupshow>补充数据上传</el-button>
<!--                      <div slot="tip" class="el-upload__tip">只能上传zip文件</div>-->
                    </el-upload>
                </el-form-item>

                <el-alert title="使用帮助" type="success">
                    <template slot='title'>
                        <div class="iconSize">使用帮助:</div>
<!--                        <div class="iconSize">1.只能上传zip文件，且不超过500kb</div>-->
                        <div class="iconSize">将病人数据打包zip格式，选择文件，点击补充数据上传</div>
                    </template>
                </el-alert>
            </el-form>
<!--            <div slot="footer" class="dialog-footer">-->
<!--                <el-button @click.native="supplementVisible = false">取消</el-button>-->
<!--                <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>-->
<!--            </div>-->
        </el-dialog>


    </section>
</template>

<script>
    //import NProgress from 'nprogress'
    import {
        getbase, Delbasedata, Disablebase, Enablebase,
        UpdatebaseData, addbaseData, dicomcount, getHost, getdicomSend, getDictionary, addupload, addzipupload
    } from '../../../router/api';
    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                dataupshow:false,
                file: '',
                fileList: [],
                filetype:[],
                tags:[],
                model:[],
                filters: {
                    type: '',
                    remarks: '',
                    selecttype: 'dicom',
                    status: true
                },
                showFileName: false,
                baseData: [],
                total: 0,
                page: 1,
                page_size: 20,
                listLoading: false,
                sels: [],//列表选中列

                editFormVisible: false,//编辑界面是否显示
                editLoading: false,
                options: [{label: "dicom", value: "dicom"}],
                editFormRules: {
                    type: [
                        {required: true, message: '请选择类型', trigger: 'blur'}
                    ],
                    select_type: [
                        {required: true, message: '请输入版本号', trigger: 'change'},
                        {pattern: /^\d+\.\d+\.\d+$/, message: '请输入合法的版本号（x.x.x）'}
                    ],
                    description: [
                        {required: false, message: '请输入描述', trigger: 'blur'},
                        {max: 1024, message: '不能超过1024个字符', trigger: 'blur'}
                    ]
                },
                //编辑界面数据
                editForm: {
                    content: '',
                    select_type: '',
                    type: '',
                    description: ''
                },

                addFormVisible: false,//新增界面是否显示
                addLoading: false,
                addFormRules: {
                    remarks: [
                        { required: true, message: '请填写病种名称', trigger: 'blur' }
                    ],
                    content: [
                        { required: true, message: '请填写文件上传所在目录', trigger: 'blur' }
                    ],
                    type: [
                        { required: true, message: '请填写数据类型', trigger: 'change' }
                    ]
                },

                supplementVisible: false,//补充病人数据界面是否显示
                //补充病人数据界面数据
                supplemenForm: {
                    id:'',
                    content: '',
                    files: '',
                },
                //新增界面数据
                addForm: {
                    remarks:'',
                    content: '',
                    type:''
                    // select_type: 'dicom',
                    // type: 'endurance',
                    // description: ''
                }

            }
        },
        mounted() {
            this.gethost();
            this.getfile();
        },
        methods: {
            //展示server名
            gethost() {
                this.listLoading = true
                const self = this
                const params = {
                    page_size:100
                }
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
            // 获取字典模型
            getDict() {
                this.listLoading = true;
                let self = this;
                let params = {
                    type: 'model',
                    status: 1,
                };
                let headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))};
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
            getfile() {
                this.listLoading = true;
                let self = this;
                let params = {
                    type: 'file',
                    status: 1,
                };
                let headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))};
                getDictionary(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total
                        self.list = data.data
                        var json = JSON.stringify(self.list)
                        this.filetype = JSON.parse(json)
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            // 获取基本信息列表
            getbaseList() {
                this.listLoading = true;
                let self = this;
                let params = {
                    page: self.page,
                    page_size:self.page_size,
                    remarks: self.filters.remarks,
                    type: self.filters.type,
                    selecttype:"dicom",
                    status: 1,
                };
                let headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))};
                getbase(headers, params).then((res) => {
                    self.listLoading = false;
                    let {msg, code, data} = res;
                    if (code === '0') {
                        self.total = data.total;
                        self.baseData = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                })
            },
            //同步
            handlecount: function (index, row) {
                this.listLoading = true;
                //NProgress.start();
                let self = this;
                let params = {id: row.id};
                let header = {
                    "Content-Type": "application/json",
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                dicomcount(header, params).then(_data => {
                    let {msg, code, data} = _data;
                    if (code === '0') {
                        self.$message({
                            message: '同步成功',
                            center: true,
                            type: 'success'
                        })
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                    self.getbaseList()
                });
            },
            // 改变项目状态
            handleChangeStatus: function (index, row) {
                let self = this;
                this.listLoading = true;
                let params = {id: row.id};
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                if (row.status) {
                    Disablebase(headers, params).then(_data => {
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
                    Enablebase(headers, params).then(_data => {
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
                this.getbaseList()
            },
            //显示编辑界面
            handleEdit: function (index, row) {
                this.editFormVisible = true;
                this.editForm = Object.assign({}, row);
            },
            //显示补充病人数据界面
            handleSupplement: function (index, row) {
                this.showFileName = false//不显示列表
                this.fileList = []//清空列表数据
                this.supplementVisible = true;
                this.supplemenForm = Object.assign({}, row);
            },
            //显示新增界面
            handleAdd: function () {
                this.addFormVisible = true;
                this.addForm = {
                    select_type: 'dicom',
                    content: null,
                    status: true,
                    remarks: null,
                    other: null,
                    // type: 'endurance',
                    predictor: ''
                };
            },
            //编辑
            editSubmit: function () {
                let self = this;
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.editLoading = true;
                            //NProgress.start();
                            let params = {
                                id: self.editForm.id,
                                content: self.editForm.content,
                                type: self.editForm.type,
                                select_type: self.editForm.select_type,
                                remarks: self.editForm.remarks,
                                predictor: self.editForm.predictor
                            };
                            let header = {
                                "Content-Type": "application/json",
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            };
                            UpdatebaseData(header, params).then(_data => {
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
                                    self.getbaseList()
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
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.addLoading = true;
                            //NProgress.start();
                            let params = JSON.stringify({
                                content: this.addForm.content,
                                type: self.addForm.type,
                                select_type: self.addForm.select_type,
                                remarks: this.addForm.remarks,
                                other: self.addForm.other,
                                predictor: self.addForm.predictor,
                                status: true
                            });
                            let header = {
                                "Content-Type": "application/json",
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            };
                            addbaseData(header, params).then(_data => {
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
                                    self.getbaseList()
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
                                    self.getbaseList()
                                }
                            })
                        });
                    }
                });
            },
            selsChange: function (sels) {
                this.sels = sels;
            },
            batchSend: function () {
                const ids = this.sels.map(item => item.id)
                const self = this
                this.$confirm('确认生成选中记录吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true
                    // NProgress.start();
                    const self = this
                    const params = {
                        ids: ids,
                        server: this.filters.server
                    }
                    const header = {
                        'Content-Type': 'application/json',
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    }
                    getdicomSend(header, params).then(_data => {
                        const {msg, code, data} = _data
                        if (code === '0') {
                            self.$message({
                                message: '成功',
                                center: true,
                                type: 'success'
                            })
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true
                            })
                        }
                        self.getbaseList()
                    })
                })
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
                    Delbasedata(header, params).then(_data => {
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
                        self.getbaseList()
                    });
                })
            },

            handleChange(file, fileList) {
              if(file.name.indexOf(".zip") >= 0 ) {
                  this.showFileName = true
                    this.fileList = fileList;
              }else{
                  this.$message({
                      showClose: true,
                      message: ('上传文件格式不正确'),
                      type: 'warning'
                  });
                  this.showFileName = false
                  this.fileList = []
              }
            },
            //上传补充病人数据
            submitUpload() {
                this.dataupshow=true
                let params = new FormData();
                  this.fileList.forEach(item => {
                    params.append("files", item.raw);
                });
                params.append('type', this.supplemenForm.content)
                params.append('id', this.supplemenForm.id)

                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                addzipupload(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        // alert("ok")
                        // this.$message(data.filename,'上传成功');
                        this.$message({
                            showClose: true,
                          message: (data.filename+'上传成功'),
                          type: 'success'
                        });
                        this.dataupshow=false
                        this.supplementVisible = false;
                    } else {
                        this.dataupshow=false
                        this.$message({
                            showClose: true,
                            message: (msg),
                            type: 'error'
                        });
                    }
                })
            },
            handlePreview(file) {
              console.log(file);
            },
            handleExceed(files, fileList) {
              this.$message.warning(`当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
            },

        },

        mounted() {
            this.getbaseList();
        }
    }

</script>

<style>
     .iconSize{
        font-size: 14px;
        padding: 10px;
        font-weight: bold;

}

</style>