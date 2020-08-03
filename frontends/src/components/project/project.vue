<template>
    <div class="table">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-cascades"></i>测试项目版本</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="handle-box" style="clear:both;margin-bottom:80px">
               <!--  <el-button type="primary" icon="delete" class="handle-del mr10" @click="delAll">批量删除</el-button> -->
                <div class="add" style="float:left">
                    <el-button type="primary"  icon="add" class="handle-del mr10" @click="handleAdd()">添加版本</el-button>
                </div>
                <div class="search" style="float:left">
                    <el-form ref="searchform"  :model="searchform" label-width="100px">
                    <el-select v-model="searchform.select_app" clearable  placeholder="筛选APP" prop="select_app" class="handle-select mr10">
                        <el-option key="Boimind" label="Boimind" value="Boimind"></el-option>
                        <el-option key="CoinNess" label="CoinNess" value="CoinNess"></el-option>
                    </el-select>
                    <el-input v-model="searchform.select_version" prop="select_version" placeholder="筛选版本" class="handle-input mr10"></el-input>
                    <el-button type="primary" icon="search" @click="searchProject('searchform')">搜索</el-button>
                </el-form>
                </div>

            </div>
            <el-table :data="tableData" border class="table" ref="multipleTable" @selection-change="handleSelectionChange">
                <el-table-column  label="项目" width="100">
                    <template slot-scope="scope">
                        <span>{{ scope.row.project }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="版本" width="100">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.version }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="研发进度" width="100">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.development_progress}}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="测试进度" width="100">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.test_progress }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="状态" width="100">
                    <template slot-scope="scope">
                        <span >{{ scope.row.status }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="项目开始时间" width="180">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.start_date }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="接口提测时间" width="180" :formatter="dateFormatter">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.api_date }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="app提测时间" width="180" :formatter="dateFormatter">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.app_date }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="接口上线时间" width="180" :formatter="dateFormatter">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.api_online_date }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="全部上线日期" width="180" :formatter="dateFormatter">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.end_date }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="bug统计日期" width="180" :formatter="dateFormatter">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.bug_count_date }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="客户端" width="100">
                    <template slot-scope="scope">
                        <el-tooltip content="0:安卓 1:ios 2:安卓和IOS" placement="bottom">
                          <el-button>{{ scope.row.app }}</el-button>
                        </el-tooltip>
                    </template>
            </el-table-column>
                <el-table-column  label="上线状态" width="100">
                     <template slot-scope="scope">
                        <el-tooltip content="0:未上线 1:已上线" placement="bottom">
                          <el-button>{{ scope.row.on_line }}</el-button>
                        </el-tooltip>
                    </template>
                </el-table-column>

                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
                        <el-button type="text" icon="el-icon-find" @click="showRisk(scope.$index, scope.row)">查看风险点</el-button>
                        <el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                        <el-button type="text" icon="el-icon-delete" class="red" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <!-- 数据分页 -->
            <div class="pagination">
                <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"
                    :page-sizes="[10, 20, 30, 40]"
                    :page-size="100"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="currentTotal"
                    >
              </el-pagination>
            </div>
        </div>

        <!-- 编辑弹出框 -->
        <el-dialog title="编辑" :visible.sync="editVisible" width="30%">
            <el-form ref="editform" :model="editform" label-width="100px">
                   <el-form-item  label="项目ID">
                         <el-input :disabled="true" v-model="editform.project_id"></el-input>
                    </el-form-item>
                    <el-form-item  label="项目版本">
                         <!-- <el-input :disabled="true"  v-model="editform.version"></el-input> -->
                         <el-input :disabled="true" v-model="editform.version"></el-input>
                    </el-form-item>
                    <el-form-item  label="项目名称">
                         <el-input :disabled="true"  v-model="editform.project"></el-input>
                    </el-form-item>
                   <el-form-item label="研发进度">
                    <el-select v-model="editform.development_progress" placeholder="请选择">
                        <el-option key="未开发" label="未开发" value="未开发"></el-option>
                        <el-option key="开发中" label="开发中" value="开发中"></el-option>
                        <el-option key="开发提测" label="开发提测" value="开发提测"></el-option>
                        <el-option key="开发完成" label="开发完成" value="开发完成"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="测试进度">
                   <el-select v-model="editform.test_progress" placeholder="请选择">
                        <el-option key="未测试" label="未测试" value="未测试"></el-option>
                        <el-option key="测试中" label="测试中" value="测试中"></el-option>
                        <el-option key="测试完成" label="测试完成" value="测试完成"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="发版状态">
                    <el-select v-model="editform.status" placeholder="请选择">
                        <el-option key="未发版" label="未发版" value="未发版"></el-option>
                        <el-option key="已发版" label="已发版" value="已发版"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="项目开始时间">
                    <el-date-picker v-model="editform.start_date" type="datetime" placeholder="选择日期"></el-date-picker>
                </el-form-item>
                <el-form-item label="接口提测时间">
                    <el-date-picker v-model="editform.api_date" type="datetime" placeholder="选择日期"></el-date-picker>
                </el-form-item>
                <el-form-item label="app提测时间">
                    <el-date-picker v-model="editform.app_date" type="datetime" placeholder="选择日期"></el-date-picker>
                </el-form-item>
                <el-form-item label="接口上线时间">
                    <el-date-picker v-model="editform.api_online_date" type="datetime" placeholder="选择日期"></el-date-picker>
                </el-form-item>
                <el-form-item label="全部上线日期">
                    <el-date-picker v-model="editform.end_date" type="datetime" placeholder="选择日期"></el-date-picker>
                </el-form-item>
                <el-form-item label="bug统计日期">
                    <el-date-picker v-model="editform.bug_count_date" type="datetime" placeholder="选择日期"></el-date-picker>
                </el-form-item>
                <el-form-item label="客户端">
                        <el-select v-model="editform.app" placeholder="请选择">
                            <el-option key="0" label="ios" value="0"></el-option>
                            <el-option key="1" label="安卓" value="1"></el-option>
                            <el-option key="2" label="所有" value="2"></el-option>
                        </el-select>
                </el-form-item>
                <el-form-item label="上线状态">
                        <el-select v-model="editform.on_line" placeholder="请选择">
                            <el-option key="0" label="未上线" value="0"></el-option>
                            <el-option key="1" label="已上线" value="1"></el-option>
                        </el-select>
                </el-form-item>

            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit(editform)">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 添加弹出框 -->
        <el-dialog title="添加" :rules="rules" :visible.sync="dialogFormVisible" width="30%">
            <el-form :model="addForm" :rules="rules" ref="addForm" label-width="120px">
                      <el-form-item label="项目名称" prop='project'>
                        <el-select v-model="addForm.project" placeholder="请选择" >
                            <el-option key="Boimind" label="Boimind" value="Boimind"></el-option>
                            <el-option key="CoinNess" label="CoinNess" value="CoinNess"></el-option>
                        </el-select>
                    </el-form-item>
                     <el-form-item  label="项目版本" prop='version'>
                         <el-input  v-model="addForm.version"></el-input>
                     </el-form-item>
                     <el-form-item label="研发进度" prop='development_progress'>
                        <el-select v-model="addForm.development_progress" placeholder="请选择" >
                            <el-option key="未开发" label="未开发" value="未开发"></el-option>
                            <el-option key="开发中" label="开发中" value="开发中"></el-option>
                            <el-option key="开发提测" label="开发提测" value="开发提测"></el-option>
                            <el-option key="开发完成" label="开发完成" value="开发完成"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="测试进度" prop='test_progress'>
                     <el-select v-model="addForm.test_progress" placeholder="请选择" >
                        <el-option key="未测试" label="未测试" value="未测试"></el-option>
                        <el-option key="测试中" label="测试中" value="测试中"></el-option>
                        <el-option key="测试完成" label="测试完成" value="测试完成"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="发版状态" prop='status'>
                    <el-select v-model="addForm.status" placeholder="请选择" >
                        <el-option key="未发版" label="未发版" value="未发版"></el-option>
                        <el-option key="已发版" label="已发版" value="已发版"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="项目开始时间" prop='start_date'>
                    <el-date-picker v-model="addForm.start_date"  type="datetime" placeholder="选择日期"></el-date-picker>
                </el-form-item>
                <el-form-item label="接口提测时间" prop='api_date'>
                    <el-date-picker v-model="addForm.api_date"  type="datetime" placeholder="选择日期"></el-date-picker>
                </el-form-item>
                <el-form-item label="app提测时间" prop='app_date'>
                    <el-date-picker v-model="addForm.app_date"  type="datetime" placeholder="选择日期"></el-date-picker>
                </el-form-item>
                <el-form-item label="接口上线时间" prop='api_online_date'>
                    <el-date-picker v-model="addForm.api_online_date"  type="datetime" placeholder="选择日期"></el-date-picker>
                </el-form-item>
                <el-form-item label="全部上线日期" prop='end_date'>
                    <el-date-picker v-model="addForm.end_date"  type="datetime" placeholder="选择日期"></el-date-picker>
                </el-form-item>
                <el-form-item label="bug统计日期" prop='bug_count_date'>
                    <el-date-picker v-model="addForm.bug_count_date"  type="datetime" placeholder="选择日期"></el-date-picker>
                </el-form-item>
                <el-form-item label="APP类型" prop="app">
                    <el-select v-model="addForm.app" placeholder="请选择">
                        <el-option key="0" label="ios" value="0"></el-option>
                        <el-option key="1" label="安卓" value="1"></el-option>
                        <el-option key="2" label="所有" value="2"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="上线状态" prop="on_line">
                    <el-select v-model="addForm.on_line" placeholder="请选择">
                        <el-option key="0" label="未上线" value="0"></el-option>
                        <el-option key="1" label="已上线" value="1"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="客户端" prop="type">
                    <el-select v-model="addForm.type" placeholder="请选择">
                        <el-option key="Web" label="Web" value="Web"></el-option>
                        <el-option key="App" label="App" value="App"></el-option>
                    </el-select>
                </el-form-item>

            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible  = false">取 消</el-button>
                <el-button type="primary" @click="addProject('addForm')">添加</el-button>
            </span>
        </el-dialog>

        <!-- 删除提示框 -->
        <!-- <el-dialog title="提示" :visible.sync="delVisible" width="300px" center>
            <div class="del-dialog-cnt">删除不可恢复，是否确定删除？</div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="delVisible = false">取 消</el-button>
                <el-button type="primary" @click="deleteRow(scope.$index, scope.row)">确 定</el-button>
            </span>
        </el-dialog> -->
    </div>
