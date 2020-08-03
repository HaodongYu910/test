<template :index='report_id'>
    <div class="wid-2000 " for="pc">
        <el-container style="height: 2000px; border: 1px solid #eee">
            <el-container>
                <el-header style="text-align: center; color: #FFFFFF; font-size: 24px">
                    <el-dropdown>
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item>查看</el-dropdown-item>
                            <el-dropdown-item>新增</el-dropdown-item>
                            <el-dropdown-item>删除</el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                    <span>Boimind【】& CoinNess【】质量分析报告</span>
                </el-header>
                <el-main>
                    <div>
                        <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                            <span class="bug-ex-item">项目描述</span>
                            <img class="img-revers" src="../../assets/img/bug-10.png"></p>
                    </div>
                    <el-input
                            type="textarea"
                            :rows="5"
                            placeholder="请输入内容"
                            v-model="textarea">
                    </el-input>
                    <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                        <span class="bug-ex-item">2 需求上线情况</span><img src="../../assets/img/bug-10.png"></p>
                    <el-table :data="tableData" border style="width: 100%">
                        <el-table-column
                                prop="business"
                                label="问题ID"
                                width="180">
                        </el-table-column>
                        <el-table-column
                                prop="product"
                                label="问题内容">
                        </el-table-column>
                        <el-table-column
                                prop="pm"
                                label="经办人"
                                width="180">
                        </el-table-column>
                        <el-table-column
                                prop="测试人员"
                                label="缺陷等级">
                        </el-table-column>
                        <el-table-column
                                prop="online"
                                label="解决状态"
                                width="180">
                        </el-table-column>
                    </el-table>
                    <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                        <span class="bug-ex-item">3 Case执行情况</span>
                        <img class="img-revers" src="../../assets/img/bug-10.png"></p>
                    <el-table :data="tableData" border style="width: 100%">
                        <el-table-column
                                prop="project"
                                label="项目列"
                                width="180">
                        </el-table-column>
                        <el-table-column
                                prop="param"
                                label="相关参数">
                        </el-table-column>
                        <el-table-column
                                prop="device"
                                label="覆盖设备"
                                width="180">
                        </el-table-column>
                        <el-table-column
                                prop="check"
                                label="验收负责人">
                        </el-table-column>
                    </el-table>
                    <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                        <span class="bug-ex-item">4  Bug明细</span>
                        <img class="img-revers" src="../../assets/img/bug-10.png"></p>
                    <el-table :data="tableData" border style="width: 100%">
                        <el-table-column
                                prop="priority"
                                label="方向/优先级"
                                width="180">
                        </el-table-column>
                        <el-table-column
                                prop="Highest"
                                label="Highest">
                        </el-table-column>
                        <el-table-column
                                prop="High"
                                label="High"
                                width="180">
                        </el-table-column>
                        <el-table-column
                                prop="Medium"
                                label="Medium">
                        </el-table-column>
                        <el-table-column
                                prop="Low"
                                label="Low"
                                width="180">
                        </el-table-column>
                        <el-table-column
                                prop="Lowest"
                                label="Lowest">
                        </el-table-column>
                    </el-table>
                    <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                        <span class="bug-ex-item">5 性能/压力测试</span>
                        <img class="img-revers" src="../../assets/img/bug-10.png"></p>
                </el-main>

            </el-container>
        </el-container>

    </div>
</template>

<style>
    .el-header {
        background-color: #B3C0D1;
        color: #333;
        line-height: 60px;
    }

    .el-aside {
        color: #333;
    }
</style>

<script>
import {loadreport,updatereport,Send} from "../../router/api";
    export default {
        name: 'basetable',
        data() {
            return {
                textarea: '1.Boimind x.x.x & CoinNess x.x.x 版本已于x月x日测试完成\n' +
                '2.Android已提交给渠道同学、iOS已提交App Store等待审核；\n' +
                '3.当前版本共消化 糖果红包权益、快讯+图片、热门频道、行情侧需求、广告也无需求、平台基础需求等；\n' +
                '4.本版本共 328个 bug，己解决 307个 ，部分Server Bug 与 P3Bug待到下版本修复。',
                tableData: [{
                    business: '1.糖果红包积分权益',
                    product: '1.糖果红包积分权益\n' +
                    '2.积分权益后台\n' +
                    '3.数据需求',
                    pm: '王晓东',
                    qa: '李兰兰',
                    online: '已上线',
                    status: ' ',
                    project: '用例执行情况',
                    product: '用例执行情况',
                    param: 'Boimind：\n' +
                    '总共执行用例数：1453\n' +
                    '通过数：1281\n' +
                    '未通过：172\n' +
                    '\n' +
                    'CoinNess:\n' +
                    '总共执行用例数：433\n' +
                    '通过数：372\n' +
                    '未通过：61',
                    device: 'Android：三星S7、vivo X9i、红米note 4x、\n' +
                    '小米 MI 5、华为 P10、华为 P10 Plus、华为Mate 9、\n' +
                    'vivo X20、一加 5T、华为mate10、小米 MI 5等\n' +
                    '\n' +
                    'iOS：iPhone SE、5s、6s plus、6s、7 plus、8 plus、iPhoneX，\n' +
                    'iPhone XS max',
                    check: '尹航\n' +
                    '李虎\n' +
                    '刘畅\n' +
                    '柯尊森\n' +
                    '李兰兰\n' +
                    '蒋银山\n',
                    priority: 'Boimind',
                    Highest: '12',
                    High: '32',
                    Medium: '23',
                    Low: '4',
                    Lowest: '1'
                }, {
                    business: '1.糖果红包积分权益',
                    product: '1.糖果红包积分权益\n' +
                    '2.积分权益后台\n' +
                    '3.数据需求',
                    pm: '王晓东',
                    qa: '李兰兰',
                    online: '已上线',
                    status: ' ',
                    project: '',
                    product: '',
                    parameter: '',
                    device: '',
                    check: '',
                    priority: 'Boimind',
                    Highest: '12',
                    High: '32',
                    Medium: '23',
                    Low: '4',
                    Lowest: '1'
                }, {
                    business: '1.糖果红包积分权益',
                    product: '1.糖果红包积分权益\n' +
                    '2.积分权益后台\n' +
                    '3.数据需求',
                    pm: '王晓东',
                    qa: '李兰兰',
                    online: '已上线',
                    status: ' ',
                    project: '',
                    product: '',
                    param: '',
                    device: '',
                    check: '',
                    priority: 'Boimind',
                    Highest: '12',
                    High: '32',
                    Medium: '23',
                    Low: '4',
                    Lowest: '1'
                }, {
                    business: '1.糖果红包积分权益',
                    product: '1.糖果红包积分权益\n' +
                    '2.积分权益后台\n' +
                    '3.数据需求',
                    pm: '王晓东',
                    qa: '李兰兰',
                    online: '已上线',
                    status: ' ',
                    project: '',
                    product: '',
                    param: '',
                    device: '',
                    check: '',
                    priority: 'Boimind',
                    Highest: '12',
                    High: '32',
                    Medium: '23',
                    Low: '4',
                    Lowest: '1'
                }],
                form: {
                    title: '',
                    test_version: '',
                    cns_version: ''
                },
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
                            type: this.addForm.type,
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
                    type:item.type,
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
                    type:item.type,
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
                    type: form.type,
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