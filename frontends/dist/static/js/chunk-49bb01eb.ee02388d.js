(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-49bb01eb"],{"2d92":function(e,t,a){"use strict";a.d(t,"nb",(function(){return s})),a.d(t,"O",(function(){return i})),a.d(t,"t",(function(){return o})),a.d(t,"E",(function(){return l})),a.d(t,"I",(function(){return d})),a.d(t,"qb",(function(){return c})),a.d(t,"k",(function(){return u})),a.d(t,"P",(function(){return p})),a.d(t,"N",(function(){return m})),a.d(t,"s",(function(){return h})),a.d(t,"D",(function(){return f})),a.d(t,"H",(function(){return b})),a.d(t,"pb",(function(){return _})),a.d(t,"j",(function(){return g})),a.d(t,"Q",(function(){return v})),a.d(t,"R",(function(){return y})),a.d(t,"M",(function(){return k})),a.d(t,"r",(function(){return x})),a.d(t,"i",(function(){return w})),a.d(t,"S",(function(){return $})),a.d(t,"U",(function(){return F})),a.d(t,"T",(function(){return D})),a.d(t,"g",(function(){return j})),a.d(t,"L",(function(){return C})),a.d(t,"h",(function(){return S})),a.d(t,"ob",(function(){return z})),a.d(t,"q",(function(){return V})),a.d(t,"G",(function(){return I})),a.d(t,"kb",(function(){return q})),a.d(t,"rb",(function(){return O})),a.d(t,"l",(function(){return T})),a.d(t,"J",(function(){return E})),a.d(t,"x",(function(){return P})),a.d(t,"hb",(function(){return B})),a.d(t,"jb",(function(){return Y})),a.d(t,"ib",(function(){return A})),a.d(t,"p",(function(){return L})),a.d(t,"ub",(function(){return N})),a.d(t,"z",(function(){return J})),a.d(t,"d",(function(){return M})),a.d(t,"mb",(function(){return R})),a.d(t,"e",(function(){return G})),a.d(t,"lb",(function(){return H})),a.d(t,"V",(function(){return K})),a.d(t,"u",(function(){return Q})),a.d(t,"sb",(function(){return U})),a.d(t,"n",(function(){return W})),a.d(t,"C",(function(){return X})),a.d(t,"Y",(function(){return Z})),a.d(t,"B",(function(){return ee})),a.d(t,"v",(function(){return te})),a.d(t,"gb",(function(){return ae})),a.d(t,"fb",(function(){return re})),a.d(t,"cb",(function(){return ne})),a.d(t,"y",(function(){return se})),a.d(t,"Z",(function(){return ie})),a.d(t,"ab",(function(){return oe})),a.d(t,"o",(function(){return le})),a.d(t,"tb",(function(){return de})),a.d(t,"w",(function(){return ce})),a.d(t,"K",(function(){return ue})),a.d(t,"F",(function(){return pe})),a.d(t,"bb",(function(){return me})),a.d(t,"db",(function(){return he})),a.d(t,"eb",(function(){return fe})),a.d(t,"X",(function(){return be})),a.d(t,"W",(function(){return _e})),a.d(t,"m",(function(){return ge})),a.d(t,"f",(function(){return ve})),a.d(t,"c",(function(){return ye})),a.d(t,"b",(function(){return ke})),a.d(t,"a",(function(){return xe})),a.d(t,"A",(function(){return we}));var r=a("bc3a"),n=a.n(r);a("c896");const s="http://192.168.1.121:9000",i=(e,t)=>n.a.get(s+"/api/project/project_list",{params:t,headers:e}).then(e=>e.data),o=(e,t)=>n.a.post(s+"/api/project/del_project",t,{headers:e}).then(e=>e.data),l=(e,t)=>n.a.post(s+"/api/project/disable_project",t,{headers:e}).then(e=>e.data),d=(e,t)=>n.a.post(s+"/api/project/enable_project",t,{headers:e}).then(e=>e.data),c=(e,t)=>n.a.post(s+"/api/project/update_project",t,{headers:e}).then(e=>e.data),u=(e,t)=>n.a.post(s+"/api/project/add_project",t,{headers:e}).then(e=>e.data),p=(e,t)=>n.a.get(s+"/api/title/project_info",{params:t,headers:e}).then(e=>e.data),m=(e,t)=>n.a.get(s+"/api/global/host_total",{params:t,headers:e}).then(e=>e.data),h=(e,t)=>n.a.post(s+"/api/global/del_host",t,{headers:e}).then(e=>e.data),f=(e,t)=>n.a.post(s+"/api/global/disable_host",t,{headers:e}).then(e=>e.data),b=(e,t)=>n.a.post(s+"/api/global/enable_host",t,{headers:e}).then(e=>e.data),_=(e,t)=>n.a.post(s+"/api/global/update_host",t,{headers:e}).then(e=>e.data),g=(e,t)=>n.a.post(s+"/api/global/add_host",t,{headers:e}).then(e=>e.data),v=(e,t)=>n.a.get(s+"/api/dynamic/dynamic",{params:t,headers:e}).then(e=>e.data),y=(e,t)=>n.a.get(s+"/api/member/project_member",{params:t,headers:e}).then(e=>e.data),k=(e,t)=>n.a.get(s+"/api/member/get_email",{params:t,headers:e}).then(e=>e.data),x=(e,t)=>n.a.post(s+"/api/member/del_email",t,{headers:e}).then(e=>e.data),w=(e,t)=>n.a.post(s+"/api/member/email_config",t,{headers:e}).then(e=>e.data),$=(e,t)=>n.a.get(s+"/api/report/auto_test_report",{params:t,headers:e}).then(e=>e.data),F=(e,t)=>n.a.get(s+"/api/report/test_time",{params:t,headers:e}).then(e=>e.data),D=(e,t)=>n.a.get(s+"/api/report/lately_ten",{params:t,headers:e}).then(e=>e.data),j=(e,t)=>n.a.post(s+"/api/api/add_api",t,{headers:e}).then(e=>e.data),C=(e,t)=>n.a.get(s+"/api/api/group",{params:t,headers:e}).then(e=>e.data),S=(e,t)=>n.a.post(s+"/api/api/add_group",t,{headers:e}).then(e=>e.data),z=(e,t)=>n.a.post(s+"/api/api/update_name_group",t,{headers:e}).then(e=>e.data),V=(e,t)=>n.a.post(s+"/api/api/del_group",t,{headers:e}).then(e=>e.data),I=(e,t)=>n.a.post(s+"/api/download",t,{headers:e}).then(e=>e.data),q=(e,t)=>n.a.post(s+"/api/user/login",t,e).then(e=>e.data),O=(e,t)=>n.a.post(s+"/api/risk/update",t,{headers:e}).then(e=>e.data),T=(e,t)=>n.a.post(s+"/api/risk/add",t,{headers:e}).then(e=>e.data),E=(e,t)=>n.a.post(s+"/api/risk/add",t,{headers:e}).then(e=>e.data),P=(e,t)=>n.a.post(s+"/api/risk/del",t,e).then(e=>e.data),B=(e,t)=>n.a.get(s+"/api/risk ",{params:t},e).then(e=>e.data),Y=(e,t)=>n.a.get(s+"/api/todo ",{params:t},e).then(e=>e.data),A=(e,t)=>n.a.get(s+"/api/report ",{params:t},e).then(e=>e.data),L=(e,t)=>n.a.post(s+"/api/addreport",t,e).then(e=>e.data),N=(e,t)=>n.a.post(s+"/api/updatereport",t,e).then(e=>e.data),J=(e,t)=>n.a.post(s+"/api/delreport",t,e).then(e=>e.data),M=(e,t)=>n.a.post(s+"/api/send",t,e).then(e=>e.data),R=(e,t)=>n.a.get(s+"/api/stress/list",{params:t},{headers:e}).then(e=>e.data),G=(e,t)=>n.a.get(s+"/api/stress/stressDetail ",{params:t},e).then(e=>e.data),H=(e,t)=>n.a.post(s+"/api/stress/stresstool",t,e).then(e=>e.data),K=(e,t)=>n.a.get(s+"/api/stress/version",{params:t},{headers:e}).then(e=>e.data),Q=(e,t)=>n.a.post(s+"/api/tool/del_dicomData",t,e).then(e=>e.data),U=(e,t)=>n.a.post(s+"/api/tool/update_dicomData",t,e).then(e=>e.data),W=(e,t)=>n.a.post(s+"/api/tool/add_dicomData",t,e).then(e=>e.data),X=(e,t)=>n.a.post(s+"/api/tool/dicomdetail",t,e).then(e=>e.data),Z=(e,t)=>n.a.get(s+"/api/tool/dicomData",{params:t},{headers:e}).then(e=>e.data),ee=(e,t)=>n.a.post(s+"/api/tool/dicomcsv",t,e).then(e=>e.data),te=(e,t)=>n.a.post(s+"/api/tool/delreport",t,e).then(e=>e.data),ae=(e,t)=>n.a.get(s+"/api/stress/stressversion",{params:t},{headers:e}).then(e=>e.data),re=(e,t)=>n.a.post(s+"/api/stress/stressresult",t,e).then(e=>e.data),ne=(e,t)=>n.a.post(s+"/api/stress/stressfigure",t,e).then(e=>e.data),se=(e,t)=>n.a.post(s+"/api/tool/delete_patients",t,e).then(e=>e.data),ie=(e,t)=>n.a.get(s+"/api/tool/getduration",{params:t},{headers:e}).then(e=>e.data),oe=(e,t)=>n.a.get(s+"/api/tool/durationData",{params:t},{headers:e}).then(e=>e.data),le=(e,t)=>n.a.post(s+"/api/tool/add_duration",t,e).then(e=>e.data),de=(e,t)=>n.a.post(s+"/api/tool/update_duration",t,e).then(e=>e.data),ce=(e,t)=>n.a.post(s+"/api/tool/del_duration",t,e).then(e=>e.data),ue=(e,t)=>n.a.post(s+"/api/tool/enable_duration",t,e).then(e=>e.data),pe=(e,t)=>n.a.post(s+"/api/tool/disable_duration",t,e).then(e=>e.data),me=(e,t)=>n.a.get(s+"/api/tool/duration_verify",{params:t},{headers:e}).then(e=>e.data),he=(e,t)=>n.a.get(s+"/api/tool/somkerecord",{params:t},{headers:e}).then(e=>e.data),fe=(e,t)=>n.a.post(s+"/api/tool/somke",t,e).then(e=>e.data),be=(e,t)=>n.a.post(s+"/api/tool/dicomSend",t,e).then(e=>e.data),_e=(e,t)=>n.a.get(s+"/api/base/getdata",{params:t},{headers:e}).then(e=>e.data),ge=(e,t)=>n.a.post(s+"/api/base/addData",t,e).then(e=>e.data),ve=(e,t)=>n.a.post(s+"/api/base/updateData",t,e).then(e=>e.data),ye=(e,t)=>n.a.post(s+"/api/base/enablebase",t,e).then(e=>e.data),ke=(e,t)=>n.a.post(s+"/api/base/disablebase",t,e).then(e=>e.data),xe=(e,t)=>n.a.post(s+"/api/base/delbasedata",t,e).then(e=>e.data),we=(e,t)=>n.a.get(s+"/api/base/dicom",{params:t},{headers:e}).then(e=>e.data)},"32bc":function(e,t,a){},"41d3":function(e,t,a){},71549:function(e,t,a){"use strict";var r=a("32bc"),n=a.n(r);n.a},b119:function(e,t,a){"use strict";a.r(t);var r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"table"},[a("div",{staticClass:"crumbs"},[a("el-breadcrumb",{attrs:{separator:"/"}},[a("el-breadcrumb-item",[a("i",{staticClass:"el-icon-lx-cascades"}),e._v("测试项目版本")])],1)],1),a("div",{staticClass:"container"},[a("div",{staticClass:"handle-box",staticStyle:{clear:"both","margin-bottom":"80px"}},[a("div",{staticClass:"add",staticStyle:{float:"left"}},[a("el-button",{staticClass:"handle-del mr10",attrs:{type:"primary",icon:"add"},on:{click:function(t){return e.handleAdd()}}},[e._v("添加")])],1),a("div",{staticClass:"search",staticStyle:{float:"left"}},[a("el-form",{ref:"searchform",attrs:{model:e.searchform,"label-width":"100px"}},[a("el-select",{staticClass:"handle-select mr10",attrs:{clearable:"",placeholder:"筛选",prop:"select_app"},model:{value:e.searchform.select_app,callback:function(t){e.$set(e.searchform,"select_app",t)},expression:"searchform.select_app"}},[a("el-option",{key:"每日报告",attrs:{label:"每日报告",value:"1"}}),a("el-option",{key:"测试报告",attrs:{label:"测试报告",value:"2"}}),a("el-option",{key:"质量报告",attrs:{label:"质量报告",value:"3"}})],1),a("el-input",{staticClass:"handle-input mr10",attrs:{prop:"select_version",placeholder:"筛选"},model:{value:e.searchform.select_version,callback:function(t){e.$set(e.searchform,"select_version",t)},expression:"searchform.select_version"}}),a("el-button",{attrs:{type:"primary",icon:"search"},on:{click:function(t){return e.searchProject("searchform")}}},[e._v("搜索")])],1)],1)]),a("el-table",{ref:"multipleTable",staticClass:"table",attrs:{data:e.tableData,border:""},on:{"selection-change":e.handleSelectionChange}},[a("el-table-column",{attrs:{label:"邮件主题","min-width":"15%"},scopedSlots:e._u([{key:"default",fn:function(t){return[t.row.title?a("router-link",{staticStyle:{"text-decoration":"none",color:"#000000"},attrs:{to:{name:"邮件详情",params:{report_id:t.row.report_id}}}},[e._v(" "+e._s(t.row.title)+" ")]):e._e()]}}])}),a("el-table-column",{attrs:{label:"Boimind版本","min-width":"10%"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.test_version))])]}}])}),a("el-table-column",{attrs:{label:"CoinNess版本","min-width":"10%"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.cns_version))])]}}])}),a("el-table-column",{attrs:{label:"邮件类型","min-width":"5%"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.type))])]}}])}),a("el-table-column",{attrs:{label:"发送时间","min-width":"10%"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",[e._v(e._s(t.row.send_time))])]}}])}),a("el-table-column",{attrs:{label:"收件人员","min-width":"15%"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.receiver))])]}}])}),a("el-table-column",{attrs:{label:"抄送人员","min-width":"15%",formatter:e.dateFormatter},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.email_cc))])]}}])}),a("el-table-column",{attrs:{label:"操作","min-width":"20%",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-button",{attrs:{type:"text",icon:"el-icon-find"},on:{click:function(a){return e.showRisk(t.$index,t.row)}}},[e._v("查看模板")]),a("el-button",{attrs:{type:"text",icon:"el-icon-edit"},on:{click:function(a){return e.handleEdit(t.$index,t.row)}}},[e._v("编辑")]),a("el-button",{attrs:{type:"text",icon:"el-icon-lx-comment"},on:{click:function(a){return e.handleSend(t.$index,t.row)}}},[e._v("发送")]),a("el-button",{staticClass:"red",attrs:{type:"text",icon:"el-icon-delete"},on:{click:function(a){return e.handleDelete(t.$index,t.row)}}},[e._v("删除")])]}}])})],1),a("div",{staticClass:"pagination"},[a("el-pagination",{attrs:{"current-page":e.currentPage,"page-sizes":[10,20,30,40],"page-size":100,layout:"total, sizes, prev, pager, next, jumper",total:e.currentTotal},on:{"size-change":e.handleSizeChange,"current-change":e.handleCurrentChange}})],1)],1),a("el-dialog",{attrs:{title:"编辑",visible:e.editVisible,width:"30%"},on:{"update:visible":function(t){e.editVisible=t}}},[a("el-form",{ref:"editform",attrs:{model:e.editform,"label-width":"100px"}},[a("el-form-item",{attrs:{label:"ID"}},[a("el-input",{attrs:{disabled:!0,width:"5%"},model:{value:e.editform.report_id,callback:function(t){e.$set(e.editform,"report_id",t)},expression:"editform.report_id"}})],1),a("el-form-item",{attrs:{label:"邮件主题"}},[a("el-input",{model:{value:e.editform.title,callback:function(t){e.$set(e.editform,"title",t)},expression:"editform.title"}})],1),a("el-form-item",{attrs:{label:"Boimind版本"}},[a("el-input",{model:{value:e.editform.test_version,callback:function(t){e.$set(e.editform,"test_version",t)},expression:"editform.test_version"}})],1),a("el-form-item",{attrs:{label:"CoinNess版本"}},[a("el-input",{model:{value:e.editform.cns_version,callback:function(t){e.$set(e.editform,"cns_version",t)},expression:"editform.cns_version"}})],1),a("el-form-item",{attrs:{label:"邮件类型"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.editform.type,callback:function(t){e.$set(e.editform,"type",t)},expression:"editform.type"}},[a("el-option",{key:"1",attrs:{label:"每日报告",value:"1"}}),a("el-option",{key:"2",attrs:{label:"测试报告",value:"2"}}),a("el-option",{key:"3",attrs:{label:"质量报告",value:"3"}})],1)],1),a("el-form-item",{attrs:{label:"发送时间"}},[a("el-date-picker",{attrs:{type:"datetime",placeholder:"选择日期"},model:{value:e.editform.send_time,callback:function(t){e.$set(e.editform,"send_time",t)},expression:"editform.send_time"}})],1),a("el-form-item",{attrs:{label:"收件人员"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.editform.receiver,callback:function(t){e.$set(e.editform,"receiver",t)},expression:"editform.receiver"}},[a("el-option",{key:"test",attrs:{label:"测试",value:"test"}}),a("el-option",{key:"on",attrs:{label:"正式",value:"on"}}),a("el-option",{key:"0",attrs:{label:"当前用户",value:"0"}})],1)],1),a("el-form-item",{attrs:{label:"抄送人员"}},[a("el-input",{model:{value:e.editform.email_cc,callback:function(t){e.$set(e.editform,"email_cc",t)},expression:"editform.email_cc"}})],1)],1),a("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(t){e.editVisible=!1}}},[e._v("取 消")]),a("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.saveEdit(e.editform)}}},[e._v("确 定")])],1)],1),a("el-dialog",{attrs:{title:"添加",rules:e.rules,visible:e.dialogFormVisible,width:"40%"},on:{"update:visible":function(t){e.dialogFormVisible=t}}},[a("el-form",{ref:"addForm",attrs:{model:e.addForm,rules:e.rules,"label-width":"120px"}},[a("el-form-item",{attrs:{label:"邮件主题",prop:"title"}},[a("el-input",{model:{value:e.addForm.title,callback:function(t){e.$set(e.addForm,"title",t)},expression:"addForm.title"}})],1),a("el-form-item",{attrs:{label:"Boimind版本",prop:"title"}},[a("el-input",{model:{value:e.addForm.test_version,callback:function(t){e.$set(e.addForm,"test_version",t)},expression:"addForm.test_version"}})],1),a("el-form-item",{attrs:{label:"CoinNess版本",prop:"title"}},[a("el-input",{model:{value:e.addForm.cns_version,callback:function(t){e.$set(e.addForm,"cns_version",t)},expression:"addForm.cns_version"}})],1),a("el-form-item",{attrs:{label:"邮件类型"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.addForm.type,callback:function(t){e.$set(e.addForm,"type",t)},expression:"addForm.type"}},[a("el-option",{key:"1",attrs:{label:"每日报告",value:"1"}}),a("el-option",{key:"2",attrs:{label:"测试报告",value:"2"}}),a("el-option",{key:"3",attrs:{label:"质量报告",value:"3"}})],1)],1),a("el-form-item",{attrs:{label:"发送时间",prop:"start_date"}},[a("el-date-picker",{attrs:{type:"datetime",placeholder:"选择日期"},model:{value:e.addForm.start_date,callback:function(t){e.$set(e.addForm,"start_date",t)},expression:"addForm.start_date"}})],1),a("el-form-item",{attrs:{label:"收件人员",prop:"app"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.addForm.receiver,callback:function(t){e.$set(e.addForm,"receiver",t)},expression:"addForm.receiver"}},[a("el-option",{key:"test",attrs:{label:"测试",value:"test"}}),a("el-option",{key:"all",attrs:{label:"所有",value:"all"}}),a("el-option",{key:"0",attrs:{label:"当前用户",value:"0"}})],1)],1),a("el-form-item",{attrs:{label:"抄送人员"}},[a("el-input",{model:{value:e.addForm.email_cc,callback:function(t){e.$set(e.addForm,"email_cc",t)},expression:"addForm.email_cc"}})],1)],1),a("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(t){e.dialogFormVisible=!1}}},[e._v("取 消")]),a("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.addconfig("addForm")}}},[e._v("添加")])],1)],1)],1)},n=[],s=a("2d92"),i={name:"basetable",data(){return{rules:{title:[{required:!0,message:"请输邮件主题",trigger:"change"}],receiver:[{required:!0,message:"输入收件人员",trigger:"change"}],type:[{required:!0,message:"输入邮件类型",trigger:"change"}],email_cc:[{required:!0,message:"输入抄送人员",trigger:"change"}]},tableData:[],cur_page:1,multipleSelection:[],select_cate:"",select_word:"",del_list:[],is_search:!1,editVisible:!1,delVisible:!1,dialogFormVisible:!1,form:{title:"",test_version:"",cns_version:""},editform:{title:"",test_version:"",cns_version:""},addForm:{title:"",test_version:"",cns_version:""},searchform:{},currentPage:1,pageSize:10,currentTotal:0}},created(){this.getData()},computed:{data(){return this.tableData.filter(e=>{let t=!1;for(let a=0;a<this.del_list.length;a++)if(e.name===this.del_list[a].name){t=!0;break}if(!t&&e.address.indexOf(this.select_cate)>-1&&(e.name.indexOf(this.select_word)>-1||e.address.indexOf(this.select_word)>-1))return e})}},methods:{showRisk(e,t){this.$router.push({path:"/risk",query:{project_id:t.project_id,project:t.project}})},handleSizeChange(e){this.pageSize=e,console.log(`每页 ${e} 条`),this.getData()},handleCurrentChange(e){this.currentPage=e,console.log(`这是第${e}页`),this.getData()},getData(e,t){let a={page:this.currentPage,page_size:this.pageSize,type:e},r={"Content-Type":"application/x-www-form-urlencoded"};Object(s["ib"])(r,a).then(e=>{let{msg:t,data:a,code:r}=e;this.currentTotal=a.total,this.tableData=a.data})},search(){this.is_search=!0},dateFormatter(e,t){console.log("格式化日期");var a=e[t.property];return void 0==a?"":moment(data).format("YYYY-MM-DD")},filterTag(e,t){return t.tag===e},handleAdd(){this.dialogFormVisible=!0,this.addForm={report_id:null,test_version:null,cns_version:null,receiver:null,type:null,send_time:null,email_cc:null,title:null,content_id:null}},addconfig(e){console.log(e),this.$refs[e].validate(e=>{if(!e)return console.log("error submit!!"),!1;{let e={test_version:this.addForm.test_version,cns_version:this.addForm.cns_version,receiver:this.addForm.receiver,type:this.addForm.type,send_time:this.addForm.send_time,email_cc:this.addForm.email_cc,title:this.addForm.title,content_id:null};console.log(e);let t={"Content-Type":"application/json"};Object(s["p"])(t,e).then(e=>{let{msg:t,code:a,data:r}=e;console.log("code:"+a),"0"==a?(this.$message.success("添加成功"),this.dialogFormVisible=!1,this.getData()):this.$message.error(t)})}})},handleEdit(e,t){this.idx=e;const a=this.tableData[e];this.editform={report_id:a.report_id,test_version:a.test_version,cns_version:a.cns_version,title:a.title,receiver:a.receiver,type:a.type,send_time:a.send_time,email_cc:a.email_cc,content_id:a.content_id},this.editVisible=!0},handleEdit(e,t){this.idx=e;const a=this.tableData[e];this.editform={report_id:a.report_id,test_version:a.test_version,cns_version:a.cns_version,title:a.title,receiver:a.receiver,type:a.type,send_time:a.send_time,email_cc:a.email_cc,content_id:a.content_id},this.editVisible=!0},handleDelete(e,t){this.idx=e;const a=this.tableData[e];let r=[a.report_id],n={ids:r},i={"Content-Type":"application/json"};Object(s["z"])(i,n).then(e=>{let{msg:t,code:a,data:r}=e;"0"==a?null==r||r[0]?(this.$message.success("删除成功"),this.getData()):this.$message.error(r[1]):this.$message.error(t)})},handleSend(e,t){this.idx=e;const a=this.tableData[e];let r=a.report_id,n={report_id:r,type:1,start_time:"",endtime:""},i={"Content-Type":"application/json"};Object(s["d"])(i,n).then(e=>{let{msg:t,code:a,data:r}=e;"0"==a?null==r||r[0]?(this.$message.success("发送成功！"),this.getData()):this.$message.error(r[1]):this.$message.error(t)})},handleSelectionChange(e){this.multipleSelection=e},searchProject(e){let t=this.searchform.select_app,a=this.searchform.select_version,r=/^\d+\.\d+\.\d+$/;if("undefined"==typeof t&&"undefined"==typeof a)return void alert("请输入要搜索的版本号或者版本号");let n=typeof a;"undefined"==n||null==n||""==n||r.test(a)?this.getData(t,a):alert("请输入格式为x.x.x的版本号")},saveEdit(e){let t={report_id:e.report_id,test_version:e.test_version,cns_version:e.cns_version,receiver:e.receiver,type:e.type,send_time:e.send_time,email_cc:e.email_cc,title:e.title,content_id:""},a={"Content-Type":"application/json"};Object(s["ub"])(a,t).then(e=>{let{msg:t,code:a,data:r}=e;"0"==a?null==r||r[0]?(this.$message.success("编辑成功"),this.editVisible=!1,this.getData()):this.$message.error(r[1]):this.$message.error(t)})}}},o=i,l=(a("71549"),a("2877")),d=Object(l["a"])(o,r,n,!1,null,"d281966c",null);t["default"]=d.exports},c896:function(e,t,a){"use strict";var r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("div",{staticClass:"crumbs"},[a("el-breadcrumb",{attrs:{separator:"/"}},[a("el-breadcrumb-item",[a("i",{staticClass:"el-icon-lx-calendar"}),e._v(" 测试工具")]),a("el-breadcrumb-item",[e._v("推送工具")])],1)],1),a("div",{staticClass:"container"},[a("div",{staticClass:"form-box"},[a("el-form",{ref:"form",attrs:{model:e.form,"status-icon":"",rules:e.rules,"label-width":"80px"}},[a("el-form-item",{attrs:{label:"推送ID",prop:"pushID"}},[a("el-col",{attrs:{span:10}},[a("el-input",{attrs:{id:"pushID"},model:{value:e.form.pushID,callback:function(t){e.$set(e.form,"pushID",t)},expression:"form.pushID"}})],1)],1),a("el-form-item",{attrs:{label:"推送环境",prop:"environment"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.form.environment,callback:function(t){e.$set(e.form,"environment",t)},expression:"form.environment"}},[a("el-option",{key:"test",attrs:{label:"测试环境",value:"test"}}),a("el-option",{key:"online",attrs:{label:"线上环境",value:"online"}})],1)],1),a("el-form-item",{attrs:{label:"推送类型",prop:"types"}},[a("el-cascader",{attrs:{options:e.types},on:{change:function(t){return e.changeLang("form")}},model:{value:e.form.types,callback:function(t){e.$set(e.form,"types",t)},expression:"form.types"}})],1),a("el-form-item",{attrs:{label:"选择语言",prop:"languages"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.form.languages,callback:function(t){e.$set(e.form,"languages",t)},expression:"form.languages"}},e._l(e.languages,(function(e,t){return a("el-option",{key:e.key,attrs:{label:e.value,value:e.key}})})),1)],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.onSubmit("form")}}},[e._v("确定推送")]),a("el-button",{on:{click:function(t){return e.resetForm("form")}}},[e._v("重置")])],1)],1)],1)])])},n=[],s={name:"baseform",data:function(){return{types:[{value:"bishijie",label:"Boimind",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"replay",label:"币圈"},{value:"monitor",label:"盯盘"}]},{value:"coinness",label:"coinness",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"monitor",label:"盯盘"}]}],languages:[],form:{pushID:"",environment:"",types:[],languages:[]},rules:{pushID:[{required:!0,message:"请输入推送ID",trigger:"blur"}],environment:[{required:!0,message:"请选择推送环境",trigger:"blur"}],types:[{required:!0,message:"请选择推送类型",trigger:"blur"}],languages:[{required:!0,message:"请选择语言",trigger:"blur"}]}}},methods:{onSubmit(e){this.$refs[e].validate(e=>{if(!e)return console.log("error submit"),!1;console.log("语言："+this.form.languages),console.log("pushID："+this.form.pushID),console.log("APP："+this.form.types[0]),console.log("推送类型："+this.form.types[1]),console.log("environment："+this.form.environment),this.$ajax.post("/bishijie/push",{id:this.form.pushID,service:this.form.environment,system:this.form.types[0],module:this.form.types[1],lang:this.form.languages,rid:""}).then(e=>{"0"==e.data.code?null==e.data.data||e.data.data[0]?this.$message.success("push成功！"):this.$message.error(e.data.data[1]):this.$message.error(e.data.msg)}).catch((function(e){console.log(e)}))})},resetForm(e){this.$refs[e].resetFields()},changeLang(e){this.languages=[],this.form.languages="";var t=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"}],a=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"},{key:"en_go",value:"English"},{key:"ko_kr",value:"한글"}],r=this.form.types[0].toLowerCase();"bishijie"==r?this.languages=t:"coinness"==r&&(this.languages=a)}}},i=s,o=(a("cd97"),a("2877")),l=Object(o["a"])(i,r,n,!1,null,"6d8efc95",null);l.exports},cd97:function(e,t,a){"use strict";var r=a("41d3"),n=a.n(r);n.a}}]);