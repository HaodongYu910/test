(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-87c01ff4"],{"2d92":function(t,e,a){"use strict";a.d(e,"qb",(function(){return r})),a.d(e,"Q",(function(){return i})),a.d(e,"v",(function(){return o})),a.d(e,"G",(function(){return d})),a.d(e,"K",(function(){return l})),a.d(e,"tb",(function(){return u})),a.d(e,"k",(function(){return c})),a.d(e,"R",(function(){return p})),a.d(e,"P",(function(){return m})),a.d(e,"u",(function(){return h})),a.d(e,"F",(function(){return g})),a.d(e,"J",(function(){return f})),a.d(e,"sb",(function(){return b})),a.d(e,"j",(function(){return v})),a.d(e,"S",(function(){return y})),a.d(e,"T",(function(){return _})),a.d(e,"O",(function(){return k})),a.d(e,"t",(function(){return S})),a.d(e,"i",(function(){return w})),a.d(e,"U",(function(){return $})),a.d(e,"W",(function(){return j})),a.d(e,"V",(function(){return x})),a.d(e,"g",(function(){return F})),a.d(e,"N",(function(){return O})),a.d(e,"h",(function(){return D})),a.d(e,"rb",(function(){return I})),a.d(e,"s",(function(){return L})),a.d(e,"I",(function(){return C})),a.d(e,"mb",(function(){return T})),a.d(e,"ub",(function(){return z})),a.d(e,"l",(function(){return J})),a.d(e,"L",(function(){return N})),a.d(e,"z",(function(){return A})),a.d(e,"jb",(function(){return E})),a.d(e,"lb",(function(){return q})),a.d(e,"kb",(function(){return V})),a.d(e,"q",(function(){return P})),a.d(e,"xb",(function(){return B})),a.d(e,"B",(function(){return R})),a.d(e,"d",(function(){return G})),a.d(e,"ob",(function(){return Y})),a.d(e,"m",(function(){return H})),a.d(e,"e",(function(){return K})),a.d(e,"nb",(function(){return M})),a.d(e,"X",(function(){return Q})),a.d(e,"pb",(function(){return U})),a.d(e,"w",(function(){return W})),a.d(e,"vb",(function(){return X})),a.d(e,"o",(function(){return Z})),a.d(e,"E",(function(){return tt})),a.d(e,"ab",(function(){return et})),a.d(e,"D",(function(){return at})),a.d(e,"x",(function(){return st})),a.d(e,"ib",(function(){return nt})),a.d(e,"hb",(function(){return rt})),a.d(e,"eb",(function(){return it})),a.d(e,"A",(function(){return ot})),a.d(e,"bb",(function(){return dt})),a.d(e,"cb",(function(){return lt})),a.d(e,"p",(function(){return ut})),a.d(e,"wb",(function(){return ct})),a.d(e,"y",(function(){return pt})),a.d(e,"r",(function(){return mt})),a.d(e,"M",(function(){return ht})),a.d(e,"H",(function(){return gt})),a.d(e,"db",(function(){return ft})),a.d(e,"fb",(function(){return bt})),a.d(e,"gb",(function(){return vt})),a.d(e,"Z",(function(){return yt})),a.d(e,"Y",(function(){return _t})),a.d(e,"n",(function(){return kt})),a.d(e,"f",(function(){return St})),a.d(e,"c",(function(){return wt})),a.d(e,"b",(function(){return $t})),a.d(e,"a",(function(){return jt})),a.d(e,"C",(function(){return xt}));var s=a("bc3a"),n=a.n(s);a("c896");const r="http://192.168.1.121:9000",i=(t,e)=>n.a.get(r+"/api/project/project_list",{params:e,headers:t}).then(t=>t.data),o=(t,e)=>n.a.post(r+"/api/project/del_project",e,{headers:t}).then(t=>t.data),d=(t,e)=>n.a.post(r+"/api/project/disable_project",e,{headers:t}).then(t=>t.data),l=(t,e)=>n.a.post(r+"/api/project/enable_project",e,{headers:t}).then(t=>t.data),u=(t,e)=>n.a.post(r+"/api/project/update_project",e,{headers:t}).then(t=>t.data),c=(t,e)=>n.a.post(r+"/api/project/add_project",e,{headers:t}).then(t=>t.data),p=(t,e)=>n.a.get(r+"/api/title/project_info",{params:e,headers:t}).then(t=>t.data),m=(t,e)=>n.a.get(r+"/api/global/host_total",{params:e,headers:t}).then(t=>t.data),h=(t,e)=>n.a.post(r+"/api/global/del_host",e,{headers:t}).then(t=>t.data),g=(t,e)=>n.a.post(r+"/api/global/disable_host",e,{headers:t}).then(t=>t.data),f=(t,e)=>n.a.post(r+"/api/global/enable_host",e,{headers:t}).then(t=>t.data),b=(t,e)=>n.a.post(r+"/api/global/update_host",e,{headers:t}).then(t=>t.data),v=(t,e)=>n.a.post(r+"/api/global/add_host",e,{headers:t}).then(t=>t.data),y=(t,e)=>n.a.get(r+"/api/dynamic/dynamic",{params:e,headers:t}).then(t=>t.data),_=(t,e)=>n.a.get(r+"/api/member/project_member",{params:e,headers:t}).then(t=>t.data),k=(t,e)=>n.a.get(r+"/api/member/get_email",{params:e,headers:t}).then(t=>t.data),S=(t,e)=>n.a.post(r+"/api/member/del_email",e,{headers:t}).then(t=>t.data),w=(t,e)=>n.a.post(r+"/api/member/email_config",e,{headers:t}).then(t=>t.data),$=(t,e)=>n.a.get(r+"/api/report/auto_test_report",{params:e,headers:t}).then(t=>t.data),j=(t,e)=>n.a.get(r+"/api/report/test_time",{params:e,headers:t}).then(t=>t.data),x=(t,e)=>n.a.get(r+"/api/report/lately_ten",{params:e,headers:t}).then(t=>t.data),F=(t,e)=>n.a.post(r+"/api/api/add_api",e,{headers:t}).then(t=>t.data),O=(t,e)=>n.a.get(r+"/api/api/group",{params:e,headers:t}).then(t=>t.data),D=(t,e)=>n.a.post(r+"/api/api/add_group",e,{headers:t}).then(t=>t.data),I=(t,e)=>n.a.post(r+"/api/api/update_name_group",e,{headers:t}).then(t=>t.data),L=(t,e)=>n.a.post(r+"/api/api/del_group",e,{headers:t}).then(t=>t.data),C=(t,e)=>n.a.post(r+"/api/download",e,{headers:t}).then(t=>t.data),T=(t,e)=>n.a.post(r+"/api/user/login",e,t).then(t=>t.data),z=(t,e)=>n.a.post(r+"/api/risk/update",e,{headers:t}).then(t=>t.data),J=(t,e)=>n.a.post(r+"/api/risk/add",e,{headers:t}).then(t=>t.data),N=(t,e)=>n.a.post(r+"/api/risk/add",e,{headers:t}).then(t=>t.data),A=(t,e)=>n.a.post(r+"/api/risk/del",e,t).then(t=>t.data),E=(t,e)=>n.a.get(r+"/api/risk ",{params:e},t).then(t=>t.data),q=(t,e)=>n.a.get(r+"/api/todo ",{params:e},t).then(t=>t.data),V=(t,e)=>n.a.get(r+"/api/report ",{params:e},t).then(t=>t.data),P=(t,e)=>n.a.post(r+"/api/addreport",e,t).then(t=>t.data),B=(t,e)=>n.a.post(r+"/api/updatereport",e,t).then(t=>t.data),R=(t,e)=>n.a.post(r+"/api/delreport",e,t).then(t=>t.data),G=(t,e)=>n.a.post(r+"/api/send",e,t).then(t=>t.data),Y=(t,e)=>n.a.get(r+"/api/stress/list",{params:e},{headers:t}).then(t=>t.data),H=(t,e)=>n.a.post(r+"/api/stress/add",e,t).then(t=>t.data),K=(t,e)=>n.a.get(r+"/api/stress/stressDetail ",{params:e},t).then(t=>t.data),M=(t,e)=>n.a.post(r+"/api/stress/stresstool",e,t).then(t=>t.data),Q=(t,e)=>n.a.get(r+"/api/stress/version",{params:e},{headers:t}).then(t=>t.data),U=(t,e)=>n.a.post(r+"/api/stress/stresssave",e,t).then(t=>t.data),W=(t,e)=>n.a.post(r+"/api/tool/del_dicomData",e,t).then(t=>t.data),X=(t,e)=>n.a.post(r+"/api/dicom/update",e,t).then(t=>t.data),Z=(t,e)=>n.a.post(r+"/api/tool/add_dicomData",e,t).then(t=>t.data),tt=(t,e)=>n.a.post(r+"/api/tool/dicomdetail",e,t).then(t=>t.data),et=(t,e)=>n.a.get(r+"/api/tool/dicomData",{params:e},{headers:t}).then(t=>t.data),at=(t,e)=>n.a.post(r+"/api/tool/dicomcsv",e,t).then(t=>t.data),st=(t,e)=>n.a.post(r+"/api/tool/delreport",e,t).then(t=>t.data),nt=(t,e)=>n.a.get(r+"/api/stress/stressversion",{params:e},{headers:t}).then(t=>t.data),rt=(t,e)=>n.a.post(r+"/api/stress/stressresult",e,t).then(t=>t.data),it=(t,e)=>n.a.post(r+"/api/stress/stressfigure",e,t).then(t=>t.data),ot=(t,e)=>n.a.post(r+"/api/tool/delete_patients",e,t).then(t=>t.data),dt=(t,e)=>n.a.get(r+"/api/tool/getduration",{params:e},{headers:t}).then(t=>t.data),lt=(t,e)=>n.a.get(r+"/api/tool/durationData",{params:e},{headers:t}).then(t=>t.data),ut=(t,e)=>n.a.post(r+"/api/tool/add_duration",e,t).then(t=>t.data),ct=(t,e)=>n.a.post(r+"/api/tool/update_duration",e,t).then(t=>t.data),pt=(t,e)=>n.a.post(r+"/api/tool/del_duration",e,t).then(t=>t.data),mt=(t,e)=>n.a.post(r+"/api/tool/anonymization",e,t).then(t=>t.data),ht=(t,e)=>n.a.post(r+"/api/tool/enable_duration",e,t).then(t=>t.data),gt=(t,e)=>n.a.post(r+"/api/tool/disable_duration",e,t).then(t=>t.data),ft=(t,e)=>n.a.get(r+"/api/tool/duration_verify",{params:e},{headers:t}).then(t=>t.data),bt=(t,e)=>n.a.get(r+"/api/tool/somkerecord",{params:e},{headers:t}).then(t=>t.data),vt=(t,e)=>n.a.post(r+"/api/tool/somke",e,t).then(t=>t.data),yt=(t,e)=>n.a.post(r+"/api/tool/dicomSend",e,t).then(t=>t.data),_t=(t,e)=>n.a.get(r+"/api/base/getdata",{params:e},{headers:t}).then(t=>t.data),kt=(t,e)=>n.a.post(r+"/api/base/addData",e,t).then(t=>t.data),St=(t,e)=>n.a.post(r+"/api/base/updateData",e,t).then(t=>t.data),wt=(t,e)=>n.a.post(r+"/api/base/enablebase",e,t).then(t=>t.data),$t=(t,e)=>n.a.post(r+"/api/base/disablebase",e,t).then(t=>t.data),jt=(t,e)=>n.a.post(r+"/api/base/delbasedata",e,t).then(t=>t.data),xt=(t,e)=>n.a.get(r+"/api/base/dicom",{params:e},{headers:t}).then(t=>t.data)},"41d3":function(t,e,a){},5557:function(t,e,a){"use strict";var s=a("c18d"),n=a.n(s);n.a},c18d:function(t,e,a){},c896:function(t,e,a){"use strict";var s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("div",{staticClass:"crumbs"},[a("el-breadcrumb",{attrs:{separator:"/"}},[a("el-breadcrumb-item",[a("i",{staticClass:"el-icon-lx-calendar"}),t._v(" 测试工具")]),a("el-breadcrumb-item",[t._v("推送工具")])],1)],1),a("div",{staticClass:"container"},[a("div",{staticClass:"form-box"},[a("el-form",{ref:"form",attrs:{model:t.form,"status-icon":"",rules:t.rules,"label-width":"80px"}},[a("el-form-item",{attrs:{label:"推送ID",prop:"pushID"}},[a("el-col",{attrs:{span:10}},[a("el-input",{attrs:{id:"pushID"},model:{value:t.form.pushID,callback:function(e){t.$set(t.form,"pushID",e)},expression:"form.pushID"}})],1)],1),a("el-form-item",{attrs:{label:"推送环境",prop:"environment"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:t.form.environment,callback:function(e){t.$set(t.form,"environment",e)},expression:"form.environment"}},[a("el-option",{key:"test",attrs:{label:"测试环境",value:"test"}}),a("el-option",{key:"online",attrs:{label:"线上环境",value:"online"}})],1)],1),a("el-form-item",{attrs:{label:"推送类型",prop:"types"}},[a("el-cascader",{attrs:{options:t.types},on:{change:function(e){return t.changeLang("form")}},model:{value:t.form.types,callback:function(e){t.$set(t.form,"types",e)},expression:"form.types"}})],1),a("el-form-item",{attrs:{label:"选择语言",prop:"languages"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:t.form.languages,callback:function(e){t.$set(t.form,"languages",e)},expression:"form.languages"}},t._l(t.languages,(function(t,e){return a("el-option",{key:t.key,attrs:{label:t.value,value:t.key}})})),1)],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:function(e){return t.onSubmit("form")}}},[t._v("确定推送")]),a("el-button",{on:{click:function(e){return t.resetForm("form")}}},[t._v("重置")])],1)],1)],1)])])},n=[],r={name:"baseform",data:function(){return{types:[{value:"bishijie",label:"Boimind",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"replay",label:"币圈"},{value:"monitor",label:"盯盘"}]},{value:"coinness",label:"coinness",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"monitor",label:"盯盘"}]}],languages:[],form:{pushID:"",environment:"",types:[],languages:[]},rules:{pushID:[{required:!0,message:"请输入推送ID",trigger:"blur"}],environment:[{required:!0,message:"请选择推送环境",trigger:"blur"}],types:[{required:!0,message:"请选择推送类型",trigger:"blur"}],languages:[{required:!0,message:"请选择语言",trigger:"blur"}]}}},methods:{onSubmit(t){this.$refs[t].validate(t=>{if(!t)return console.log("error submit"),!1;console.log("语言："+this.form.languages),console.log("pushID："+this.form.pushID),console.log("APP："+this.form.types[0]),console.log("推送类型："+this.form.types[1]),console.log("environment："+this.form.environment),this.$ajax.post("/bishijie/push",{id:this.form.pushID,service:this.form.environment,system:this.form.types[0],module:this.form.types[1],lang:this.form.languages,rid:""}).then(t=>{"0"==t.data.code?null==t.data.data||t.data.data[0]?this.$message.success("push成功！"):this.$message.error(t.data.data[1]):this.$message.error(t.data.msg)}).catch((function(t){console.log(t)}))})},resetForm(t){this.$refs[t].resetFields()},changeLang(t){this.languages=[],this.form.languages="";var e=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"}],a=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"},{key:"en_go",value:"English"},{key:"ko_kr",value:"한글"}],s=this.form.types[0].toLowerCase();"bishijie"==s?this.languages=e:"coinness"==s&&(this.languages=a)}}},i=r,o=(a("cd97"),a("2877")),d=Object(o["a"])(i,s,n,!1,null,"6d8efc95",null);d.exports},cd97:function(t,e,a){"use strict";var s=a("41d3"),n=a.n(s);n.a},e7f2:function(t,e,a){"use strict";a.r(e);var s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"app-container"},[a("div",{staticClass:"filter-container"},[a("el-col",{staticClass:"toolbar",staticStyle:{"padding-bottom":"0px"},attrs:{span:20}},[a("el-form",{attrs:{inline:!0,model:t.filters},nativeOn:{submit:function(t){t.preventDefault()}}},[a("el-form-item",{attrs:{label:"服务器",prop:"server"}},[a("el-select",{attrs:{placeholder:"请选择服务"},nativeOn:{click:function(e){return t.gethost()}},model:{value:t.filters.server,callback:function(e){t.$set(t.filters,"server",e)},expression:"filters.server"}},t._l(t.tags,(function(t,e){return a("el-option",{key:t.host,attrs:{label:t.name,value:t.host}})})),1)],1),a("el-form-item",{attrs:{label:"版本"}},[a("el-input",{model:{value:t.filters.version,callback:function(e){t.$set(t.filters,"version",e)},expression:"filters.version"}})],1),a("el-form-item",[a("el-select",{attrs:{placeholder:"请选择病种类型"},nativeOn:{click:function(e){return t.getBase()}},model:{value:t.filters.diseases,callback:function(e){t.$set(t.filters,"diseases",e)},expression:"filters.diseases"}},t._l(t.tags,(function(t,e){return a("el-option",{key:t.remarks,attrs:{label:t.remarks,value:t.remarks}})})),1)],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:t.handleAdd}},[t._v("新增")])],1),a("el-form-item",[a("el-button",{attrs:{type:"warning"},on:{click:t.somketest}},[t._v("smoke测试")])],1),a("el-button",{attrs:{type:"danger",disabled:0===this.sels.length},on:{click:t.batchdel}},[t._v("删除报告")])],1)],1),a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.listLoading,expression:"listLoading"}],staticStyle:{width:"100%"},attrs:{data:t.stresslist,"highlight-current-row":""},on:{"selection-change":t.selsChange}},[a("el-table-column",{attrs:{prop:"ID",label:"ID","min-width":"4%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.id))])]}}])}),a("el-table-column",{attrs:{prop:"version",label:"版本","min-width":"8%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.version))])]}}])}),a("el-table-column",{attrs:{prop:"patientid",label:"Patientid","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.patientid))])]}}])}),a("el-table-column",{attrs:{prop:"studyinstanceuid",label:"Studyinstanceuid","min-width":"25%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.studyinstanceuid))])]}}])}),a("el-table-column",{attrs:{label:"预测时间","min-width":"8%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.time))])]}}])}),a("el-table-column",{attrs:{label:"slicenumber","min-width":"8%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.slicenumber))])]}}])}),a("el-table-column",{attrs:{label:"预测张数","min-width":"5%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.imagecount))])]}}])}),a("el-table-column",{attrs:{label:"标准","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{class:t.valuestatus(e.row.report),staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.diagnosis))])]}}])}),a("el-table-column",{attrs:{label:"实际","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{class:t.valuestatus(e.row.report),staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.aidiagnosis))])]}}])}),a("el-table-column",{attrs:{label:"结果","min-width":"8%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{class:t.valuestatus(e.row.report),staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.report))])]}}])}),a("el-table-column",{attrs:{label:"操作","min-width":"8px"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("el-button",{attrs:{type:"warning",size:"small"},on:{click:function(a){return t.handleEdit(e.$index,e.row)}}},[t._v("重测")])]}}])})],1),a("el-col",{staticClass:"toolbar",attrs:{span:24}},[a("el-pagination",{staticStyle:{float:"right"},attrs:{layout:"prev, pager, next","page-size":20,"page-count":t.total},on:{"current-change":t.handleCurrentChange}})],1)],1)])},n=[],r=a("2d92"),i={data(){return{filters:{diseases:null,slicenumber:null},total:0,page:1,listLoading:!1,sels:[],addForm:{diseases:"",server:"192.168.1.208",studyinstanceuid:""},addFormVisible:!1,addLoading:!1,addFormRules:{diseases:[{required:!0,message:"请输入名称",trigger:"blur"},{min:1,max:50,message:"长度在 1 到 50 个字符",trigger:"blur"}]}}},mounted(){this.getdata(),this.gethost()},methods:{valuestatus:function(t){return"匹配成功"===t?"statuscssb":"statuscssa"},gethost(){this.listLoading=!0;const t=this,e={},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(r["P"])(a,e).then(e=>{t.listLoading=!1;const{msg:a,code:s,data:n}=e;if("0"===s){t.total=n.total,t.list=n.data;var r=JSON.stringify(t.list);this.tags=JSON.parse(r)}else t.$message.error({message:a,center:!0})})},getBase(){this.listLoading=!0;const t=this,e={selecttype:"dicom",status:1},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(r["Y"])(a,e).then(e=>{t.listLoading=!1;const{msg:a,code:s,data:n}=e;if("0"===s){t.total=n.total,t.list=n.data;var r=JSON.stringify(t.list);this.tags=JSON.parse(r)}else t.$message.error({message:a,center:!0})})},somketest(){this.listLoading=!0;const t=this,e={server_ip:t.filters.server,diseases:t.filters.diseases,version:t.filters.version},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(r["gb"])(a,e).then(e=>{t.listLoading=!1;const{msg:a,code:s,data:n}=e;"0"===s?t.stresslist=n.data:t.$message.error({message:a,center:!0})})},getdata(){this.listLoading=!0;const t=this,e={page:t.page,diseases:t.filters.diseases,server:t.filters.server,slicenumber:t.filters.slicenumber,type:"Gold"},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(r["fb"])(a,e).then(e=>{t.listLoading=!1;const{msg:a,code:s,data:n}=e;"0"===s?(t.total=n.total,t.page=n.page,t.stresslist=n.data):t.$message.error({message:a,center:!0})})},handleDel:function(t,e){this.$confirm("确认删除该记录吗?","提示",{type:"warning"}).then(()=>{this.listLoading=!0;const t=this,a={ids:[e.id]},s={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};deldicomdata(s,a).then(e=>{const{msg:a,code:s,data:n}=e;"0"===s?t.$message({message:"删除成功",center:!0,type:"success"}):t.$message.error({message:a,center:!0}),t.getdata()})})},handleCurrentChange(t){this.page=t,this.getdata()},handleEdit:function(t,e){this.editFormVisible=!0,this.editForm=Object.assign({},e)},handleAdd:function(){this.addFormVisible=!0,this.addForm={patientid:null,diseases:null,studyinstanceuid:null}},editSubmit:function(){const t=this;this.$refs.editForm.validate(e=>{e&&this.$confirm("确认提交吗？","提示",{}).then(()=>{t.editLoading=!0;const e={id:t.editForm.id,patientid:t.editForm.patientid,studyinstanceuid:t.editForm.studyinstanceuid,diseases:t.editForm.diseases,slicenumber:t.editForm.slicenumber,vote:t.editForm.vote},a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};updatedicomdata(a,e).then(e=>{const{msg:a,code:s,data:n}=e;t.editLoading=!1,"0"===s?(t.$message({message:"修改成功",center:!0,type:"success"}),t.$refs["editForm"].resetFields(),t.editFormVisible=!1,t.getdata()):t.$message.error({message:a,center:!0})})})})},addSubmit:function(){this.$refs.addForm.validate(t=>{if(t){const t=this;this.$confirm("确认提交吗？","提示",{}).then(()=>{t.addLoading=!0;const e=JSON.stringify({diseases:t.addForm.diseases,patientid:t.addForm.patientid,server:t.addForm.server,studyinstanceuid:t.addForm.studyinstanceuid}),a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};adddicomdata(a,e).then(e=>{const{msg:a,code:s,data:n}=e;t.addLoading=!1,"0"===s?(t.$message({message:"添加成功",center:!0,type:"success"}),t.$refs["addForm"].resetFields(),t.addFormVisible=!1,t.getdata()):"999997"===s?t.$message.error({message:a,center:!0}):(t.$message.error({message:a,center:!0}),t.$refs["addForm"].resetFields(),t.addFormVisible=!1,t.getdata())})})}})},selsChange:function(t){this.sels=t},cancelEdit(t){t.title=t.originalTitle,t.edit=!1,this.$message({message:"The title has been restored to the original value",type:"warning"})},confirmEdit(t){t.edit=!1,t.originalTitle=t.title,this.$message({message:"The title has been edited",type:"success"})},batchRemove:function(){const t=this.sels.map(t=>t.id);this.$confirm("确认删除选中记录吗？","提示",{type:"warning"}).then(()=>{this.listLoading=!0;const e=this,a={ids:t},s={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};deldicomdata(s,a).then(t=>{const{msg:a,code:s,data:n}=t;"0"===s?e.$message({message:"删除成功",center:!0,type:"success"}):e.$message.error({message:a,center:!0}),e.getdata()})})},batchCsv:function(){const t=this.sels.map(t=>t.id);this.$confirm("确认生成选中记录吗？","提示",{type:"warning"}).then(()=>{this.listLoading=!0;const e=this,a={ids:t},s={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};dicomcsv(s,a).then(t=>{const{msg:a,code:s,data:n}=t;"0"===s?e.$message({message:"生成成功",center:!0,type:"success"}):e.$message.error({message:a,center:!0}),e.getdata()})})},batchDel:function(){const t=this.sels.map(t=>t.id);this.$confirm("确认删除选中记录的报告吗？","提示",{type:"warning"}).then(()=>{this.listLoading=!0;const e=this,a={ids:t},s={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(r["x"])(s,a).then(t=>{const{msg:a,code:s,data:n}=t;"0"===s?e.$message({message:"删除成功",center:!0,type:"success"}):e.$message.error({message:a,center:!0}),e.getdata()})})}}},o=i,d=(a("5557"),a("2877")),l=Object(d["a"])(o,s,n,!1,null,"c167262c",null);e["default"]=l.exports}}]);