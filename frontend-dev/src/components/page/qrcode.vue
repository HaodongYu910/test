<template>
    <div>
        <div class="container">
            <div class="form-box">
                <el-form ref="form" :model="form" status-icon :rules="rules" label-width="80px">
                    <el-form-item label="系统" prop="system">
                        <el-cascader :options="system" v-model="form.system" @change="changeLang('form')"></el-cascader>
                    </el-form-item>
                        <el-form-item label="客户端" prop="client">
                        <el-select v-model="form.client" placeholder="请选择">
                            <el-option key="Android" label="Android" value="Android"></el-option>
                            <el-option key="iOS" label="iOS" value="iOS"></el-option>
                        </el-select>
                    </el-form-item>
                     <el-form-item label="版本" prop="version" >
                        <el-select v-model="form.version" placeholder="请选择" >
                            <el-option 
                            v-for="(item,index) in version"
                            :key='item.key'
                            :label='item.value'
                            :value='item.key'
                            ></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="onSubmit('form')">下载</el-button>
                        <el-button @click="resetForm('form')">打包</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>

    </div>
</template>

<script type="text/javascript">
import {download} from "../../router/api";
var u = navigator.userAgent;
var isAndroid = u.indexOf('Android') > -1 || u.indexOf('Adr') > -1; //android终端
var isiOS = !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/); //ios终端
if (isAndroid == true){
    var client="Android";
}
else if(isiOS == true){
    var client="iOS"
}
else{
    var aa= "a"
}

export default {
    name: 'baseform',
    data: function(){
        return {
            system:[
            {
                value: 'bishijie',
                label: 'Boimind',
                children: [
                {
                    value: 'Debug',
                    label: 'Debug',
                },
                {
                    value: 'Huidu',
                    label: 'Huidu',
                },
                {
                    value: 'Release',
                    label: 'Release',
                }
                ]
            },
            {
                value: 'coinness',
                label: 'CoinNess',
                children: [
                {
                    value: 'Debug',
                    label: 'Debug',
                },
                {
                    value: 'Huidu',
                    label: 'Huidu',
                },
                {
                    value: 'Release',
                    label: 'Release',
                }
                ]
            }
            ],
            client:[
                {
                    value: 'Android',
                    label: 'Android',
                },
                {
                    value: 'iOS',
                    label: 'iOS',
                },
            ],
            form: {
                system: '',
                system:[],
                version: []
            },
            rules:{
                system: [
                {  required: true, message: '请选择客户端', trigger: 'blur' }
                ],
                version: [
                { required: true, message: '下载版本', trigger: 'blur' }
                ]
            }

        }
    },
    methods: {
        onSubmit(formName) {
            this.$refs[formName].validate((valid)=>{
                if(valid){
                    var version=this.form.version;
                    if (this.form.system[0] ==="bishijie"){
                        var clm = "CoinWorld"
                    }
                    else{
                        var clm = "CoinNess"
                    }
                    if (aa ==="a"){
                        var client = this.form.client
                    }
                    if (typeof version == "undefined" || version == null || version == ""){
                        alert("请选择版本");
                        return;
                    }
                    let params={
                        system:clm,
                        channel:this.form.system[1],
                        client:client,
                        version:this.form.version
                    };
                    let headers = {
                        "Content-Type": "application/json"
                    };

                    download(headers,params).then(_data=>{
                        console.log(_data);
                        let{msg,code,data}=_data;
                        if(code ==='0'){
                            var mydata=data["url"];
                            this.$router.push(mydata);
                        }
                        else{
                            this.$message.error(msg);
                            return;
                        }
                        }
                        //请求正确时执行的代码
                        // var mydata=data;
                        // var json=JSON.stringify(tableData);
                        // this.tableData=JSON.parse(json);
                        // this.$message.location.href =(mydata);
                        // this.response.redirect(mydata);
                    );
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
            this.version=[];
            this.form.version='';
            var lan_bishijie=[
            {key:"v2.7.0",value:"v2.7.0"},
            {key:"v2.6.5",value:"v2.6.5"},
            {key:"v2.6.0",value:"v2.6.0"},
            {key:"v2.5.0",value:"v2.5.0"}];
            var lan_coniness=[
            {key:"v2.0.0",value:"v2.0.0"},
            {key:"v1.9.5",value:"v1.9.5"},
            {key:"v1.9.0",value:"v1.9.0"},
            {key:"v1.8.0",value:"v1.8.0"},
            {key:"v1.7.0",value:"v1.7.0"}];
              var type=this.form.system[0].toLowerCase();
              if(type=='bishijie'){
                 this.version=lan_bishijie;
              }else if(type=='coinness'){
                 this.version=lan_coniness;
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