<template>
    <section>
        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
            <el-form :inline="true" :model="filters" @submit.native.prevent>
                <el-form-item>
                    <el-cascader :options="groupOptions" :props="{ checkStrictly: true }" v-model="filters.type" clearable @click.native="getgroupbase()"></el-cascader>
                </el-form-item>
                <el-form-item>
                    <el-input v-model="filters.name" placeholder="名称"
                                  @keyup.enter.native="getGroupList"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="getGroupList">查询</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleAdd">新增</el-button>
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
            <el-table-column prop="name" label="名称" min-width="16%" show-overflow-tooltip>
                <template slot-scope="scope">
                    <el-icon name="name"></el-icon>
                    <router-link v-if=true :to="{ name: 'Dicom数据', params: {type: [scope.row.type, scope.row.id]}}"
                                 style='text-decoration: none;color: #0000ff;'>
                        {{ scope.row.name }}
                    </router-link>
                </template>
            </el-table-column>
            <el-table-column prop="route" label="路径" min-width="25%">
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.route }}</span>
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
                    <span style="margin-left: 10px">{{ scope.row.amount }}</span>
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
                    <el-button type ="primary" size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                    <el-button type="primary" size="small" :style="{ display: displaystatus(scope.row.group) }"  @click="handleSupplement(scope.$index, scope.row)">补充病人数据</el-button>
                    <el-button type="primary" size="small" :style="{ display: displaystatus(scope.row.group) }" @click="ViewResults(scope.$index, scope.row)">查看结果</el-button>
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
                <el-row :gutter="24">
                    <el-col :span="12">
                        <el-form-item label="名称">
                            <el-input v-model="editForm.name"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                         <el-form-item label="备注">
                            <el-input v-model="editForm.remarks"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="模型类型" prop='predictor'>
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

                <div v-if="Virtual">
                    <el-divider>选择组数据</el-divider>
                    <el-row>
                        <div style="text-align: center">
                            <el-transfer
                                    class="el-transfer-panel__list.is-filterable"
                                    style="text-align: left; display: inline-block"
                                    v-model="groupData"
                                    filterable
                                    :left-default-checked="[2, 3]"
                                    :right-default-checked="[1]"
                                    :titles="['全部数据', '虚拟组数据']"
                                    :button-texts="['到左边', '到右边']"
                                    :format="{
                                noChecked: '${total}',
                                hasChecked: '${checked}/${total}'
                              }"
                                    @change="ChangeHandle"
                                    :data="infoData">
                                <span slot-scope="{ option }">{{ option.key }} - {{ option.label }}</span>
<!--                                <el-button class="transfer-footer" slot="left-footer" size="small">操作</el-button>-->
<!--                                <el-button class="transfer-footer" slot="right-footer" size="small">操作</el-button>-->
                            </el-transfer>
                        </div>
                    </el-row>
                </div>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="editFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="editSubmit" :loading="editLoading">保存</el-button>
            </div>
        </el-dialog>

        <!--新增界面-->
        <el-dialog title="新增" :visible.sync="addFormVisible" :close-on-click-modal="false"
                   style="width: 75%; left: 12.5%">
            <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="病种名称" prop='name'>
                            <el-input v-model.trim="addForm.name" auto-complete="off" style="width: 215px;height:32px;"></el-input>
                        </el-form-item>
                    </el-col>
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
                </el-row>
                <el-row>
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
                        <el-col :span="12">
                             <el-form-item label="虚拟组" prop='predictor'>
                            <el-switch
                              v-model="Virtual"
                              active-color="#13ce66"
                              inactive-color="#ff4949">
                            </el-switch>
                                 </el-form-item>
                        </el-col>
                </el-row>
                <div v-if="Virtual">
                    <el-divider>选择组数据</el-divider>
                    <el-row>
                        <div style="text-align: center">
                            <el-transfer
                                    class="el-transfer-panel__list.is-filterable"
                                    style="text-align: left; display: inline-block"
                                    v-model="groupData"
                                    filterable
                                    :left-default-checked="[2, 3]"
                                    :right-default-checked="[1]"
                                    :titles="['全部数据', '虚拟组数据']"
                                    :button-texts="['到左边', '到右边']"
                                    :format="{
                                noChecked: '${total}',
                                hasChecked: '${checked}/${total}'
                              }"
                                    @change="ChangeHandle"
                                    :data="infoData">
                                <span slot-scope="{ option }">{{ option.key }} - {{ option.label }}</span>
