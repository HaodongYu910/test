(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-8ea85048"],{"2d92":function(t,e,a){"use strict";a.d(e,"nb",(function(){return o})),a.d(e,"O",(function(){return s})),a.d(e,"t",(function(){return i})),a.d(e,"E",(function(){return d})),a.d(e,"I",(function(){return u})),a.d(e,"qb",(function(){return l})),a.d(e,"k",(function(){return p})),a.d(e,"P",(function(){return c})),a.d(e,"N",(function(){return h})),a.d(e,"s",(function(){return m})),a.d(e,"D",(function(){return f})),a.d(e,"H",(function(){return g})),a.d(e,"pb",(function(){return b})),a.d(e,"j",(function(){return v})),a.d(e,"Q",(function(){return _})),a.d(e,"R",(function(){return y})),a.d(e,"M",(function(){return k})),a.d(e,"r",(function(){return j})),a.d(e,"i",(function(){return D})),a.d(e,"S",(function(){return w})),a.d(e,"U",(function(){return I})),a.d(e,"T",(function(){return $})),a.d(e,"g",(function(){return x})),a.d(e,"L",(function(){return C})),a.d(e,"h",(function(){return L})),a.d(e,"ob",(function(){return S})),a.d(e,"q",(function(){return z})),a.d(e,"G",(function(){return q})),a.d(e,"kb",(function(){return O})),a.d(e,"rb",(function(){return P})),a.d(e,"l",(function(){return E})),a.d(e,"J",(function(){return F})),a.d(e,"x",(function(){return J})),a.d(e,"hb",(function(){return N})),a.d(e,"jb",(function(){return A})),a.d(e,"ib",(function(){return T})),a.d(e,"p",(function(){return B})),a.d(e,"ub",(function(){return Q})),a.d(e,"z",(function(){return U})),a.d(e,"d",(function(){return G})),a.d(e,"mb",(function(){return H})),a.d(e,"e",(function(){return K})),a.d(e,"lb",(function(){return M})),a.d(e,"V",(function(){return R})),a.d(e,"u",(function(){return V})),a.d(e,"sb",(function(){return W})),a.d(e,"n",(function(){return X})),a.d(e,"C",(function(){return Y})),a.d(e,"Y",(function(){return Z})),a.d(e,"B",(function(){return tt})),a.d(e,"v",(function(){return et})),a.d(e,"gb",(function(){return at})),a.d(e,"fb",(function(){return nt})),a.d(e,"cb",(function(){return rt})),a.d(e,"y",(function(){return ot})),a.d(e,"Z",(function(){return st})),a.d(e,"ab",(function(){return it})),a.d(e,"o",(function(){return dt})),a.d(e,"tb",(function(){return ut})),a.d(e,"w",(function(){return lt})),a.d(e,"K",(function(){return pt})),a.d(e,"F",(function(){return ct})),a.d(e,"bb",(function(){return ht})),a.d(e,"db",(function(){return mt})),a.d(e,"eb",(function(){return ft})),a.d(e,"X",(function(){return gt})),a.d(e,"W",(function(){return bt})),a.d(e,"m",(function(){return vt})),a.d(e,"f",(function(){return _t})),a.d(e,"c",(function(){return yt})),a.d(e,"b",(function(){return kt})),a.d(e,"a",(function(){return jt})),a.d(e,"A",(function(){return Dt}));var n=a("bc3a"),r=a.n(n);a("c896");const o="http://192.168.1.121:9000",s=(t,e)=>r.a.get(o+"/api/project/project_list",{params:e,headers:t}).then(t=>t.data),i=(t,e)=>r.a.post(o+"/api/project/del_project",e,{headers:t}).then(t=>t.data),d=(t,e)=>r.a.post(o+"/api/project/disable_project",e,{headers:t}).then(t=>t.data),u=(t,e)=>r.a.post(o+"/api/project/enable_project",e,{headers:t}).then(t=>t.data),l=(t,e)=>r.a.post(o+"/api/project/update_project",e,{headers:t}).then(t=>t.data),p=(t,e)=>r.a.post(o+"/api/project/add_project",e,{headers:t}).then(t=>t.data),c=(t,e)=>r.a.get(o+"/api/title/project_info",{params:e,headers:t}).then(t=>t.data),h=(t,e)=>r.a.get(o+"/api/global/host_total",{params:e,headers:t}).then(t=>t.data),m=(t,e)=>r.a.post(o+"/api/global/del_host",e,{headers:t}).then(t=>t.data),f=(t,e)=>r.a.post(o+"/api/global/disable_host",e,{headers:t}).then(t=>t.data),g=(t,e)=>r.a.post(o+"/api/global/enable_host",e,{headers:t}).then(t=>t.data),b=(t,e)=>r.a.post(o+"/api/global/update_host",e,{headers:t}).then(t=>t.data),v=(t,e)=>r.a.post(o+"/api/global/add_host",e,{headers:t}).then(t=>t.data),_=(t,e)=>r.a.get(o+"/api/dynamic/dynamic",{params:e,headers:t}).then(t=>t.data),y=(t,e)=>r.a.get(o+"/api/member/project_member",{params:e,headers:t}).then(t=>t.data),k=(t,e)=>r.a.get(o+"/api/member/get_email",{params:e,headers:t}).then(t=>t.data),j=(t,e)=>r.a.post(o+"/api/member/del_email",e,{headers:t}).then(t=>t.data),D=(t,e)=>r.a.post(o+"/api/member/email_config",e,{headers:t}).then(t=>t.data),w=(t,e)=>r.a.get(o+"/api/report/auto_test_report",{params:e,headers:t}).then(t=>t.data),I=(t,e)=>r.a.get(o+"/api/report/test_time",{params:e,headers:t}).then(t=>t.data),$=(t,e)=>r.a.get(o+"/api/report/lately_ten",{params:e,headers:t}).then(t=>t.data),x=(t,e)=>r.a.post(o+"/api/api/add_api",e,{headers:t}).then(t=>t.data),C=(t,e)=>r.a.get(o+"/api/api/group",{params:e,headers:t}).then(t=>t.data),L=(t,e)=>r.a.post(o+"/api/api/add_group",e,{headers:t}).then(t=>t.data),S=(t,e)=>r.a.post(o+"/api/api/update_name_group",e,{headers:t}).then(t=>t.data),z=(t,e)=>r.a.post(o+"/api/api/del_group",e,{headers:t}).then(t=>t.data),q=(t,e)=>r.a.post(o+"/api/download",e,{headers:t}).then(t=>t.data),O=(t,e)=>r.a.post(o+"/api/user/login",e,t).then(t=>t.data),P=(t,e)=>r.a.post(o+"/api/risk/update",e,{headers:t}).then(t=>t.data),E=(t,e)=>r.a.post(o+"/api/risk/add",e,{headers:t}).then(t=>t.data),F=(t,e)=>r.a.post(o+"/api/risk/add",e,{headers:t}).then(t=>t.data),J=(t,e)=>r.a.post(o+"/api/risk/del",e,t).then(t=>t.data),N=(t,e)=>r.a.get(o+"/api/risk ",{params:e},t).then(t=>t.data),A=(t,e)=>r.a.get(o+"/api/todo ",{params:e},t).then(t=>t.data),T=(t,e)=>r.a.get(o+"/api/report ",{params:e},t).then(t=>t.data),B=(t,e)=>r.a.post(o+"/api/addreport",e,t).then(t=>t.data),Q=(t,e)=>r.a.post(o+"/api/updatereport",e,t).then(t=>t.data),U=(t,e)=>r.a.post(o+"/api/delreport",e,t).then(t=>t.data),G=(t,e)=>r.a.post(o+"/api/send",e,t).then(t=>t.data),H=(t,e)=>r.a.get(o+"/api/stress/list",{params:e},{headers:t}).then(t=>t.data),K=(t,e)=>r.a.get(o+"/api/stress/stressDetail ",{params:e},t).then(t=>t.data),M=(t,e)=>r.a.post(o+"/api/stress/stresstool",e,t).then(t=>t.data),R=(t,e)=>r.a.get(o+"/api/stress/version",{params:e},{headers:t}).then(t=>t.data),V=(t,e)=>r.a.post(o+"/api/tool/del_dicomData",e,t).then(t=>t.data),W=(t,e)=>r.a.post(o+"/api/tool/update_dicomData",e,t).then(t=>t.data),X=(t,e)=>r.a.post(o+"/api/tool/add_dicomData",e,t).then(t=>t.data),Y=(t,e)=>r.a.post(o+"/api/tool/dicomdetail",e,t).then(t=>t.data),Z=(t,e)=>r.a.get(o+"/api/tool/dicomData",{params:e},{headers:t}).then(t=>t.data),tt=(t,e)=>r.a.post(o+"/api/tool/dicomcsv",e,t).then(t=>t.data),et=(t,e)=>r.a.post(o+"/api/tool/delreport",e,t).then(t=>t.data),at=(t,e)=>r.a.get(o+"/api/stress/stressversion",{params:e},{headers:t}).then(t=>t.data),nt=(t,e)=>r.a.post(o+"/api/stress/stressresult",e,t).then(t=>t.data),rt=(t,e)=>r.a.post(o+"/api/stress/stressfigure",e,t).then(t=>t.data),ot=(t,e)=>r.a.post(o+"/api/tool/delete_patients",e,t).then(t=>t.data),st=(t,e)=>r.a.get(o+"/api/tool/getduration",{params:e},{headers:t}).then(t=>t.data),it=(t,e)=>r.a.get(o+"/api/tool/durationData",{params:e},{headers:t}).then(t=>t.data),dt=(t,e)=>r.a.post(o+"/api/tool/add_duration",e,t).then(t=>t.data),ut=(t,e)=>r.a.post(o+"/api/tool/update_duration",e,t).then(t=>t.data),lt=(t,e)=>r.a.post(o+"/api/tool/del_duration",e,t).then(t=>t.data),pt=(t,e)=>r.a.post(o+"/api/tool/enable_duration",e,t).then(t=>t.data),ct=(t,e)=>r.a.post(o+"/api/tool/disable_duration",e,t).then(t=>t.data),ht=(t,e)=>r.a.get(o+"/api/tool/duration_verify",{params:e},{headers:t}).then(t=>t.data),mt=(t,e)=>r.a.get(o+"/api/tool/somkerecord",{params:e},{headers:t}).then(t=>t.data),ft=(t,e)=>r.a.post(o+"/api/tool/somke",e,t).then(t=>t.data),gt=(t,e)=>r.a.post(o+"/api/tool/dicomSend",e,t).then(t=>t.data),bt=(t,e)=>r.a.get(o+"/api/base/getdata",{params:e},{headers:t}).then(t=>t.data),vt=(t,e)=>r.a.post(o+"/api/base/addData",e,t).then(t=>t.data),_t=(t,e)=>r.a.post(o+"/api/base/updateData",e,t).then(t=>t.data),yt=(t,e)=>r.a.post(o+"/api/base/enablebase",e,t).then(t=>t.data),kt=(t,e)=>r.a.post(o+"/api/base/disablebase",e,t).then(t=>t.data),jt=(t,e)=>r.a.post(o+"/api/base/delbasedata",e,t).then(t=>t.data),Dt=(t,e)=>r.a.get(o+"/api/base/dicom",{params:e},{headers:t}).then(t=>t.data)},"41d3":function(t,e,a){},"5d82":function(t,e,a){"use strict";a.r(e);var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("el-row",{staticClass:"dynamic-manage"},[a("el-col",{attrs:{span:24}},[a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.listLoading,expression:"listLoading"}],staticStyle:{width:"100%"},attrs:{data:t.tableData,stripe:""}},[a("el-table-column",{attrs:{prop:"time",label:"操作时间","min-width":"13%"}}),a("el-table-column",{attrs:{prop:"type",label:"类型","min-width":"10%"}}),a("el-table-column",{attrs:{prop:"operationObject",label:"操作对象","min-width":"15%"}}),a("el-table-column",{attrs:{prop:"operationUser",label:"操作人","min-width":"15%"}}),a("el-table-column",{attrs:{prop:"description",label:"描述","min-width":"47%"}})],1),a("el-pagination",{staticStyle:{float:"right"},attrs:{layout:"prev, pager, next","page-size":20,"page-count":t.total},on:{"current-change":t.handleCurrentChange}})],1)],1)},r=[],o=a("2d92"),s={data(){return{tableData:[],total:0,page:1,listLoading:!1}},methods:{handleCurrentChange(t){this.page=t,this.getProjectDynamic()},getProjectDynamic(){this.listLoading=!0;let t=this,e={project_id:Number(this.$route.params.project_id),page:t.page},a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["Q"])(a,e).then(e=>{let{msg:a,code:n,data:r}=e;t.listLoading=!1,"0"===n?(t.total=r.total,t.tableData=r.data):t.$message.error({message:a,center:!0})})}},mounted(){this.getProjectDynamic()}},i=s,d=(a("7023e"),a("2877")),u=Object(d["a"])(i,n,r,!1,null,"5b22c6f8",null);e["default"]=u.exports},"7023e":function(t,e,a){"use strict";var n=a("b34e"),r=a.n(n);r.a},b34e:function(t,e,a){},c896:function(t,e,a){"use strict";var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("div",{staticClass:"crumbs"},[a("el-breadcrumb",{attrs:{separator:"/"}},[a("el-breadcrumb-item",[a("i",{staticClass:"el-icon-lx-calendar"}),t._v(" 测试工具")]),a("el-breadcrumb-item",[t._v("推送工具")])],1)],1),a("div",{staticClass:"container"},[a("div",{staticClass:"form-box"},[a("el-form",{ref:"form",attrs:{model:t.form,"status-icon":"",rules:t.rules,"label-width":"80px"}},[a("el-form-item",{attrs:{label:"推送ID",prop:"pushID"}},[a("el-col",{attrs:{span:10}},[a("el-input",{attrs:{id:"pushID"},model:{value:t.form.pushID,callback:function(e){t.$set(t.form,"pushID",e)},expression:"form.pushID"}})],1)],1),a("el-form-item",{attrs:{label:"推送环境",prop:"environment"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:t.form.environment,callback:function(e){t.$set(t.form,"environment",e)},expression:"form.environment"}},[a("el-option",{key:"test",attrs:{label:"测试环境",value:"test"}}),a("el-option",{key:"online",attrs:{label:"线上环境",value:"online"}})],1)],1),a("el-form-item",{attrs:{label:"推送类型",prop:"types"}},[a("el-cascader",{attrs:{options:t.types},on:{change:function(e){return t.changeLang("form")}},model:{value:t.form.types,callback:function(e){t.$set(t.form,"types",e)},expression:"form.types"}})],1),a("el-form-item",{attrs:{label:"选择语言",prop:"languages"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:t.form.languages,callback:function(e){t.$set(t.form,"languages",e)},expression:"form.languages"}},t._l(t.languages,(function(t,e){return a("el-option",{key:t.key,attrs:{label:t.value,value:t.key}})})),1)],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:function(e){return t.onSubmit("form")}}},[t._v("确定推送")]),a("el-button",{on:{click:function(e){return t.resetForm("form")}}},[t._v("重置")])],1)],1)],1)])])},r=[],o={name:"baseform",data:function(){return{types:[{value:"bishijie",label:"Boimind",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"replay",label:"币圈"},{value:"monitor",label:"盯盘"}]},{value:"coinness",label:"coinness",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"monitor",label:"盯盘"}]}],languages:[],form:{pushID:"",environment:"",types:[],languages:[]},rules:{pushID:[{required:!0,message:"请输入推送ID",trigger:"blur"}],environment:[{required:!0,message:"请选择推送环境",trigger:"blur"}],types:[{required:!0,message:"请选择推送类型",trigger:"blur"}],languages:[{required:!0,message:"请选择语言",trigger:"blur"}]}}},methods:{onSubmit(t){this.$refs[t].validate(t=>{if(!t)return console.log("error submit"),!1;console.log("语言："+this.form.languages),console.log("pushID："+this.form.pushID),console.log("APP："+this.form.types[0]),console.log("推送类型："+this.form.types[1]),console.log("environment："+this.form.environment),this.$ajax.post("/bishijie/push",{id:this.form.pushID,service:this.form.environment,system:this.form.types[0],module:this.form.types[1],lang:this.form.languages,rid:""}).then(t=>{"0"==t.data.code?null==t.data.data||t.data.data[0]?this.$message.success("push成功！"):this.$message.error(t.data.data[1]):this.$message.error(t.data.msg)}).catch((function(t){console.log(t)}))})},resetForm(t){this.$refs[t].resetFields()},changeLang(t){this.languages=[],this.form.languages="";var e=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"}],a=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"},{key:"en_go",value:"English"},{key:"ko_kr",value:"한글"}],n=this.form.types[0].toLowerCase();"bishijie"==n?this.languages=e:"coinness"==n&&(this.languages=a)}}},s=o,i=(a("cd97"),a("2877")),d=Object(i["a"])(s,n,r,!1,null,"6d8efc95",null);d.exports},cd97:function(t,e,a){"use strict";var n=a("41d3"),r=a.n(n);r.a}}]);