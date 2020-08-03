<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-calendar"></i> 风险列表</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="handle-box" style="clear:both;margin-bottom:60px">
                <div class="add" style="float:left">
                    <el-button type="primary"  icon="add" class="handle-del mr10" @click="handleAdd()">添加风险项</el-button>
                </div>
            </div>
            <el-table :data="riskData" border class="table" ref="multipleTable" @selection-change="handleSelectionChange">
                <el-table-column  label="风险内容" width="350">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{scope.row.risk}}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="研发人员" width="150">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{scope.row.development}}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="延期时间" width="150">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{scope.row.delay}}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="解决状态" width="150">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{scope.row.solution_status==0?'未解决':scope.row.solution_status==1?'已解决':'解决中'}}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="重要程度" width="100">
                    <template slot-scope="scope">
                         <span style="margin-left: 10px">{{scope.row.status==0?'Highest':scope.row.status==1?'High':'Medium'}}</span>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
                        <el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.$index, scope.row)">编辑</el-button> 
                        <el-button type="text" icon="el-icon-delete" class="red" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                        <el-button type="text" size="small" @click="handleChangeStatus(scope.$index, scope.row)">
                        {{scope.row.status===0?'显示':'不显示'}}
                    </el-button>
                    </template>
                </el-table-column>
            </el-table>
            
        </div>
         <!-- 编辑弹出框 -->
        <el-dialog title="编辑" :visible.sync="editVisible" width="30%">
            <el-form ref="editform" :model="editform" label-width="100px">
                    <el-form-item  label="项目名称">
                         <el-input :disabled="true"  v-model="editform.project"></el-input>
                    </el-form-item>
                    <el-form-item  label="项目风险点">
                         <el-input  v-model="editform.risk"></el-input>
                    </el-form-item>
                    <el-form-item  label="项目研发人员">
                         <el-input  v-model="editform.development"></el-input>
                    </el-form-item>
                    <el-form-item label="延期日期">
                        <el-input  v-model="editform.delay" placeholder="添加日期"></el-input>
                    </el-form-item>
                    <el-form-item label="解决状态">
                        <el-select v-model="editform.solution_status" placeholder="请选择">
                            <el-option key="0" label="未解决" value="0"></el-option>
                            <el-option key="1" label="已解决" value="1"></el-option>
                            <el-option key="2" label="处理中" value="2"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="重要程度">
                        <el-select v-model="editform.status" placeholder="请选择">
                            <el-option key="0" label="Highest" value="0"></el-option>
                            <el-option key="1" label="High" value="1"></el-option>
                            <el-option key="2" label="Medium" value="2"></el-option>
                        </el-select>
                    </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit(editform)">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 添加弹出框 -->
        <el-dialog title="编辑" :visible.sync="dialogFormVisible" width="30%">
            <el-form ref="addform" :model="addform" label-width="100px" :rules='addRiskRules'>
                    <el-form-item  label="项目风险点" prop='risk'>
                         <el-input  v-model="addform.risk"></el-input>
                    </el-form-item>
                    <el-form-item  label="研发人员" prop='development'>
                         <el-input  v-model="addform.development"></el-input>
                    </el-form-item>
                    <el-form-item label="延期天数" prop='delay'>
                        <el-input  v-model="addform.delay"  placeholder="请输入延期天数"></el-input>
                    </el-form-item>
                    <el-form-item label="解决状态" prop='solution_status'>
                        <el-select v-model="addform.solution_status" placeholder="请选择">
                            <el-option key="0" label="未解决" value="0"></el-option>
                            <el-option key="1" label="已解决" value="1"></el-option>
                            <el-option key="2" label="处理中" value="2"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="重要程度" prop='status'>
                        <el-select v-model="addform.status" placeholder="请选择">
                           <el-option key="0" label="Highest" value="0"></el-option>
                            <el-option key="1" label="High" value="1"></el-option>
                            <el-option key="2" label="Medium" value="2"></el-option>
                        </el-select>
                    </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="addRisk('addform')">确 定</el-button>
            </span>
        </el-dialog>
    </div>

</template>

