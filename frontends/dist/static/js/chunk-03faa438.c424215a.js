(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-03faa438"],{"0d81":function(e,t,a){"use strict";a.r(t);var r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("div",{staticClass:"container"},[a("div",{staticClass:"form-box"},[a("el-form",{ref:"form",attrs:{model:e.form,"status-icon":"",rules:e.rules,"label-width":"80px"}},[a("el-form-item",{attrs:{label:"系统",prop:"system"}},[a("el-cascader",{attrs:{options:e.system},on:{change:function(t){return e.changeLang("form")}},model:{value:e.form.system,callback:function(t){e.$set(e.form,"system",t)},expression:"form.system"}})],1),a("el-form-item",{attrs:{label:"客户端",prop:"client"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.form.client,callback:function(t){e.$set(e.form,"client",t)},expression:"form.client"}},[a("el-option",{key:"Android",attrs:{label:"Android",value:"Android"}}),a("el-option",{key:"iOS",attrs:{label:"iOS",value:"iOS"}})],1)],1),a("el-form-item",{attrs:{label:"版本",prop:"version"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.form.version,callback:function(t){e.$set(e.form,"version",t)},expression:"form.version"}},e._l(e.version,(function(e,t){return a("el-option",{key:e.key,attrs:{label:e.value,value:e.key}})})),1)],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.onSubmit("form")}}},[e._v("下载")]),a("el-button",{on:{click:function(t){return e.resetForm("form")}}},[e._v("打包")])],1)],1)],1)])])},n=[],s=a("2d92"),o=navigator.userAgent,i=o.indexOf("Android")>-1||o.indexOf("Adr")>-1,l=!!o.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/);if(1==i);else if(1==l);else var u="a";var d={name:"baseform",data:function(){return{system:[{value:"bishijie",label:"Boimind",children:[{value:"Debug",label:"Debug"},{value:"Huidu",label:"Huidu"},{value:"Release",label:"Release"}]},{value:"coinness",label:"CoinNess",children:[{value:"Debug",label:"Debug"},{value:"Huidu",label:"Huidu"},{value:"Release",label:"Release"}]}],client:[{value:"Android",label:"Android"},{value:"iOS",label:"iOS"}],form:{system:"",system:[],version:[]},rules:{system:[{required:!0,message:"请选择客户端",trigger:"blur"}],version:[{required:!0,message:"下载版本",trigger:"blur"}]}}},methods:{onSubmit(e){this.$refs[e].validate(e=>{if(!e)return console.log("error submit"),!1;{var t=this.form.version;if("bishijie"===this.form.system[0])var a="CoinWorld";else a="CoinNess";if("a"===u)var r=this.form.client;if("undefined"==typeof t||null==t||""==t)return void alert("请选择版本");let e={system:a,channel:this.form.system[1],client:r,version:this.form.version},n={"Content-Type":"application/json"};Object(s["H"])(n,e).then(e=>{console.log(e);let{msg:t,code:a,data:r}=e;if("0"===a){var n=r["url"];this.$router.push(n)}else this.$message.error(t)})}})},resetForm(e){this.$refs[e].resetFields()},changeLang(e){this.version=[],this.form.version="";var t=[{key:"v2.7.0",value:"v2.7.0"},{key:"v2.6.5",value:"v2.6.5"},{key:"v2.6.0",value:"v2.6.0"},{key:"v2.5.0",value:"v2.5.0"}],a=[{key:"v2.0.0",value:"v2.0.0"},{key:"v1.9.5",value:"v1.9.5"},{key:"v1.9.0",value:"v1.9.0"},{key:"v1.8.0",value:"v1.8.0"},{key:"v1.7.0",value:"v1.7.0"}],r=this.form.system[0].toLowerCase();"bishijie"==r?this.version=t:"coinness"==r&&(this.version=a)}}},p=d,c=(a("3f55"),a("2877")),h=Object(c["a"])(p,r,n,!1,null,"3a535963",null);t["default"]=h.exports},"2d92":function(e,t,a){"use strict";a.d(t,"pb",(function(){return s})),a.d(t,"P",(function(){return o})),a.d(t,"u",(function(){return i})),a.d(t,"F",(function(){return l})),a.d(t,"J",(function(){return u})),a.d(t,"sb",(function(){return d})),a.d(t,"k",(function(){return p})),a.d(t,"Q",(function(){return c})),a.d(t,"O",(function(){return h})),a.d(t,"t",(function(){return m})),a.d(t,"E",(function(){return f})),a.d(t,"I",(function(){return b})),a.d(t,"rb",(function(){return v})),a.d(t,"j",(function(){return g})),a.d(t,"R",(function(){return y})),a.d(t,"S",(function(){return _})),a.d(t,"N",(function(){return k})),a.d(t,"s",(function(){return j})),a.d(t,"i",(function(){return D})),a.d(t,"T",(function(){return $})),a.d(t,"V",(function(){return x})),a.d(t,"U",(function(){return w})),a.d(t,"g",(function(){return C})),a.d(t,"M",(function(){return I})),a.d(t,"h",(function(){return O})),a.d(t,"qb",(function(){return S})),a.d(t,"r",(function(){return A})),a.d(t,"H",(function(){return q})),a.d(t,"lb",(function(){return F})),a.d(t,"tb",(function(){return L})),a.d(t,"l",(function(){return z})),a.d(t,"K",(function(){return H})),a.d(t,"y",(function(){return R})),a.d(t,"ib",(function(){return E})),a.d(t,"kb",(function(){return P})),a.d(t,"jb",(function(){return B})),a.d(t,"p",(function(){return J})),a.d(t,"wb",(function(){return N})),a.d(t,"A",(function(){return U})),a.d(t,"d",(function(){return M})),a.d(t,"nb",(function(){return T})),a.d(t,"e",(function(){return W})),a.d(t,"mb",(function(){return X})),a.d(t,"W",(function(){return G})),a.d(t,"ob",(function(){return K})),a.d(t,"v",(function(){return Q})),a.d(t,"ub",(function(){return V})),a.d(t,"n",(function(){return Y})),a.d(t,"D",(function(){return Z})),a.d(t,"Z",(function(){return ee})),a.d(t,"C",(function(){return te})),a.d(t,"w",(function(){return ae})),a.d(t,"hb",(function(){return re})),a.d(t,"gb",(function(){return ne})),a.d(t,"db",(function(){return se})),a.d(t,"z",(function(){return oe})),a.d(t,"ab",(function(){return ie})),a.d(t,"bb",(function(){return le})),a.d(t,"o",(function(){return ue})),a.d(t,"vb",(function(){return de})),a.d(t,"x",(function(){return pe})),a.d(t,"q",(function(){return ce})),a.d(t,"L",(function(){return he})),a.d(t,"G",(function(){return me})),a.d(t,"cb",(function(){return fe})),a.d(t,"eb",(function(){return be})),a.d(t,"fb",(function(){return ve})),a.d(t,"Y",(function(){return ge})),a.d(t,"X",(function(){return ye})),a.d(t,"m",(function(){return _e})),a.d(t,"f",(function(){return ke})),a.d(t,"c",(function(){return je})),a.d(t,"b",(function(){return De})),a.d(t,"a",(function(){return $e})),a.d(t,"B",(function(){return xe}));var r=a("bc3a"),n=a.n(r);a("c896");const s="http://192.168.1.121:9000",o=(e,t)=>n.a.get(s+"/api/project/project_list",{params:t,headers:e}).then(e=>e.data),i=(e,t)=>n.a.post(s+"/api/project/del_project",t,{headers:e}).then(e=>e.data),l=(e,t)=>n.a.post(s+"/api/project/disable_project",t,{headers:e}).then(e=>e.data),u=(e,t)=>n.a.post(s+"/api/project/enable_project",t,{headers:e}).then(e=>e.data),d=(e,t)=>n.a.post(s+"/api/project/update_project",t,{headers:e}).then(e=>e.data),p=(e,t)=>n.a.post(s+"/api/project/add_project",t,{headers:e}).then(e=>e.data),c=(e,t)=>n.a.get(s+"/api/title/project_info",{params:t,headers:e}).then(e=>e.data),h=(e,t)=>n.a.get(s+"/api/global/host_total",{params:t,headers:e}).then(e=>e.data),m=(e,t)=>n.a.post(s+"/api/global/del_host",t,{headers:e}).then(e=>e.data),f=(e,t)=>n.a.post(s+"/api/global/disable_host",t,{headers:e}).then(e=>e.data),b=(e,t)=>n.a.post(s+"/api/global/enable_host",t,{headers:e}).then(e=>e.data),v=(e,t)=>n.a.post(s+"/api/global/update_host",t,{headers:e}).then(e=>e.data),g=(e,t)=>n.a.post(s+"/api/global/add_host",t,{headers:e}).then(e=>e.data),y=(e,t)=>n.a.get(s+"/api/dynamic/dynamic",{params:t,headers:e}).then(e=>e.data),_=(e,t)=>n.a.get(s+"/api/member/project_member",{params:t,headers:e}).then(e=>e.data),k=(e,t)=>n.a.get(s+"/api/member/get_email",{params:t,headers:e}).then(e=>e.data),j=(e,t)=>n.a.post(s+"/api/member/del_email",t,{headers:e}).then(e=>e.data),D=(e,t)=>n.a.post(s+"/api/member/email_config",t,{headers:e}).then(e=>e.data),$=(e,t)=>n.a.get(s+"/api/report/auto_test_report",{params:t,headers:e}).then(e=>e.data),x=(e,t)=>n.a.get(s+"/api/report/test_time",{params:t,headers:e}).then(e=>e.data),w=(e,t)=>n.a.get(s+"/api/report/lately_ten",{params:t,headers:e}).then(e=>e.data),C=(e,t)=>n.a.post(s+"/api/api/add_api",t,{headers:e}).then(e=>e.data),I=(e,t)=>n.a.get(s+"/api/api/group",{params:t,headers:e}).then(e=>e.data),O=(e,t)=>n.a.post(s+"/api/api/add_group",t,{headers:e}).then(e=>e.data),S=(e,t)=>n.a.post(s+"/api/api/update_name_group",t,{headers:e}).then(e=>e.data),A=(e,t)=>n.a.post(s+"/api/api/del_group",t,{headers:e}).then(e=>e.data),q=(e,t)=>n.a.post(s+"/api/download",t,{headers:e}).then(e=>e.data),F=(e,t)=>n.a.post(s+"/api/user/login",t,e).then(e=>e.data),L=(e,t)=>n.a.post(s+"/api/risk/update",t,{headers:e}).then(e=>e.data),z=(e,t)=>n.a.post(s+"/api/risk/add",t,{headers:e}).then(e=>e.data),H=(e,t)=>n.a.post(s+"/api/risk/add",t,{headers:e}).then(e=>e.data),R=(e,t)=>n.a.post(s+"/api/risk/del",t,e).then(e=>e.data),E=(e,t)=>n.a.get(s+"/api/risk ",{params:t},e).then(e=>e.data),P=(e,t)=>n.a.get(s+"/api/todo ",{params:t},e).then(e=>e.data),B=(e,t)=>n.a.get(s+"/api/report ",{params:t},e).then(e=>e.data),J=(e,t)=>n.a.post(s+"/api/addreport",t,e).then(e=>e.data),N=(e,t)=>n.a.post(s+"/api/updatereport",t,e).then(e=>e.data),U=(e,t)=>n.a.post(s+"/api/delreport",t,e).then(e=>e.data),M=(e,t)=>n.a.post(s+"/api/send",t,e).then(e=>e.data),T=(e,t)=>n.a.get(s+"/api/stress/list",{params:t},{headers:e}).then(e=>e.data),W=(e,t)=>n.a.get(s+"/api/stress/stressDetail ",{params:t},e).then(e=>e.data),X=(e,t)=>n.a.post(s+"/api/stress/stresstool",t,e).then(e=>e.data),G=(e,t)=>n.a.get(s+"/api/stress/version",{params:t},{headers:e}).then(e=>e.data),K=(e,t)=>n.a.post(s+"/api/stress/stresssave",t,e).then(e=>e.data),Q=(e,t)=>n.a.post(s+"/api/tool/del_dicomData",t,e).then(e=>e.data),V=(e,t)=>n.a.post(s+"/api/tool/update_dicomData",t,e).then(e=>e.data),Y=(e,t)=>n.a.post(s+"/api/tool/add_dicomData",t,e).then(e=>e.data),Z=(e,t)=>n.a.post(s+"/api/tool/dicomdetail",t,e).then(e=>e.data),ee=(e,t)=>n.a.get(s+"/api/tool/dicomData",{params:t},{headers:e}).then(e=>e.data),te=(e,t)=>n.a.post(s+"/api/tool/dicomcsv",t,e).then(e=>e.data),ae=(e,t)=>n.a.post(s+"/api/tool/delreport",t,e).then(e=>e.data),re=(e,t)=>n.a.get(s+"/api/stress/stressversion",{params:t},{headers:e}).then(e=>e.data),ne=(e,t)=>n.a.post(s+"/api/stress/stressresult",t,e).then(e=>e.data),se=(e,t)=>n.a.post(s+"/api/stress/stressfigure",t,e).then(e=>e.data),oe=(e,t)=>n.a.post(s+"/api/tool/delete_patients",t,e).then(e=>e.data),ie=(e,t)=>n.a.get(s+"/api/tool/getduration",{params:t},{headers:e}).then(e=>e.data),le=(e,t)=>n.a.get(s+"/api/tool/durationData",{params:t},{headers:e}).then(e=>e.data),ue=(e,t)=>n.a.post(s+"/api/tool/add_duration",t,e).then(e=>e.data),de=(e,t)=>n.a.post(s+"/api/tool/update_duration",t,e).then(e=>e.data),pe=(e,t)=>n.a.post(s+"/api/tool/del_duration",t,e).then(e=>e.data),ce=(e,t)=>n.a.post(s+"/api/tool/anonymization",t,e).then(e=>e.data),he=(e,t)=>n.a.post(s+"/api/tool/enable_duration",t,e).then(e=>e.data),me=(e,t)=>n.a.post(s+"/api/tool/disable_duration",t,e).then(e=>e.data),fe=(e,t)=>n.a.get(s+"/api/tool/duration_verify",{params:t},{headers:e}).then(e=>e.data),be=(e,t)=>n.a.get(s+"/api/tool/somkerecord",{params:t},{headers:e}).then(e=>e.data),ve=(e,t)=>n.a.post(s+"/api/tool/somke",t,e).then(e=>e.data),ge=(e,t)=>n.a.post(s+"/api/tool/dicomSend",t,e).then(e=>e.data),ye=(e,t)=>n.a.get(s+"/api/base/getdata",{params:t},{headers:e}).then(e=>e.data),_e=(e,t)=>n.a.post(s+"/api/base/addData",t,e).then(e=>e.data),ke=(e,t)=>n.a.post(s+"/api/base/updateData",t,e).then(e=>e.data),je=(e,t)=>n.a.post(s+"/api/base/enablebase",t,e).then(e=>e.data),De=(e,t)=>n.a.post(s+"/api/base/disablebase",t,e).then(e=>e.data),$e=(e,t)=>n.a.post(s+"/api/base/delbasedata",t,e).then(e=>e.data),xe=(e,t)=>n.a.get(s+"/api/base/dicom",{params:t},{headers:e}).then(e=>e.data)},"3f55":function(e,t,a){"use strict";var r=a("5e99"),n=a.n(r);n.a},"41d3":function(e,t,a){},"5e99":function(e,t,a){},c896:function(e,t,a){"use strict";var r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("div",{staticClass:"crumbs"},[a("el-breadcrumb",{attrs:{separator:"/"}},[a("el-breadcrumb-item",[a("i",{staticClass:"el-icon-lx-calendar"}),e._v(" 测试工具")]),a("el-breadcrumb-item",[e._v("推送工具")])],1)],1),a("div",{staticClass:"container"},[a("div",{staticClass:"form-box"},[a("el-form",{ref:"form",attrs:{model:e.form,"status-icon":"",rules:e.rules,"label-width":"80px"}},[a("el-form-item",{attrs:{label:"推送ID",prop:"pushID"}},[a("el-col",{attrs:{span:10}},[a("el-input",{attrs:{id:"pushID"},model:{value:e.form.pushID,callback:function(t){e.$set(e.form,"pushID",t)},expression:"form.pushID"}})],1)],1),a("el-form-item",{attrs:{label:"推送环境",prop:"environment"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.form.environment,callback:function(t){e.$set(e.form,"environment",t)},expression:"form.environment"}},[a("el-option",{key:"test",attrs:{label:"测试环境",value:"test"}}),a("el-option",{key:"online",attrs:{label:"线上环境",value:"online"}})],1)],1),a("el-form-item",{attrs:{label:"推送类型",prop:"types"}},[a("el-cascader",{attrs:{options:e.types},on:{change:function(t){return e.changeLang("form")}},model:{value:e.form.types,callback:function(t){e.$set(e.form,"types",t)},expression:"form.types"}})],1),a("el-form-item",{attrs:{label:"选择语言",prop:"languages"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.form.languages,callback:function(t){e.$set(e.form,"languages",t)},expression:"form.languages"}},e._l(e.languages,(function(e,t){return a("el-option",{key:e.key,attrs:{label:e.value,value:e.key}})})),1)],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.onSubmit("form")}}},[e._v("确定推送")]),a("el-button",{on:{click:function(t){return e.resetForm("form")}}},[e._v("重置")])],1)],1)],1)])])},n=[],s={name:"baseform",data:function(){return{types:[{value:"bishijie",label:"Boimind",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"replay",label:"币圈"},{value:"monitor",label:"盯盘"}]},{value:"coinness",label:"coinness",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"monitor",label:"盯盘"}]}],languages:[],form:{pushID:"",environment:"",types:[],languages:[]},rules:{pushID:[{required:!0,message:"请输入推送ID",trigger:"blur"}],environment:[{required:!0,message:"请选择推送环境",trigger:"blur"}],types:[{required:!0,message:"请选择推送类型",trigger:"blur"}],languages:[{required:!0,message:"请选择语言",trigger:"blur"}]}}},methods:{onSubmit(e){this.$refs[e].validate(e=>{if(!e)return console.log("error submit"),!1;console.log("语言："+this.form.languages),console.log("pushID："+this.form.pushID),console.log("APP："+this.form.types[0]),console.log("推送类型："+this.form.types[1]),console.log("environment："+this.form.environment),this.$ajax.post("/bishijie/push",{id:this.form.pushID,service:this.form.environment,system:this.form.types[0],module:this.form.types[1],lang:this.form.languages,rid:""}).then(e=>{"0"==e.data.code?null==e.data.data||e.data.data[0]?this.$message.success("push成功！"):this.$message.error(e.data.data[1]):this.$message.error(e.data.msg)}).catch((function(e){console.log(e)}))})},resetForm(e){this.$refs[e].resetFields()},changeLang(e){this.languages=[],this.form.languages="";var t=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"}],a=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"},{key:"en_go",value:"English"},{key:"ko_kr",value:"한글"}],r=this.form.types[0].toLowerCase();"bishijie"==r?this.languages=t:"coinness"==r&&(this.languages=a)}}},o=s,i=(a("cd97"),a("2877")),l=Object(i["a"])(o,r,n,!1,null,"6d8efc95",null);l.exports},cd97:function(e,t,a){"use strict";var r=a("41d3"),n=a.n(r);n.a}}]);