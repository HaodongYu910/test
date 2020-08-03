<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-calendar"></i> 测试工具</el-breadcrumb-item>
                <el-breadcrumb-item>推送工具</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="form-box">
                <el-form ref="form" :model="form" status-icon :rules="rules" label-width="80px">
                    <el-form-item  label="推送ID" prop="pushID">
                       <el-col :span='10'>
                         <el-input v-model="form.pushID" id='pushID'></el-input>
                       </el-col>
                    </el-form-item>
                    <el-form-item label="推送环境" prop="environment" >
                        <el-select v-model="form.environment" placeholder="请选择" >
                            <el-option key="test" label="测试环境" value="test"></el-option>
                            <el-option key="online" label="线上环境" value="online"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="推送类型" prop="types">
                        <el-cascader :options="types" v-model="form.types" @change="changeLang('form')"></el-cascader>
                    </el-form-item>
                     <el-form-item label="选择语言" prop="languages" >
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
                        <el-button type="primary" @click="onSubmit('form')">确定推送</el-button>
                        <el-button @click="resetForm('form')">重置</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>

    </div>
</template>

<script>
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
            languages:[],
            form: {
                pushID: '',
                environment: '',
                types:[],
                languages: []
            },
            rules:{
                pushID: [
                { required: true, message: '请输入推送ID', trigger: 'blur' }
                ],
                environment: [
                {  required: true, message: '请选择推送环境', trigger: 'blur' }
                ],
                types: [
                {  required: true, message: '请选择推送类型', trigger: 'blur' }
                ],
                languages: [
                { required: true, message: '请选择语言', trigger: 'blur' }
                ]
            }

        }
    },
    methods: {
        onSubmit(formName) {
            this.$refs[formName].validate((valid)=>{
                if(valid){
                    console.log("语言："+this.form.languages);
                    console.log("pushID："+this.form.pushID);
                    console.log("APP："+this.form.types[0]);
                    console.log("推送类型："+this.form.types[1]);
                    console.log("environment："+this.form.environment);
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
                    console.log(response); //发生错误时执行的代码  
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
            this.form.languages='';
            var lan_bishijie=[
            {key:"zh_cn",value:"简体中文"},
            {key:"zh_tw",value:"繁体"}];
            var lan_coniness=[
            {key:"zh_cn",value:"简体中文"},
            {key:"zh_tw",value:"繁体"},
            {key:"en_go",value:"English"},
            {key:"ko_kr",value:"한글"}];
              var type=this.form.types[0].toLowerCase();
              if(type=='bishijie'){
                 this.languages=lan_bishijie;
              }else if(type=='coinness'){
                 this.languages=lan_coniness;
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