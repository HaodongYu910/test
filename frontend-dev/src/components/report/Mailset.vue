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
                    <el-button type="primary"  icon="add" class="handle-del mr10" @click="handleAdd()">添加</el-button>
                </div>
                <div class="search" style="float:left">
                    <el-form ref="searchform"  :model="searchform" label-width="100px">
                    <el-select v-model="searchform.select_app" clearable  placeholder="筛选" prop="select_app" class="handle-select mr10">
                        <el-option key="Boimind" label="Boimind" value="Boimind"></el-option>
                        <el-option key="CoinNess" label="CoinNess" value="CoinNess"></el-option>
                    </el-select>
                    <el-input v-model="searchform.select_version" prop="select_version" placeholder="筛选" class="handle-input mr10"></el-input>
                    <el-button type="primary" icon="search" @click="searchProject('searchform')">搜索</el-button>
                </el-form>
                </div>

            </div>
            <el-table :data="tableData" border class="table" ref="multipleTable" @selection-change="handleSelectionChange">
                <el-table-column  label="邮件主题" width="240">
                    <template slot-scope="scope">
                        <span>{{ scope.row.title }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="Boimind版本" width="150">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.test_version }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="CoinNess版本" width="150">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.cns_version}}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="是否发送" width="100">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.is_send }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="发送时间" width="200">
                    <template slot-scope="scope">
                        <span >{{ scope.row.send_time }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="收件人员" width="300">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.receiver }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="抄送人员" width="250" :formatter="dateFormatter">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.email_cc }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
                        <el-button type="text" icon="el-icon-find" @click="showRisk(scope.$index, scope.row)">查看模板</el-button>
                        <el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                        <el-button type="text" icon="el-icon-lx-comment"  @click="handleSend(scope.$index, scope.row)">发送</el-button>
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
                   <el-form-item  label="ID">
                         <el-input :disabled="true" v-model="editform.id" width="5%"></el-input>
                    </el-form-item>
                    <el-form-item  label="邮件主题">
                         <el-input  v-model="editform.title"></el-input>
                    </el-form-item>
                    <el-form-item  label="Boimind版本">
                         <el-input  v-model="editform.test_version"></el-input>
                    </el-form-item>
                   <el-form-item label="CoinNess版本">
                       <el-input  v-model="editform.cns_version"></el-input>
                   </el-form-item>
                <el-form-item label="是否发送">
                   <el-select v-model="editform.is_send" placeholder="请选择">
                        <el-option key="1" label="是" value="1"></el-option>
                        <el-option key="0" label="否" value="0"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="发送时间">
                    <el-date-picker v-model="editform.send_time" type="datetime" placeholder="选择日期"></el-date-picker>
                </el-form-item>
                <el-form-item label="收件人员">
                        <el-select v-model="editform.receiver" placeholder="请选择">
                            <el-option key="test" label="测试" value="test"></el-option>
                            <el-option key="on" label="正式" value="on"></el-option>
                        </el-select>
                </el-form-item>
                <el-form-item label="抄送人员">
                       <el-input  v-model="editform.email_cc"></el-input>
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
                     <el-form-item  label="邮件主题" prop='title'>
                         <el-input  v-model="addForm.title"></el-input>
                     </el-form-item>
                     <el-form-item  label="Boimind版本" prop='title'>
                         <el-input  v-model="addForm.title"></el-input>
                     </el-form-item>
                     <el-form-item  label="CoinNess版本" prop='title'>
                         <el-input  v-model="addForm.title"></el-input>
                     </el-form-item>
                     <el-form-item label="是否发送" prop='development_progress'>
                        <el-select v-model="addForm.development_progress" placeholder="请选择" >
                            <el-option key="0" label="否" value="-"></el-option>
                            <el-option key="1" label="是" value="1"></el-option>
                        </el-select>
                    </el-form-item>
                <el-form-item label="发送时间" prop='start_date'>
                    <el-date-picker v-model="addForm.start_date"  type="datetime" placeholder="选择日期"></el-date-picker>
                </el-form-item>
                <el-form-item label="收件人员" prop="app">
                    <el-select v-model="addForm.app" placeholder="请选择">
                        <el-option key="0" label="ios" value="0"></el-option>
                        <el-option key="1" label="安卓" value="1"></el-option>
                        <el-option key="2" label="所有" value="2"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="抄送人员">
                       <el-input  v-model="editform.email_cc"></el-input>
                </el-form-item>

            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible  = false">取 消</el-button>
                <el-button type="primary" @click="addreportconfig('addForm')">添加</el-button>
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
    import {loadreport,updatereport,Send} from "../../router/api";
    export default {
        name: 'basetable',
        data() {
            return {
                rules:{
                    title: [
                    {  required: true, message: '请输邮件主题', trigger: 'change' }
                    ],
                    receiver: [
                    {  required: true, message: '收件人员', trigger: 'change' },
                    ],
                    is_send: [
                    {  required: true, message: '是否发送', trigger: 'change' }
                    ],
                    email_cc: [
                    {  required: true, message: '抄送人员', trigger: 'change' }
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
                    title: '',
                    test_version: '',
                    cns_version: ''
                },
                editform: {
                    title: '',
                    test_version: '',
                    cns_version: ''
                },
                addForm: {
                    title: '',
                    test_version: '',
                    cns_version: ''
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
                loadreport(headers,params).then(_data=>{
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
                    id:null,
                    test_version:null,
                    cns_version:null,
                    receiver: null,
                    is_send:null,
                    send_time:null,
                    email_cc:null,
                    title:null,
                    template:null
                };
            },
            //添加版本
            addreportconfig(form){
                console.log(form);
                this.$refs[form].validate((valid) => {
                    if (valid) {
                        let params={
                            test_version: this.addForm.test_version,
                            cns_version: this.addForm.cns_version,
                            receiver: this.addForm.receiver,
                            is_send: this.addForm.is_send,
                            send_time: this.addForm.send_time,
                            email_cc: this.addForm.email_cc,
                            title: this.addForm.title,
                            template: this.addForm.template
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
            //打开
            handleEdit(index, row) {
                this.idx = index;
                const item = this.tableData[index];
                this.editform = {
                    id:item.id,
                    test_version:item.test_version,
                    cns_version: item.cns_version,
                    title:item.title,
                    receiver:item.receiver,
                    is_send:item.is_send,
                    send_time:item.send_time,
                    email_cc:item.email_cc,
                    template:''
                }
                this.editVisible = true;
            },
            //打开编辑页面
            handleEdit(index, row) {
                this.idx = index;
                const item = this.tableData[index];
                this.editform = {
                    id:item.id,
                    test_version:item.test_version,
                    cns_version: item.cns_version,
                    title:item.title,
                    receiver:item.receiver,
                    is_send:item.is_send,
                    send_time:item.send_time,
                    email_cc:item.email_cc,
                    template:''
                }
                this.editVisible = true;
            },
            //删除版本记录
            handleDelete(index, row) {
                this.idx = index;
                const item = this.tableData[index];
                let ids=[item.id];
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
            handleSend(index, row) {
                this.idx = index;
                const item = this.tableData[index];
                let id=item.id;
                let params={
                        id:id,
                        type:1,
                        start_time:'',
                        endtime:''
                };
                let headers = {
                    "Content-Type": "application/json"
                };
                Send(headers,params).then(_data=>{
                    let{msg,code,data}=_data;
                    if(code!='0'){
                        this.$message.error(msg);
                        return;
                    }
                    if(data!=null&&!data[0]){
                        this.$message.error(data[1]);
                        return;
                    }
                    this.$message.success('发送成功！');
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
                    id: form.id,
                    test_version: form.test_version,
                    cns_version: form.cns_version,
                    receiver: form.receiver,
                    is_send: form.is_send,
                    send_time: form.send_time,
                    email_cc: form.email_cc,
                    title: form.title,
                    template: ''
                };
                let headers={
                     "Content-Type": "application/json"
                };
                updatereport(headers,params).then(_data=>{
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