<!--                                <el-button class="transfer-footer" slot="left-footer" size="small">操作</el-button>-->
<!--                                <el-button class="transfer-footer" slot="right-footer" size="small">操作</el-button>-->
                            </el-transfer>
                        </div>
                    </el-row>
                </div>
                <el-alert title="使用帮助" type="success">
                    <template slot='title'>
                        <div class="iconSize">使用帮助:</div>
                        <div class="iconSize">1、病种名称:测试部自定义病种名称，一个病种下可以有多个病人数据,此处是新增病种</div>
                        <div class="iconSize">2、数据类型:测试用途不同，需要不同的类型数据</div>
                        <div class="iconSize">3、模型类型:开发部定义，该病种使用哪种模型算法进行智能分析</div>
                        <div class="iconSize">4、提交，下一步请添加病人数据</div>
                    </template>
                </el-alert>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="addFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
            </div>
        </el-dialog>

        <!--补充病人数据界面-->
        <el-dialog title="补充病人数据" :visible.sync="supplementVisible" :close-on-click-modal="false"
                   style="width: 75%; left: 12.5%">
            <el-form :model="supplemenForm" label-width="80px" ref="supplementForm" enctype="multipart/form-data">
                <el-form-item label="文件路径">
                    <el-input v-model="supplemenForm.route" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item label="文件id">
                    <el-input v-model="supplemenForm.id" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item label="定义名称">
                    <el-input v-model="supplemenForm.custom"></el-input>
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
                      <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload()" :disabled="isUploadingStatusMap[this.supplemenForm.id]">补充数据上传</el-button>