</template>

<script>
    import {loadTestProject,deleteTestProject,addTestProject,updateTestProject} from "../../router/api";
    export default {
        name: 'basetable',
        data() {
            return {
                /*url: '/api/test_project',*/
                /*tableData: [{
                    "project_id": "2",
                    "project": "CoinNess",
                    "version": "V1.5.3",
                    "development_progress": "开发中",
                    "test_progress": "测试完成",
                    "status": "已发版",
                    "start_date": "2018-12-06T00:00:00",
                    "api_date": "2018-12-06T00:00:00",
                    "app_date": "2018-12-06T00:00:00",
                    "api_online_date": "2018-12-06T00:00:00",
                    "end_date": "2018-12-06T00:00:00",
                    "bug_count_date": "2018-12-06T00:00:00",
                    "app": "2",
                    "on_line": "1"
                }],*/
                rules:{
                    project: [
                    {  required: true, message: '请输入项目名称', trigger: 'change' }
                    ],
                    version: [
                    {  required: true, message: '请选择项目版本', trigger: 'change' },
                    {  pattern:/^\d+\.\d+\.\d+$/,message:'请输入合法的版本号（x.x.x）'}
                    ],
                    development_progress: [
                    {  required: true, message: '请选择研发进度', trigger: 'change' }
                    ],
                    test_progress: [
                    {  required: true, message: '请选择测试进度', trigger: 'change' }
                    ],
                    status: [
                    {  required: true, message: '请选择项目状态', trigger: 'change' }
                    ],
                    start_date: [
                    {  required: true, message: '请输入项目开始时间', trigger: 'change' }
                    ],
                    api_date: [
                    {  required: true, message: '请输入接口提测时间', trigger: 'change' }
                    ],
                    app_date: [
                    {  required: true, message: '请输入APP提测时间', trigger: 'change' }
                    ],
                    api_online_date: [
                    {  required: true, message: '请输入接口上线时间', trigger: 'change' }
                    ],
                    end_date: [
                    {  required: true, message: '请输入项目全部上线时间', trigger: 'change' }
                    ],
                    bug_count_date: [
                    {  required: true, message: '请输入bug统计日期', trigger: 'change' }
                    ],
                    app: [
                    {  required: true, message: '请选择app类型', trigger: 'change' }
                    ],
                    on_line: [
                    {  required: true, message: '请选择上线状态', trigger: 'change' }
                    ],
                    type: [
                    {  required: true, message: '请选择客户端', trigger: 'change' }
                    ],

                },
                tableData:[],
                cur_page: 1,
                multipleSelection: [],
                select_cate: '',
                select_word: '',
                del_list: [],
                is_search: false,
                editVisible: false,
                delVisible: false,
                dialogFormVisible :false,
                form: {
                    project: '',
                    version: '',
                    development_progress: ''
                },
                editform: {
                    project: '',
                    version: '',
                    development_progress: ''
                },
                addForm: {
                    project: '',
                    version: '',
                    development_progress: ''
                },
                searchform:{

                },
                currentPage: 1,
                pageSize: 10,
                currentTotal: 0
                /*idx: -1,
                total:9*/
            }
        },
        loadProject(){
            loadProject().then(_data=>{
                let{msg,data,code}=_data;
                console(_data);
            });
        },
        //页面一加载便向后台发送请求
        created() {
            this.getData();
        },
        computed: {
            data() {
                return this.tableData.filter((d) => {
                    let is_del = false;
                    for (let i = 0; i < this.del_list.length; i++) {
                        if (d.name === this.del_list[i].name) {
                            is_del = true;
                            break;
                        }
                    }
                    if (!is_del) {
                        if (d.address.indexOf(this.select_cate) > -1 &&
                            (d.name.indexOf(this.select_word) > -1 ||
                                d.address.indexOf(this.select_word) > -1)
                        ) {
                            return d;
                        }
                    }
                })
            }
        },
        methods: {
            //展示风险项
            showRisk(index,row){
                this.$router.push({
                    path:'/risk',
                    query:{
                        project_id:row.project_id,
                        project:row.project
                    }
                });
            },
            handleSizeChange(val) {
                this.pageSize = val;
                console.log(`每页 ${val} 条`);
                this.getData();
            },
            // 分页导航
            handleCurrentChange(val) {
                this.currentPage = val;
                console.log(`这是第${val}页`);
                this.getData();
            },
            getData(name,version) {
                let params={
                    page:this.currentPage,
                    page_size:this.pageSize,
                    name:name,
                    version:version
                };
                let headers= {
                    'Content-Type': 'application/x-www-form-urlencoded'
                };
                loadTestProject(headers,params).then(_data=>{
                    let{msg,data,code}=_data;
                    this.currentTotal=data.total;
                    this.tableData=data.data;
                });
            },
            search() {
                this.is_search = true;
            },
            dateFormatter(row, column) {
                console.log('格式化日期');
                var date=row[column.property];
                if(date==undefined)
                    return "";
                return moment(data).format('YYYY-MM-DD');
            },
            filterTag(value, row) {
                return row.tag === value;
            },
            handleAdd(){
                this.dialogFormVisible=true;
                this.addForm={
                    project_id:null,
                    version:null,
                    project:null,
                    development_progress: null,
                    test_progress:null,
                    status:null,
                    start_date:null,
                    api_date:null,
                    app_date:null,
                    api_online_date:null,
                    end_date:null,
                    bug_count_date:null,
                    app:null,
                    on_line:null
                };
            },
            //添加版本
            addProject(form){
                console.log(form);
                this.$refs[form].validate((valid) => {
                    if (valid) {
                        let params={
                            project: this.addForm.project,
                            version: 'V'+this.addForm.version,
                            development_progress: this.addForm.development_progress,
                            test_progress: this.addForm.test_progress,
                            status: this.addForm.status,
                            start_date: this.addForm.start_date,
                            api_date: this.addForm.api_date,
                            app_date: this.addForm.app_date,
                            api_online_date: this.addForm.api_online_date,
                            end_date: this.addForm.end_date,
                            bug_count_date: this.addForm.bug_count_date,
                            app: this.addForm.app,
                            on_line: this.addForm.on_line,
                            client:2,
                            type:this.addForm.type
                        };
                        console.log(params);
                        let headers={
                           "Content-Type": "application/json"
                       };
                       addTestProject(headers,params).then(_data=>{
                            let{msg,code,data}=_data;
                            console.log("code:"+code);
                            if(code!='0'){
                                this.$message.error(msg);
                                return;
                            }
                            this.$message.success("添加成功");
                            this.dialogFormVisible=false;
                            this.getData();
                    });
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });

            },
            //打开编辑页面
            handleEdit(index, row) {
                this.idx = index;
                const item = this.tableData[index];
                this.editform = {
                    project_id:item.project_id,
                    version:item.version,
                    project:item.project,
                    development_progress: item.development_progress,
                    test_progress:item.test_progress,
                    status:item.status,
                    start_date:item.start_date,
                    api_date:item.api_date,
                    app_date:item.app_date,
                    api_online_date:item.api_online_date,
                    end_date:item.end_date,
                    bug_count_date:item.bug_count_date,
                    app:item.app,
                    on_line:item.on_line
                }
                this.editVisible = true;
            },
            //删除版本记录
            handleDelete(index, row) {
                this.idx = index;
                const item = this.tableData[index];
                let ids=[item.project_id];
                let params={
                        ids:ids
                };
                let headers = {
                    "Content-Type": "application/json"
                };
                deleteTestProject(headers,params).then(_data=>{
                    let{msg,code,data}=_data;
                    if(code!='0'){
                        this.$message.error(msg);
                        return;
                    }
                    if(data!=null&&!data[0]){
                        this.$message.error(data[1]);
                        return;
                    }
                    this.$message.success('删除成功！');
                    this.getData();
                    /*
                    this.tableData=_data;*/
                });

            },
           /* delAll() {
                const length = this.multipleSelection.length;
                let str = '';
                this.del_list = this.del_list.concat(this.multipleSelection);
                for (let i = 0; i < length; i++) {
                    str += this.multipleSelection[i].name + ' ';
                }
                this.$message.error('删除了' + str);
                this.multipleSelection = [];
            },*/
            handleSelectionChange(val) {
                this.multipleSelection = val;
            },
            //搜索功能
            searchProject(formName) {

                let select_app=this.searchform.select_app;
                let select_version=this.searchform.select_version;
                let reg=/^\d+\.\d+\.\d+$/;
                if((typeof select_app == "undefined")&&(typeof select_version == "undefined")){
                    alert("请输入要搜索的版本号或者版本号");
                    return;
                }
                let result=typeof select_version;
                if( result!= "undefined"&&result!=null&&result!=''){
                    if(!reg.test(select_version)){
                        alert("请输入格式为x.x.x的版本号");
                        return;
                    }

                }


                this.getData(select_app,select_version);
            },
            // 保存编辑
            saveEdit(form) {
                let params={
                    project_id: form.project_id,
                    project: form.project,
                    version: form.version,
                    development_progress: form.development_progress,
                    test_progress: form.test_progress,
                    status: form.status,
                    start_date: form.start_date,
                    api_date: form.api_date,
                    app_date: form.app_date,
                    api_online_date: form.api_online_date,
                    end_date: form.end_date,
                    bug_count_date: form.bug_count_date,
                    app: form.app,
                    on_line: form.on_line
                };
                let headers={
                     "Content-Type": "application/json"
                };
                updateTestProject(headers,params).then(_data=>{
                    let{msg,code,data}=_data;
                    if(code!='0'){
                        this.$message.error(msg);
                        return;   
                    }
                    if(data!=null&&!data[0]){
                        this.$message.error(data[1]);
                        return;
                    }
                    this.$message.success("编辑成功");
                    this.editVisible=false;
                    this.getData();
                });
            },
            
        }
    }

</script>
<style scoped>

    .handle-box {
        margin-bottom: 20px;
    }

    .handle-select {
        width: 120px;
    }

    .handle-input {
        width: 300px;
        display: inline-block;
    }
    .del-dialog-cnt{
        font-size: 16px;
        text-align: center
    }
    .table{
        width: 100%;
        font-size: 14px;
    }
    .red{
        color: #ff0000;
    }
    .mr10{
        margin-right: 10px;
    }

    .el-input__inner,#pushID{
        height:10px;
    }
</style>