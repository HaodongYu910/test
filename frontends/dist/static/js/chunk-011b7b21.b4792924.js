(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-011b7b21"],{"056f":function(t,e,a){},"1eb9":function(t,e,a){"use strict";var r=a("056f"),o=a.n(r);o.a},"2d92":function(t,e,a){"use strict";a.d(e,"mb",(function(){return i})),a.d(e,"N",(function(){return s})),a.d(e,"t",(function(){return n})),a.d(e,"D",(function(){return d})),a.d(e,"H",(function(){return u})),a.d(e,"pb",(function(){return p})),a.d(e,"k",(function(){return l})),a.d(e,"O",(function(){return c})),a.d(e,"M",(function(){return m})),a.d(e,"s",(function(){return h})),a.d(e,"C",(function(){return f})),a.d(e,"G",(function(){return g})),a.d(e,"ob",(function(){return b})),a.d(e,"j",(function(){return F})),a.d(e,"P",(function(){return v})),a.d(e,"Q",(function(){return _})),a.d(e,"L",(function(){return G})),a.d(e,"r",(function(){return y})),a.d(e,"i",(function(){return k})),a.d(e,"R",(function(){return j})),a.d(e,"T",(function(){return $})),a.d(e,"S",(function(){return w})),a.d(e,"g",(function(){return D})),a.d(e,"K",(function(){return S})),a.d(e,"h",(function(){return x})),a.d(e,"nb",(function(){return C})),a.d(e,"q",(function(){return V})),a.d(e,"F",(function(){return I})),a.d(e,"jb",(function(){return O})),a.d(e,"qb",(function(){return A})),a.d(e,"l",(function(){return L})),a.d(e,"I",(function(){return q})),a.d(e,"x",(function(){return z})),a.d(e,"gb",(function(){return N})),a.d(e,"ib",(function(){return T})),a.d(e,"hb",(function(){return J})),a.d(e,"p",(function(){return E})),a.d(e,"tb",(function(){return R})),a.d(e,"z",(function(){return P})),a.d(e,"d",(function(){return B})),a.d(e,"lb",(function(){return K})),a.d(e,"e",(function(){return H})),a.d(e,"kb",(function(){return M})),a.d(e,"U",(function(){return Q})),a.d(e,"u",(function(){return U})),a.d(e,"rb",(function(){return W})),a.d(e,"n",(function(){return X})),a.d(e,"X",(function(){return Y})),a.d(e,"B",(function(){return Z})),a.d(e,"v",(function(){return tt})),a.d(e,"fb",(function(){return et})),a.d(e,"eb",(function(){return at})),a.d(e,"bb",(function(){return rt})),a.d(e,"y",(function(){return ot})),a.d(e,"Y",(function(){return it})),a.d(e,"Z",(function(){return st})),a.d(e,"o",(function(){return nt})),a.d(e,"sb",(function(){return dt})),a.d(e,"w",(function(){return ut})),a.d(e,"J",(function(){return pt})),a.d(e,"E",(function(){return lt})),a.d(e,"ab",(function(){return ct})),a.d(e,"cb",(function(){return mt})),a.d(e,"db",(function(){return ht})),a.d(e,"W",(function(){return ft})),a.d(e,"V",(function(){return gt})),a.d(e,"m",(function(){return bt})),a.d(e,"f",(function(){return Ft})),a.d(e,"c",(function(){return vt})),a.d(e,"b",(function(){return _t})),a.d(e,"a",(function(){return Gt})),a.d(e,"A",(function(){return yt}));var r=a("bc3a"),o=a.n(r);a("c896");const i="http://192.168.2.38:9000",s=(t,e)=>o.a.get(i+"/api/project/project_list",{params:e,headers:t}).then(t=>t.data),n=(t,e)=>o.a.post(i+"/api/project/del_project",e,{headers:t}).then(t=>t.data),d=(t,e)=>o.a.post(i+"/api/project/disable_project",e,{headers:t}).then(t=>t.data),u=(t,e)=>o.a.post(i+"/api/project/enable_project",e,{headers:t}).then(t=>t.data),p=(t,e)=>o.a.post(i+"/api/project/update_project",e,{headers:t}).then(t=>t.data),l=(t,e)=>o.a.post(i+"/api/project/add_project",e,{headers:t}).then(t=>t.data),c=(t,e)=>o.a.get(i+"/api/title/project_info",{params:e,headers:t}).then(t=>t.data),m=(t,e)=>o.a.get(i+"/api/global/host_total",{params:e,headers:t}).then(t=>t.data),h=(t,e)=>o.a.post(i+"/api/global/del_host",e,{headers:t}).then(t=>t.data),f=(t,e)=>o.a.post(i+"/api/global/disable_host",e,{headers:t}).then(t=>t.data),g=(t,e)=>o.a.post(i+"/api/global/enable_host",e,{headers:t}).then(t=>t.data),b=(t,e)=>o.a.post(i+"/api/global/update_host",e,{headers:t}).then(t=>t.data),F=(t,e)=>o.a.post(i+"/api/global/add_host",e,{headers:t}).then(t=>t.data),v=(t,e)=>o.a.get(i+"/api/dynamic/dynamic",{params:e,headers:t}).then(t=>t.data),_=(t,e)=>o.a.get(i+"/api/member/project_member",{params:e,headers:t}).then(t=>t.data),G=(t,e)=>o.a.get(i+"/api/member/get_email",{params:e,headers:t}).then(t=>t.data),y=(t,e)=>o.a.post(i+"/api/member/del_email",e,{headers:t}).then(t=>t.data),k=(t,e)=>o.a.post(i+"/api/member/email_config",e,{headers:t}).then(t=>t.data),j=(t,e)=>o.a.get(i+"/api/report/auto_test_report",{params:e,headers:t}).then(t=>t.data),$=(t,e)=>o.a.get(i+"/api/report/test_time",{params:e,headers:t}).then(t=>t.data),w=(t,e)=>o.a.get(i+"/api/report/lately_ten",{params:e,headers:t}).then(t=>t.data),D=(t,e)=>o.a.post(i+"/api/api/add_api",e,{headers:t}).then(t=>t.data),S=(t,e)=>o.a.get(i+"/api/api/group",{params:e,headers:t}).then(t=>t.data),x=(t,e)=>o.a.post(i+"/api/api/add_group",e,{headers:t}).then(t=>t.data),C=(t,e)=>o.a.post(i+"/api/api/update_name_group",e,{headers:t}).then(t=>t.data),V=(t,e)=>o.a.post(i+"/api/api/del_group",e,{headers:t}).then(t=>t.data),I=(t,e)=>o.a.post(i+"/api/download",e,{headers:t}).then(t=>t.data),O=(t,e)=>o.a.post(i+"/api/user/login",e,t).then(t=>t.data),A=(t,e)=>o.a.post(i+"/api/risk/update",e,{headers:t}).then(t=>t.data),L=(t,e)=>o.a.post(i+"/api/risk/add",e,{headers:t}).then(t=>t.data),q=(t,e)=>o.a.post(i+"/api/risk/add",e,{headers:t}).then(t=>t.data),z=(t,e)=>o.a.post(i+"/api/risk/del",e,t).then(t=>t.data),N=(t,e)=>o.a.get(i+"/api/risk ",{params:e},t).then(t=>t.data),T=(t,e)=>o.a.get(i+"/api/todo ",{params:e},t).then(t=>t.data),J=(t,e)=>o.a.get(i+"/api/report ",{params:e},t).then(t=>t.data),E=(t,e)=>o.a.post(i+"/api/addreport",e,t).then(t=>t.data),R=(t,e)=>o.a.post(i+"/api/updatereport",e,t).then(t=>t.data),P=(t,e)=>o.a.post(i+"/api/delreport",e,t).then(t=>t.data),B=(t,e)=>o.a.post(i+"/api/send",e,t).then(t=>t.data),K=(t,e)=>o.a.get(i+"/api/stress/list",{params:e},{headers:t}).then(t=>t.data),H=(t,e)=>o.a.get(i+"/api/stress/stressDetail ",{params:e},t).then(t=>t.data),M=(t,e)=>o.a.post(i+"/api/stress/stresstool",e,t).then(t=>t.data),Q=(t,e)=>o.a.get(i+"/api/stress/version",{params:e},{headers:t}).then(t=>t.data),U=(t,e)=>o.a.post(i+"/api/tool/del_dicomData",e,t).then(t=>t.data),W=(t,e)=>o.a.post(i+"/api/tool/update_dicomData",e,t).then(t=>t.data),X=(t,e)=>o.a.post(i+"/api/tool/add_dicomData",e,t).then(t=>t.data),Y=(t,e)=>o.a.get(i+"/api/tool/dicomData",{params:e},{headers:t}).then(t=>t.data),Z=(t,e)=>o.a.post(i+"/api/tool/dicomcsv",e,t).then(t=>t.data),tt=(t,e)=>o.a.post(i+"/api/tool/delreport",e,t).then(t=>t.data),et=(t,e)=>o.a.get(i+"/api/stress/stressversion",{params:e},{headers:t}).then(t=>t.data),at=(t,e)=>o.a.post(i+"/api/stress/stressresult",e,t).then(t=>t.data),rt=(t,e)=>o.a.post(i+"/api/stress/stressfigure",e,t).then(t=>t.data),ot=(t,e)=>o.a.post(i+"/api/tool/delete_patients",e,t).then(t=>t.data),it=(t,e)=>o.a.get(i+"/api/tool/getduration",{params:e},{headers:t}).then(t=>t.data),st=(t,e)=>o.a.get(i+"/api/tool/durationData",{params:e},{headers:t}).then(t=>t.data),nt=(t,e)=>o.a.post(i+"/api/tool/add_duration",e,t).then(t=>t.data),dt=(t,e)=>o.a.post(i+"/api/tool/update_duration",e,t).then(t=>t.data),ut=(t,e)=>o.a.post(i+"/api/tool/del_duration",e,t).then(t=>t.data),pt=(t,e)=>o.a.post(i+"/api/tool/enable_duration",e,t).then(t=>t.data),lt=(t,e)=>o.a.post(i+"/api/tool/disable_duration",e,t).then(t=>t.data),ct=(t,e)=>o.a.get(i+"/api/tool/duration_verify",{params:e},{headers:t}).then(t=>t.data),mt=(t,e)=>o.a.get(i+"/api/tool/somkerecord",{params:e},{headers:t}).then(t=>t.data),ht=(t,e)=>o.a.post(i+"/api/tool/somke",e,t).then(t=>t.data),ft=(t,e)=>o.a.post(i+"/api/tool/dicomSend",e,t).then(t=>t.data),gt=(t,e)=>o.a.get(i+"/api/base/getdata",{params:e},{headers:t}).then(t=>t.data),bt=(t,e)=>o.a.post(i+"/api/base/addData",e,t).then(t=>t.data),Ft=(t,e)=>o.a.post(i+"/api/base/updateData",e,t).then(t=>t.data),vt=(t,e)=>o.a.post(i+"/api/base/enablebase",e,t).then(t=>t.data),_t=(t,e)=>o.a.post(i+"/api/base/disablebase",e,t).then(t=>t.data),Gt=(t,e)=>o.a.post(i+"/api/base/delbasedata",e,t).then(t=>t.data),yt=(t,e)=>o.a.get(i+"/api/base/dicom",{params:e},{headers:t}).then(t=>t.data)},"41d3":function(t,e,a){},6344:function(t,e,a){"use strict";a.r(e);var r=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("section",[a("el-row",{staticClass:"row-title",attrs:{span:24}},[a("el-col",{attrs:{span:4}},[a("el-button",{staticClass:"addGroup",on:{click:t.handleAddGroup}},[t._v("新增分组")]),a("router-link",{staticStyle:{"text-decoration":"none",color:"aliceblue"},attrs:{to:{name:"快速测试",params:{project_id:this.$route.params.project_id}}}},[a("el-button",{staticClass:"addGroup"},[t._v("快速测试")])],1),a("div",{staticClass:"api-title"},[a("strong",[t._v("接口分组")])]),a("div",{staticClass:"api-title",staticStyle:{cursor:"pointer"}},[a("router-link",{staticStyle:{"text-decoration":"none",color:"aliceblue"},attrs:{to:{name:"接口列表",params:{project_id:this.$route.params.project_id}}}},[t._v(" 所有接口 ")])],1),a("aside",[a("el-menu",{staticClass:"el-menu-vertical-demo",attrs:{"default-active":"2","active-text-color":"rgb(32, 160, 255)","unique-opened":!0}},[t._l(t.groupData,(function(e,r){return[a("router-link",{staticStyle:{"text-decoration":"none"},attrs:{to:{name:"分组接口列表",params:{project_id:t.project,firstGroup:e.id}}}},[a("el-menu-item",{key:e.id,staticClass:"group",attrs:{index:r+""}},[a("template",{slot:"title"},[t._v(t._s(e.name)+" "),a("el-dropdown",{staticClass:"editGroup",staticStyle:{"margin-right":"10%"},attrs:{trigger:"hover"}},[a("i",{staticClass:"el-icon-more"}),a("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},[a("el-dropdown-item",{nativeOn:{click:function(a){return t.handleDelFirst(e.id)}}},[t._v("删除")]),a("el-dropdown-item",{nativeOn:{click:function(a){return t.handleEditFirstGroup(e.id,e.name)}}},[t._v("修改")])],1)],1)],1)],2)],1)]}))],2)],1)],1),a("el-dialog",{staticStyle:{width:"60%",left:"20%"},attrs:{title:"新增分组",visible:t.addGroupFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(e){t.addGroupFormVisible=e}}},[a("el-form",{ref:"addGroupForm",attrs:{model:t.addGroupForm,"label-width":"80px",rules:t.addGroupFormRules}},[a("el-form-item",{attrs:{label:"分组名称",prop:"firstgroup"}},[a("el-input",{staticStyle:{width:"90%"},attrs:{"auto-complete":"off"},model:{value:t.addGroupForm.firstgroup,callback:function(e){t.$set(t.addGroupForm,"firstgroup","string"===typeof e?e.trim():e)},expression:"addGroupForm.firstgroup"}})],1)],1),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{nativeOn:{click:function(e){t.addGroupFormVisible=!1}}},[t._v("取消")]),a("el-button",{attrs:{type:"primary",loading:t.addGroupLoading},nativeOn:{click:function(e){return t.addGroupSubmit(e)}}},[t._v("提交")])],1)],1),a("el-dialog",{staticStyle:{width:"60%",left:"20%"},attrs:{title:"编辑分组",visible:t.editFirstGroupFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(e){t.editFirstGroupFormVisible=e}}},[a("el-form",{ref:"editFirstGroupForm",attrs:{model:t.editFirstGroupForm,"label-width":"80px",rules:t.editFirstGroupFormRules}},[a("el-form-item",{attrs:{label:"分组名称",prop:"secondFirstGroup"}},[a("el-input",{attrs:{"auto-complete":"off"},model:{value:t.editFirstGroupForm.secondFirstGroup,callback:function(e){t.$set(t.editFirstGroupForm,"secondFirstGroup","string"===typeof e?e.trim():e)},expression:"editFirstGroupForm.secondFirstGroup"}})],1)],1),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{nativeOn:{click:function(e){t.editFirstGroupFormVisible=!1}}},[t._v("取消")]),a("el-button",{attrs:{type:"primary",loading:t.editFirstGroupLoading},nativeOn:{click:function(e){return t.editFirstGroupSubmit(e)}}},[t._v("提交")])],1)],1),a("el-col",{attrs:{span:20}},[a("div",{staticStyle:{"margin-left":"10px","margin-right":"20px"}},[a("router-view")],1)])],1)],1)},o=[],i=a("2d92"),s={data(){return{project:"",groupData:[],addGroupFormVisible:!1,addGroupLoading:!1,addFormVisible:!1,addGroupFormRules:{firstgroup:[{required:!0,message:"请输入子分组名称",trigger:"blur"}]},addGroupForm:{firstgroup:""},editFirstGroupFormVisible:!1,editFirstGroupLoading:!1,editFirstFormVisible:!1,editFirstGroupFormRules:{secondFirstGroup:[{required:!0,message:"请输入分组名称",trigger:"blur"}]},editFirstGroupForm:{firstgroup:"",second_id:""},filters:{name:""},api:[],total:0,page:1,listLoading:!1,sels:[],apiView:!0}},methods:{init(){this.addGroupForm.firstgroup=""},getApiGroup(){let t=this,e={project_id:this.$route.params.project_id},a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(i["K"])(a,e).then(e=>{let{msg:a,code:r,data:o}=e;"0"===r?(t.groupData=o,t.init()):t.$message.error({message:a,center:!0})})},handleAddGroup(){this.addGroupFormVisible=!0},handleEditFirstGroup(t,e){this.editFirstGroupFormVisible=!0,this.editFirstGroupForm.second_id=t,this.editFirstGroupForm.secondFirstGroup=e},addGroupSubmit(){this.$refs.addGroupForm.validate(t=>{if(t){let t=this;this.$confirm("确认提交吗？","提示",{}).then(()=>{t.addGroupLoading=!0;let e={project_id:Number(this.$route.params.project_id),name:t.addGroupForm.firstgroup},a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(i["h"])(a,e).then(e=>{let{msg:a,code:r,data:o}=e;t.addGroupLoading=!1,"0"===r?(t.$message({message:"添加成功",center:!0,type:"success"}),t.$refs["addGroupForm"].resetFields(),t.addGroupFormVisible=!1,t.getApiGroup(),t.init()):"999997"===r?t.$message.error({message:a,center:!0}):(t.$message.error({message:a,center:!0}),t.$refs["addGroupForm"].resetFields(),t.addGroupFormVisible=!1,t.getApiGroup(),t.init())})})}})},editFirstGroupSubmit(){this.$refs.editFirstGroupForm.validate(t=>{if(t){let t=this;this.$confirm("确认提交吗？","提示",{}).then(()=>{t.editFirstGroupLoading=!0;let e={project_id:Number(this.$route.params.project_id),name:t.editFirstGroupForm.secondFirstGroup,id:t.editFirstGroupForm.second_id},a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(i["nb"])(a,e).then(e=>{let{msg:a,code:r,data:o}=e;t.editFirstGroupLoading=!1,"0"===r?(t.$message({message:"修改成功",center:!0,type:"success"}),t.$refs["editFirstGroupForm"].resetFields(),t.editFirstGroupFormVisible=!1,t.getApiGroup(),t.init()):"999997"===r?t.$message.error({message:a,center:!0}):(t.$message.error({message:a,center:!0}),t.$refs["editFirstGroupForm"].resetFields(),t.editFirstGroupFormVisible=!1,t.getApiGroup(),t.init())})})}})},handleDelFirst:function(t){this.$confirm("确认删除该记录吗?","提示",{type:"warning"}).then(()=>{let e=this,a={id:Number(t),project_id:Number(this.$route.params.project_id)},r={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(i["q"])(r,a).then(t=>{let{msg:a,code:r,data:o}=t;"0"===r?e.$message({message:"删除成功",center:!0,type:"success"}):e.$message.error({message:a,center:!0}),e.getApiGroup()})})}},mounted(){this.getApiGroup(),this.project=this.$route.params.project_id}},n=s,d=(a("1eb9"),a("2877")),u=Object(d["a"])(n,r,o,!1,null,"ceb0f8e4",null);e["default"]=u.exports},c896:function(t,e,a){"use strict";var r=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("div",{staticClass:"crumbs"},[a("el-breadcrumb",{attrs:{separator:"/"}},[a("el-breadcrumb-item",[a("i",{staticClass:"el-icon-lx-calendar"}),t._v(" 测试工具")]),a("el-breadcrumb-item",[t._v("推送工具")])],1)],1),a("div",{staticClass:"container"},[a("div",{staticClass:"form-box"},[a("el-form",{ref:"form",attrs:{model:t.form,"status-icon":"",rules:t.rules,"label-width":"80px"}},[a("el-form-item",{attrs:{label:"推送ID",prop:"pushID"}},[a("el-col",{attrs:{span:10}},[a("el-input",{attrs:{id:"pushID"},model:{value:t.form.pushID,callback:function(e){t.$set(t.form,"pushID",e)},expression:"form.pushID"}})],1)],1),a("el-form-item",{attrs:{label:"推送环境",prop:"environment"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:t.form.environment,callback:function(e){t.$set(t.form,"environment",e)},expression:"form.environment"}},[a("el-option",{key:"test",attrs:{label:"测试环境",value:"test"}}),a("el-option",{key:"online",attrs:{label:"线上环境",value:"online"}})],1)],1),a("el-form-item",{attrs:{label:"推送类型",prop:"types"}},[a("el-cascader",{attrs:{options:t.types},on:{change:function(e){return t.changeLang("form")}},model:{value:t.form.types,callback:function(e){t.$set(t.form,"types",e)},expression:"form.types"}})],1),a("el-form-item",{attrs:{label:"选择语言",prop:"languages"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:t.form.languages,callback:function(e){t.$set(t.form,"languages",e)},expression:"form.languages"}},t._l(t.languages,(function(t,e){return a("el-option",{key:t.key,attrs:{label:t.value,value:t.key}})})),1)],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:function(e){return t.onSubmit("form")}}},[t._v("确定推送")]),a("el-button",{on:{click:function(e){return t.resetForm("form")}}},[t._v("重置")])],1)],1)],1)])])},o=[],i={name:"baseform",data:function(){return{types:[{value:"bishijie",label:"Boimind",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"replay",label:"币圈"},{value:"monitor",label:"盯盘"}]},{value:"coinness",label:"coinness",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"monitor",label:"盯盘"}]}],languages:[],form:{pushID:"",environment:"",types:[],languages:[]},rules:{pushID:[{required:!0,message:"请输入推送ID",trigger:"blur"}],environment:[{required:!0,message:"请选择推送环境",trigger:"blur"}],types:[{required:!0,message:"请选择推送类型",trigger:"blur"}],languages:[{required:!0,message:"请选择语言",trigger:"blur"}]}}},methods:{onSubmit(t){this.$refs[t].validate(t=>{if(!t)return console.log("error submit"),!1;console.log("语言："+this.form.languages),console.log("pushID："+this.form.pushID),console.log("APP："+this.form.types[0]),console.log("推送类型："+this.form.types[1]),console.log("environment："+this.form.environment),this.$ajax.post("/bishijie/push",{id:this.form.pushID,service:this.form.environment,system:this.form.types[0],module:this.form.types[1],lang:this.form.languages,rid:""}).then(t=>{"0"==t.data.code?null==t.data.data||t.data.data[0]?this.$message.success("push成功！"):this.$message.error(t.data.data[1]):this.$message.error(t.data.msg)}).catch((function(t){console.log(t)}))})},resetForm(t){this.$refs[t].resetFields()},changeLang(t){this.languages=[],this.form.languages="";var e=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"}],a=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"},{key:"en_go",value:"English"},{key:"ko_kr",value:"한글"}],r=this.form.types[0].toLowerCase();"bishijie"==r?this.languages=e:"coinness"==r&&(this.languages=a)}}},s=i,n=(a("cd97"),a("2877")),d=Object(n["a"])(s,r,o,!1,null,"6d8efc95",null);d.exports},cd97:function(t,e,a){"use strict";var r=a("41d3"),o=a.n(r);o.a}}]);