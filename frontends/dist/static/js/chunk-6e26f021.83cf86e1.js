(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-6e26f021"],{"2d92":function(e,t,a){"use strict";a.d(t,"fb",(function(){return n})),a.d(t,"J",(function(){return s})),a.d(t,"s",(function(){return o})),a.d(t,"z",(function(){return l})),a.d(t,"D",(function(){return d})),a.d(t,"ib",(function(){return c})),a.d(t,"j",(function(){return p})),a.d(t,"K",(function(){return u})),a.d(t,"I",(function(){return m})),a.d(t,"r",(function(){return h})),a.d(t,"y",(function(){return f})),a.d(t,"C",(function(){return _})),a.d(t,"hb",(function(){return b})),a.d(t,"i",(function(){return g})),a.d(t,"L",(function(){return v})),a.d(t,"M",(function(){return k})),a.d(t,"H",(function(){return y})),a.d(t,"q",(function(){return x})),a.d(t,"h",(function(){return w})),a.d(t,"N",(function(){return F})),a.d(t,"P",(function(){return $})),a.d(t,"O",(function(){return C})),a.d(t,"f",(function(){return j})),a.d(t,"G",(function(){return S})),a.d(t,"g",(function(){return D})),a.d(t,"gb",(function(){return V})),a.d(t,"p",(function(){return T})),a.d(t,"B",(function(){return z})),a.d(t,"db",(function(){return P})),a.d(t,"jb",(function(){return O})),a.d(t,"k",(function(){return B})),a.d(t,"E",(function(){return E})),a.d(t,"u",(function(){return N})),a.d(t,"ab",(function(){return q})),a.d(t,"Z",(function(){return Y})),a.d(t,"cb",(function(){return A})),a.d(t,"bb",(function(){return J})),a.d(t,"n",(function(){return M})),a.d(t,"lb",(function(){return R})),a.d(t,"w",(function(){return I})),a.d(t,"d",(function(){return G})),a.d(t,"eb",(function(){return H})),a.d(t,"Q",(function(){return K})),a.d(t,"x",(function(){return L})),a.d(t,"mb",(function(){return Q})),a.d(t,"o",(function(){return U})),a.d(t,"Y",(function(){return W})),a.d(t,"W",(function(){return X})),a.d(t,"X",(function(){return Z})),a.d(t,"V",(function(){return ee})),a.d(t,"v",(function(){return te})),a.d(t,"S",(function(){return ae})),a.d(t,"T",(function(){return re})),a.d(t,"m",(function(){return ie})),a.d(t,"kb",(function(){return ne})),a.d(t,"t",(function(){return se})),a.d(t,"F",(function(){return oe})),a.d(t,"A",(function(){return le})),a.d(t,"U",(function(){return de})),a.d(t,"R",(function(){return ce})),a.d(t,"l",(function(){return pe})),a.d(t,"e",(function(){return ue})),a.d(t,"c",(function(){return me})),a.d(t,"b",(function(){return he})),a.d(t,"a",(function(){return fe}));var r=a("bc3a"),i=a.n(r);const n="http://192.168.2.38:9000",s=(e,t)=>i.a.get(n+"/api/project/project_list",{params:t,headers:e}).then(e=>e.data),o=(e,t)=>i.a.post(n+"/api/project/del_project",t,{headers:e}).then(e=>e.data),l=(e,t)=>i.a.post(n+"/api/project/disable_project",t,{headers:e}).then(e=>e.data),d=(e,t)=>i.a.post(n+"/api/project/enable_project",t,{headers:e}).then(e=>e.data),c=(e,t)=>i.a.post(n+"/api/project/update_project",t,{headers:e}).then(e=>e.data),p=(e,t)=>i.a.post(n+"/api/project/add_project",t,{headers:e}).then(e=>e.data),u=(e,t)=>i.a.get(n+"/api/title/project_info",{params:t,headers:e}).then(e=>e.data),m=(e,t)=>i.a.get(n+"/api/global/host_total",{params:t,headers:e}).then(e=>e.data),h=(e,t)=>i.a.post(n+"/api/global/del_host",t,{headers:e}).then(e=>e.data),f=(e,t)=>i.a.post(n+"/api/global/disable_host",t,{headers:e}).then(e=>e.data),_=(e,t)=>i.a.post(n+"/api/global/enable_host",t,{headers:e}).then(e=>e.data),b=(e,t)=>i.a.post(n+"/api/global/update_host",t,{headers:e}).then(e=>e.data),g=(e,t)=>i.a.post(n+"/api/global/add_host",t,{headers:e}).then(e=>e.data),v=(e,t)=>i.a.get(n+"/api/dynamic/dynamic",{params:t,headers:e}).then(e=>e.data),k=(e,t)=>i.a.get(n+"/api/member/project_member",{params:t,headers:e}).then(e=>e.data),y=(e,t)=>i.a.get(n+"/api/member/get_email",{params:t,headers:e}).then(e=>e.data),x=(e,t)=>i.a.post(n+"/api/member/del_email",t,{headers:e}).then(e=>e.data),w=(e,t)=>i.a.post(n+"/api/member/email_config",t,{headers:e}).then(e=>e.data),F=(e,t)=>i.a.get(n+"/api/report/auto_test_report",{params:t,headers:e}).then(e=>e.data),$=(e,t)=>i.a.get(n+"/api/report/test_time",{params:t,headers:e}).then(e=>e.data),C=(e,t)=>i.a.get(n+"/api/report/lately_ten",{params:t,headers:e}).then(e=>e.data),j=(e,t)=>i.a.post(n+"/api/api/add_api",t,{headers:e}).then(e=>e.data),S=(e,t)=>i.a.get(n+"/api/api/group",{params:t,headers:e}).then(e=>e.data),D=(e,t)=>i.a.post(n+"/api/api/add_group",t,{headers:e}).then(e=>e.data),V=(e,t)=>i.a.post(n+"/api/api/update_name_group",t,{headers:e}).then(e=>e.data),T=(e,t)=>i.a.post(n+"/api/api/del_group",t,{headers:e}).then(e=>e.data),z=(e,t)=>i.a.post(n+"/api/download",t,{headers:e}).then(e=>e.data),P=(e,t)=>i.a.post(n+"/api/user/login",t,e).then(e=>e.data),O=(e,t)=>i.a.post(n+"/api/risk/update",t,{headers:e}).then(e=>e.data),B=(e,t)=>i.a.post(n+"/api/risk/add",t,{headers:e}).then(e=>e.data),E=(e,t)=>i.a.post(n+"/api/risk/add",t,{headers:e}).then(e=>e.data),N=(e,t)=>i.a.post(n+"/api/risk/del",t,e).then(e=>e.data),q=(e,t)=>i.a.get(n+"/api/risk ",{params:t},e).then(e=>e.data),Y=(e,t)=>i.a.post(n+"/api/jira/figure ",t,e).then(e=>e.data),A=(e,t)=>i.a.get(n+"/api/todo ",{params:t},e).then(e=>e.data),J=(e,t)=>i.a.get(n+"/api/report ",{params:t},e).then(e=>e.data),M=(e,t)=>i.a.post(n+"/api/addreport",t,e).then(e=>e.data),R=(e,t)=>i.a.post(n+"/api/updatereport",t,e).then(e=>e.data),I=(e,t)=>i.a.post(n+"/api/delreport",t,e).then(e=>e.data),G=(e,t)=>i.a.post(n+"/api/send",t,e).then(e=>e.data),H=(e,t)=>i.a.post(n+"/api/tool/stresstool",t,e).then(e=>e.data),K=(e,t)=>i.a.get(n+"/api/tool/version",{params:t},{headers:e}).then(e=>e.data),L=(e,t)=>i.a.post(n+"/api/tool/del_stressdata",t,e).then(e=>e.data),Q=(e,t)=>i.a.post(n+"/api/tool/update_stressdata",t,e).then(e=>e.data),U=(e,t)=>i.a.post(n+"/api/tool/add_stressdata",t,e).then(e=>e.data),W=(e,t)=>i.a.get(n+"/api/tool/stressversion",{params:t},{headers:e}).then(e=>e.data),X=(e,t)=>i.a.get(n+"/api/tool/stressdata",{params:t},{headers:e}).then(e=>e.data),Z=(e,t)=>i.a.post(n+"/api/tool/stressresult",t,e).then(e=>e.data),ee=(e,t)=>i.a.post(n+"/api/tool/stressfigure",t,e).then(e=>e.data),te=(e,t)=>i.a.post(n+"/api/tool/delete_patients",t,e).then(e=>e.data),ae=(e,t)=>i.a.get(n+"/api/tool/getduration",{params:t},{headers:e}).then(e=>e.data),re=(e,t)=>i.a.get(n+"/api/tool/durationData",{params:t},{headers:e}).then(e=>e.data),ie=(e,t)=>i.a.post(n+"/api/tool/add_duration",t,e).then(e=>e.data),ne=(e,t)=>i.a.post(n+"/api/tool/update_duration",t,e).then(e=>e.data),se=(e,t)=>i.a.post(n+"/api/tool/del_duration",t,e).then(e=>e.data),oe=(e,t)=>i.a.post(n+"/api/tool/enable_duration",t,e).then(e=>e.data),le=(e,t)=>i.a.post(n+"/api/tool/disable_duration",t,e).then(e=>e.data),de=(e,t)=>i.a.get(n+"/api/tool/duration_verify",{params:t},{headers:e}).then(e=>e.data),ce=(e,t)=>i.a.get(n+"/api/base/getdata",{params:t},{headers:e}).then(e=>e.data),pe=(e,t)=>i.a.post(n+"/api/base/addData",t,e).then(e=>e.data),ue=(e,t)=>i.a.post(n+"/api/base/updateData",t,e).then(e=>e.data),me=(e,t)=>i.a.post(n+"/api/base/enablebase",t,e).then(e=>e.data),he=(e,t)=>i.a.post(n+"/api/base/disablebase",t,e).then(e=>e.data),fe=(e,t)=>i.a.post(n+"/api/base/delbasedata",t,e).then(e=>e.data)},8829:function(e,t,a){},8876:function(e,t,a){"use strict";a.r(t);var r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"table"},[a("div",{staticClass:"crumbs"},[a("el-breadcrumb",{attrs:{separator:"/"}},[a("el-breadcrumb-item",[a("i",{staticClass:"el-icon-lx-cascades"}),e._v("测试项目版本")])],1)],1),a("div",{staticClass:"container"},[a("div",{staticClass:"handle-box",staticStyle:{clear:"both","margin-bottom":"80px"}},[a("div",{staticClass:"add",staticStyle:{float:"left"}},[a("el-button",{staticClass:"handle-del mr10",attrs:{type:"primary",icon:"add"},on:{click:function(t){return e.handleAdd()}}},[e._v("添加")])],1),a("div",{staticClass:"search",staticStyle:{float:"left"}},[a("el-form",{ref:"searchform",attrs:{model:e.searchform,"label-width":"100px"}},[a("el-select",{staticClass:"handle-select mr10",attrs:{clearable:"",placeholder:"筛选",prop:"select_app"},model:{value:e.searchform.select_app,callback:function(t){e.$set(e.searchform,"select_app",t)},expression:"searchform.select_app"}},[a("el-option",{key:"Boimind",attrs:{label:"Boimind",value:"Boimind"}}),a("el-option",{key:"CoinNess",attrs:{label:"CoinNess",value:"CoinNess"}})],1),a("el-input",{staticClass:"handle-input mr10",attrs:{prop:"select_version",placeholder:"筛选"},model:{value:e.searchform.select_version,callback:function(t){e.$set(e.searchform,"select_version",t)},expression:"searchform.select_version"}}),a("el-button",{attrs:{type:"primary",icon:"search"},on:{click:function(t){return e.searchProject("searchform")}}},[e._v("搜索")])],1)],1)]),a("el-table",{ref:"multipleTable",staticClass:"table",attrs:{data:e.tableData,border:""},on:{"selection-change":e.handleSelectionChange}},[a("el-table-column",{attrs:{label:"邮件主题",width:"240"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",[e._v(e._s(t.row.title))])]}}])}),a("el-table-column",{attrs:{label:"Boimind版本",width:"150"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.test_version))])]}}])}),a("el-table-column",{attrs:{label:"CoinNess版本",width:"150"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.cns_version))])]}}])}),a("el-table-column",{attrs:{label:"是否发送",width:"100"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.is_send))])]}}])}),a("el-table-column",{attrs:{label:"发送时间",width:"200"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",[e._v(e._s(t.row.send_time))])]}}])}),a("el-table-column",{attrs:{label:"收件人员",width:"300"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.receiver))])]}}])}),a("el-table-column",{attrs:{label:"抄送人员",width:"250",formatter:e.dateFormatter},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.email_cc))])]}}])}),a("el-table-column",{attrs:{label:"操作",width:"180",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-button",{attrs:{type:"text",icon:"el-icon-find"},on:{click:function(a){return e.showRisk(t.$index,t.row)}}},[e._v("查看模板")]),a("el-button",{attrs:{type:"text",icon:"el-icon-edit"},on:{click:function(a){return e.handleEdit(t.$index,t.row)}}},[e._v("编辑")]),a("el-button",{attrs:{type:"text",icon:"el-icon-lx-comment"},on:{click:function(a){return e.handleSend(t.$index,t.row)}}},[e._v("发送")]),a("el-button",{staticClass:"red",attrs:{type:"text",icon:"el-icon-delete"},on:{click:function(a){return e.handleDelete(t.$index,t.row)}}},[e._v("删除")])]}}])})],1),a("div",{staticClass:"pagination"},[a("el-pagination",{attrs:{"current-page":e.currentPage,"page-sizes":[10,20,30,40],"page-size":100,layout:"total, sizes, prev, pager, next, jumper",total:e.currentTotal},on:{"size-change":e.handleSizeChange,"current-change":e.handleCurrentChange}})],1)],1),a("el-dialog",{attrs:{title:"编辑",visible:e.editVisible,width:"30%"},on:{"update:visible":function(t){e.editVisible=t}}},[a("el-form",{ref:"editform",attrs:{model:e.editform,"label-width":"100px"}},[a("el-form-item",{attrs:{label:"ID"}},[a("el-input",{attrs:{disabled:!0,width:"5%"},model:{value:e.editform.id,callback:function(t){e.$set(e.editform,"id",t)},expression:"editform.id"}})],1),a("el-form-item",{attrs:{label:"邮件主题"}},[a("el-input",{model:{value:e.editform.title,callback:function(t){e.$set(e.editform,"title",t)},expression:"editform.title"}})],1),a("el-form-item",{attrs:{label:"Boimind版本"}},[a("el-input",{model:{value:e.editform.test_version,callback:function(t){e.$set(e.editform,"test_version",t)},expression:"editform.test_version"}})],1),a("el-form-item",{attrs:{label:"CoinNess版本"}},[a("el-input",{model:{value:e.editform.cns_version,callback:function(t){e.$set(e.editform,"cns_version",t)},expression:"editform.cns_version"}})],1),a("el-form-item",{attrs:{label:"是否发送"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.editform.is_send,callback:function(t){e.$set(e.editform,"is_send",t)},expression:"editform.is_send"}},[a("el-option",{key:"1",attrs:{label:"是",value:"1"}}),a("el-option",{key:"0",attrs:{label:"否",value:"0"}})],1)],1),a("el-form-item",{attrs:{label:"发送时间"}},[a("el-date-picker",{attrs:{type:"datetime",placeholder:"选择日期"},model:{value:e.editform.send_time,callback:function(t){e.$set(e.editform,"send_time",t)},expression:"editform.send_time"}})],1),a("el-form-item",{attrs:{label:"收件人员"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.editform.receiver,callback:function(t){e.$set(e.editform,"receiver",t)},expression:"editform.receiver"}},[a("el-option",{key:"test",attrs:{label:"测试",value:"test"}}),a("el-option",{key:"on",attrs:{label:"正式",value:"on"}})],1)],1),a("el-form-item",{attrs:{label:"抄送人员"}},[a("el-input",{model:{value:e.editform.email_cc,callback:function(t){e.$set(e.editform,"email_cc",t)},expression:"editform.email_cc"}})],1)],1),a("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(t){e.editVisible=!1}}},[e._v("取 消")]),a("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.saveEdit(e.editform)}}},[e._v("确 定")])],1)],1),a("el-dialog",{attrs:{title:"添加",rules:e.rules,visible:e.dialogFormVisible,width:"30%"},on:{"update:visible":function(t){e.dialogFormVisible=t}}},[a("el-form",{ref:"addForm",attrs:{model:e.addForm,rules:e.rules,"label-width":"120px"}},[a("el-form-item",{attrs:{label:"邮件主题",prop:"title"}},[a("el-input",{model:{value:e.addForm.title,callback:function(t){e.$set(e.addForm,"title",t)},expression:"addForm.title"}})],1),a("el-form-item",{attrs:{label:"Boimind版本",prop:"title"}},[a("el-input",{model:{value:e.addForm.title,callback:function(t){e.$set(e.addForm,"title",t)},expression:"addForm.title"}})],1),a("el-form-item",{attrs:{label:"CoinNess版本",prop:"title"}},[a("el-input",{model:{value:e.addForm.title,callback:function(t){e.$set(e.addForm,"title",t)},expression:"addForm.title"}})],1),a("el-form-item",{attrs:{label:"是否发送",prop:"development_progress"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.addForm.development_progress,callback:function(t){e.$set(e.addForm,"development_progress",t)},expression:"addForm.development_progress"}},[a("el-option",{key:"0",attrs:{label:"否",value:"-"}}),a("el-option",{key:"1",attrs:{label:"是",value:"1"}})],1)],1),a("el-form-item",{attrs:{label:"发送时间",prop:"start_date"}},[a("el-date-picker",{attrs:{type:"datetime",placeholder:"选择日期"},model:{value:e.addForm.start_date,callback:function(t){e.$set(e.addForm,"start_date",t)},expression:"addForm.start_date"}})],1),a("el-form-item",{attrs:{label:"收件人员",prop:"app"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.addForm.app,callback:function(t){e.$set(e.addForm,"app",t)},expression:"addForm.app"}},[a("el-option",{key:"0",attrs:{label:"ios",value:"0"}}),a("el-option",{key:"1",attrs:{label:"安卓",value:"1"}}),a("el-option",{key:"2",attrs:{label:"所有",value:"2"}})],1)],1),a("el-form-item",{attrs:{label:"抄送人员"}},[a("el-input",{model:{value:e.editform.email_cc,callback:function(t){e.$set(e.editform,"email_cc",t)},expression:"editform.email_cc"}})],1)],1),a("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(t){e.dialogFormVisible=!1}}},[e._v("取 消")]),a("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.addreportconfig("addForm")}}},[e._v("添加")])],1)],1)],1)},i=[],n=a("2d92"),s={name:"basetable",data(){return{rules:{title:[{required:!0,message:"请输邮件主题",trigger:"change"}],receiver:[{required:!0,message:"收件人员",trigger:"change"}],is_send:[{required:!0,message:"是否发送",trigger:"change"}],email_cc:[{required:!0,message:"抄送人员",trigger:"change"}]},tableData:[],cur_page:1,multipleSelection:[],select_cate:"",select_word:"",del_list:[],is_search:!1,editVisible:!1,delVisible:!1,dialogFormVisible:!1,form:{title:"",test_version:"",cns_version:""},editform:{title:"",test_version:"",cns_version:""},addForm:{title:"",test_version:"",cns_version:""},searchform:{},currentPage:1,pageSize:10,currentTotal:0}},created(){this.getData()},computed:{data(){return this.tableData.filter(e=>{let t=!1;for(let a=0;a<this.del_list.length;a++)if(e.name===this.del_list[a].name){t=!0;break}if(!t&&e.address.indexOf(this.select_cate)>-1&&(e.name.indexOf(this.select_word)>-1||e.address.indexOf(this.select_word)>-1))return e})}},methods:{showRisk(e,t){this.$router.push({path:"/risk",query:{project_id:t.project_id,project:t.project}})},handleSizeChange(e){this.pageSize=e,console.log(`每页 ${e} 条`),this.getData()},handleCurrentChange(e){this.currentPage=e,console.log(`这是第${e}页`),this.getData()},getData(e,t){let a={page:this.currentPage,page_size:this.pageSize,name:e,version:t},r={"Content-Type":"application/x-www-form-urlencoded"};Object(n["bb"])(r,a).then(e=>{let{msg:t,data:a,code:r}=e;this.currentTotal=a.total,this.tableData=a.data})},search(){this.is_search=!0},dateFormatter(e,t){console.log("格式化日期");var a=e[t.property];return void 0==a?"":moment(data).format("YYYY-MM-DD")},filterTag(e,t){return t.tag===e},handleAdd(){this.dialogFormVisible=!0,this.addForm={id:null,test_version:null,cns_version:null,receiver:null,is_send:null,send_time:null,email_cc:null,title:null,template:null}},addreportconfig(e){console.log(e),this.$refs[e].validate(e=>{if(!e)return console.log("error submit!!"),!1;{let e={test_version:this.addForm.test_version,cns_version:this.addForm.cns_version,receiver:this.addForm.receiver,is_send:this.addForm.is_send,send_time:this.addForm.send_time,email_cc:this.addForm.email_cc,title:this.addForm.title,template:this.addForm.template};console.log(e);let t={"Content-Type":"application/json"};addTestProject(t,e).then(e=>{let{msg:t,code:a,data:r}=e;console.log("code:"+a),"0"==a?(this.$message.success("添加成功"),this.dialogFormVisible=!1,this.getData()):this.$message.error(t)})}})},handleEdit(e,t){this.idx=e;const a=this.tableData[e];this.editform={id:a.id,test_version:a.test_version,cns_version:a.cns_version,title:a.title,receiver:a.receiver,is_send:a.is_send,send_time:a.send_time,email_cc:a.email_cc,template:""},this.editVisible=!0},handleEdit(e,t){this.idx=e;const a=this.tableData[e];this.editform={id:a.id,test_version:a.test_version,cns_version:a.cns_version,title:a.title,receiver:a.receiver,is_send:a.is_send,send_time:a.send_time,email_cc:a.email_cc,template:""},this.editVisible=!0},handleDelete(e,t){this.idx=e;const a=this.tableData[e];let r=[a.id],i={ids:r},n={"Content-Type":"application/json"};deleteTestProject(n,i).then(e=>{let{msg:t,code:a,data:r}=e;"0"==a?null==r||r[0]?(this.$message.success("删除成功！"),this.getData()):this.$message.error(r[1]):this.$message.error(t)})},handleSend(e,t){this.idx=e;const a=this.tableData[e];let r=a.id,i={id:r,type:1,start_time:"",endtime:""},s={"Content-Type":"application/json"};Object(n["d"])(s,i).then(e=>{let{msg:t,code:a,data:r}=e;"0"==a?null==r||r[0]?(this.$message.success("发送成功！"),this.getData()):this.$message.error(r[1]):this.$message.error(t)})},handleSelectionChange(e){this.multipleSelection=e},searchProject(e){let t=this.searchform.select_app,a=this.searchform.select_version,r=/^\d+\.\d+\.\d+$/;if("undefined"==typeof t&&"undefined"==typeof a)return void alert("请输入要搜索的版本号或者版本号");let i=typeof a;"undefined"==i||null==i||""==i||r.test(a)?this.getData(t,a):alert("请输入格式为x.x.x的版本号")},saveEdit(e){let t={id:e.id,test_version:e.test_version,cns_version:e.cns_version,receiver:e.receiver,is_send:e.is_send,send_time:e.send_time,email_cc:e.email_cc,title:e.title,template:""},a={"Content-Type":"application/json"};Object(n["lb"])(a,t).then(e=>{let{msg:t,code:a,data:r}=e;"0"==a?null==r||r[0]?(this.$message.success("编辑成功"),this.editVisible=!1,this.getData()):this.$message.error(r[1]):this.$message.error(t)})}}},o=s,l=(a("ca4f"),a("2877")),d=Object(l["a"])(o,r,i,!1,null,"435235b7",null);t["default"]=d.exports},ca4f:function(e,t,a){"use strict";var r=a("8829"),i=a.n(r);i.a}}]);