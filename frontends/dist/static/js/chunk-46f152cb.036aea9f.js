(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-46f152cb"],{"0938":function(e,t,a){"use strict";a.r(t);var r=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("section",[r("el-col",{staticClass:"toolbar",staticStyle:{"padding-bottom":"0px"},attrs:{span:24}},[r("el-form",{attrs:{inline:!0,model:e.filters},nativeOn:{submit:function(e){e.preventDefault()}}},[r("el-form-item",[r("el-input",{attrs:{placeholder:"名称"},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.stresslistList(t)}},model:{value:e.filters.name,callback:function(t){e.$set(e.filters,"name",t)},expression:"filters.name"}})],1),r("el-form-item",[r("el-button",{attrs:{type:"primary"},on:{click:e.stresslistList}},[e._v("查询")])],1),r("el-form-item",[r("el-button",{attrs:{type:"primary"},on:{click:e.handleAdd}},[e._v("创建测试")])],1)],1)],1),r("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.listLoading,expression:"listLoading"}],staticStyle:{width:"100%"},attrs:{data:e.project,"highlight-current-row":""},on:{"selection-change":e.selsChange}},[r("el-table-column",{attrs:{type:"selection","min-width":"5%"}}),r("el-table-column",{attrs:{prop:"version",label:"版本","min-width":"12%",sortable:"","show-overflow-tooltip":""},scopedSlots:e._u([{key:"default",fn:function(t){return[r("el-icon",{attrs:{name:"name"}}),t.row.status?r("router-link",{staticStyle:{"text-decoration":"none",color:"#000000"},attrs:{to:{version:"概况",params:{id:t.row.id}}}},[e._v(" "+e._s(t.row.version)+" ")]):e._e(),e._v(" "+e._s(t.row.status?"":t.row.version)+" ")]}}])}),r("el-table-column",{attrs:{prop:"version",label:"服务","min-width":"12%",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[r("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.loadserver))])]}}])}),r("el-table-column",{attrs:{prop:"type",label:"类型","min-width":"9%"},scopedSlots:e._u([{key:"default",fn:function(t){return[r("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.type))])]}}])}),r("el-table-column",{attrs:{prop:"type",label:"线程数","min-width":"9%"},scopedSlots:e._u([{key:"default",fn:function(t){return[r("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.type))])]}}])}),r("el-table-column",{attrs:{prop:"type",label:"运行规则","min-width":"20%"},scopedSlots:e._u([{key:"default",fn:function(t){return[r("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.testdata))])]}}])}),r("el-table-column",{attrs:{label:"开始时间","min-width":"16%",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[r("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(e._f("dateformat")(t.row.start_date,"YYYY-MM-DD ")))])]}}])}),r("el-table-column",{attrs:{label:"结束时间","min-width":"16%",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[r("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(e._f("dateformat")(t.row.end_date,"YYYY-MM-DD ")))])]}}])}),r("el-table-column",{attrs:{label:"测试状态","min-width":"9%"},scopedSlots:e._u([{key:"default",fn:function(t){return[r("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.status))])]}}])}),r("el-table-column",{attrs:{prop:"status",label:"状态","min-width":"9%"},scopedSlots:e._u([{key:"default",fn:function(e){return[r("img",{directives:[{name:"show",rawName:"v-show",value:e.row.status,expression:"scope.row.status"}],attrs:{src:a("e7a2")}}),r("img",{directives:[{name:"show",rawName:"v-show",value:!e.row.status,expression:"!scope.row.status"}],attrs:{src:a("cb08")}})]}}])}),r("el-table-column",{attrs:{label:"操作","min-width":"50px"},scopedSlots:e._u([{key:"default",fn:function(t){return[r("el-button",{attrs:{type:"warning",size:"small"},on:{click:function(a){return e.showdetail(t.$index,t.row)}}},[e._v("查看")]),r("el-button",{attrs:{size:"small"},on:{click:function(a){return e.handleEdit(t.$index,t.row)}}},[e._v("生成结果")]),r("el-button",{attrs:{type:"danger",size:"small"},on:{click:function(a){return e.handleDel(t.$index,t.row)}}},[e._v("测试报告")]),r("el-button",{attrs:{type:"info",size:"small"},on:{click:function(a){return e.handleChangeStatus(t.$index,t.row)}}},[e._v(" "+e._s(!1===t.row.status?"启用":"禁用")+" ")])]}}])})],1),r("el-col",{staticClass:"toolbar",attrs:{span:24}},[r("el-button",{attrs:{type:"danger",disabled:0===this.sels.length},on:{click:e.batchRemove}},[e._v("批量删除")]),r("el-pagination",{staticStyle:{float:"right"},attrs:{layout:"prev, pager, next","page-size":20,"page-count":e.total},on:{"current-change":e.handleCurrentChange}})],1),r("el-dialog",{staticStyle:{width:"75%",left:"12.5%"},attrs:{title:"编辑",visible:e.editFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(t){e.editFormVisible=t}}},[r("el-form",{ref:"editForm",attrs:{model:e.editForm,"label-width":"80px",rules:e.editFormRules}},[r("el-form-item",{attrs:{label:"项目名称"}},[r("el-input",{attrs:{"auto-complete":"off",disabled:!0},model:{value:e.editForm.name,callback:function(t){e.$set(e.editForm,"name",t)},expression:"editForm.name"}})],1),r("el-row",{attrs:{gutter:24}},[r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"类型",prop:"type"}},[r("el-select",{attrs:{placeholder:"请选择"},model:{value:e.editForm.type,callback:function(t){e.$set(e.editForm,"type",t)},expression:"editForm.type"}},e._l(e.options,(function(e){return r("el-option",{key:e.value,attrs:{label:e.label,value:e.value}})})),1)],1)],1),r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"版本号"}},[r("el-input",{attrs:{disabled:!0,"auto-complete":"off"},model:{value:e.editForm.version,callback:function(t){e.$set(e.editForm,"version",t)},expression:"editForm.version"}})],1)],1)],1),r("el-row",{attrs:{gutter:24}},[r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"项目开始时间"}},[r("el-date-picker",{attrs:{type:"datetime","value-format":"yyyy-MM-dd HH:mm:ss",placeholder:"选择日期"},model:{value:e.editForm.start_date,callback:function(t){e.$set(e.editForm,"start_date",t)},expression:"editForm.start_date"}})],1)],1),r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"接口提测时间",prop:"api_date"}},[r("el-date-picker",{attrs:{type:"datetime","value-format":"yyyy-MM-dd HH:mm:ss",placeholder:"选择日期"},model:{value:e.editForm.api_date,callback:function(t){e.$set(e.editForm,"api_date",t)},expression:"editForm.api_date"}})],1)],1)],1),r("el-row",{attrs:{gutter:24}},[r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"APP提测时间",prop:"app_date"}},[r("el-date-picker",{attrs:{type:"datetime","value-format":"yyyy-MM-dd HH:mm:ss",placeholder:"选择日期"},model:{value:e.editForm.app_date,callback:function(t){e.$set(e.editForm,"app_date",t)},expression:"editForm.app_date"}})],1)],1),r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"接口上线时间",prop:"api_online_date"}},[r("el-date-picker",{attrs:{type:"datetime","value-format":"yyyy-MM-dd HH:mm:ss",placeholder:"选择日期"},model:{value:e.editForm.api_online_date,callback:function(t){e.$set(e.editForm,"api_online_date",t)},expression:"editForm.api_online_date"}})],1)],1)],1),r("el-row",{attrs:{gutter:24}},[r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"发布日期",prop:"end_date"}},[r("el-date-picker",{attrs:{type:"datetime","value-format":"yyyy-MM-dd HH:mm:ss",placeholder:"选择日期"},model:{value:e.editForm.end_date,callback:function(t){e.$set(e.editForm,"end_date",t)},expression:"editForm.end_date"}})],1)],1),r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"项目状态",prop:"projectstatus"}},[r("el-select",{attrs:{placeholder:"请选择"},model:{value:e.editForm.projectstatus,callback:function(t){e.$set(e.editForm,"projectstatus",t)},expression:"editForm.projectstatus"}},[r("el-option",{key:"未开发",attrs:{label:"未开发",value:"未开发"}}),r("el-option",{key:"开发中",attrs:{label:"开发中",value:"开发中"}}),r("el-option",{key:"接口测试",attrs:{label:"接口测试",value:"接口测试"}}),r("el-option",{key:"功能测试",attrs:{label:"功能测试",value:"功能测试"}}),r("el-option",{key:"灰度测试",attrs:{label:"灰度测试",value:"灰度测试"}}),r("el-option",{key:"已上线",attrs:{label:"已上线",value:"已上线"}})],1)],1)],1)],1),r("el-form-item",{attrs:{label:"描述",prop:"description"}},[r("el-input",{attrs:{type:"textarea",rows:6},model:{value:e.editForm.description,callback:function(t){e.$set(e.editForm,"description",t)},expression:"editForm.description"}})],1)],1),r("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[r("el-button",{nativeOn:{click:function(t){e.editFormVisible=!1}}},[e._v("取消")]),r("el-button",{attrs:{type:"primary",loading:e.editLoading},nativeOn:{click:function(t){return e.editSubmit(t)}}},[e._v("提交")])],1)],1),r("el-dialog",{staticStyle:{width:"75%",left:"12.5%"},attrs:{title:"新增",visible:e.addFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(t){e.addFormVisible=t}}},[r("el-form",{ref:"addForm",attrs:{model:e.addForm,"label-width":"80px",rules:e.addFormRules}},[r("el-form-item",{attrs:{label:"项目名称",prop:"name"}},[r("el-select",{attrs:{placeholder:"请选择"},model:{value:e.addForm.name,callback:function(t){e.$set(e.addForm,"name",t)},expression:"addForm.name"}},[r("el-option",{key:"Boimind",attrs:{label:"Boimind",value:"Boimind"}})],1)],1),r("el-row",{attrs:{gutter:24}},[r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"服务器",prop:"server"}},[r("el-select",{attrs:{placeholder:"请选择服务器"},nativeOn:{click:function(t){return e.gethost()}},model:{value:e.addForm.server,callback:function(t){e.$set(e.addForm,"server",t)},expression:"addForm.server"}},e._l(e.tags,(function(e,t){return r("el-option",{key:e.host,attrs:{label:e.name,value:e.host}})})),1)],1)],1),r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"版本号",prop:"version"}},[r("el-input",{attrs:{"auto-complete":"off"},model:{value:e.addForm.version,callback:function(t){e.$set(e.addForm,"version","string"===typeof t?t.trim():t)},expression:"addForm.version"}})],1)],1)],1),r("el-row",{attrs:{gutter:24}},[r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"压测时长",prop:"version"}},[r("el-input",{attrs:{"auto-complete":"off"},model:{value:e.addForm.version,callback:function(t){e.$set(e.addForm,"version","string"===typeof t?t.trim():t)},expression:"addForm.version"}})],1)],1),r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"线程数",prop:"version"}},[r("el-input",{attrs:{"auto-complete":"off"},model:{value:e.addForm.version,callback:function(t){e.$set(e.addForm,"version","string"===typeof t?t.trim():t)},expression:"addForm.version"}})],1)],1)],1),r("el-row",{attrs:{gutter:24}},[r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"循环次数",prop:"version"}},[r("el-input",{attrs:{"auto-complete":"off"},model:{value:e.addForm.version,callback:function(t){e.$set(e.addForm,"version","string"===typeof t?t.trim():t)},expression:"addForm.version"}})],1)],1),r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"并发数",prop:"version"}},[r("el-input",{attrs:{"auto-complete":"off"},model:{value:e.addForm.version,callback:function(t){e.$set(e.addForm,"version","string"===typeof t?t.trim():t)},expression:"addForm.version"}})],1)],1)],1),r("el-row",{attrs:{gutter:24}},[r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"发布日期",prop:"end_date"}},[r("el-date-picker",{attrs:{type:"datetime","value-format":"yyyy-MM-dd HH:mm:ss",placeholder:"选择日期"},model:{value:e.addForm.end_date,callback:function(t){e.$set(e.addForm,"end_date",t)},expression:"addForm.end_date"}})],1)],1),r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"项目状态",prop:"projectstatus"}},[r("el-select",{attrs:{placeholder:"请选择"},model:{value:e.addForm.projectstatus,callback:function(t){e.$set(e.addForm,"projectstatus",t)},expression:"addForm.projectstatus"}},[r("el-option",{key:"未开发",attrs:{label:"未开发",value:"未开发"}}),r("el-option",{key:"开发中",attrs:{label:"开发中",value:"开发中"}}),r("el-option",{key:"接口测试",attrs:{label:"接口测试",value:"接口测试"}}),r("el-option",{key:"功能测试",attrs:{label:"功能测试",value:"功能测试"}}),r("el-option",{key:"灰度测试",attrs:{label:"灰度测试",value:"灰度测试"}}),r("el-option",{key:"已上线",attrs:{label:"已上线",value:"已上线"}})],1)],1)],1)],1),r("el-form-item",{attrs:{label:"描述",prop:"description"}},[r("el-input",{attrs:{type:"textarea",rows:6},model:{value:e.addForm.description,callback:function(t){e.$set(e.addForm,"description",t)},expression:"addForm.description"}})],1)],1),r("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[r("el-button",{nativeOn:{click:function(t){e.addFormVisible=!1}}},[e._v("取消")]),r("el-button",{attrs:{type:"primary",loading:e.addLoading},nativeOn:{click:function(t){return e.addSubmit(t)}}},[e._v("提交")])],1)],1)],1)},s=[],o=a("2d92"),n={data(){return{filters:{name:""},project:[],total:0,page:1,listLoading:!1,sels:[],editFormVisible:!1,editLoading:!1,options:[{label:"Web",value:"Web"},{label:"App",value:"App"}],editFormRules:{name:[{required:!0,message:"请输入名称",trigger:"blur"},{min:1,max:50,message:"长度在 1 到 50 个字符",trigger:"blur"}],type:[{required:!0,message:"请选择类型",trigger:"blur"}],version:[{required:!0,message:"请输入版本号",trigger:"change"},{pattern:/^\d+\.\d+\.\d+$/,message:"请输入合法的版本号（x.x.x）"}],description:[{required:!1,message:"请输入描述",trigger:"blur"},{max:1024,message:"不能超过1024个字符",trigger:"blur"}]},editForm:{name:"",version:"",type:"",description:""},addFormVisible:!1,addLoading:!1,addFormRules:{name:[{required:!0,message:"请输入名称",trigger:"blur"},{min:1,max:50,message:"长度在 1 到 50 个字符",trigger:"blur"}],type:[{required:!0,message:"请选择类型",trigger:"blur"}],version:[{required:!0,message:"请输入版本号",trigger:"change"},{pattern:/^\d+\.\d+\.\d+$/,message:"请输入合法的版本号（x.x.x）"}]},addForm:{name:"",version:"",type:"",description:""}}},methods:{showdetail(e,t){this.$router.push({path:"/stressdetail",query:{id:t.id,name:t.name}})},stresslistList(){this.listLoading=!0;let e=this,t={page:e.page,name:e.filters.name,type:""},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["mb"])(a,t).then(t=>{e.listLoading=!1;let{msg:a,code:r,data:s}=t;"0"===r?(e.total=s.total,e.project=s.data):e.$message.error({message:a,center:!0})})},handleDel:function(e,t){this.$confirm("确认删除该记录吗?","提示",{type:"warning"}).then(()=>{this.listLoading=!0;let e=this,a={ids:[t.id]},r={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["t"])(r,a).then(t=>{let{msg:a,code:r,data:s}=t;"0"===r?e.$message({message:"删除成功",center:!0,type:"success"}):e.$message.error({message:a,center:!0}),e.stresslistList()})})},handleChangeStatus:function(e,t){let a=this;this.listLoading=!0;let r={project_id:t.id},s={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};t.status?Object(o["E"])(s,r).then(e=>{let{msg:r,code:s,data:o}=e;a.listLoading=!1,"0"===s?(a.$message({message:"禁用成功",center:!0,type:"success"}),t.status=!t.status):a.$message.error({message:r,center:!0})}):Object(o["I"])(s,r).then(e=>{let{msg:r,code:s,data:o}=e;a.listLoading=!1,"0"===s?(a.$message({message:"启用成功",center:!0,type:"success"}),t.status=!t.status):a.$message.error({message:r,center:!0})})},handleCurrentChange(e){this.page=e,this.stresslistList()},handleEdit:function(e,t){this.editFormVisible=!0,this.editForm=Object.assign({},t)},handleAdd:function(){this.addFormVisible=!0,this.addForm={version:null,name:null,status:null,start_date:null,api_date:null,app_date:null,api_online_date:null,end_date:null,type:null,projectstatus:null,description:null}},editSubmit:function(){let e=this;this.$refs.editForm.validate(t=>{t&&this.$confirm("确认提交吗？","提示",{}).then(()=>{e.editLoading=!0;let t={project_id:e.editForm.id,name:e.editForm.name,type:e.editForm.type,version:e.editForm.version,start_date:e.editForm.start_date,api_date:e.editForm.api_date,app_date:e.editForm.app_date,api_online_date:e.editForm.api_online_date,end_date:e.editForm.end_date,projectstatus:e.editForm.projectstatus,description:e.editForm.description},a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["qb"])(a,t).then(t=>{let{msg:a,code:r,data:s}=t;e.editLoading=!1,"0"===r?(e.$message({message:"修改成功",center:!0,type:"success"}),e.$refs["editForm"].resetFields(),e.editFormVisible=!1,e.stresslistList()):e.$message.error({message:a,center:!0})})})})},addSubmit:function(){this.$refs.addForm.validate(e=>{if(e){let e=this;this.$confirm("确认提交吗？","提示",{}).then(()=>{e.addLoading=!0;let t=JSON.stringify({name:e.addForm.name,type:e.addForm.type,version:e.addForm.version,description:e.addForm.description,start_date:this.addForm.start_date,api_date:this.addForm.api_date,app_date:this.addForm.app_date,api_online_date:this.addForm.api_online_date,end_date:this.addForm.end_date,projectstatus:this.addForm.projectstatus}),a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["k"])(a,t).then(t=>{let{msg:a,code:r,data:s}=t;e.addLoading=!1,"0"===r?(e.$message({message:"添加成功",center:!0,type:"success"}),e.$refs["addForm"].resetFields(),e.addFormVisible=!1,e.stresslistList()):"999997"===r?e.$message.error({message:a,center:!0}):(e.$message.error({message:a,center:!0}),e.$refs["addForm"].resetFields(),e.addFormVisible=!1,e.stresslistList())})})}})},selsChange:function(e){this.sels=e},batchRemove:function(){let e=this.sels.map(e=>e.id);this.$confirm("确认删除选中记录吗？","提示",{type:"warning"}).then(()=>{this.listLoading=!0;let t=this,a={ids:e},r={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["t"])(r,a).then(e=>{let{msg:a,code:r,data:s}=e;"0"===r?t.$message({message:"删除成功",center:!0,type:"success"}):t.$message.error({message:a,center:!0}),t.stresslistList()})})}},mounted(){this.stresslistList()}},i=n,l=a("2877"),d=Object(l["a"])(i,r,s,!1,null,null,null);t["default"]=d.exports},"2d92":function(e,t,a){"use strict";a.d(t,"nb",(function(){return o})),a.d(t,"O",(function(){return n})),a.d(t,"t",(function(){return i})),a.d(t,"E",(function(){return l})),a.d(t,"I",(function(){return d})),a.d(t,"qb",(function(){return p})),a.d(t,"k",(function(){return u})),a.d(t,"P",(function(){return c})),a.d(t,"N",(function(){return m})),a.d(t,"s",(function(){return f})),a.d(t,"D",(function(){return h})),a.d(t,"H",(function(){return g})),a.d(t,"pb",(function(){return b})),a.d(t,"j",(function(){return v})),a.d(t,"Q",(function(){return y})),a.d(t,"R",(function(){return _})),a.d(t,"M",(function(){return F})),a.d(t,"r",(function(){return k})),a.d(t,"i",(function(){return w})),a.d(t,"S",(function(){return x})),a.d(t,"U",(function(){return $})),a.d(t,"T",(function(){return j})),a.d(t,"g",(function(){return S})),a.d(t,"L",(function(){return L})),a.d(t,"h",(function(){return D})),a.d(t,"ob",(function(){return O})),a.d(t,"q",(function(){return C})),a.d(t,"G",(function(){return I})),a.d(t,"kb",(function(){return M})),a.d(t,"rb",(function(){return z})),a.d(t,"l",(function(){return q})),a.d(t,"J",(function(){return V})),a.d(t,"x",(function(){return A})),a.d(t,"hb",(function(){return H})),a.d(t,"jb",(function(){return T})),a.d(t,"ib",(function(){return N})),a.d(t,"p",(function(){return J})),a.d(t,"ub",(function(){return Y})),a.d(t,"z",(function(){return E})),a.d(t,"d",(function(){return R})),a.d(t,"mb",(function(){return B})),a.d(t,"e",(function(){return P})),a.d(t,"lb",(function(){return W})),a.d(t,"V",(function(){return G})),a.d(t,"u",(function(){return K})),a.d(t,"sb",(function(){return Q})),a.d(t,"n",(function(){return U})),a.d(t,"C",(function(){return X})),a.d(t,"Y",(function(){return Z})),a.d(t,"B",(function(){return ee})),a.d(t,"v",(function(){return te})),a.d(t,"gb",(function(){return ae})),a.d(t,"fb",(function(){return re})),a.d(t,"cb",(function(){return se})),a.d(t,"y",(function(){return oe})),a.d(t,"Z",(function(){return ne})),a.d(t,"ab",(function(){return ie})),a.d(t,"o",(function(){return le})),a.d(t,"tb",(function(){return de})),a.d(t,"w",(function(){return pe})),a.d(t,"K",(function(){return ue})),a.d(t,"F",(function(){return ce})),a.d(t,"bb",(function(){return me})),a.d(t,"db",(function(){return fe})),a.d(t,"eb",(function(){return he})),a.d(t,"X",(function(){return ge})),a.d(t,"W",(function(){return be})),a.d(t,"m",(function(){return ve})),a.d(t,"f",(function(){return ye})),a.d(t,"c",(function(){return _e})),a.d(t,"b",(function(){return Fe})),a.d(t,"a",(function(){return ke})),a.d(t,"A",(function(){return we}));var r=a("bc3a"),s=a.n(r);a("c896");const o="http://192.168.2.38:9000",n=(e,t)=>s.a.get(o+"/api/project/project_list",{params:t,headers:e}).then(e=>e.data),i=(e,t)=>s.a.post(o+"/api/project/del_project",t,{headers:e}).then(e=>e.data),l=(e,t)=>s.a.post(o+"/api/project/disable_project",t,{headers:e}).then(e=>e.data),d=(e,t)=>s.a.post(o+"/api/project/enable_project",t,{headers:e}).then(e=>e.data),p=(e,t)=>s.a.post(o+"/api/project/update_project",t,{headers:e}).then(e=>e.data),u=(e,t)=>s.a.post(o+"/api/project/add_project",t,{headers:e}).then(e=>e.data),c=(e,t)=>s.a.get(o+"/api/title/project_info",{params:t,headers:e}).then(e=>e.data),m=(e,t)=>s.a.get(o+"/api/global/host_total",{params:t,headers:e}).then(e=>e.data),f=(e,t)=>s.a.post(o+"/api/global/del_host",t,{headers:e}).then(e=>e.data),h=(e,t)=>s.a.post(o+"/api/global/disable_host",t,{headers:e}).then(e=>e.data),g=(e,t)=>s.a.post(o+"/api/global/enable_host",t,{headers:e}).then(e=>e.data),b=(e,t)=>s.a.post(o+"/api/global/update_host",t,{headers:e}).then(e=>e.data),v=(e,t)=>s.a.post(o+"/api/global/add_host",t,{headers:e}).then(e=>e.data),y=(e,t)=>s.a.get(o+"/api/dynamic/dynamic",{params:t,headers:e}).then(e=>e.data),_=(e,t)=>s.a.get(o+"/api/member/project_member",{params:t,headers:e}).then(e=>e.data),F=(e,t)=>s.a.get(o+"/api/member/get_email",{params:t,headers:e}).then(e=>e.data),k=(e,t)=>s.a.post(o+"/api/member/del_email",t,{headers:e}).then(e=>e.data),w=(e,t)=>s.a.post(o+"/api/member/email_config",t,{headers:e}).then(e=>e.data),x=(e,t)=>s.a.get(o+"/api/report/auto_test_report",{params:t,headers:e}).then(e=>e.data),$=(e,t)=>s.a.get(o+"/api/report/test_time",{params:t,headers:e}).then(e=>e.data),j=(e,t)=>s.a.get(o+"/api/report/lately_ten",{params:t,headers:e}).then(e=>e.data),S=(e,t)=>s.a.post(o+"/api/api/add_api",t,{headers:e}).then(e=>e.data),L=(e,t)=>s.a.get(o+"/api/api/group",{params:t,headers:e}).then(e=>e.data),D=(e,t)=>s.a.post(o+"/api/api/add_group",t,{headers:e}).then(e=>e.data),O=(e,t)=>s.a.post(o+"/api/api/update_name_group",t,{headers:e}).then(e=>e.data),C=(e,t)=>s.a.post(o+"/api/api/del_group",t,{headers:e}).then(e=>e.data),I=(e,t)=>s.a.post(o+"/api/download",t,{headers:e}).then(e=>e.data),M=(e,t)=>s.a.post(o+"/api/user/login",t,e).then(e=>e.data),z=(e,t)=>s.a.post(o+"/api/risk/update",t,{headers:e}).then(e=>e.data),q=(e,t)=>s.a.post(o+"/api/risk/add",t,{headers:e}).then(e=>e.data),V=(e,t)=>s.a.post(o+"/api/risk/add",t,{headers:e}).then(e=>e.data),A=(e,t)=>s.a.post(o+"/api/risk/del",t,e).then(e=>e.data),H=(e,t)=>s.a.get(o+"/api/risk ",{params:t},e).then(e=>e.data),T=(e,t)=>s.a.get(o+"/api/todo ",{params:t},e).then(e=>e.data),N=(e,t)=>s.a.get(o+"/api/report ",{params:t},e).then(e=>e.data),J=(e,t)=>s.a.post(o+"/api/addreport",t,e).then(e=>e.data),Y=(e,t)=>s.a.post(o+"/api/updatereport",t,e).then(e=>e.data),E=(e,t)=>s.a.post(o+"/api/delreport",t,e).then(e=>e.data),R=(e,t)=>s.a.post(o+"/api/send",t,e).then(e=>e.data),B=(e,t)=>s.a.get(o+"/api/stress/list",{params:t},{headers:e}).then(e=>e.data),P=(e,t)=>s.a.get(o+"/api/stress/stressDetail ",{params:t},e).then(e=>e.data),W=(e,t)=>s.a.post(o+"/api/stress/stresstool",t,e).then(e=>e.data),G=(e,t)=>s.a.get(o+"/api/stress/version",{params:t},{headers:e}).then(e=>e.data),K=(e,t)=>s.a.post(o+"/api/tool/del_dicomData",t,e).then(e=>e.data),Q=(e,t)=>s.a.post(o+"/api/tool/update_dicomData",t,e).then(e=>e.data),U=(e,t)=>s.a.post(o+"/api/tool/add_dicomData",t,e).then(e=>e.data),X=(e,t)=>s.a.post(o+"/api/tool/dicomdetail",t,e).then(e=>e.data),Z=(e,t)=>s.a.get(o+"/api/tool/dicomData",{params:t},{headers:e}).then(e=>e.data),ee=(e,t)=>s.a.post(o+"/api/tool/dicomcsv",t,e).then(e=>e.data),te=(e,t)=>s.a.post(o+"/api/tool/delreport",t,e).then(e=>e.data),ae=(e,t)=>s.a.get(o+"/api/stress/stressversion",{params:t},{headers:e}).then(e=>e.data),re=(e,t)=>s.a.post(o+"/api/stress/stressresult",t,e).then(e=>e.data),se=(e,t)=>s.a.post(o+"/api/stress/stressfigure",t,e).then(e=>e.data),oe=(e,t)=>s.a.post(o+"/api/tool/delete_patients",t,e).then(e=>e.data),ne=(e,t)=>s.a.get(o+"/api/tool/getduration",{params:t},{headers:e}).then(e=>e.data),ie=(e,t)=>s.a.get(o+"/api/tool/durationData",{params:t},{headers:e}).then(e=>e.data),le=(e,t)=>s.a.post(o+"/api/tool/add_duration",t,e).then(e=>e.data),de=(e,t)=>s.a.post(o+"/api/tool/update_duration",t,e).then(e=>e.data),pe=(e,t)=>s.a.post(o+"/api/tool/del_duration",t,e).then(e=>e.data),ue=(e,t)=>s.a.post(o+"/api/tool/enable_duration",t,e).then(e=>e.data),ce=(e,t)=>s.a.post(o+"/api/tool/disable_duration",t,e).then(e=>e.data),me=(e,t)=>s.a.get(o+"/api/tool/duration_verify",{params:t},{headers:e}).then(e=>e.data),fe=(e,t)=>s.a.get(o+"/api/tool/somkerecord",{params:t},{headers:e}).then(e=>e.data),he=(e,t)=>s.a.post(o+"/api/tool/somke",t,e).then(e=>e.data),ge=(e,t)=>s.a.post(o+"/api/tool/dicomSend",t,e).then(e=>e.data),be=(e,t)=>s.a.get(o+"/api/base/getdata",{params:t},{headers:e}).then(e=>e.data),ve=(e,t)=>s.a.post(o+"/api/base/addData",t,e).then(e=>e.data),ye=(e,t)=>s.a.post(o+"/api/base/updateData",t,e).then(e=>e.data),_e=(e,t)=>s.a.post(o+"/api/base/enablebase",t,e).then(e=>e.data),Fe=(e,t)=>s.a.post(o+"/api/base/disablebase",t,e).then(e=>e.data),ke=(e,t)=>s.a.post(o+"/api/base/delbasedata",t,e).then(e=>e.data),we=(e,t)=>s.a.get(o+"/api/base/dicom",{params:t},{headers:e}).then(e=>e.data)},"41d3":function(e,t,a){},c896:function(e,t,a){"use strict";var r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("div",{staticClass:"crumbs"},[a("el-breadcrumb",{attrs:{separator:"/"}},[a("el-breadcrumb-item",[a("i",{staticClass:"el-icon-lx-calendar"}),e._v(" 测试工具")]),a("el-breadcrumb-item",[e._v("推送工具")])],1)],1),a("div",{staticClass:"container"},[a("div",{staticClass:"form-box"},[a("el-form",{ref:"form",attrs:{model:e.form,"status-icon":"",rules:e.rules,"label-width":"80px"}},[a("el-form-item",{attrs:{label:"推送ID",prop:"pushID"}},[a("el-col",{attrs:{span:10}},[a("el-input",{attrs:{id:"pushID"},model:{value:e.form.pushID,callback:function(t){e.$set(e.form,"pushID",t)},expression:"form.pushID"}})],1)],1),a("el-form-item",{attrs:{label:"推送环境",prop:"environment"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.form.environment,callback:function(t){e.$set(e.form,"environment",t)},expression:"form.environment"}},[a("el-option",{key:"test",attrs:{label:"测试环境",value:"test"}}),a("el-option",{key:"online",attrs:{label:"线上环境",value:"online"}})],1)],1),a("el-form-item",{attrs:{label:"推送类型",prop:"types"}},[a("el-cascader",{attrs:{options:e.types},on:{change:function(t){return e.changeLang("form")}},model:{value:e.form.types,callback:function(t){e.$set(e.form,"types",t)},expression:"form.types"}})],1),a("el-form-item",{attrs:{label:"选择语言",prop:"languages"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.form.languages,callback:function(t){e.$set(e.form,"languages",t)},expression:"form.languages"}},e._l(e.languages,(function(e,t){return a("el-option",{key:e.key,attrs:{label:e.value,value:e.key}})})),1)],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.onSubmit("form")}}},[e._v("确定推送")]),a("el-button",{on:{click:function(t){return e.resetForm("form")}}},[e._v("重置")])],1)],1)],1)])])},s=[],o={name:"baseform",data:function(){return{types:[{value:"bishijie",label:"Boimind",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"replay",label:"币圈"},{value:"monitor",label:"盯盘"}]},{value:"coinness",label:"coinness",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"monitor",label:"盯盘"}]}],languages:[],form:{pushID:"",environment:"",types:[],languages:[]},rules:{pushID:[{required:!0,message:"请输入推送ID",trigger:"blur"}],environment:[{required:!0,message:"请选择推送环境",trigger:"blur"}],types:[{required:!0,message:"请选择推送类型",trigger:"blur"}],languages:[{required:!0,message:"请选择语言",trigger:"blur"}]}}},methods:{onSubmit(e){this.$refs[e].validate(e=>{if(!e)return console.log("error submit"),!1;console.log("语言："+this.form.languages),console.log("pushID："+this.form.pushID),console.log("APP："+this.form.types[0]),console.log("推送类型："+this.form.types[1]),console.log("environment："+this.form.environment),this.$ajax.post("/bishijie/push",{id:this.form.pushID,service:this.form.environment,system:this.form.types[0],module:this.form.types[1],lang:this.form.languages,rid:""}).then(e=>{"0"==e.data.code?null==e.data.data||e.data.data[0]?this.$message.success("push成功！"):this.$message.error(e.data.data[1]):this.$message.error(e.data.msg)}).catch((function(e){console.log(e)}))})},resetForm(e){this.$refs[e].resetFields()},changeLang(e){this.languages=[],this.form.languages="";var t=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"}],a=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"},{key:"en_go",value:"English"},{key:"ko_kr",value:"한글"}],r=this.form.types[0].toLowerCase();"bishijie"==r?this.languages=t:"coinness"==r&&(this.languages=a)}}},n=o,i=(a("cd97"),a("2877")),l=Object(i["a"])(n,r,s,!1,null,"6d8efc95",null);l.exports},cb08:function(e,t,a){e.exports=a.p+"static/img/icon-no.233633bc.svg"},cd97:function(e,t,a){"use strict";var r=a("41d3"),s=a.n(r);s.a},e7a2:function(e,t,a){e.exports=a.p+"static/img/icon-yes.06589da8.svg"}}]);