<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-calendar"></i> 测试工具</el-breadcrumb-item>
                <el-breadcrumb-item>性能工具</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="form-box">
                <el-form ref="form" :model="form" status-icon :rules="rules" label-width="200px">
                    <el-form-item  label="负载量" prop="pushID">
                       <el-col :span='10'>
                         <el-input v-model="form.pushID" id='pushID'></el-input>
                       </el-col>
                    </el-form-item>
                    <el-form-item label="负载服务器" prop="environment" >
                        <el-select clearable  v-model="form.environment" placeholder="请选择" >
                            <el-option key="test" label="192.168.1.208" value="192.168.1.20"></el-option>
                            <el-option key="online" label="192.168.4.85" value="192.168.4.85"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item  label="测试数据" prop="pushID">
                       <el-col :span='10'>
                         <el-input v-model="form.pushID" id='pushID'></el-input>
                       </el-col>
                    </el-form-item>
                     <el-form-item label="是否及时返回数据" prop="languages" >
                        <el-select v-model="form.languages" placeholder="请选择" >
                            <el-option 
                            v-for="(item,index) in languages"
                            :key='item.key'
                            :label='item.value'
                            :value='item.key'
                            ></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="onSubmit('form')">确定</el-button>
                        <el-button @click="resetForm('form')">重置</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>

    </div>
</template>

<script>
import {pushTool} from "../../router/api";
export default {
    name: 'baseform',
    data: function(){
        return {
            types:[
            {
                value: 'bishijie',
                label: 'Boimind',
                children: [
                {
                    value: 'news',
                    label: '快讯',
                },
                {
                    value: 'shendu',
                    label: '深度',
                },
                {
                    value: 'replay',
                    label: '币圈',
                },
                {
                    value: 'monitor',
                    label: '盯盘',
                }
                ]
            },
            {
                value: 'coinness',
                label: 'coinness',
                children: [
                {
                    value: 'news',
                    label: '快讯',
                },
                {
                    value: 'shendu',
                    label: '深度',
                },
                {
                    value: 'monitor',
                    label: '盯盘',
                }
                ]
            }
            ],
            languages:[
                {key:"zh_cn",value:"简体中文"},
                {key:"zh_tw",value:"繁体"}
            ],
            form: {
                pushID: '',
                environment: '',
                types:[],
                languages: [],
                app:'bishijie',
                moudle:[]
            },
            rules:{
                pushID: [
                { required: true, message: '请输入推送ID', trigger: 'blur' }
                ],
                environment: [
                {  required: true, message: '请选择推送环境', trigger: 'blur' }
                ],
                moudle: [
                {  required: true, message: '请添加推送类型', trigger: 'blur' }
                ],
                languages: [
                { required: true, message: '请选择语言', trigger: 'blur' }
                ],
                app: [
                { required: true, message: '请选择推送端', trigger: 'blur' }
                ]
            },
            system:'',
            moudles:[
                {key:"news",value:"快讯"},
                {key:"shendu",value:"深度"},
                {key:"apply",value:"币圈"},
                {key:"monitor",value:"盯盘"}
            ]

        }
    },
    methods: {
       /* onSubmit(formName) {
            this.$refs[formName].validate((valid)=>{
                if(valid){
                    console.logs("语言："+this.form.languages);
                    console.logs("pushID："+this.form.pushID);
                    console.logs("APP："+this.form.types[0]);
                    console.logs("推送类型："+this.form.types[1]);
                    console.logs("environment："+this.form.environment);
                    this.$ajax.post('/bishijie/push',{
                        id:this.form.pushID,
                        service:this.form.environment,
                        system:this.form.types[0],
                        module:this.form.types[1],
                        lang:this.form.languages,
                        rid:''
                    }).then((response) => {
                        if(response.data.code!='0'){
                            this.$message.error(response.data.msg);
                            return;   
                        }
                        if(response.data.data!=null&&!response.data.data[0]){
                            this.$message.error(response.data.data[1]);
                            return;
                        }
                        this.$message.success('push成功！');
                }).catch(function(response) {
                    console.logs(response); //发生错误时执行的代码
                });

            }else{
                console.logs('error submit');
                return false;
            }
        });
        },*/
        onSubmit(formName) {
            this.$refs[formName].validate((valid)=>{
                if(valid){
                    let params={
                        id:this.form.pushID,
                        service:this.form.environment,
                        system:this.form.app,
                        module:this.form.moudle,
                        lang:this.form.languages,
                        rid:''
                    };
                    let headers = {
                        "Content-Type": "application/json"
                    };
                    pushTool(headers,params).then(_data=>{
                        let{msg,code,data}=_data;
                        if(code!='0'){
                            this.$message.error(msg);
                            return;   
                        }
                        if(data!=null&&!data[0]){
                            this.$message.error(data[1]);
                            return;
                        }
                        this.$message.success('push成功！');
                    });
            }else{
                console.log('error submit');
                return false;
            }
        });
        },
        resetForm(formName) {
            this.$refs[formName].resetFields();
        },
        changeLang(formName){
            this.languages=[];
            this.moudles=[];
            this.form.moudle=[];
            this.form.languages='';
            var lan_bishijie=[
                {key:"zh_cn",value:"简体中文"},
                {key:"zh_tw",value:"繁体"}];
            var lan_coniness=[
                {key:"zh_cn",value:"简体中文"},
                {key:"zh_tw",value:"繁体"},
                {key:"en_gb",value:"English"},
                {key:"ko_kr",value:"한글"}];
            var moudles_test=[
                {key:"news",value:"快讯"},
                {key:"shendu",value:"深度"},
                {key:"apply",value:"币圈"},
                {key:"monitor",value:"盯盘"}
            ];
            var moudles_coinness=[
                {key:"news",value:"快讯"},
                {key:"shendu",value:"深度"},
                {key:"monitor",value:"盯盘"}
            ];
            var type=this.form.app.toLowerCase();
            if(type=='bishijie'){
                this.languages=lan_bishijie;
                this.moudles=moudles_test;
            }else if(type=='coinness'){
                this.languages=lan_coniness;
                this.moudles=moudles_coinness;
                console.log(this.modules);
            }
        }
    }
}
</script>
<style scoped>
<style>
    .el-input__inner,#pushID{
        height:10px;
    }
</style>