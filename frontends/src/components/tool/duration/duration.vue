<template>
    <div class="app-container">
        <div class="filter-container">

            <!--工具条-->
            <aside>
                <a href="http://192.168.2.38:9000/" target="_blank">匿名发送dicom数据
                </a>
            </aside>

            <!--工具条-->
            <el-col :span="30" class="toolbar" style="padding-bottom: 0px;">
                <el-form :inline="true" :model="filters" @submit.native.prevent>
                    <el-form-item>
                        <el-input v-model="filters.name" placeholder="名称"
                                  @keyup.enter.native="getDurationlist"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="getDurationlist">查询</el-button>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="handleAdd">新增</el-button>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="handleAnon">匿名化文件夹</el-button>
                    </el-form-item>
                </el-form>
            </el-col>


            <!--列表-->
            <el-table :data="durationlist" highlight-current-row v-loading="listLoading"
                      @selection-change="selsChange"
                      width="95%">
                <el-table-column type="selection" min-width="5%">
                </el-table-column>
                <el-table-column prop="type" label="服务器" min-width="20%">
                    <template slot-scope="scope">
                        <router-link v-if="scope.row.server" :to="{ name: '持续化数据详情', params: {id: scope.row.id}}"
                                     style='text-decoration: none;color: #000000;'>
                            <span style="margin-left: 10px">{{ scope.row.server }}：{{ scope.row.port }}</span>
                        </router-link>
                    </template>
                </el-table-column>
                <el-table-column prop="type" label="匿名名称" min-width="12%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.keyword }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="type" label="发送类型" min-width="25%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.dicom }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="预发送数量" min-width="10%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.sendcount }} 个</span>
                    </template>
                </el-table-column>
                <el-table-column label="实际已发送" min-width="12%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px;color: #FF0000;">{{ scope.row.send }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="结束时间" min-width="10%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px;color: #00A600;;">{{ scope.row.end_time }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="延时时间" min-width="10%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.sleeptime }} 秒 </span>
                    </template>
                </el-table-column>
                <el-table-column label="延时数量" min-width="10%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.sleepcount }} 个 </span>
                    </template>
                </el-table-column>
                <el-table-column label="series延时" min-width="10%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.series }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="DDS" min-width="12%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px;color: #02C874;">{{ scope.row.dds }}</span>
                    </template>
                </el-table-column>

                <el-table-column prop="sendstatus" label="运行状态" min-width="10%">
                    <template slot-scope="scope">
                        <img v-show="scope.row.sendstatus"
                             style="width:18px;height:18px;margin-right:5px;margin-bottom:5px"
                             src="../../../assets/img/qidong.png"/>
                        <img v-show="!scope.row.sendstatus"
                             style="width:15px;height:15px;margin-right:5px;margin-bottom:5px"
                             src="../../../assets/img/ting-zhi.png"/>
                    </template>
                </el-table-column>
                <el-table-column label="操作" min-width="30%">
                    <template slot-scope="scope">
                        <el-button type="info" size="small" @click="handleChangeStatus(scope.$index, scope.row)">
                            {{scope.row.sendstatus===false?'启用':'停用'}}
                        </el-button>
                        <el-button type="danger" size="small" @click="showDetail(scope.$index, scope.row)">数据
                        </el-button>
                        <el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)">修改
                        </el-button>


                    </template>
                </el-table-column>
            </el-table>

            <!--工具条-->
            <el-col :span="24" class="toolbar">
                <el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">删除</el-button>
                <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20"
                               :page-count="total" style="float:right;">
                </el-pagination>
            </el-col>

            <!--编辑界面-->
            <el-dialog title="修改" :visible.sync="editFormVisible" :close-on-click-modal="false"
                       style="width: 75%; left: 12.5%">
                <el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
                    <el-row>
                        <el-col :span="6">
                            <el-form-item label="数据类型" prop="senddata">
                                <el-cascader :options="options" v-model="editForm.senddata" clearable :props="props"
                                             @click.native="getBase()"></el-cascader>
                            </el-form-item>
                        </el-col>
                        <el-col :span="6">
                            <el-form-item label="匿名名称" prop="keyword">
                                <el-input id="key_word" v-model="editForm.keyword" placeholder="数据名称"/>
                            </el-form-item>
                        </el-col>
                        <el-col :span="6">
                            <el-form-item label="发送个数" prop="keyword">
                                <el-input id="sendcount" v-model="editForm.sendcount" placeholder="共/个"/>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>

                        <el-col :span="6">
                            <el-form-item label="持续时间" prop="loop_time">
                                <el-input id="looptime" v-model="editForm.loop_time" placeholder="小时"/>
                            </el-form-item>
                        </el-col>
                        <el-col :span="6">
                            <el-form-item label="延时时间" prop="sleeptime">
                                <el-input id="sleeptime" v-model="editForm.sleeptime" placeholder="秒"/>
                            </el-form-item>
                        </el-col>
                        <el-col :span="6">
                            <el-form-item label="延时数量" prop="sleepcount">
                                <el-input id="sleepcount" v-model="editForm.sleepcount" placeholder="张"/>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="6">
                            <el-form-item label="series" prop="series">
                                <el-switch v-model="editForm.series" active-color="#13ce66"
                                           inactive-color="#ff4949"></el-switch>
                            </el-form-item>
                        </el-col>
                        <el-col :span="4">
                            <el-form-item label="操作" prop="keyword">
                                <el-button type="primary" @click.native="editSubmit" :loading="editLoading">保存
                                </el-button>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form>
            </el-dialog>

            <!--匿名化文件夹界面-->
            <el-dialog title="匿名化文件夹" :visible.sync="anonFormVisible" :close-on-click-modal="false"
                       style="width: 75%; left: 12.5%">
                <el-form :model="anonForm" label-width="80px" :rules="anonFormRules" ref="anonForm">
                    <el-form :inline="true" :model="filters" @submit.native.prevent>
                        <el-row>
                            <el-col :span="10">
                                <el-form-item label="匿名名称（以什么开头）" prop="anon-name">
                                    <el-input id="anon-name" v-model="anonForm.anon_name" placeholder="匿名名称"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="8">
                                <el-form-item label="匿名后文件夹名" prop="anon-disease">
                                    <el-input id="anon-disease" v-model="anonForm.anon_disease" placeholder="文件名"/>
                                </el-form-item>
                            </el-col>
                        </el-row>

                        <el-row>
                            <el-col :span="10">
                                <el-form-item label="需要被匿名文件路径" prop="anon_addr">
                                    <el-input id="anon_addr" v-model="anonForm.anon_addr" placeholder="路径"/>
                                </el-form-item>
                            </el-col>

                            <el-col :span="8">
                                <el-form-item label="匿名后储存路径" prop="appointed_addr">
                                    <el-input id="appointed_addr" v-model="anonForm.appointed_addr" placeholder="储存路径"/>
                                </el-form-item>
                            </el-col>
                        </el-row>

                        <el-row>

                            <el-col :span="10">
                                <el-form-item label="匿名患者姓名？" prop="wPN">
                                    <el-switch v-model="anonForm.wPN" active-color="#13ce66"
                                               inactive-color="#ff4949"></el-switch>
                                </el-form-item>
                            </el-col>

                            <el-col :span="8">
                                <el-form-item label="匿名患者ID？" prop="wPID">
                                    <el-switch v-model="anonForm.wPID" active-color="#13ce66"
                                               inactive-color="#ff4949"></el-switch>
                                </el-form-item>
                            </el-col>
                            <el-col :span="5">
                                <el-form-item label="" prop="anon_start">
                                    <el-button type="primary" @click="startAnon('form')">应用并开始匿名</el-button>
                                </el-form-item>
                            </el-col>

                        </el-row>

                    </el-form>
                </el-form>
            </el-dialog>
            <!--新增界面-->
            <el-dialog title="新增" :visible.sync="addFormVisible" :close-on-click-modal="false"
                       style="width: 75%; left: 12.5%">
                <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
                    <el-form :inline="true" :model="filters" @submit.native.prevent>
                        <el-row>
                            <el-col :span="5">
                                <el-form-item label="发送服务器" prop="sendserver">
                                    <el-select v-model="addForm.sendserver" placeholder="请选择"
                                               @click.native="gethost()">
                                        <el-option
                                                v-for="(item,index) in tags"
                                                :key="item.id"
                                                :label="item.name"
                                                :value="item.id"
                                        />
                                    </el-select>
                                </el-form-item>
                            </el-col>
                            <el-col :span="4">
                                <el-form-item label="端口号" prop="port">
                                    <el-input id="port" v-model="addForm.port" placeholder=""/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="4">
                                <el-form-item label="匿名名称" prop="keyword">
                                    <el-input id="keyword" v-model="addForm.keyword" placeholder="数据名称"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="6">
                                <el-form-item label="数据类型" prop="senddata">
                                    <el-cascader :options="options" v-model="addForm.senddata" clearable :props="props"
                                                 @click.native="getBase()"></el-cascader>
                                </el-form-item>
                            </el-col>
                        </el-row>
                        <el-row>
                            <el-col :span="4">
                                <el-form-item label="持续时间" prop="loop_time">
                                    <el-input id="loop_time" v-model="addForm.loop_time" placeholder="小时"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="4">
                                <el-form-item label="发送数量" prop="count">
                                    <el-input id="sendcount" v-model="addForm.sendcount" placeholder="共/个"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="6">
                                <el-form-item label="是否dds" prop="dds">
                                    <el-input id="dds" v-model="addForm.dds" placeholder="DDS服务"/>
                                </el-form-item>
                            </el-col>
                        </el-row>
                        <el-row>
                            <el-col :span="4">
                                <el-form-item label="延时时间" prop="sleeptime">
                                    <el-input id="sleeptime" v-model="addForm.sleeptime" placeholder="秒"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="4">
                                <el-form-item label="延时数量" prop="sleepcount">
                                    <el-input id="sleepcount" v-model="addForm.sleepcount" placeholder="张"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="3">
                                <el-form-item label="series" prop="series">
                                    <el-switch v-model="addForm.series" active-color="#13ce66"
                                               inactive-color="#ff4949"></el-switch>
                                </el-form-item>
                            </el-col>

                            <el-col :span="4">
                                <el-form-item label="操作" prop="save">
                                    <el-button type="primary" @click="addSubmit('form')">保存</el-button>
                                </el-form-item>
                            </el-col>
                        </el-row>
                    </el-form>
                </el-form>
            </el-dialog>
        </div>
    </div>
</template>

<script>
    // import NProgress from 'nprogress'

    import {
        getduration,
        getdurationverifydata,
        addduration,
        delduration,
        updateduration,
        delete_patients,
        getHost,
        getVersion,
        disable_duration,
        enable_duration,
        getbase
    } from '@/router/api'

    import {anonStart} from "../../../router/api";

    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                props: {multiple: true},
                options: [{
                    value: 'test',
                    label: 'test',
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
                        {required: true, message: '请输入版本号', trigger: 'change'},
                        {pattern: /^\d+\.\d+\.\d+$/, message: '请输入合法的版本号（x.x.x）'}
                    ]
                },
                filters: {
                    diseases: ''
                },
                durationlist: {},
                total: 0,
                page: 1,
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
                    ],
                    description: [
                        {required: false, message: '请输入描述', trigger: 'blur'},
                        {max: 1024, message: '不能超过1024个字符', trigger: 'blur'}
                    ]
                },
                // 编辑界面数据
                editForm: {
                    loop_time: '',
                    port: '4242'
                },
                // 匿名化界面初始数据
                anonForm: {
                    anon_name: '',
                    anon_addr: '',
                    anon_disease: '',
                    wPN: '',
                    wPID: '',
                    appointed_addr: '',
                },
                anonFormVisible: false, // 匿名化界面是否显示
                anonLoading: false,
                anonFormRules: {
                    anon_name: [
                        {required: false, message: '请输入匿名名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ],
                    anon_addr: [
                        {required: true, message: '请输入待匿名文件地址', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ],
                    anon_disease: [
                        {required: true, message: '请输入疾病种类', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ],
                },

                addForm: {
                    port: '4242'
                },
                addFormVisible: false, // 新增界面是否显示
                addLoading: false,
                addFormRules: {
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
                    ]
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
            this.durationVerifyData()
        },
        methods: {
            showDetail(index, row) {
                this.$router.push({
                    path: '/durationData',
                    query: {
                        id: row.id,
                        name: row.server_ip
                    }
                });
            },
            deldicom(formName) {
                this.tableData = null
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        const params = {
                            server_ip: this.form.server_ip,
                            deldata: this.form.deldata,
                            testtype: this.form.testtype,
                            fuzzy: this.form.fuzzy
                        }
                        const headers = {
                            'Content-Type': 'application/json'
                        }
                        delete_patients(headers, params).then(_data => {

                            const {msg, code, data} = _data
                            if (code != '0') {
                                this.$message.error(msg)
                                return
                            }
                            var result = data[0]
                            if (data != null && result == false) {
                                this.$message.error(data[1])
                                return
                            }
                            // 请求正确时执行的代码
                            var mydata = data[1]
                            var tableData = []
                            for (var i = 0; i < mydata.length; i++) {
                                tableData.push({'name': mydata[i]})
                            }
                            var json = JSON.stringify(tableData)
                            this.tableData = JSON.parse(json)
                        })
                    } else {
                        console.log('error submit')
                        return false
                    }
                })
            },
            getversion() {
                const params = {
                    type: '1'
                }
                const headers = {
                    'Content-Type': 'application/json'
                }
                getVersion(headers, params).then(_data => {
                    const {msg, code, data} = _data
                    if (code != '0') {
                        this.$message.error(msg)
                        return
                    }
                    // 请求正确时执行的代码
                    var mydata = data.data
                    var json = JSON.stringify(mydata)
                    this.tags = JSON.parse(json)
                })
            },
            durationVerifyData() {
                const params = {}
                const headers = {
                    'Content-Type': 'application/json'
                }
                durationverifydata(headers, params).then(_data => {
                    const {msg, code, data} = _data
                    if (code != '0') {
                        this.$message.error(msg)
                        return
                    }
                    // 请求正确时执行的代码
                    var mydata = data.data
                    var json = JSON.stringify(mydata)
                    this.tags = JSON.parse(json)
                })
            },
            // 获取getBase列表
            getBase() {
                this.listLoading = true
                const self = this
                const params = {
                    selecttype: "dicom",
                    page_size: 100
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getbase(headers, params).then((res) => {
                        self.listLoading = false
                        const {msg, code, data} = res
                        if (code === '0') {
                            self.total = data.total
                            self.list = data.data
                            self.type = data.type
                            this.options = []
                            var json = JSON.stringify(self.list)
                            this.dis = JSON.parse(json)
                            for (var k in self.type) {
                                var testchildren = []
                                for (var i in this.dis) {
                                    var disjson = this.dis[i]
                                    if (self.type[k] === disjson['type']) {
                                        testchildren.push({
                                                value: disjson['id'],
                                                label: disjson['remarks']
                                            }
                                        )
                                    }
                                }
                                this.options.push({
                                    value: self.type[k],
                                    label: self.type[k],
                                    children: testchildren
                                })
                            }
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true
                            })
                        }
                    }
                )
            },
            // 获取host数据列表
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
            }
            ,
            // 获取数据列表
            getDurationlist() {
                this.listLoading = true
                const self = this
                const params = {}
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getduration(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total
                        self.durationlist = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            }
            ,
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
                        self.getDurationlist()
                    })
                })
            }
            ,
            handleCurrentChange(val) {
                this.page = val
                this.handleDel()
            }
            ,
            // 显示编辑界面
            handleEdit: function (index, row) {
                this.editFormVisible = true
                this.editForm = Object.assign({}, row)
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
                    series: false
                }
            }
            ,
            //显示匿名化文件夹界面
            handleAnon: function () {
                this.anonFormVisible = true
                this.anonForm = {
                    anon_addr: '',
                    wPN: true,
                    wPID: true
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
                                loop_time: self.editForm.loop_time,
                                keyword: this.editForm.keyword,
                                dicom: this.editForm.senddata,
                                sendcount: this.editForm.sendcount,
                                sleepcount: this.editForm.sleepcount,
                                sleeptime: this.editForm.sleeptime,
                                series: this.editForm.series
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
            // 开始匿名
            startAnon: function () {
                this.$refs.anonForm.validate((valid) => {
                    if (valid) {
                        const self = this
                        self.addLoading = true
                        // NProgress.start();
                        const params = JSON.stringify({
                            anon_name: self.anonForm.anon_name,
                            anon_addr: self.anonForm.anon_addr,
                            anon_disease: self.anonForm.anon_disease,
                            appointed_addr: self.anonForm.appointed_addr,
                            wPN: self.anonForm.wPN,
                            wPID: self.anonForm.wPID
                        })
                        const header = {
                            'Content-Type': 'application/json',
                            Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                        }
                        anonStart(header, params).then(_data => {
                            const {msg, code, data} = _data
                            self.addLoading = false
                            if (code === '0') {
                                self.$message({
                                    message: 'anonymization start',
                                    center: true,
                                    type: 'success'
                                })
                                self.$refs['anonForm'].resetFields()
                                self.anonFormVisible = false
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
                                self.$refs['anonForm'].resetFields()
                                self.anonFormVisible = false
                                self.getDurationlist()
                            }
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
                                loop_time: self.addForm.loop_time,
                                keyword: this.addForm.keyword,
                                dicom: this.addForm.senddata,
                                sendcount: this.addForm.sendcount,
                                dds: this.addForm.dds,
                                sleepcount: this.addForm.sleepcount,
                                sleeptime: this.addForm.sleeptime,
                                series: this.addForm.series,
                                sendstatus: false,
                                status: false,
                                hostid:this.addForm.sendserver
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
                        self.getDurationlist()
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
</style>
