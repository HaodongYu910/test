(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-15b4a86a"],{"2d92":function(t,e,a){"use strict";a.d(e,"qb",(function(){return n})),a.d(e,"Q",(function(){return o})),a.d(e,"v",(function(){return i})),a.d(e,"G",(function(){return l})),a.d(e,"K",(function(){return d})),a.d(e,"tb",(function(){return c})),a.d(e,"k",(function(){return u})),a.d(e,"R",(function(){return p})),a.d(e,"P",(function(){return m})),a.d(e,"u",(function(){return h})),a.d(e,"F",(function(){return f})),a.d(e,"J",(function(){return g})),a.d(e,"sb",(function(){return b})),a.d(e,"j",(function(){return v})),a.d(e,"S",(function(){return y})),a.d(e,"T",(function(){return k})),a.d(e,"O",(function(){return _})),a.d(e,"t",(function(){return F})),a.d(e,"i",(function(){return w})),a.d(e,"U",(function(){return $})),a.d(e,"W",(function(){return S})),a.d(e,"V",(function(){return x})),a.d(e,"g",(function(){return j})),a.d(e,"N",(function(){return L})),a.d(e,"h",(function(){return O})),a.d(e,"rb",(function(){return C})),a.d(e,"s",(function(){return D})),a.d(e,"I",(function(){return I})),a.d(e,"mb",(function(){return z})),a.d(e,"ub",(function(){return N})),a.d(e,"l",(function(){return T})),a.d(e,"L",(function(){return J})),a.d(e,"z",(function(){return V})),a.d(e,"jb",(function(){return A})),a.d(e,"lb",(function(){return q})),a.d(e,"kb",(function(){return R})),a.d(e,"q",(function(){return E})),a.d(e,"xb",(function(){return G})),a.d(e,"B",(function(){return Y})),a.d(e,"d",(function(){return P})),a.d(e,"ob",(function(){return M})),a.d(e,"m",(function(){return B})),a.d(e,"e",(function(){return Z})),a.d(e,"nb",(function(){return H})),a.d(e,"X",(function(){return K})),a.d(e,"pb",(function(){return Q})),a.d(e,"w",(function(){return U})),a.d(e,"vb",(function(){return W})),a.d(e,"o",(function(){return X})),a.d(e,"E",(function(){return tt})),a.d(e,"ab",(function(){return et})),a.d(e,"D",(function(){return at})),a.d(e,"x",(function(){return st})),a.d(e,"ib",(function(){return rt})),a.d(e,"hb",(function(){return nt})),a.d(e,"eb",(function(){return ot})),a.d(e,"A",(function(){return it})),a.d(e,"bb",(function(){return lt})),a.d(e,"cb",(function(){return dt})),a.d(e,"p",(function(){return ct})),a.d(e,"wb",(function(){return ut})),a.d(e,"y",(function(){return pt})),a.d(e,"r",(function(){return mt})),a.d(e,"M",(function(){return ht})),a.d(e,"H",(function(){return ft})),a.d(e,"db",(function(){return gt})),a.d(e,"fb",(function(){return bt})),a.d(e,"gb",(function(){return vt})),a.d(e,"Z",(function(){return yt})),a.d(e,"Y",(function(){return kt})),a.d(e,"n",(function(){return _t})),a.d(e,"f",(function(){return Ft})),a.d(e,"c",(function(){return wt})),a.d(e,"b",(function(){return $t})),a.d(e,"a",(function(){return St})),a.d(e,"C",(function(){return xt}));var s=a("bc3a"),r=a.n(s);a("c896");const n="http://192.168.1.121:9000",o=(t,e)=>r.a.get(n+"/api/project/project_list",{params:e,headers:t}).then(t=>t.data),i=(t,e)=>r.a.post(n+"/api/project/del_project",e,{headers:t}).then(t=>t.data),l=(t,e)=>r.a.post(n+"/api/project/disable_project",e,{headers:t}).then(t=>t.data),d=(t,e)=>r.a.post(n+"/api/project/enable_project",e,{headers:t}).then(t=>t.data),c=(t,e)=>r.a.post(n+"/api/project/update_project",e,{headers:t}).then(t=>t.data),u=(t,e)=>r.a.post(n+"/api/project/add_project",e,{headers:t}).then(t=>t.data),p=(t,e)=>r.a.get(n+"/api/title/project_info",{params:e,headers:t}).then(t=>t.data),m=(t,e)=>r.a.get(n+"/api/global/host_total",{params:e,headers:t}).then(t=>t.data),h=(t,e)=>r.a.post(n+"/api/global/del_host",e,{headers:t}).then(t=>t.data),f=(t,e)=>r.a.post(n+"/api/global/disable_host",e,{headers:t}).then(t=>t.data),g=(t,e)=>r.a.post(n+"/api/global/enable_host",e,{headers:t}).then(t=>t.data),b=(t,e)=>r.a.post(n+"/api/global/update_host",e,{headers:t}).then(t=>t.data),v=(t,e)=>r.a.post(n+"/api/global/add_host",e,{headers:t}).then(t=>t.data),y=(t,e)=>r.a.get(n+"/api/dynamic/dynamic",{params:e,headers:t}).then(t=>t.data),k=(t,e)=>r.a.get(n+"/api/member/project_member",{params:e,headers:t}).then(t=>t.data),_=(t,e)=>r.a.get(n+"/api/member/get_email",{params:e,headers:t}).then(t=>t.data),F=(t,e)=>r.a.post(n+"/api/member/del_email",e,{headers:t}).then(t=>t.data),w=(t,e)=>r.a.post(n+"/api/member/email_config",e,{headers:t}).then(t=>t.data),$=(t,e)=>r.a.get(n+"/api/report/auto_test_report",{params:e,headers:t}).then(t=>t.data),S=(t,e)=>r.a.get(n+"/api/report/test_time",{params:e,headers:t}).then(t=>t.data),x=(t,e)=>r.a.get(n+"/api/report/lately_ten",{params:e,headers:t}).then(t=>t.data),j=(t,e)=>r.a.post(n+"/api/api/add_api",e,{headers:t}).then(t=>t.data),L=(t,e)=>r.a.get(n+"/api/api/group",{params:e,headers:t}).then(t=>t.data),O=(t,e)=>r.a.post(n+"/api/api/add_group",e,{headers:t}).then(t=>t.data),C=(t,e)=>r.a.post(n+"/api/api/update_name_group",e,{headers:t}).then(t=>t.data),D=(t,e)=>r.a.post(n+"/api/api/del_group",e,{headers:t}).then(t=>t.data),I=(t,e)=>r.a.post(n+"/api/download",e,{headers:t}).then(t=>t.data),z=(t,e)=>r.a.post(n+"/api/user/login",e,t).then(t=>t.data),N=(t,e)=>r.a.post(n+"/api/risk/update",e,{headers:t}).then(t=>t.data),T=(t,e)=>r.a.post(n+"/api/risk/add",e,{headers:t}).then(t=>t.data),J=(t,e)=>r.a.post(n+"/api/risk/add",e,{headers:t}).then(t=>t.data),V=(t,e)=>r.a.post(n+"/api/risk/del",e,t).then(t=>t.data),A=(t,e)=>r.a.get(n+"/api/risk ",{params:e},t).then(t=>t.data),q=(t,e)=>r.a.get(n+"/api/todo ",{params:e},t).then(t=>t.data),R=(t,e)=>r.a.get(n+"/api/report ",{params:e},t).then(t=>t.data),E=(t,e)=>r.a.post(n+"/api/addreport",e,t).then(t=>t.data),G=(t,e)=>r.a.post(n+"/api/updatereport",e,t).then(t=>t.data),Y=(t,e)=>r.a.post(n+"/api/delreport",e,t).then(t=>t.data),P=(t,e)=>r.a.post(n+"/api/send",e,t).then(t=>t.data),M=(t,e)=>r.a.get(n+"/api/stress/list",{params:e},{headers:t}).then(t=>t.data),B=(t,e)=>r.a.post(n+"/api/stress/add",e,t).then(t=>t.data),Z=(t,e)=>r.a.get(n+"/api/stress/stressDetail ",{params:e},t).then(t=>t.data),H=(t,e)=>r.a.post(n+"/api/stress/stresstool",e,t).then(t=>t.data),K=(t,e)=>r.a.get(n+"/api/stress/version",{params:e},{headers:t}).then(t=>t.data),Q=(t,e)=>r.a.post(n+"/api/stress/stresssave",e,t).then(t=>t.data),U=(t,e)=>r.a.post(n+"/api/tool/del_dicomData",e,t).then(t=>t.data),W=(t,e)=>r.a.post(n+"/api/dicom/update",e,t).then(t=>t.data),X=(t,e)=>r.a.post(n+"/api/tool/add_dicomData",e,t).then(t=>t.data),tt=(t,e)=>r.a.post(n+"/api/tool/dicomdetail",e,t).then(t=>t.data),et=(t,e)=>r.a.get(n+"/api/tool/dicomData",{params:e},{headers:t}).then(t=>t.data),at=(t,e)=>r.a.post(n+"/api/tool/dicomcsv",e,t).then(t=>t.data),st=(t,e)=>r.a.post(n+"/api/tool/delreport",e,t).then(t=>t.data),rt=(t,e)=>r.a.get(n+"/api/stress/stressversion",{params:e},{headers:t}).then(t=>t.data),nt=(t,e)=>r.a.post(n+"/api/stress/stressresult",e,t).then(t=>t.data),ot=(t,e)=>r.a.post(n+"/api/stress/stressfigure",e,t).then(t=>t.data),it=(t,e)=>r.a.post(n+"/api/tool/delete_patients",e,t).then(t=>t.data),lt=(t,e)=>r.a.get(n+"/api/tool/getduration",{params:e},{headers:t}).then(t=>t.data),dt=(t,e)=>r.a.get(n+"/api/tool/durationData",{params:e},{headers:t}).then(t=>t.data),ct=(t,e)=>r.a.post(n+"/api/tool/add_duration",e,t).then(t=>t.data),ut=(t,e)=>r.a.post(n+"/api/tool/update_duration",e,t).then(t=>t.data),pt=(t,e)=>r.a.post(n+"/api/tool/del_duration",e,t).then(t=>t.data),mt=(t,e)=>r.a.post(n+"/api/tool/anonymization",e,t).then(t=>t.data),ht=(t,e)=>r.a.post(n+"/api/tool/enable_duration",e,t).then(t=>t.data),ft=(t,e)=>r.a.post(n+"/api/tool/disable_duration",e,t).then(t=>t.data),gt=(t,e)=>r.a.get(n+"/api/tool/duration_verify",{params:e},{headers:t}).then(t=>t.data),bt=(t,e)=>r.a.get(n+"/api/tool/somkerecord",{params:e},{headers:t}).then(t=>t.data),vt=(t,e)=>r.a.post(n+"/api/tool/somke",e,t).then(t=>t.data),yt=(t,e)=>r.a.post(n+"/api/tool/dicomSend",e,t).then(t=>t.data),kt=(t,e)=>r.a.get(n+"/api/base/getdata",{params:e},{headers:t}).then(t=>t.data),_t=(t,e)=>r.a.post(n+"/api/base/addData",e,t).then(t=>t.data),Ft=(t,e)=>r.a.post(n+"/api/base/updateData",e,t).then(t=>t.data),wt=(t,e)=>r.a.post(n+"/api/base/enablebase",e,t).then(t=>t.data),$t=(t,e)=>r.a.post(n+"/api/base/disablebase",e,t).then(t=>t.data),St=(t,e)=>r.a.post(n+"/api/base/delbasedata",e,t).then(t=>t.data),xt=(t,e)=>r.a.get(n+"/api/base/dicom",{params:e},{headers:t}).then(t=>t.data)},"41d3":function(t,e,a){},c896:function(t,e,a){"use strict";var s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("div",{staticClass:"crumbs"},[a("el-breadcrumb",{attrs:{separator:"/"}},[a("el-breadcrumb-item",[a("i",{staticClass:"el-icon-lx-calendar"}),t._v(" 测试工具")]),a("el-breadcrumb-item",[t._v("推送工具")])],1)],1),a("div",{staticClass:"container"},[a("div",{staticClass:"form-box"},[a("el-form",{ref:"form",attrs:{model:t.form,"status-icon":"",rules:t.rules,"label-width":"80px"}},[a("el-form-item",{attrs:{label:"推送ID",prop:"pushID"}},[a("el-col",{attrs:{span:10}},[a("el-input",{attrs:{id:"pushID"},model:{value:t.form.pushID,callback:function(e){t.$set(t.form,"pushID",e)},expression:"form.pushID"}})],1)],1),a("el-form-item",{attrs:{label:"推送环境",prop:"environment"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:t.form.environment,callback:function(e){t.$set(t.form,"environment",e)},expression:"form.environment"}},[a("el-option",{key:"test",attrs:{label:"测试环境",value:"test"}}),a("el-option",{key:"online",attrs:{label:"线上环境",value:"online"}})],1)],1),a("el-form-item",{attrs:{label:"推送类型",prop:"types"}},[a("el-cascader",{attrs:{options:t.types},on:{change:function(e){return t.changeLang("form")}},model:{value:t.form.types,callback:function(e){t.$set(t.form,"types",e)},expression:"form.types"}})],1),a("el-form-item",{attrs:{label:"选择语言",prop:"languages"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:t.form.languages,callback:function(e){t.$set(t.form,"languages",e)},expression:"form.languages"}},t._l(t.languages,(function(t,e){return a("el-option",{key:t.key,attrs:{label:t.value,value:t.key}})})),1)],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:function(e){return t.onSubmit("form")}}},[t._v("确定推送")]),a("el-button",{on:{click:function(e){return t.resetForm("form")}}},[t._v("重置")])],1)],1)],1)])])},r=[],n={name:"baseform",data:function(){return{types:[{value:"bishijie",label:"Boimind",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"replay",label:"币圈"},{value:"monitor",label:"盯盘"}]},{value:"coinness",label:"coinness",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"monitor",label:"盯盘"}]}],languages:[],form:{pushID:"",environment:"",types:[],languages:[]},rules:{pushID:[{required:!0,message:"请输入推送ID",trigger:"blur"}],environment:[{required:!0,message:"请选择推送环境",trigger:"blur"}],types:[{required:!0,message:"请选择推送类型",trigger:"blur"}],languages:[{required:!0,message:"请选择语言",trigger:"blur"}]}}},methods:{onSubmit(t){this.$refs[t].validate(t=>{if(!t)return console.log("error submit"),!1;console.log("语言："+this.form.languages),console.log("pushID："+this.form.pushID),console.log("APP："+this.form.types[0]),console.log("推送类型："+this.form.types[1]),console.log("environment："+this.form.environment),this.$ajax.post("/bishijie/push",{id:this.form.pushID,service:this.form.environment,system:this.form.types[0],module:this.form.types[1],lang:this.form.languages,rid:""}).then(t=>{"0"==t.data.code?null==t.data.data||t.data.data[0]?this.$message.success("push成功！"):this.$message.error(t.data.data[1]):this.$message.error(t.data.msg)}).catch((function(t){console.log(t)}))})},resetForm(t){this.$refs[t].resetFields()},changeLang(t){this.languages=[],this.form.languages="";var e=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"}],a=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"},{key:"en_go",value:"English"},{key:"ko_kr",value:"한글"}],s=this.form.types[0].toLowerCase();"bishijie"==s?this.languages=e:"coinness"==s&&(this.languages=a)}}},o=n,i=(a("cd97"),a("2877")),l=Object(i["a"])(o,s,r,!1,null,"6d8efc95",null);l.exports},cb08:function(t,e,a){t.exports=a.p+"static/img/icon-no.233633bc.svg"},cd97:function(t,e,a){"use strict";var s=a("41d3"),r=a.n(s);r.a},d6fa:function(t,e,a){"use strict";a.r(e);var s=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("section",[s("el-col",{staticClass:"toolbar",staticStyle:{"padding-bottom":"0px"},attrs:{span:24}},[s("el-form",{attrs:{inline:!0,model:t.filters},nativeOn:{submit:function(t){t.preventDefault()}}},[s("el-form-item",{attrs:{label:"服务器",prop:"server"}},[s("el-select",{attrs:{placeholder:"请选择服务"},nativeOn:{click:function(e){return t.gethost()}},model:{value:t.filters.server,callback:function(e){t.$set(t.filters,"server",e)},expression:"filters.server"}},t._l(t.tags,(function(t,e){return s("el-option",{key:t.host,attrs:{label:t.name,value:t.host}})})),1)],1),s("el-form-item",[s("el-select",{attrs:{placeholder:"类型"},model:{value:t.filters.type,callback:function(e){t.$set(t.filters,"type",e)},expression:"filters.type"}},[s("el-option",{key:"test",attrs:{label:"test",value:"test"}}),s("el-option",{key:"Gold",attrs:{label:"Gold",value:"Gold"}})],1)],1),s("el-form-item",[s("el-select",{attrs:{placeholder:"请选择病种名称"},nativeOn:{click:function(e){return t.getbaseList()}},model:{value:t.filters.content,callback:function(e){t.$set(t.filters,"content",e)},expression:"filters.content"}},t._l(t.project,(function(t,e){return s("el-option",{key:t.remarks,attrs:{label:t.remarks,value:t.remarks}})})),1)],1),s("el-form-item",[s("el-button",{attrs:{type:"primary"},on:{click:t.getbaseList}},[t._v("查询")])],1),s("el-form-item",[s("el-button",{attrs:{type:"primary"},on:{click:t.handleAdd}},[t._v("新增")])],1),s("el-button",{attrs:{type:"warning",disabled:0===this.sels.length},on:{click:t.batchSend}},[t._v("发送数据")])],1)],1),s("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.listLoading,expression:"listLoading"}],staticStyle:{width:"100%"},attrs:{data:t.project,"highlight-current-row":""},on:{"selection-change":t.selsChange}},[s("el-table-column",{attrs:{type:"selection","min-width":"5%"}}),s("el-table-column",{attrs:{prop:"select_type",label:"ID","min-width":"6%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[s("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.id))])]}}])}),s("el-table-column",{attrs:{label:"名称","min-width":"16%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[s("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.remarks))])]}}])}),s("el-table-column",{attrs:{prop:"content",label:"路径","min-width":"25%"},scopedSlots:t._u([{key:"default",fn:function(e){return[s("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.content))])]}}])}),s("el-table-column",{attrs:{label:"模型","min-width":"16%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[s("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.predictor))])]}}])}),s("el-table-column",{attrs:{label:"类型","min-width":"16%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[s("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.type))])]}}])}),s("el-table-column",{attrs:{label:"数量","min-width":"16%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[s("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.other))])]}}])}),s("el-table-column",{attrs:{prop:"status",label:"状态","min-width":"9%"},scopedSlots:t._u([{key:"default",fn:function(t){return[s("img",{directives:[{name:"show",rawName:"v-show",value:t.row.status,expression:"scope.row.status"}],attrs:{src:a("e7a2")}}),s("img",{directives:[{name:"show",rawName:"v-show",value:!t.row.status,expression:"!scope.row.status"}],attrs:{src:a("cb08")}})]}}])}),s("el-table-column",{attrs:{label:"修改时间","min-width":"16%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[s("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(t._f("dateformat")(e.row.updatetime,"YYYY-MM-DD ")))])]}}])}),s("el-table-column",{attrs:{label:"操作","min-width":"50px"},scopedSlots:t._u([{key:"default",fn:function(e){return[s("el-button",{attrs:{size:"small"},on:{click:function(a){return t.handleEdit(e.$index,e.row)}}},[t._v("编辑")]),s("el-button",{attrs:{type:"danger",size:"small"},on:{click:function(a){return t.handlecount(e.$index,e.row)}}},[t._v("同步")]),s("el-button",{attrs:{type:"info",size:"small"},on:{click:function(a){return t.handleChangeStatus(e.$index,e.row)}}},[t._v(" "+t._s(!1===e.row.status?"启用":"禁用")+" ")])]}}])})],1),s("el-col",{staticClass:"toolbar",attrs:{span:24}},[s("el-button",{attrs:{type:"danger",disabled:0===this.sels.length},on:{click:t.batchRemove}},[t._v("批量删除")]),s("el-pagination",{staticStyle:{float:"right"},attrs:{layout:"prev, pager, next","page-size":20,"page-count":t.total},on:{"current-change":t.handleCurrentChange}})],1),s("el-dialog",{staticStyle:{width:"75%",left:"12.5%"},attrs:{title:"编辑",visible:t.editFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(e){t.editFormVisible=e}}},[s("el-form",{ref:"editForm",attrs:{model:t.editForm,"label-width":"80px",rules:t.editFormRules}},[s("el-form-item",{attrs:{label:"文件路径"}},[s("el-input",{model:{value:t.editForm.content,callback:function(e){t.$set(t.editForm,"content",e)},expression:"editForm.content"}})],1),s("el-row",{attrs:{gutter:24}},[s("el-col",{attrs:{span:12}},[s("el-form-item",{attrs:{label:"分类",prop:"type"}},[s("el-select",{attrs:{placeholder:"请选择","auto-complete":"off",disabled:!0},model:{value:t.editForm.type,callback:function(e){t.$set(t.editForm,"type",e)},expression:"editForm.type"}},t._l(t.options,(function(t){return s("el-option",{key:t.value,attrs:{label:t.label,value:t.value}})})),1)],1)],1),s("el-col",{attrs:{span:12}},[s("el-form-item",{attrs:{label:"类型"}},[s("el-input",{attrs:{disabled:!0,"auto-complete":"off"},model:{value:t.editForm.select_type,callback:function(e){t.$set(t.editForm,"select_type",e)},expression:"editForm.select_type"}})],1)],1),s("el-col",{attrs:{span:12}},[s("el-form-item",{attrs:{label:"类型"}},[s("el-input",{attrs:{"auto-complete":"off"},model:{value:t.editForm.predictor,callback:function(e){t.$set(t.editForm,"predictor",e)},expression:"editForm.predictor"}})],1)],1)],1),s("el-form-item",{attrs:{label:"说明"}},[s("el-input",{model:{value:t.editForm.remarks,callback:function(e){t.$set(t.editForm,"remarks",e)},expression:"editForm.remarks"}})],1)],1),s("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[s("el-button",{nativeOn:{click:function(e){t.editFormVisible=!1}}},[t._v("取消")]),s("el-button",{attrs:{type:"primary",loading:t.editLoading},nativeOn:{click:function(e){return t.editSubmit(e)}}},[t._v("提交")])],1)],1),s("el-dialog",{staticStyle:{width:"75%",left:"12.5%"},attrs:{title:"新增",visible:t.addFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(e){t.addFormVisible=e}}},[s("el-form",{ref:"addForm",attrs:{model:t.addForm,"label-width":"80px",rules:t.addFormRules}},[s("el-row",{attrs:{gutter:24}},[s("el-col",{attrs:{span:12}},[s("el-form-item",{attrs:{label:"病种名称",prop:"remarks"}},[s("el-input",{attrs:{"auto-complete":"off"},model:{value:t.addForm.remarks,callback:function(e){t.$set(t.addForm,"remarks","string"===typeof e?e.trim():e)},expression:"addForm.remarks"}})],1)],1),s("el-col",{attrs:{span:12}},[s("el-form-item",{attrs:{label:"文件路径",prop:"content"}},[s("el-input",{attrs:{"auto-complete":"off"},model:{value:t.addForm.content,callback:function(e){t.$set(t.addForm,"content","string"===typeof e?e.trim():e)},expression:"addForm.content"}})],1)],1),s("el-col",{attrs:{span:12}},[s("el-form-item",{attrs:{label:"数据类型",prop:"environment"}},[s("el-select",{attrs:{clearable:"",placeholder:"请选择类型"},model:{value:t.addForm.type,callback:function(e){t.$set(t.addForm,"type",e)},expression:"addForm.type"}},[s("el-option",{key:"Gold",attrs:{label:"金标准",value:"Gold"}}),s("el-option",{key:"test",attrs:{label:"测试数据",value:"test"}})],1)],1),s("el-form-item",{attrs:{label:"模型",prop:"content"}},[s("el-input",{attrs:{"auto-complete":"off"},model:{value:t.addForm.predictor,callback:function(e){t.$set(t.addForm,"predictor","string"===typeof e?e.trim():e)},expression:"addForm.predictor"}})],1)],1)],1)],1),s("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[s("el-button",{nativeOn:{click:function(e){t.addFormVisible=!1}}},[t._v("取消")]),s("el-button",{attrs:{type:"primary",loading:t.addLoading},nativeOn:{click:function(e){return t.addSubmit(e)}}},[t._v("保存")])],1)],1)],1)},r=[],n=a("2d92"),o={data(){return{filters:{type:"",remarks:"",selecttype:"dicom",status:!0},project:[],total:0,page:1,listLoading:!1,sels:[],editFormVisible:!1,editLoading:!1,options:[{label:"dicom",value:"dicom"}],editFormRules:{type:[{required:!0,message:"请选择类型",trigger:"blur"}],select_type:[{required:!0,message:"请输入版本号",trigger:"change"},{pattern:/^\d+\.\d+\.\d+$/,message:"请输入合法的版本号（x.x.x）"}],description:[{required:!1,message:"请输入描述",trigger:"blur"},{max:1024,message:"不能超过1024个字符",trigger:"blur"}]},editForm:{content:"",select_type:"",type:"",description:""},addFormVisible:!1,addLoading:!1,addFormRules:{type:[{required:!0,message:"请选择类型",trigger:"blur"}]},addForm:{content:"",select_type:"dicom",type:"test",description:""}}},mounted(){this.gethost()},methods:{gethost(){this.listLoading=!0;const t=this,e={},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(n["P"])(a,e).then(e=>{t.listLoading=!1;const{msg:a,code:s,data:r}=e;if("0"===s){t.total=r.total,t.list=r.data;var n=JSON.stringify(t.list);this.tags=JSON.parse(n)}else t.$message.error({message:a,center:!0})})},getbaseList(){this.listLoading=!0;let t=this,e={page:t.page,remarks:t.filters.remarks,type:t.filters.type},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(n["Y"])(a,e).then(e=>{t.listLoading=!1;let{msg:a,code:s,data:r}=e;"0"===s?(t.total=r.total,t.project=r.data):t.$message.error({message:a,center:!0})})},handlecount:function(t,e){this.listLoading=!0;let a=this,s={id:e.id},r={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(n["C"])(r,s).then(t=>{let{msg:e,code:s,data:r}=t;"0"===s?a.$message({message:"同步成功",center:!0,type:"success"}):a.$message.error({message:e,center:!0}),a.getbaseList()})},handleChangeStatus:function(t,e){let a=this;this.listLoading=!0;let s={project_id:e.id},r={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};e.status?Object(n["b"])(r,s).then(t=>{let{msg:s,code:r,data:n}=t;a.listLoading=!1,"0"===r?(a.$message({message:"禁用成功",center:!0,type:"success"}),e.status=!e.status):a.$message.error({message:s,center:!0})}):Object(n["c"])(r,s).then(t=>{let{msg:s,code:r,data:n}=t;a.listLoading=!1,"0"===r?(a.$message({message:"启用成功",center:!0,type:"success"}),e.status=!e.status):a.$message.error({message:s,center:!0})})},handleCurrentChange(t){this.page=t,this.getbaseList()},handleEdit:function(t,e){this.editFormVisible=!0,this.editForm=Object.assign({},e)},handleAdd:function(){this.addFormVisible=!0,this.addForm={select_type:"dicom",content:null,status:!0,remarks:null,other:null,type:"test",predictor:""}},editSubmit:function(){let t=this;this.$refs.editForm.validate(e=>{e&&this.$confirm("确认提交吗？","提示",{}).then(()=>{t.editLoading=!0;let e={id:t.editForm.id,content:t.editForm.content,type:t.editForm.type,select_type:t.editForm.select_type,start_date:t.editForm.start_date,status:t.editForm.status,remarks:t.editForm.remarks,other:t.editForm.other},a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(n["f"])(a,e).then(e=>{let{msg:a,code:s,data:r}=e;t.editLoading=!1,"0"===s?(t.$message({message:"修改成功",center:!0,type:"success"}),t.$refs["editForm"].resetFields(),t.editFormVisible=!1,t.getbaseList()):t.$message.error({message:a,center:!0})})})})},addSubmit:function(){this.$refs.addForm.validate(t=>{if(t){let t=this;this.$confirm("确认提交吗？","提示",{}).then(()=>{t.addLoading=!0;let e=JSON.stringify({content:this.addForm.content,type:t.addForm.type,select_type:t.addForm.select_type,remarks:this.addForm.remarks,other:t.addForm.other,predictor:t.addForm.predictor,status:!0}),a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(n["n"])(a,e).then(e=>{let{msg:a,code:s,data:r}=e;t.addLoading=!1,"0"===s?(t.$message({message:"添加成功",center:!0,type:"success"}),t.$refs["addForm"].resetFields(),t.addFormVisible=!1,t.getbaseList()):"999997"===s?t.$message.error({message:a,center:!0}):(t.$message.error({message:a,center:!0}),t.$refs["addForm"].resetFields(),t.addFormVisible=!1,t.getbaseList())})})}})},selsChange:function(t){this.sels=t},batchSend:function(){const t=this.sels.map(t=>t.id);this.$confirm("确认生成选中记录吗？","提示",{type:"warning"}).then(()=>{this.listLoading=!0;const e=this,a={ids:t,server_ip:this.filters.server},s={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(n["Z"])(s,a).then(t=>{const{msg:a,code:s,data:r}=t;"0"===s?e.$message({message:"成功",center:!0,type:"success"}):e.$message.error({message:a,center:!0}),e.getbaseList()})})},batchRemove:function(){let t=this.sels.map(t=>t.id);this.$confirm("确认删除选中记录吗？","提示",{type:"warning"}).then(()=>{this.listLoading=!0;let e=this,a={ids:t},s={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(n["a"])(s,a).then(t=>{let{msg:a,code:s,data:r}=t;"0"===s?e.$message({message:"删除成功",center:!0,type:"success"}):e.$message.error({message:a,center:!0}),e.getbaseList()})})}},mounted(){this.getbaseList()}},i=o,l=a("2877"),d=Object(l["a"])(i,s,r,!1,null,null,null);e["default"]=d.exports},e7a2:function(t,e,a){t.exports=a.p+"static/img/icon-yes.06589da8.svg"}}]);