<script>
import {loadRisk,deleteRisk,addRisk,updateRisk,disableRisk,enableRisk} from "../../router/api";
export default {
    name: 'baseform',
    data: function(){
        return {
            addRiskRules:{
                project: [
                    {  required: true, message: '请选择项目名称', trigger: 'change' }
                ],
                risk: [
                    {  required: true, message: '请输入项目风险点内容', trigger: 'change' }
                ],
                development: [
                    {  required: true, message: '请输入项目研发人员', trigger: 'change' }
                ],
                delay: [
                    {  required: true, message: '请输入延期日期', trigger: 'change' }
                ],
                solution_status: [
                    {  required: true, message: '请选择风险点的解决状态', trigger: 'change' }
                ],
                status: [
                    {  required: true, message: '请选择版本的重要程度', trigger: 'change' }
                ],
            },
            //表格数据
            /*riskData:[{
                "project": "CoinNess",
                "risk": " iOS测试",
                "development": "张三",
                "delay": "",
                "solution_status": "1",
                "status": "1"
            },
            {
                "project": "CoinNess",
                "risk": " iOS测试",
                "development": "张三",
                "delay": "",
                "solution_status": "1",
                "status": "1"
            }],*/
            riskData:[],
            editform:{
                risk_id:'',
                project_id:''
            },
            addform:{
            },
            editVisible: false,
            delVisible: false,
            dialogFormVisible :false,
            multipleSelection: [],
            routerParams:null
        }
    },
    created(){
        this.getParams();
        this.getData();
    },
    activated() {
        this.getParams();
        this.getData();
    },
    methods: {
        //初始化数据
        getData(){
            let params={
                project_id:this.routerParams.project_id
            };
            let headers= {
                'Content-Type': 'application/x-www-form-urlencoded'
            };
            loadRisk(headers,params).then(_data=>{
                if(_data.length==0) {
                    this.riskData=null;
                    return;
                }
                this.riskData=_data;
            });
        },
        //获取由路由传递过来的参数
        getParams(){
            this.routerParams=this.$route.query;
        },
        handleSelectionChange(val) {
            this.multipleSelection = val;
        },
        //打开编辑页面
        handleEdit(index, row) {
            this.idx = index;
            const item = this.riskData[index];
            console.log(this.routerParams.project_id);
            this.editform = {
                project:this.routerParams.name,
                risk:item.risk,
                development:item.development,
                delay:item.delay,
                solution_status:item.solution_status,
                status:item.status,
                risk_id:item.risk_id,
                project_id:this.routerParams.project_id
            }
            this.editVisible = true;
        },
        // 保存编辑的风险点
        saveEdit() {
            console.log("solution_status==="+this.editform.solution_status);
            console.log("status==="+this.editform.status);
            let params={
                risk:this.editform.risk,
                development:this.editform.development,
                delay:this.editform.delay,
                solution_status:this.editform.solution_status,
                status:this.editform.status,
                risk_id:this.editform.risk_id,
                project_id:this.editform.project_id
            };
            let headers={
             "Content-Type": "application/json"
            };
            updateRisk(headers,params).then(_data=>{
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
        // 改变风险状态
            handleChangeStatus: function (index, row) {
                let self = this;
                this.listLoading = true;
                let params = {risk_id: row.id};
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                if (row.status) {
                    disableProject(headers, params).then(_data => {
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
                    enableRisk(headers, params).then(_data => {
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
        //删除风险点
        handleDelete(index, row) {
            this.idx = index;
            const item = this.riskData[index];
            let ids=[item.risk_id];
            let params={
                ids:ids
            };
            let headers = {
                "Content-Type": "application/json"
            };
            deleteRisk(headers,params).then(_data=>{
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
            });

        },
        //打开添加风险项页面
        handleAdd(){
            this.dialogFormVisible=true;
            this.addform={
                project:this.routerParams.project,
                risk:null,
                development:null,
                delay:null,
                solution_status:null,
                status:null
            };
        },
        //添加风险项
        addRisk(form){
            this.$refs[form].validate((valid) => {
                    if (valid) {
                        let params={
                            project_id:this.routerParams.project_id,
                            risk:this.addform.risk,
                            development:this.addform.development,
                            delay:this.addform.delay,
                            solution_status:this.addform.solution_status,
                            status:this.addform.status
                        };
                        console.log(params);
                        let headers={
                           "Content-Type": "application/json"
                       };
                       addRisk(headers,params).then(_data=>{
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
        }
    }
}
</script>
<style scoped>
    .el-input__inner,#pushID{
        height:10px;
    }
</style>