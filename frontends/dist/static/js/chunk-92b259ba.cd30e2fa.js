(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-92b259ba"],{"0fe1":function(e,t,a){"use strict";var s=a("3e17"),n=a.n(s);n.a},2661:function(e,t,a){"use strict";a.r(t);var s=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"app-container"},[a("div",{staticClass:"filter-container"},[a("el-col",{staticClass:"toolbar",staticStyle:{"padding-bottom":"0px"},attrs:{span:20}},[a("el-form",{attrs:{inline:!0,model:e.filters},nativeOn:{submit:function(e){e.preventDefault()}}},[a("el-form-item",{attrs:{label:"过滤器",prop:"server"}},[a("el-select",{attrs:{placeholder:"请选择服务"},nativeOn:{click:function(t){return e.gethost()}},model:{value:e.filters.server,callback:function(t){e.$set(e.filters,"server",t)},expression:"filters.server"}},e._l(e.tags,(function(e,t){return a("el-option",{key:e.host,attrs:{label:e.name,value:e.host}})})),1)],1),a("el-form-item",[a("el-select",{attrs:{placeholder:"请选择病种类型"},nativeOn:{click:function(t){return e.getBase()}},model:{value:e.filters.diseases,callback:function(t){e.$set(e.filters,"diseases",t)},expression:"filters.diseases"}},e._l(e.tags,(function(e,t){return a("el-option",{key:e.remarks,attrs:{label:e.remarks,value:e.remarks}})})),1)],1),a("el-form-item",[a("el-select",{attrs:{placeholder:"肺炎层厚"},model:{value:e.filters.slicenumber,callback:function(t){e.$set(e.filters,"slicenumber",t)},expression:"filters.slicenumber"}},[a("el-option",{key:"1.0",attrs:{label:"1.0",value:"1.0"}}),a("el-option",{key:"1.25",attrs:{label:"1.25",value:"1.25"}}),a("el-option",{key:"1.5",attrs:{label:"1.5",value:"1.5"}}),a("el-option",{key:"5.0",attrs:{label:"5.0",value:"5.0"}}),a("el-option",{key:"10.0",attrs:{label:"10.0",value:"10.0"}})],1)],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:e.getdata}},[e._v("查询")])],1),a("el-button",{attrs:{type:"warning",disabled:0===this.sels.length},on:{click:e.batchCsv}},[e._v("生成CSV")]),a("el-button",{attrs:{type:"primary"},on:{click:e.getdetail}},[e._v("同步")]),a("el-button",{attrs:{type:"danger",disabled:0===this.sels.length},on:{click:e.batchvote}},[e._v("同步挂载")])],1)],1),a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.listLoading,expression:"listLoading"}],staticStyle:{width:"100%"},attrs:{data:e.stresslist,"highlight-current-row":""},on:{"selection-change":e.selsChange}},[a("el-table-column",{attrs:{type:"selection","min-width":"4%"}}),a("el-table-column",{attrs:{prop:"ID",label:"ID","min-width":"4%"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.id))])]}}])}),a("el-table-column",{attrs:{prop:"patientid",label:"Patientid","min-width":"10%",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.patientid))])]}}])}),a("el-table-column",{attrs:{prop:"studyinstanceuid",label:"Studyinstanceuid","min-width":"25%"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.studyinstanceuid))])]}}])}),a("el-table-column",{attrs:{label:"类型","min-width":"10%",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.diseases))])]}}])}),a("el-table-column",{attrs:{label:"slicenumber","min-width":"10%",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.slicenumber))])]}}])}),a("el-table-column",{attrs:{label:"预测张数","min-width":"10%"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.imagecount))])]}}])}),a("el-table-column",{attrs:{label:"类型","min-width":"10%"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.type))])]}}])}),a("el-table-column",{attrs:{label:"标准诊断","min-width":"15   %"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.diagnosis))])]}}])}),a("el-table-column",{attrs:{label:"操作","min-width":"12px"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-button",{attrs:{type:"warning",size:"small"},on:{click:function(a){return e.handleEdit(t.$index,t.row)}}},[e._v("编辑 ")])]}}])})],1),a("el-col",{staticClass:"toolbar",attrs:{span:24}},[a("el-button",{attrs:{type:"danger",disabled:0===this.sels.length},on:{click:e.batchRemove}},[e._v("批量删除")]),a("el-pagination",{staticStyle:{float:"right"},attrs:{layout:"prev, pager, next","page-size":20,"page-count":e.total},on:{"current-change":e.handleCurrentChange}})],1),a("el-dialog",{staticStyle:{width:"75%",left:"12.5%"},attrs:{title:"编辑",visible:e.editFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(t){e.editFormVisible=t}}},[a("el-form",{ref:"editForm",attrs:{model:e.editForm,"label-width":"80px",rules:e.editFormRules}},[a("el-row",{attrs:{gutter:24}},[a("el-col",{attrs:{span:12}},[a("el-form-item",{attrs:{label:"标注诊断"}},[a("el-input",{model:{value:e.editForm.diagnosis,callback:function(t){e.$set(e.editForm,"diagnosis",t)},expression:"editForm.diagnosis"}})],1)],1),a("el-col",{attrs:{span:12}},[a("el-form-item",{attrs:{label:"病种"}},[a("el-input",{model:{value:e.editForm.diseases,callback:function(t){e.$set(e.editForm,"diseases",t)},expression:"editForm.diseases"}})],1)],1)],1),a("el-row",{attrs:{gutter:24}},[a("el-col",{attrs:{span:12}},[a("el-form-item",{attrs:{label:"层厚"}},[a("el-input",{model:{value:e.editForm.slicenumber,callback:function(t){e.$set(e.editForm,"slicenumber",t)},expression:"editForm.slicenumber"}})],1)],1),a("el-col",{attrs:{span:12}},[a("el-form-item",{attrs:{label:"影像张数"}},[a("el-input",{attrs:{"auto-complete":"off"},model:{value:e.editForm.imagecount,callback:function(t){e.$set(e.editForm,"imagecount",t)},expression:"editForm.imagecount"}})],1)],1)],1),a("el-form-item",{attrs:{label:"挂载"}},[a("el-input",{attrs:{disabled:!0,"auto-complete":"off"},model:{value:e.editForm.vote,callback:function(t){e.$set(e.editForm,"vote",t)},expression:"editForm.vote"}})],1)],1),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{nativeOn:{click:function(t){e.editFormVisible=!1}}},[e._v("取消")]),a("el-button",{attrs:{type:"primary",loading:e.editLoading},nativeOn:{click:function(t){return e.editSubmit(t)}}},[e._v("提交")])],1)],1),a("el-dialog",{staticStyle:{width:"75%",left:"12.5%"},attrs:{title:"新增",visible:e.addFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(t){e.addFormVisible=t}}},[a("el-form",{ref:"addForm",attrs:{model:e.addForm,"label-width":"80px",rules:e.addFormRules}},[a("el-row",{attrs:{gutter:24}},[a("el-col",{attrs:{span:10}},[a("el-form-item",{attrs:{label:"服务器",prop:"server"}},[a("el-select",{attrs:{placeholder:"请选择"},nativeOn:{click:function(t){return e.gethost()}},model:{value:e.addForm.server,callback:function(t){e.$set(e.addForm,"server",t)},expression:"addForm.server"}},e._l(e.tags,(function(e,t){return a("el-option",{key:e.host,attrs:{label:e.name,value:e.host}})})),1)],1)],1),a("el-col",{attrs:{span:12}},[a("el-form-item",{attrs:{label:"patientid",prop:"patientid"}},[a("el-input",{attrs:{"auto-complete":"off"},model:{value:e.addForm.patientid,callback:function(t){e.$set(e.addForm,"patientid","string"===typeof t?t.trim():t)},expression:"addForm.patientid"}})],1)],1),a("el-col",{attrs:{span:12}},[a("el-form-item",{attrs:{label:"studyinstanceuid",prop:"studyinstanceuid"}},[a("el-input",{attrs:{"auto-complete":"off"},model:{value:e.addForm.studyinstanceuid,callback:function(t){e.$set(e.addForm,"studyinstanceuid","string"===typeof t?t.trim():t)},expression:"addForm.studyinstanceuid"}})],1)],1),a("el-col",{attrs:{span:12}},[a("el-form-item",{attrs:{label:"类型",prop:"diseases"}},[a("el-select",{attrs:{placeholder:"请选择"},nativeOn:{click:function(t){return e.getBase()}},model:{value:e.addForm.diseases,callback:function(t){e.$set(e.addForm,"diseases",t)},expression:"addForm.diseases"}},e._l(e.tags,(function(e,t){return a("el-option",{key:e.remarks,attrs:{label:e.remarks,value:e.remarks}})})),1)],1)],1)],1)],1),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{nativeOn:{click:function(t){e.addFormVisible=!1}}},[e._v("取消")]),a("el-button",{attrs:{type:"primary",loading:e.addLoading},nativeOn:{click:function(t){return e.addSubmit(t)}}},[e._v("提交")])],1)],1)],1)])},n=[],r=a("2d92"),i={data(){return{filters:{diseases:null,slicenumber:null},total:0,page:1,listLoading:!1,sels:[],editFormRules:{diagnosis:[{required:!0,message:"请输入名称",trigger:"blur"},{min:1,max:500,message:"长度在 1 到 50 个字符",trigger:"blur"}],type:[{required:!0,message:"请选择类型",trigger:"blur"}],slicenumber:[{required:!1,message:"请输入",trigger:"blur"},{max:1024,message:"不能超过1024个字符",trigger:"blur"}]},editForm:{diseases:"",slicenumber:"",type:"",diagnosis:""},editFormVisible:!1,editLoading:!1,addForm:{diseases:"",server:"192.168.1.208",studyinstanceuid:""},addFormVisible:!1,addLoading:!1,addFormRules:{diseases:[{required:!0,message:"请输入名称",trigger:"blur"},{min:1,max:50,message:"长度在 1 到 50 个字符",trigger:"blur"}]}}},mounted(){this.getdata(),this.gethost()},methods:{gethost(){this.listLoading=!0;const e=this,t={},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(r["P"])(a,t).then(t=>{e.listLoading=!1;const{msg:a,code:s,data:n}=t;if("0"===s){e.total=n.total,e.list=n.data;var r=JSON.stringify(e.list);this.tags=JSON.parse(r)}else e.$message.error({message:a,center:!0})})},getBase(){this.listLoading=!0;const e=this,t={selecttype:"dicom",status:1},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(r["Y"])(a,t).then(t=>{e.listLoading=!1;const{msg:a,code:s,data:n}=t;if("0"===s){e.total=n.total,e.list=n.data;var r=JSON.stringify(e.list);this.tags=JSON.parse(r)}else e.$message.error({message:a,center:!0})})},run(e){this.tableData=null,this.$refs[e].validate(e=>{if(!e)return console.log("error submit"),!1;{const e={version:this.form.version,loadserver:this.form.Loadserver,loop_time:this.form.loop_time,testdata:this.form.testdata,duration:this.form.duration,keyword:this.form.keyword},t={"Content-Type":"application/json"};Object(r["nb"])(t,e).then(e=>{console.log(this.form.testdata);const{msg:t,code:a,data:s}=e;if("0"==a){var n=s[0];if(null==s||0!=n){for(var r=s[1],i=[],o=0;o<r.length;o++)i.push({name:r[o]});var l=JSON.stringify(i);this.tableData=JSON.parse(l)}else this.$message.error(s[1])}else this.$message.error(t)})}})},getdata(){this.listLoading=!0;const e=this,t={page:e.page,diseases:e.filters.diseases,server:e.filters.server,slicenumber:e.filters.slicenumber,type:"Gold"},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(r["ab"])(a,t).then(t=>{e.listLoading=!1;const{msg:a,code:s,data:n}=t;"0"===s?(e.total=n.total,e.page=n.page,e.stresslist=n.data):e.$message.error({message:a,center:!0})})},handleDel:function(e,t){this.$confirm("确认删除该记录吗?","提示",{type:"warning"}).then(()=>{this.listLoading=!0;const e=this,a={ids:[t.id]},s={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(r["w"])(s,a).then(t=>{const{msg:a,code:s,data:n}=t;"0"===s?e.$message({message:"删除成功",center:!0,type:"success"}):e.$message.error({message:a,center:!0}),e.getdata()})})},handleCurrentChange(e){this.page=e,this.getdata()},handleEdit:function(e,t){this.editFormVisible=!0,this.editForm=Object.assign({},t)},handleAdd:function(){this.addFormVisible=!0,this.addForm={patientid:null,diseases:null,studyinstanceuid:null}},editSubmit:function(){const e=this;this.$refs.editForm.validate(t=>{t&&this.$confirm("确认提交吗？","提示",{}).then(()=>{e.editLoading=!0;const t={id:e.editForm.id,diseases:e.editForm.diseases,slicenumber:e.editForm.slicenumber,vote:e.editForm.vote,diagnosis:e.editForm.diagnosis,imagecount:e.editForm.imagecount},a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(r["vb"])(a,t).then(t=>{const{msg:a,code:s,data:n}=t;e.editLoading=!1,"0"===s?(e.$message({message:"修改成功",center:!0,type:"success"}),e.$refs["editForm"].resetFields(),e.editFormVisible=!1,e.getdata()):e.$message.error({message:a,center:!0})})})})},getdetail(){this.listLoading=!0;const e=this,t={diseases:e.filters.diseases,server:e.filters.server,type:e.filters.type,ids:""},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(r["E"])(a,t).then(t=>{e.listLoading=!1;const{msg:a,code:s,data:n}=t;"0"===s?(e.total=n.total,e.page=n.page,e.stresslist=n.data):e.$message.error({message:a,center:!0})})},addSubmit:function(){this.$refs.addForm.validate(e=>{if(e){const e=this;this.$confirm("确认提交吗？","提示",{}).then(()=>{e.addLoading=!0;const t=JSON.stringify({diseases:e.addForm.diseases,patientid:e.addForm.patientid,server:e.addForm.server,studyinstanceuid:e.addForm.studyinstanceuid}),a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(r["o"])(a,t).then(t=>{const{msg:a,code:s,data:n}=t;e.addLoading=!1,"0"===s?(e.$message({message:"添加成功",center:!0,type:"success"}),e.$refs["addForm"].resetFields(),e.addFormVisible=!1,e.getdata()):"999997"===s?e.$message.error({message:a,center:!0}):(e.$message.error({message:a,center:!0}),e.$refs["addForm"].resetFields(),e.addFormVisible=!1,e.getdata())})})}})},selsChange:function(e){this.sels=e},cancelEdit(e){e.title=e.originalTitle,e.edit=!1,this.$message({message:"The title has been restored to the original value",type:"warning"})},confirmEdit(e){e.edit=!1,e.originalTitle=e.title,this.$message({message:"The title has been edited",type:"success"})},batchRemove:function(){const e=this.sels.map(e=>e.id);this.$confirm("确认删除选中记录吗？","提示",{type:"warning"}).then(()=>{this.listLoading=!0;const t=this,a={ids:e},s={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(r["w"])(s,a).then(e=>{const{msg:a,code:s,data:n}=e;"0"===s?t.$message({message:"删除成功",center:!0,type:"success"}):t.$message.error({message:a,center:!0}),t.getdata()})})},batchCsv:function(){const e=this.sels.map(e=>e.id);this.$confirm("确认生成选中记录吗？","提示",{type:"warning"}).then(()=>{this.listLoading=!0;const t=this,a={ids:e},s={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(r["D"])(s,a).then(e=>{const{msg:a,code:s,data:n}=e;"0"===s?t.$message({message:"生成成功",center:!0,type:"success"}):t.$message.error({message:a,center:!0}),t.getdata()})})},batchDel:function(){const e=this.sels.map(e=>e.id);this.$confirm("确认删除选中记录的报告吗？","提示",{type:"warning"}).then(()=>{this.listLoading=!0;const t=this,a={ids:e},s={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(r["x"])(s,a).then(e=>{const{msg:a,code:s,data:n}=e;"0"===s?t.$message({message:"删除成功",center:!0,type:"success"}):t.$message.error({message:a,center:!0}),t.getdata()})})}}},o=i,l=(a("0fe1"),a("2877")),d=Object(l["a"])(o,s,n,!1,null,"69d1be04",null);t["default"]=d.exports},"2d92":function(e,t,a){"use strict";a.d(t,"qb",(function(){return r})),a.d(t,"Q",(function(){return i})),a.d(t,"v",(function(){return o})),a.d(t,"G",(function(){return l})),a.d(t,"K",(function(){return d})),a.d(t,"tb",(function(){return u})),a.d(t,"k",(function(){return c})),a.d(t,"R",(function(){return p})),a.d(t,"P",(function(){return m})),a.d(t,"u",(function(){return h})),a.d(t,"F",(function(){return g})),a.d(t,"J",(function(){return f})),a.d(t,"sb",(function(){return b})),a.d(t,"j",(function(){return v})),a.d(t,"S",(function(){return y})),a.d(t,"T",(function(){return k})),a.d(t,"O",(function(){return _})),a.d(t,"t",(function(){return F})),a.d(t,"i",(function(){return S})),a.d(t,"U",(function(){return $})),a.d(t,"W",(function(){return w})),a.d(t,"V",(function(){return x})),a.d(t,"g",(function(){return j})),a.d(t,"N",(function(){return O})),a.d(t,"h",(function(){return C})),a.d(t,"rb",(function(){return D})),a.d(t,"s",(function(){return L})),a.d(t,"I",(function(){return I})),a.d(t,"mb",(function(){return T})),a.d(t,"ub",(function(){return J})),a.d(t,"l",(function(){return N})),a.d(t,"L",(function(){return z})),a.d(t,"z",(function(){return V})),a.d(t,"jb",(function(){return A})),a.d(t,"lb",(function(){return q})),a.d(t,"kb",(function(){return E})),a.d(t,"q",(function(){return R})),a.d(t,"xb",(function(){return B})),a.d(t,"B",(function(){return P})),a.d(t,"d",(function(){return G})),a.d(t,"ob",(function(){return Y})),a.d(t,"m",(function(){return H})),a.d(t,"e",(function(){return K})),a.d(t,"nb",(function(){return M})),a.d(t,"X",(function(){return Q})),a.d(t,"pb",(function(){return U})),a.d(t,"w",(function(){return W})),a.d(t,"vb",(function(){return X})),a.d(t,"o",(function(){return Z})),a.d(t,"E",(function(){return ee})),a.d(t,"ab",(function(){return te})),a.d(t,"D",(function(){return ae})),a.d(t,"x",(function(){return se})),a.d(t,"ib",(function(){return ne})),a.d(t,"hb",(function(){return re})),a.d(t,"eb",(function(){return ie})),a.d(t,"A",(function(){return oe})),a.d(t,"bb",(function(){return le})),a.d(t,"cb",(function(){return de})),a.d(t,"p",(function(){return ue})),a.d(t,"wb",(function(){return ce})),a.d(t,"y",(function(){return pe})),a.d(t,"r",(function(){return me})),a.d(t,"M",(function(){return he})),a.d(t,"H",(function(){return ge})),a.d(t,"db",(function(){return fe})),a.d(t,"fb",(function(){return be})),a.d(t,"gb",(function(){return ve})),a.d(t,"Z",(function(){return ye})),a.d(t,"Y",(function(){return ke})),a.d(t,"n",(function(){return _e})),a.d(t,"f",(function(){return Fe})),a.d(t,"c",(function(){return Se})),a.d(t,"b",(function(){return $e})),a.d(t,"a",(function(){return we})),a.d(t,"C",(function(){return xe}));var s=a("bc3a"),n=a.n(s);a("c896");const r="http://192.168.1.121:9000",i=(e,t)=>n.a.get(r+"/api/project/project_list",{params:t,headers:e}).then(e=>e.data),o=(e,t)=>n.a.post(r+"/api/project/del_project",t,{headers:e}).then(e=>e.data),l=(e,t)=>n.a.post(r+"/api/project/disable_project",t,{headers:e}).then(e=>e.data),d=(e,t)=>n.a.post(r+"/api/project/enable_project",t,{headers:e}).then(e=>e.data),u=(e,t)=>n.a.post(r+"/api/project/update_project",t,{headers:e}).then(e=>e.data),c=(e,t)=>n.a.post(r+"/api/project/add_project",t,{headers:e}).then(e=>e.data),p=(e,t)=>n.a.get(r+"/api/title/project_info",{params:t,headers:e}).then(e=>e.data),m=(e,t)=>n.a.get(r+"/api/global/host_total",{params:t,headers:e}).then(e=>e.data),h=(e,t)=>n.a.post(r+"/api/global/del_host",t,{headers:e}).then(e=>e.data),g=(e,t)=>n.a.post(r+"/api/global/disable_host",t,{headers:e}).then(e=>e.data),f=(e,t)=>n.a.post(r+"/api/global/enable_host",t,{headers:e}).then(e=>e.data),b=(e,t)=>n.a.post(r+"/api/global/update_host",t,{headers:e}).then(e=>e.data),v=(e,t)=>n.a.post(r+"/api/global/add_host",t,{headers:e}).then(e=>e.data),y=(e,t)=>n.a.get(r+"/api/dynamic/dynamic",{params:t,headers:e}).then(e=>e.data),k=(e,t)=>n.a.get(r+"/api/member/project_member",{params:t,headers:e}).then(e=>e.data),_=(e,t)=>n.a.get(r+"/api/member/get_email",{params:t,headers:e}).then(e=>e.data),F=(e,t)=>n.a.post(r+"/api/member/del_email",t,{headers:e}).then(e=>e.data),S=(e,t)=>n.a.post(r+"/api/member/email_config",t,{headers:e}).then(e=>e.data),$=(e,t)=>n.a.get(r+"/api/report/auto_test_report",{params:t,headers:e}).then(e=>e.data),w=(e,t)=>n.a.get(r+"/api/report/test_time",{params:t,headers:e}).then(e=>e.data),x=(e,t)=>n.a.get(r+"/api/report/lately_ten",{params:t,headers:e}).then(e=>e.data),j=(e,t)=>n.a.post(r+"/api/api/add_api",t,{headers:e}).then(e=>e.data),O=(e,t)=>n.a.get(r+"/api/api/group",{params:t,headers:e}).then(e=>e.data),C=(e,t)=>n.a.post(r+"/api/api/add_group",t,{headers:e}).then(e=>e.data),D=(e,t)=>n.a.post(r+"/api/api/update_name_group",t,{headers:e}).then(e=>e.data),L=(e,t)=>n.a.post(r+"/api/api/del_group",t,{headers:e}).then(e=>e.data),I=(e,t)=>n.a.post(r+"/api/download",t,{headers:e}).then(e=>e.data),T=(e,t)=>n.a.post(r+"/api/user/login",t,e).then(e=>e.data),J=(e,t)=>n.a.post(r+"/api/risk/update",t,{headers:e}).then(e=>e.data),N=(e,t)=>n.a.post(r+"/api/risk/add",t,{headers:e}).then(e=>e.data),z=(e,t)=>n.a.post(r+"/api/risk/add",t,{headers:e}).then(e=>e.data),V=(e,t)=>n.a.post(r+"/api/risk/del",t,e).then(e=>e.data),A=(e,t)=>n.a.get(r+"/api/risk ",{params:t},e).then(e=>e.data),q=(e,t)=>n.a.get(r+"/api/todo ",{params:t},e).then(e=>e.data),E=(e,t)=>n.a.get(r+"/api/report ",{params:t},e).then(e=>e.data),R=(e,t)=>n.a.post(r+"/api/addreport",t,e).then(e=>e.data),B=(e,t)=>n.a.post(r+"/api/updatereport",t,e).then(e=>e.data),P=(e,t)=>n.a.post(r+"/api/delreport",t,e).then(e=>e.data),G=(e,t)=>n.a.post(r+"/api/send",t,e).then(e=>e.data),Y=(e,t)=>n.a.get(r+"/api/stress/list",{params:t},{headers:e}).then(e=>e.data),H=(e,t)=>n.a.post(r+"/api/stress/add",t,e).then(e=>e.data),K=(e,t)=>n.a.get(r+"/api/stress/stressDetail ",{params:t},e).then(e=>e.data),M=(e,t)=>n.a.post(r+"/api/stress/stresstool",t,e).then(e=>e.data),Q=(e,t)=>n.a.get(r+"/api/stress/version",{params:t},{headers:e}).then(e=>e.data),U=(e,t)=>n.a.post(r+"/api/stress/stresssave",t,e).then(e=>e.data),W=(e,t)=>n.a.post(r+"/api/tool/del_dicomData",t,e).then(e=>e.data),X=(e,t)=>n.a.post(r+"/api/dicom/update",t,e).then(e=>e.data),Z=(e,t)=>n.a.post(r+"/api/tool/add_dicomData",t,e).then(e=>e.data),ee=(e,t)=>n.a.post(r+"/api/tool/dicomdetail",t,e).then(e=>e.data),te=(e,t)=>n.a.get(r+"/api/tool/dicomData",{params:t},{headers:e}).then(e=>e.data),ae=(e,t)=>n.a.post(r+"/api/tool/dicomcsv",t,e).then(e=>e.data),se=(e,t)=>n.a.post(r+"/api/tool/delreport",t,e).then(e=>e.data),ne=(e,t)=>n.a.get(r+"/api/stress/stressversion",{params:t},{headers:e}).then(e=>e.data),re=(e,t)=>n.a.post(r+"/api/stress/stressresult",t,e).then(e=>e.data),ie=(e,t)=>n.a.post(r+"/api/stress/stressfigure",t,e).then(e=>e.data),oe=(e,t)=>n.a.post(r+"/api/tool/delete_patients",t,e).then(e=>e.data),le=(e,t)=>n.a.get(r+"/api/tool/getduration",{params:t},{headers:e}).then(e=>e.data),de=(e,t)=>n.a.get(r+"/api/tool/durationData",{params:t},{headers:e}).then(e=>e.data),ue=(e,t)=>n.a.post(r+"/api/tool/add_duration",t,e).then(e=>e.data),ce=(e,t)=>n.a.post(r+"/api/tool/update_duration",t,e).then(e=>e.data),pe=(e,t)=>n.a.post(r+"/api/tool/del_duration",t,e).then(e=>e.data),me=(e,t)=>n.a.post(r+"/api/tool/anonymization",t,e).then(e=>e.data),he=(e,t)=>n.a.post(r+"/api/tool/enable_duration",t,e).then(e=>e.data),ge=(e,t)=>n.a.post(r+"/api/tool/disable_duration",t,e).then(e=>e.data),fe=(e,t)=>n.a.get(r+"/api/tool/duration_verify",{params:t},{headers:e}).then(e=>e.data),be=(e,t)=>n.a.get(r+"/api/tool/somkerecord",{params:t},{headers:e}).then(e=>e.data),ve=(e,t)=>n.a.post(r+"/api/tool/somke",t,e).then(e=>e.data),ye=(e,t)=>n.a.post(r+"/api/tool/dicomSend",t,e).then(e=>e.data),ke=(e,t)=>n.a.get(r+"/api/base/getdata",{params:t},{headers:e}).then(e=>e.data),_e=(e,t)=>n.a.post(r+"/api/base/addData",t,e).then(e=>e.data),Fe=(e,t)=>n.a.post(r+"/api/base/updateData",t,e).then(e=>e.data),Se=(e,t)=>n.a.post(r+"/api/base/enablebase",t,e).then(e=>e.data),$e=(e,t)=>n.a.post(r+"/api/base/disablebase",t,e).then(e=>e.data),we=(e,t)=>n.a.post(r+"/api/base/delbasedata",t,e).then(e=>e.data),xe=(e,t)=>n.a.get(r+"/api/base/dicom",{params:t},{headers:e}).then(e=>e.data)},"3e17":function(e,t,a){},"41d3":function(e,t,a){},c896:function(e,t,a){"use strict";var s=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("div",{staticClass:"crumbs"},[a("el-breadcrumb",{attrs:{separator:"/"}},[a("el-breadcrumb-item",[a("i",{staticClass:"el-icon-lx-calendar"}),e._v(" 测试工具")]),a("el-breadcrumb-item",[e._v("推送工具")])],1)],1),a("div",{staticClass:"container"},[a("div",{staticClass:"form-box"},[a("el-form",{ref:"form",attrs:{model:e.form,"status-icon":"",rules:e.rules,"label-width":"80px"}},[a("el-form-item",{attrs:{label:"推送ID",prop:"pushID"}},[a("el-col",{attrs:{span:10}},[a("el-input",{attrs:{id:"pushID"},model:{value:e.form.pushID,callback:function(t){e.$set(e.form,"pushID",t)},expression:"form.pushID"}})],1)],1),a("el-form-item",{attrs:{label:"推送环境",prop:"environment"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.form.environment,callback:function(t){e.$set(e.form,"environment",t)},expression:"form.environment"}},[a("el-option",{key:"test",attrs:{label:"测试环境",value:"test"}}),a("el-option",{key:"online",attrs:{label:"线上环境",value:"online"}})],1)],1),a("el-form-item",{attrs:{label:"推送类型",prop:"types"}},[a("el-cascader",{attrs:{options:e.types},on:{change:function(t){return e.changeLang("form")}},model:{value:e.form.types,callback:function(t){e.$set(e.form,"types",t)},expression:"form.types"}})],1),a("el-form-item",{attrs:{label:"选择语言",prop:"languages"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.form.languages,callback:function(t){e.$set(e.form,"languages",t)},expression:"form.languages"}},e._l(e.languages,(function(e,t){return a("el-option",{key:e.key,attrs:{label:e.value,value:e.key}})})),1)],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.onSubmit("form")}}},[e._v("确定推送")]),a("el-button",{on:{click:function(t){return e.resetForm("form")}}},[e._v("重置")])],1)],1)],1)])])},n=[],r={name:"baseform",data:function(){return{types:[{value:"bishijie",label:"Boimind",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"replay",label:"币圈"},{value:"monitor",label:"盯盘"}]},{value:"coinness",label:"coinness",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"monitor",label:"盯盘"}]}],languages:[],form:{pushID:"",environment:"",types:[],languages:[]},rules:{pushID:[{required:!0,message:"请输入推送ID",trigger:"blur"}],environment:[{required:!0,message:"请选择推送环境",trigger:"blur"}],types:[{required:!0,message:"请选择推送类型",trigger:"blur"}],languages:[{required:!0,message:"请选择语言",trigger:"blur"}]}}},methods:{onSubmit(e){this.$refs[e].validate(e=>{if(!e)return console.log("error submit"),!1;console.log("语言："+this.form.languages),console.log("pushID："+this.form.pushID),console.log("APP："+this.form.types[0]),console.log("推送类型："+this.form.types[1]),console.log("environment："+this.form.environment),this.$ajax.post("/bishijie/push",{id:this.form.pushID,service:this.form.environment,system:this.form.types[0],module:this.form.types[1],lang:this.form.languages,rid:""}).then(e=>{"0"==e.data.code?null==e.data.data||e.data.data[0]?this.$message.success("push成功！"):this.$message.error(e.data.data[1]):this.$message.error(e.data.msg)}).catch((function(e){console.log(e)}))})},resetForm(e){this.$refs[e].resetFields()},changeLang(e){this.languages=[],this.form.languages="";var t=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"}],a=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"},{key:"en_go",value:"English"},{key:"ko_kr",value:"한글"}],s=this.form.types[0].toLowerCase();"bishijie"==s?this.languages=t:"coinness"==s&&(this.languages=a)}}},i=r,o=(a("cd97"),a("2877")),l=Object(o["a"])(i,s,n,!1,null,"6d8efc95",null);l.exports},cd97:function(e,t,a){"use strict";var s=a("41d3"),n=a.n(s);n.a}}]);