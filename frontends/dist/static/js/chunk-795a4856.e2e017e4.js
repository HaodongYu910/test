(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-795a4856"],{"0d81":function(e,t,a){"use strict";a.r(t);var n=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("div",{staticClass:"container"},[a("div",{staticClass:"form-box"},[a("el-form",{ref:"form",attrs:{model:e.form,"status-icon":"",rules:e.rules,"label-width":"80px"}},[a("el-form-item",{attrs:{label:"系统",prop:"system"}},[a("el-cascader",{attrs:{options:e.system},on:{change:function(t){return e.changeLang("form")}},model:{value:e.form.system,callback:function(t){e.$set(e.form,"system",t)},expression:"form.system"}})],1),a("el-form-item",{attrs:{label:"客户端",prop:"client"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.form.client,callback:function(t){e.$set(e.form,"client",t)},expression:"form.client"}},[a("el-option",{key:"Android",attrs:{label:"Android",value:"Android"}}),a("el-option",{key:"iOS",attrs:{label:"iOS",value:"iOS"}})],1)],1),a("el-form-item",{attrs:{label:"版本",prop:"version"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.form.version,callback:function(t){e.$set(e.form,"version",t)},expression:"form.version"}},e._l(e.version,(function(e,t){return a("el-option",{key:e.key,attrs:{label:e.value,value:e.key}})})),1)],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.onSubmit("form")}}},[e._v("下载")]),a("el-button",{on:{click:function(t){return e.resetForm("form")}}},[e._v("打包")])],1)],1)],1)])])},r=[],o=a("2d92"),i=navigator.userAgent,s=i.indexOf("Android")>-1||i.indexOf("Adr")>-1,d=!!i.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/);if(1==s);else if(1==d);else var u="a";var l={name:"baseform",data:function(){return{system:[{value:"bishijie",label:"Boimind",children:[{value:"Debug",label:"Debug"},{value:"Huidu",label:"Huidu"},{value:"Release",label:"Release"}]},{value:"coinness",label:"CoinNess",children:[{value:"Debug",label:"Debug"},{value:"Huidu",label:"Huidu"},{value:"Release",label:"Release"}]}],client:[{value:"Android",label:"Android"},{value:"iOS",label:"iOS"}],form:{system:"",system:[],version:[]},rules:{system:[{required:!0,message:"请选择客户端",trigger:"blur"}],version:[{required:!0,message:"下载版本",trigger:"blur"}]}}},methods:{onSubmit(e){this.$refs[e].validate(e=>{if(!e)return console.log("error submit"),!1;{var t=this.form.version;if("bishijie"===this.form.system[0])var a="CoinWorld";else a="CoinNess";if("a"===u)var n=this.form.client;if("undefined"==typeof t||null==t||""==t)return void alert("请选择版本");let e={system:a,channel:this.form.system[1],client:n,version:this.form.version},r={"Content-Type":"application/json"};Object(o["B"])(r,e).then(e=>{console.log(e);let{msg:t,code:a,data:n}=e;if("0"===a){var r=n["url"];this.$router.push(r)}else this.$message.error(t)})}})},resetForm(e){this.$refs[e].resetFields()},changeLang(e){this.version=[],this.form.version="";var t=[{key:"v2.7.0",value:"v2.7.0"},{key:"v2.6.5",value:"v2.6.5"},{key:"v2.6.0",value:"v2.6.0"},{key:"v2.5.0",value:"v2.5.0"}],a=[{key:"v2.0.0",value:"v2.0.0"},{key:"v1.9.5",value:"v1.9.5"},{key:"v1.9.0",value:"v1.9.0"},{key:"v1.8.0",value:"v1.8.0"},{key:"v1.7.0",value:"v1.7.0"}],n=this.form.system[0].toLowerCase();"bishijie"==n?this.version=t:"coinness"==n&&(this.version=a)}}},p=l,c=(a("3f55"),a("2877")),h=Object(c["a"])(p,n,r,!1,null,"3a535963",null);t["default"]=h.exports},"2d92":function(e,t,a){"use strict";a.d(t,"fb",(function(){return o})),a.d(t,"J",(function(){return i})),a.d(t,"s",(function(){return s})),a.d(t,"z",(function(){return d})),a.d(t,"D",(function(){return u})),a.d(t,"ib",(function(){return l})),a.d(t,"j",(function(){return p})),a.d(t,"K",(function(){return c})),a.d(t,"I",(function(){return h})),a.d(t,"r",(function(){return f})),a.d(t,"y",(function(){return m})),a.d(t,"C",(function(){return b})),a.d(t,"hb",(function(){return v})),a.d(t,"i",(function(){return g})),a.d(t,"L",(function(){return _})),a.d(t,"M",(function(){return y})),a.d(t,"H",(function(){return k})),a.d(t,"q",(function(){return j})),a.d(t,"h",(function(){return O})),a.d(t,"N",(function(){return w})),a.d(t,"P",(function(){return x})),a.d(t,"O",(function(){return A})),a.d(t,"f",(function(){return C})),a.d(t,"G",(function(){return S})),a.d(t,"g",(function(){return D})),a.d(t,"gb",(function(){return $})),a.d(t,"p",(function(){return H})),a.d(t,"B",(function(){return R})),a.d(t,"db",(function(){return F})),a.d(t,"jb",(function(){return L})),a.d(t,"k",(function(){return q})),a.d(t,"E",(function(){return B})),a.d(t,"u",(function(){return J})),a.d(t,"ab",(function(){return N})),a.d(t,"Z",(function(){return U})),a.d(t,"cb",(function(){return E})),a.d(t,"bb",(function(){return M})),a.d(t,"n",(function(){return P})),a.d(t,"lb",(function(){return T})),a.d(t,"w",(function(){return W})),a.d(t,"d",(function(){return X})),a.d(t,"eb",(function(){return z})),a.d(t,"Q",(function(){return G})),a.d(t,"x",(function(){return I})),a.d(t,"mb",(function(){return K})),a.d(t,"o",(function(){return Q})),a.d(t,"Y",(function(){return V})),a.d(t,"W",(function(){return Y})),a.d(t,"X",(function(){return Z})),a.d(t,"V",(function(){return ee})),a.d(t,"v",(function(){return te})),a.d(t,"S",(function(){return ae})),a.d(t,"T",(function(){return ne})),a.d(t,"m",(function(){return re})),a.d(t,"kb",(function(){return oe})),a.d(t,"t",(function(){return ie})),a.d(t,"F",(function(){return se})),a.d(t,"A",(function(){return de})),a.d(t,"U",(function(){return ue})),a.d(t,"R",(function(){return le})),a.d(t,"l",(function(){return pe})),a.d(t,"e",(function(){return ce})),a.d(t,"c",(function(){return he})),a.d(t,"b",(function(){return fe})),a.d(t,"a",(function(){return me}));var n=a("bc3a"),r=a.n(n);const o="http://192.168.2.38:9000",i=(e,t)=>r.a.get(o+"/api/project/project_list",{params:t,headers:e}).then(e=>e.data),s=(e,t)=>r.a.post(o+"/api/project/del_project",t,{headers:e}).then(e=>e.data),d=(e,t)=>r.a.post(o+"/api/project/disable_project",t,{headers:e}).then(e=>e.data),u=(e,t)=>r.a.post(o+"/api/project/enable_project",t,{headers:e}).then(e=>e.data),l=(e,t)=>r.a.post(o+"/api/project/update_project",t,{headers:e}).then(e=>e.data),p=(e,t)=>r.a.post(o+"/api/project/add_project",t,{headers:e}).then(e=>e.data),c=(e,t)=>r.a.get(o+"/api/title/project_info",{params:t,headers:e}).then(e=>e.data),h=(e,t)=>r.a.get(o+"/api/global/host_total",{params:t,headers:e}).then(e=>e.data),f=(e,t)=>r.a.post(o+"/api/global/del_host",t,{headers:e}).then(e=>e.data),m=(e,t)=>r.a.post(o+"/api/global/disable_host",t,{headers:e}).then(e=>e.data),b=(e,t)=>r.a.post(o+"/api/global/enable_host",t,{headers:e}).then(e=>e.data),v=(e,t)=>r.a.post(o+"/api/global/update_host",t,{headers:e}).then(e=>e.data),g=(e,t)=>r.a.post(o+"/api/global/add_host",t,{headers:e}).then(e=>e.data),_=(e,t)=>r.a.get(o+"/api/dynamic/dynamic",{params:t,headers:e}).then(e=>e.data),y=(e,t)=>r.a.get(o+"/api/member/project_member",{params:t,headers:e}).then(e=>e.data),k=(e,t)=>r.a.get(o+"/api/member/get_email",{params:t,headers:e}).then(e=>e.data),j=(e,t)=>r.a.post(o+"/api/member/del_email",t,{headers:e}).then(e=>e.data),O=(e,t)=>r.a.post(o+"/api/member/email_config",t,{headers:e}).then(e=>e.data),w=(e,t)=>r.a.get(o+"/api/report/auto_test_report",{params:t,headers:e}).then(e=>e.data),x=(e,t)=>r.a.get(o+"/api/report/test_time",{params:t,headers:e}).then(e=>e.data),A=(e,t)=>r.a.get(o+"/api/report/lately_ten",{params:t,headers:e}).then(e=>e.data),C=(e,t)=>r.a.post(o+"/api/api/add_api",t,{headers:e}).then(e=>e.data),S=(e,t)=>r.a.get(o+"/api/api/group",{params:t,headers:e}).then(e=>e.data),D=(e,t)=>r.a.post(o+"/api/api/add_group",t,{headers:e}).then(e=>e.data),$=(e,t)=>r.a.post(o+"/api/api/update_name_group",t,{headers:e}).then(e=>e.data),H=(e,t)=>r.a.post(o+"/api/api/del_group",t,{headers:e}).then(e=>e.data),R=(e,t)=>r.a.post(o+"/api/download",t,{headers:e}).then(e=>e.data),F=(e,t)=>r.a.post(o+"/api/user/login",t,e).then(e=>e.data),L=(e,t)=>r.a.post(o+"/api/risk/update",t,{headers:e}).then(e=>e.data),q=(e,t)=>r.a.post(o+"/api/risk/add",t,{headers:e}).then(e=>e.data),B=(e,t)=>r.a.post(o+"/api/risk/add",t,{headers:e}).then(e=>e.data),J=(e,t)=>r.a.post(o+"/api/risk/del",t,e).then(e=>e.data),N=(e,t)=>r.a.get(o+"/api/risk ",{params:t},e).then(e=>e.data),U=(e,t)=>r.a.post(o+"/api/jira/figure ",t,e).then(e=>e.data),E=(e,t)=>r.a.get(o+"/api/todo ",{params:t},e).then(e=>e.data),M=(e,t)=>r.a.get(o+"/api/report ",{params:t},e).then(e=>e.data),P=(e,t)=>r.a.post(o+"/api/addreport",t,e).then(e=>e.data),T=(e,t)=>r.a.post(o+"/api/updatereport",t,e).then(e=>e.data),W=(e,t)=>r.a.post(o+"/api/delreport",t,e).then(e=>e.data),X=(e,t)=>r.a.post(o+"/api/send",t,e).then(e=>e.data),z=(e,t)=>r.a.post(o+"/api/tool/stresstool",t,e).then(e=>e.data),G=(e,t)=>r.a.get(o+"/api/tool/version",{params:t},{headers:e}).then(e=>e.data),I=(e,t)=>r.a.post(o+"/api/tool/del_stressdata",t,e).then(e=>e.data),K=(e,t)=>r.a.post(o+"/api/tool/update_stressdata",t,e).then(e=>e.data),Q=(e,t)=>r.a.post(o+"/api/tool/add_stressdata",t,e).then(e=>e.data),V=(e,t)=>r.a.get(o+"/api/tool/stressversion",{params:t},{headers:e}).then(e=>e.data),Y=(e,t)=>r.a.get(o+"/api/tool/stressdata",{params:t},{headers:e}).then(e=>e.data),Z=(e,t)=>r.a.post(o+"/api/tool/stressresult",t,e).then(e=>e.data),ee=(e,t)=>r.a.post(o+"/api/tool/stressfigure",t,e).then(e=>e.data),te=(e,t)=>r.a.post(o+"/api/tool/delete_patients",t,e).then(e=>e.data),ae=(e,t)=>r.a.get(o+"/api/tool/getduration",{params:t},{headers:e}).then(e=>e.data),ne=(e,t)=>r.a.get(o+"/api/tool/durationData",{params:t},{headers:e}).then(e=>e.data),re=(e,t)=>r.a.post(o+"/api/tool/add_duration",t,e).then(e=>e.data),oe=(e,t)=>r.a.post(o+"/api/tool/update_duration",t,e).then(e=>e.data),ie=(e,t)=>r.a.post(o+"/api/tool/del_duration",t,e).then(e=>e.data),se=(e,t)=>r.a.post(o+"/api/tool/enable_duration",t,e).then(e=>e.data),de=(e,t)=>r.a.post(o+"/api/tool/disable_duration",t,e).then(e=>e.data),ue=(e,t)=>r.a.get(o+"/api/tool/duration_verify",{params:t},{headers:e}).then(e=>e.data),le=(e,t)=>r.a.get(o+"/api/base/getdata",{params:t},{headers:e}).then(e=>e.data),pe=(e,t)=>r.a.post(o+"/api/base/addData",t,e).then(e=>e.data),ce=(e,t)=>r.a.post(o+"/api/base/updateData",t,e).then(e=>e.data),he=(e,t)=>r.a.post(o+"/api/base/enablebase",t,e).then(e=>e.data),fe=(e,t)=>r.a.post(o+"/api/base/disablebase",t,e).then(e=>e.data),me=(e,t)=>r.a.post(o+"/api/base/delbasedata",t,e).then(e=>e.data)},"3f55":function(e,t,a){"use strict";var n=a("5e99"),r=a.n(n);r.a},"5e99":function(e,t,a){}}]);