<!--                      <div slot="tip" class="el-upload__tip">只能上传zip文件</div>-->
                    </el-upload>
                </el-form-item>
                <div class="progress-box" v-if="isUploadingByIdMap[supplemenForm.id]">
                    <div>上传进度：</div>
                    <el-progress :text-inside="true" :stroke-width="24" :percentage="isUploadingByIdMap[supplemenForm.id]" status="success" class="progress-item"></el-progress>
                </div>

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
        getGroup, AddGroup, Updategroup,
        DelGroup, DisableGroup, EnableGroup,
        getdicomSend, getDictionary, addzipupload,
         getDataResult, getGroupBase, getGroupInfo
    } from '../../../router/api';
    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                project_id:localStorage.getItem("project_id"),
                dataupshow:false,
                file_path :'',
                file: '',
                fileList: [],
                filetype:[],
                model:[],
                filters: {
                    type: [],
                    remarks: '',
                    selecttype: 'dicom',
                    status: true
                },
                showFileName: false,
                baseData: [],
                total: 0,
                Virtual: false,
                page: 1,
                page_size: 20,
                listLoading: false,
                sels: [],//列表选中列
                // options:{},
                groupOptions:{},
                editFormVisible: false,//编辑界面是否显示
                editLoading: false,
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
                    name: '',
                    route: '',
                    type: ''
                },

                addFormVisible: false,//新增界面是否显示
                addLoading: false,
                addFormRules: {
                    remarks: [
                        { required: true, message: '请填写病种名称', trigger: 'blur' }
                    ],

                    type: [
                        { required: true, message: '请填写数据类型', trigger: 'change' }
                    ]
                },

                supplementVisible: false,//补充病人数据界面是否显示
                //补充病人数据界面数据
                supplemenForm: {
                    id:'',
                    custom:'',
                    route: '',
                    files: '',
                },
                //新增界面数据
                addForm: {
                    remarks:'',
                    name: '',
                    type:''
                },
                infoData:[],
                groupData:[],
                dicomgrouplist: {},
                noneFileListFlag: true,
                isUploadingByIdMap: {},
                isUploadingStatusMap: {},
                fileSizeMap: {
                    A: 10,   //<1G
                    B: 1.2,   //<2G
                    C: 0.8,     //<5G
                    D: 0.4,     //<10Gset
                    E: 0.2      //>10G
                }
            }
        },
        mounted() {
            this.getgroupbase();
            this.getfile();
        },
        methods: {
            //
            displaystatus: function (i) {
                // if (i === 'Virtual') {
                //     this.GroupInfo()
                //     this.Virtual = true
                // }
                //
                if (i ==='Virtual') {
                    return 'none'
                } else {
                    return ''
                }
            },
            // 修改组内数据
            ChangeHandle(groupData, direction, movedKeys) {
                console.log(groupData, direction, movedKeys);
            },
            // 组内dicom 信息
            GroupInfo(id) {
                this.listLoading = true
                let self = this;
                const params = {
                    groupId: id
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getGroupInfo(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.groupData = data.groupData
                        this.infoData = data.info
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            // 获取级联 查询 组信息列表
            getgroupbase() {
                this.listLoading = true
                const self = this
                const params = {}
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getGroupBase(headers, params).then((res) => {
                        self.listLoading = false
                        const {msg, code, data} = res
                        if (code === '0') {
                            this.groupOptions = data.groupOptions

                        } else {
                            self.$message.error({
                                message: msg,
                                center: true
                            })
                        }
                    }
                )
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
            getGroupList() {
                this.listLoading = true;
                let self = this;
                let params = {
                    page: self.page,
                    page_size:self.page_size,
                    type: self.filters.type[0],
                    id: self.filters.type[1],
                    name:self.filters.name,
                    project_id:this.project_id
                };
                let headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))};
                getGroup(headers, params).then((res) => {
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
                    DisableGroup(headers, params).then(_data => {
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
                    if(row.other == 0){
                        this.$message({
                            showClose: true,
                            message: '病人数据=0,请添加病人数据刷新页面,之后点击启用',
                            type: 'error'
                        });
                        self.listLoading = false;
                    }else{
                        EnableGroup(headers, params).then(_data => {
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

                }
            },
            handleCurrentChange(val) {
                this.page = val;
                this.getGroupList()
            },
            //显示编辑界面
            handleEdit: function (index, row) {
                if (row.group === 'Virtual') {
                    this.GroupInfo(row.id)
                    this.Virtual = true
                }
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
            //查看结果
            ViewResults: function (index, row) {
                // this.$refs.addForm.validate((valid) => {
                //     this.$message({
                //         message: row.content + "," + row.id + "," + this.file_path,
                //         center: true,
                //         type: 'success'
                //     });
                let params = JSON.stringify({
                    file_path: this.file_path,
                });
                let header = {
                    "Content-Type": "application/json",
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                getDataResult(header, params).then(_data => {
                    let {msg, code, data} = _data;
                        this.$message({
                        message: msg,
                        center: true,
                        // type: 'success'
                    });
                })
                // });
            },
            //显示新增界面
            handleAdd: function () {
                this.addFormVisible = true;
                this.addForm = {
                    name: null,
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
                                id: this.editForm.id,
                                name: this.editForm.name,
                                remask: this.editForm.remask,
                                type: this.editForm.type,
                                groupData: this.groupData,
                                predictor: self.editForm.predictor
                            };
                            let header = {
                                "Content-Type": "application/json",
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            };
                            Updategroup(header, params).then(_data => {
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
                                    self.getGroupList()
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
                                name: this.addForm.name,
                                remask: this.addForm.remask,
                                groupData: this.groupData,
                                type: self.addForm.type,
                                group:self.addForm.type,
                                project:this.project_id,
                                predictor: self.addForm.predictor,
                                status: true
                            });
                            let header = {
                                "Content-Type": "application/json",
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            };
                            AddGroup(header, params).then(_data => {
                                let {msg, code, data} = _data;
                                self.addLoading = false;
                                if (code === '0') {
                                    self.$message({
                                        message: msg,
                                        center: true,
                                        type: 'success'
                                    });
                                    self.$refs['addForm'].resetFields();
                                    self.addFormVisible = false;
                                    self.getGroupList()
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
                                    self.getGroupList()
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
                        self.getGroupList()
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
                    DelGroup(header, params).then(_data => {
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
                        self.getGroupList()
                    });
                })
            },

            handleChange(file, fileList) {
              if(file.name.indexOf(".zip") >= 0 ) {
                  this.showFileName = true
                  this.noneFileListFlag = false
                    this.fileList = fileList;
              }else{
                  this.$message({
                      showClose: true,
                      message: ('上传文件格式不正确'),
                      type: 'warning'
                  });
                  this.showFileName = false
                  this.noneFileListFlag = true
                  this.fileList = []
              }
            },
            //上传补充病人数据
            submitUpload() {
                this.dataupshow=true
                this.isUploadingByIdMap = {
                    ...this.isUploadingByIdMap,
                    [this.supplemenForm.id]: 1
                }
                this.isUploadingStatusMap = {
                    ...this.isUploadingStatusMap,
                    [this.supplemenForm.id]: true 
                }
                const fileSize = this.fileList.length ? this.fileList[0].size / 1024 / 1024 / 1024 : 1;
                const fileSizeMapVal = this.getCurrFileSize(+fileSize)
                const progress = this.fileSizeMap[fileSizeMapVal]

                let tempVal = this.supplemenForm.id
                window[`interval-${tempVal}`] = this.queryCurrUploadingProgress(this.supplemenForm.id, progress)
                let params = new FormData();
                  this.fileList.forEach(item => {
                    params.append("files", item.raw);
                });
                params.append('type', this.supplemenForm.route)
                params.append('id', this.supplemenForm.id)
                params.append('custom', this.supplemenForm.custom)

                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                addzipupload(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    console.log(code)
                    this.isUploadingStatusMap = {
                        ...this.isUploadingStatusMap,
                        [tempVal]: false 
                    }
                    clearInterval(window[`interval-${tempVal}`])
                    if (code === '0') {
                        // alert("ok")
                        // this.$message(data.filename,'上传成功');
                        this.file_path=data.file_path,
                        this.isUploadingByIdMap = {
                            ...this.isUploadingByIdMap,
                            [tempVal]: 100
                        }
                        this.$message({
                            showClose: true,
                          message: (data.filename+'上传成功'),
                          type: 'success'
                        });
                        this.dataupshow=false
                        this.supplementVisible = false;
                    } else {
                        console.log('code !== 0')
                        console.log('code !== 0 && upload fail ! Please try again')
                        clearInterval(window[`interval-${tempVal}`])
                        this.$message({
                            showClose: true,
                            message: ('upload fail ! Please try again'),
                            type: 'error'
                        });
                        this.isUploadingByIdMap = {
                            ...this.isUploadingByIdMap,
                            [tempVal]: 0
                        }
                        this.dataupshow=false
                        this.$message({
                            showClose: true,
                            message: (msg),
                            type: 'error'
                        });
                    }
                }).catch(err => {
                    clearInterval(window[`interval-${tempVal}`])
                    console.log('upload fail ! Please try again')
                    this.isUploadingStatusMap = {
                        ...this.isUploadingStatusMap,
                        [tempVal]: 0
                    }
                    this.isUploadingByIdMap = {
                        ...this.isUploadingByIdMap,
                        [tempVal]: 0
                    }
                    this.$message({
                        showClose: true,
                        message: ('upload fail ! Please try again'),
                        type: 'error'
                    });
                })
            },
            handlePreview(file) {
              console.log(file);
            },
            handleExceed(files, fileList) {
              this.$message.warning(`当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
            },
            queryCurrUploadingProgress(id, progress) {
                const fileSize = this.fileList
                return setInterval(() => {
                    const currProgressVal = +this.isUploadingByIdMap[id]
                    // console.log('id-currProgressVal', id, currProgressVal)
                    if(currProgressVal < 99) {
                        this.isUploadingByIdMap = {
                            ...this.isUploadingByIdMap,
                            [id]: currProgressVal + +progress > 99 ? 99 : +((currProgressVal + +progress / 2).toFixed(1))
                        }
                    }
                }, 500)
            },
            getCurrFileSize(fileSize) {
                let val = 'A'
                if(fileSize >= 10) {
                    val = 'E'
                } else if(fileSize >= 5){
                    val = 'D'
                } else if(fileSize >= 2){
                    val = 'C'
                } else if(fileSize >= 1) {
                    val = 'B'
                } else {
                    val = 'A'
                }
                return val
            }

        },

        mounted() {
            this.getGroupList();
        }
    }

</script>

<style>
    .iconSize{
        font-size: 14px;
        padding: 10px;
        font-weight: bold;
    }
    .progress-box {
        display: flex;
        margin-bottom: 15px;
    }
    .progress-item {
        padding: 0 10px 0 15px;
        flex: 1;
    }

</style>