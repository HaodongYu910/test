(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-37759658"],{"3c75":function(e,t,a){"use strict";a.r(t);var r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("section",[a("el-col",{staticStyle:{height:"46px"},attrs:{span:24}},[a("el-form",{attrs:{inline:!0,model:e.filters},nativeOn:{submit:function(e){e.preventDefault()}}},[a("el-form-item",[a("el-input",{attrs:{placeholder:"名称"},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.getCaseList(t)}},model:{value:e.filters.name,callback:function(t){e.$set(e.filters,"name","string"===typeof t?t.trim():t)},expression:"filters.name"}})],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:e.getCaseList}},[e._v("查询")])],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:e.handleAdd}},[e._v("新增用例")])],1),a("el-form-item",[a("el-button",{attrs:{type:"primary",disabled:e.update},on:{click:e.changeGroup}},[e._v("修改分组")])],1)],1)],1),a("el-dialog",{staticStyle:{width:"60%",left:"20%"},attrs:{title:"编辑",visible:e.editFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(t){e.editFormVisible=t}}},[a("el-form",{ref:"editForm",attrs:{model:e.editForm,rules:e.editFormRules,"label-width":"80px"}},[a("el-form-item",{attrs:{label:"名称",prop:"caseName"}},[a("el-input",{attrs:{"auto-complete":"off"},model:{value:e.editForm.caseName,callback:function(t){e.$set(e.editForm,"caseName","string"===typeof t?t.trim():t)},expression:"editForm.caseName"}})],1),a("el-form-item",{attrs:{label:"接口分组:","label-width":"83px",prop:"automationGroupLevelFirst"}},[a("el-select",{attrs:{placeholder:"分组"},model:{value:e.editForm.automationGroupLevelFirst,callback:function(t){e.$set(e.editForm,"automationGroupLevelFirst",t)},expression:"editForm.automationGroupLevelFirst"}},e._l(e.group,(function(e,t){return a("el-option",{key:t+"",attrs:{label:e.name,value:e.id}})})),1)],1),a("el-form-item",{attrs:{label:"描述",prop:"description"}},[a("el-input",{attrs:{type:"textarea",rows:4},model:{value:e.editForm.description,callback:function(t){e.$set(e.editForm,"description","string"===typeof t?t.trim():t)},expression:"editForm.description"}})],1)],1),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{nativeOn:{click:function(t){e.editFormVisible=!1}}},[e._v("取消")]),a("el-button",{attrs:{type:"primary",loading:e.editLoading},nativeOn:{click:function(t){return e.editSubmit(t)}}},[e._v("提交")])],1)],1),a("el-dialog",{staticStyle:{width:"65%",left:"17.5%"},attrs:{title:"新增",visible:e.addFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(t){e.addFormVisible=t}}},[a("el-form",{ref:"addForm",attrs:{model:e.addForm,"label-width":"80px",rules:e.addFormRules}},[a("el-form-item",{attrs:{label:"名称",prop:"caseName"}},[a("el-input",{attrs:{"auto-complete":"off"},model:{value:e.addForm.caseName,callback:function(t){e.$set(e.addForm,"caseName","string"===typeof t?t.trim():t)},expression:"addForm.caseName"}})],1),a("el-form-item",{attrs:{label:"接口分组:","label-width":"83px",prop:"firstGroup"}},[a("el-select",{attrs:{placeholder:"分组"},model:{value:e.addForm.firstGroup,callback:function(t){e.$set(e.addForm,"firstGroup",t)},expression:"addForm.firstGroup"}},e._l(e.group,(function(e,t){return a("el-option",{key:t+"",attrs:{label:e.name,value:e.id}})})),1)],1),a("el-form-item",{attrs:{label:"描述",prop:"description"}},[a("el-input",{attrs:{type:"textarea",rows:4},model:{value:e.addForm.description,callback:function(t){e.$set(e.addForm,"description","string"===typeof t?t.trim():t)},expression:"addForm.description"}})],1)],1),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{nativeOn:{click:function(t){e.addFormVisible=!1}}},[e._v("取消")]),a("el-button",{attrs:{type:"primary",loading:e.addLoading},nativeOn:{click:function(t){return e.addSubmit(t)}}},[e._v("提交")])],1)],1),a("el-dialog",{staticStyle:{width:"65%",left:"17.5%"},attrs:{title:"修改所属分组",visible:e.updateGroupFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(t){e.updateGroupFormVisible=t}}},[a("el-form",{ref:"updateGroupForm",attrs:{model:e.updateGroupForm,"label-width":"80px",rules:e.updateGroupFormRules}},[a("el-form-item",{attrs:{label:"分组",prop:"firstGroup"}},[a("el-select",{attrs:{placeholder:"请选择分组"},model:{value:e.updateGroupForm.firstGroup,callback:function(t){e.$set(e.updateGroupForm,"firstGroup",t)},expression:"updateGroupForm.firstGroup"}},e._l(e.group,(function(e,t){return a("el-option",{key:t+"",attrs:{label:e.name,value:e.id}})})),1)],1)],1),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{nativeOn:{click:function(t){e.updateGroupFormVisible=!1}}},[e._v("取消")]),a("el-button",{attrs:{type:"primary",loading:e.updateGroupLoading},nativeOn:{click:function(t){return e.updateGroupSubmit(t)}}},[e._v("提交")])],1)],1),a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.listLoading,expression:"listLoading"}],staticStyle:{width:"100%"},attrs:{data:e.Case,"highlight-current-row":""},on:{"selection-change":e.selsChange}},[a("el-table-column",{attrs:{type:"selection","min-width":"5%"}}),a("el-table-column",{attrs:{prop:"caseName",label:"用例名称","min-width":"20%",sortable:"","show-overflow-tooltip":""},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-icon",{attrs:{name:"caseName"}}),a("router-link",{staticStyle:{"text-decoration":"none"},attrs:{to:{name:"用例接口列表",params:{case_id:t.row.id}}}},[e._v(e._s(t.row.caseName))])]}}])}),a("el-table-column",{attrs:{prop:"description",label:"描述","min-width":"35%",sortable:"","show-overflow-tooltip":""}}),a("el-table-column",{attrs:{prop:"createUser",label:"创建人","min-width":"10%",sortable:"","show-overflow-tooltip":""}}),a("el-table-column",{attrs:{prop:"updateTime",label:"更新日期","min-width":"15%",sortable:"","show-overflow-tooltip":""}}),a("el-table-column",{attrs:{label:"操作","min-width":"15%"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-button",{attrs:{type:"danger",size:"small"},on:{click:function(a){return e.handleDel(t.$index,t.row)}}},[e._v("删除")]),a("el-button",{attrs:{type:"info",size:"small"},on:{click:function(a){return e.handleEdit(t.$index,t.row)}}},[e._v("修改")])]}}])})],1),a("el-col",{staticClass:"toolbar",attrs:{span:24}},[a("el-button",{attrs:{type:"danger",disabled:0===this.sels.length},on:{click:e.batchRemove}},[e._v("批量删除")]),a("el-pagination",{staticStyle:{float:"right"},attrs:{layout:"prev, pager, next","page-size":20,"page-count":e.total},on:{"current-change":e.handleCurrentChange}})],1)],1)},i=[],o=a("2d92"),s=a("1157"),n=a.n(s),l=(a("c1df"),{data(){return{filters:{name:""},Case:[],total:0,page:1,listLoading:!1,sels:[],delLoading:!1,disDel:!0,updateGroupFormVisible:!1,updateGroupForm:{firstGroup:""},updateGroupFormRules:{firstGroup:[{type:"number",required:!0,message:"请选择父分组",trigger:"blur"}]},group:[],updateGroupLoading:!1,update:!0,editFormVisible:!1,editLoading:!1,editFormRules:{caseName:[{required:!0,message:"请输入名称",trigger:"blur"},{min:1,max:50,message:"长度在 1 到 50 个字符",trigger:"blur"}],automationGroupLevelFirst:[{type:"number",required:!0,message:"请选择分组",trigger:"blur"}],description:[{required:!1,message:"请输入描述",trigger:"blur"},{max:1024,message:"不能超过1024个字符",trigger:"blur"}]},editForm:{caseName:"",automationGroupLevelFirst:"",description:""},addFormVisible:!1,addLoading:!1,addFormRules:{caseName:[{required:!0,message:"请输入名称",trigger:"blur"},{min:1,max:50,message:"长度在 1 到 50 个字符",trigger:"blur"}],firstGroup:[{type:"number",required:!0,message:"请选择父分组",trigger:"blur"}],description:[{required:!1,message:"请输入版本号",trigger:"blur"},{max:1024,message:"不能超过1024个字符",trigger:"blur"}]},addForm:{caseName:"",firstGroup:"",description:""}}},methods:{getCaseList(){this.listLoading=!0;let e=this,t={project_id:this.$route.params.project_id,page:e.page,name:e.filters.name};this.$route.params.firstGroup&&(t["first_group_id"]=this.$route.params.firstGroup,this.$route.params.secondGroup&&(t["second_group_id"]=this.$route.params.secondGroup)),n.a.ajax({type:"get",url:o["Z"]+"/api/automation/case_list",async:!0,data:t,headers:{Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))},timeout:5e3,success:function(t){e.listLoading=!1,"0"===t.code?(e.total=t.data.total,e.Case=t.data.data):e.$message.error({message:t.msg,center:!0})}})},updateGroupSubmit(){let e=this.sels.map(e=>e.id),t=this;this.$confirm("确认修改所属分组吗？","提示",{type:"warning"}).then(()=>{t.updateGroupLoading=!0;let a=JSON.stringify({project_id:Number(this.$route.params.project_id),automationGroupLevelFirst_id:t.updateGroupForm.firstGroup,ids:e});n.a.ajax({type:"post",url:o["Z"]+"/api/automation/update_case_group",async:!0,data:a,headers:{"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))},timeout:5e3,success:function(e){t.updateGroupLoading=!1,"0"===e.code?(t.$message({message:"修改成功",center:!0,type:"success"}),t.$router.push({name:"分组用例列表",params:{project_id:t.$route.params.project_id,firstGroup:t.updateGroupForm.firstGroup}})):t.$message.error({message:e.msg,center:!0}),t.updateGroupFormVisible=!1,t.getCaseList()}})}).catch(()=>{})},getCaseGroup(){let e=this;n.a.ajax({type:"get",url:o["Z"]+"/api/automation/group",async:!0,data:{project_id:this.$route.params.project_id},headers:{Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))},timeout:5e3,success:function(t){"0"===t.code?(e.group=t.data,e.updateGroupForm.firstGroup=e.group[0].id,e.addForm.firstGroup=e.group[0].id):e.$message.error({message:t.msg,center:!0})}})},changeGroup(){this.getCaseGroup(),this.updateGroupFormVisible=!0},handleDel:function(e,t){this.$confirm("确认删除该记录吗?","提示",{type:"warning"}).then(()=>{this.listLoading=!0;let e=this;n.a.ajax({type:"post",url:o["Z"]+"/api/automation/del_case",async:!0,data:JSON.stringify({project_id:Number(this.$route.params.project_id),ids:[t.id]}),headers:{"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))},timeout:5e3,success:function(t){"0"===t.code?e.$message({message:"删除成功",center:!0,type:"success"}):e.$message.error({message:t.msg,center:!0}),e.getCaseList()}})}).catch(()=>{})},handleCurrentChange(e){this.page=e,this.getCaseList()},selsChange:function(e){e.length>0?(this.sels=e,this.update=!1):this.update=!0},batchRemove:function(){let e=this.sels.map(e=>e.id),t=this;this.$confirm("确认删除选中记录吗？","提示",{type:"warning"}).then(()=>{t.listLoading=!0,n.a.ajax({type:"post",url:o["Z"]+"/api/automation/del_case",async:!0,data:JSON.stringify({project_id:Number(this.$route.params.project_id),ids:e}),headers:{"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))},timeout:5e3,success:function(e){t.listLoading=!1,"0"===e.code?t.$message({message:"删除成功",center:!0,type:"success"}):t.$message.error({message:e.msg,center:!0}),t.getCaseList()}})}).catch(()=>{})},handleEdit:function(e,t){this.getCaseGroup(),this.editFormVisible=!0,this.editForm=Object.assign({},t)},handleAdd:function(){this.getCaseGroup(),this.addFormVisible=!0},editSubmit:function(){let e=this;this.$refs.editForm.validate(t=>{t&&this.$confirm("确认提交吗？","提示",{}).then(()=>{e.editLoading=!0;let t=JSON.stringify({project_id:Number(this.$route.params.project_id),id:Number(e.editForm.id),caseName:e.editForm.caseName,automationGroupLevelFirst_id:Number(this.editForm.automationGroupLevelFirst),description:e.editForm.description});n.a.ajax({type:"post",url:o["Z"]+"/api/automation/update_case",async:!0,data:t,headers:{Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))},timeout:5e3,success:function(t){e.editLoading=!1,"0"===t.code?(e.$message({message:"修改成功",center:!0,type:"success"}),e.$refs["editForm"].resetFields(),e.editFormVisible=!1,e.getCaseList()):(t.code,e.$message.error({message:t.msg,center:!0}))}})})})},addSubmit:function(){this.$refs.addForm.validate(e=>{if(e){let e=this;this.$confirm("确认提交吗？","提示",{}).then(()=>{e.addLoading=!0;let t=JSON.stringify({project_id:Number(this.$route.params.project_id),automationGroupLevelFirst_id:this.addForm.firstGroup,caseName:e.addForm.caseName,description:e.addForm.description});n.a.ajax({type:"post",url:o["Z"]+"/api/automation/add_case",async:!0,data:t,headers:{Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))},timeout:5e3,success:function(t){e.addLoading=!1,"0"===t.code?(e.$message({message:"添加成功",center:!0,type:"success"}),e.$refs["addForm"].resetFields(),e.addFormVisible=!1,e.getCaseList()):"999997"===t.code?e.$message.error({message:t.msg,center:!0}):(e.$message.error({message:t.msg,center:!0}),e.$refs["addForm"].resetFields(),e.addFormVisible=!1,e.getCaseList())}})})}})}},watch:{$route:function(e,t){e!==t&&this.getCaseList()}},mounted(){this.getCaseList()}}),d=l,u=(a("e825"),a("2877")),p=Object(u["a"])(d,r,i,!1,null,"dc1fd9cc",null);t["default"]=p.exports},b298:function(e,t,a){},e825:function(e,t,a){"use strict";var r=a("b298"),i=a.n(r);i.a}}]);