(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2af80dce"],{"2d92":function(t,e,a){"use strict";a.d(e,"fb",(function(){return i})),a.d(e,"J",(function(){return o})),a.d(e,"s",(function(){return s})),a.d(e,"z",(function(){return d})),a.d(e,"D",(function(){return p})),a.d(e,"ib",(function(){return l})),a.d(e,"j",(function(){return u})),a.d(e,"K",(function(){return m})),a.d(e,"I",(function(){return c})),a.d(e,"r",(function(){return h})),a.d(e,"y",(function(){return g})),a.d(e,"C",(function(){return f})),a.d(e,"hb",(function(){return b})),a.d(e,"i",(function(){return _})),a.d(e,"L",(function(){return F})),a.d(e,"M",(function(){return j})),a.d(e,"H",(function(){return v})),a.d(e,"q",(function(){return y})),a.d(e,"h",(function(){return S})),a.d(e,"N",(function(){return k})),a.d(e,"P",(function(){return w})),a.d(e,"O",(function(){return $})),a.d(e,"f",(function(){return C})),a.d(e,"G",(function(){return x})),a.d(e,"g",(function(){return L})),a.d(e,"gb",(function(){return O})),a.d(e,"p",(function(){return P})),a.d(e,"B",(function(){return T})),a.d(e,"db",(function(){return D})),a.d(e,"jb",(function(){return E})),a.d(e,"k",(function(){return N})),a.d(e,"E",(function(){return U})),a.d(e,"u",(function(){return z})),a.d(e,"ab",(function(){return J})),a.d(e,"Z",(function(){return V})),a.d(e,"cb",(function(){return q})),a.d(e,"bb",(function(){return A})),a.d(e,"n",(function(){return I})),a.d(e,"lb",(function(){return M})),a.d(e,"w",(function(){return R})),a.d(e,"d",(function(){return H})),a.d(e,"eb",(function(){return B})),a.d(e,"Q",(function(){return G})),a.d(e,"x",(function(){return K})),a.d(e,"mb",(function(){return Q})),a.d(e,"o",(function(){return W})),a.d(e,"Y",(function(){return X})),a.d(e,"W",(function(){return Y})),a.d(e,"X",(function(){return Z})),a.d(e,"V",(function(){return tt})),a.d(e,"v",(function(){return et})),a.d(e,"S",(function(){return at})),a.d(e,"T",(function(){return rt})),a.d(e,"m",(function(){return nt})),a.d(e,"kb",(function(){return it})),a.d(e,"t",(function(){return ot})),a.d(e,"F",(function(){return st})),a.d(e,"A",(function(){return dt})),a.d(e,"U",(function(){return pt})),a.d(e,"R",(function(){return lt})),a.d(e,"l",(function(){return ut})),a.d(e,"e",(function(){return mt})),a.d(e,"c",(function(){return ct})),a.d(e,"b",(function(){return ht})),a.d(e,"a",(function(){return gt}));var r=a("bc3a"),n=a.n(r);const i="http://192.168.2.38:9000",o=(t,e)=>n.a.get(i+"/api/project/project_list",{params:e,headers:t}).then(t=>t.data),s=(t,e)=>n.a.post(i+"/api/project/del_project",e,{headers:t}).then(t=>t.data),d=(t,e)=>n.a.post(i+"/api/project/disable_project",e,{headers:t}).then(t=>t.data),p=(t,e)=>n.a.post(i+"/api/project/enable_project",e,{headers:t}).then(t=>t.data),l=(t,e)=>n.a.post(i+"/api/project/update_project",e,{headers:t}).then(t=>t.data),u=(t,e)=>n.a.post(i+"/api/project/add_project",e,{headers:t}).then(t=>t.data),m=(t,e)=>n.a.get(i+"/api/title/project_info",{params:e,headers:t}).then(t=>t.data),c=(t,e)=>n.a.get(i+"/api/global/host_total",{params:e,headers:t}).then(t=>t.data),h=(t,e)=>n.a.post(i+"/api/global/del_host",e,{headers:t}).then(t=>t.data),g=(t,e)=>n.a.post(i+"/api/global/disable_host",e,{headers:t}).then(t=>t.data),f=(t,e)=>n.a.post(i+"/api/global/enable_host",e,{headers:t}).then(t=>t.data),b=(t,e)=>n.a.post(i+"/api/global/update_host",e,{headers:t}).then(t=>t.data),_=(t,e)=>n.a.post(i+"/api/global/add_host",e,{headers:t}).then(t=>t.data),F=(t,e)=>n.a.get(i+"/api/dynamic/dynamic",{params:e,headers:t}).then(t=>t.data),j=(t,e)=>n.a.get(i+"/api/member/project_member",{params:e,headers:t}).then(t=>t.data),v=(t,e)=>n.a.get(i+"/api/member/get_email",{params:e,headers:t}).then(t=>t.data),y=(t,e)=>n.a.post(i+"/api/member/del_email",e,{headers:t}).then(t=>t.data),S=(t,e)=>n.a.post(i+"/api/member/email_config",e,{headers:t}).then(t=>t.data),k=(t,e)=>n.a.get(i+"/api/report/auto_test_report",{params:e,headers:t}).then(t=>t.data),w=(t,e)=>n.a.get(i+"/api/report/test_time",{params:e,headers:t}).then(t=>t.data),$=(t,e)=>n.a.get(i+"/api/report/lately_ten",{params:e,headers:t}).then(t=>t.data),C=(t,e)=>n.a.post(i+"/api/api/add_api",e,{headers:t}).then(t=>t.data),x=(t,e)=>n.a.get(i+"/api/api/group",{params:e,headers:t}).then(t=>t.data),L=(t,e)=>n.a.post(i+"/api/api/add_group",e,{headers:t}).then(t=>t.data),O=(t,e)=>n.a.post(i+"/api/api/update_name_group",e,{headers:t}).then(t=>t.data),P=(t,e)=>n.a.post(i+"/api/api/del_group",e,{headers:t}).then(t=>t.data),T=(t,e)=>n.a.post(i+"/api/download",e,{headers:t}).then(t=>t.data),D=(t,e)=>n.a.post(i+"/api/user/login",e,t).then(t=>t.data),E=(t,e)=>n.a.post(i+"/api/risk/update",e,{headers:t}).then(t=>t.data),N=(t,e)=>n.a.post(i+"/api/risk/add",e,{headers:t}).then(t=>t.data),U=(t,e)=>n.a.post(i+"/api/risk/add",e,{headers:t}).then(t=>t.data),z=(t,e)=>n.a.post(i+"/api/risk/del",e,t).then(t=>t.data),J=(t,e)=>n.a.get(i+"/api/risk ",{params:e},t).then(t=>t.data),V=(t,e)=>n.a.post(i+"/api/jira/figure ",e,t).then(t=>t.data),q=(t,e)=>n.a.get(i+"/api/todo ",{params:e},t).then(t=>t.data),A=(t,e)=>n.a.get(i+"/api/report ",{params:e},t).then(t=>t.data),I=(t,e)=>n.a.post(i+"/api/addreport",e,t).then(t=>t.data),M=(t,e)=>n.a.post(i+"/api/updatereport",e,t).then(t=>t.data),R=(t,e)=>n.a.post(i+"/api/delreport",e,t).then(t=>t.data),H=(t,e)=>n.a.post(i+"/api/send",e,t).then(t=>t.data),B=(t,e)=>n.a.post(i+"/api/tool/stresstool",e,t).then(t=>t.data),G=(t,e)=>n.a.get(i+"/api/tool/version",{params:e},{headers:t}).then(t=>t.data),K=(t,e)=>n.a.post(i+"/api/tool/del_stressdata",e,t).then(t=>t.data),Q=(t,e)=>n.a.post(i+"/api/tool/update_stressdata",e,t).then(t=>t.data),W=(t,e)=>n.a.post(i+"/api/tool/add_stressdata",e,t).then(t=>t.data),X=(t,e)=>n.a.get(i+"/api/tool/stressversion",{params:e},{headers:t}).then(t=>t.data),Y=(t,e)=>n.a.get(i+"/api/tool/stressdata",{params:e},{headers:t}).then(t=>t.data),Z=(t,e)=>n.a.post(i+"/api/tool/stressresult",e,t).then(t=>t.data),tt=(t,e)=>n.a.post(i+"/api/tool/stressfigure",e,t).then(t=>t.data),et=(t,e)=>n.a.post(i+"/api/tool/delete_patients",e,t).then(t=>t.data),at=(t,e)=>n.a.get(i+"/api/tool/getduration",{params:e},{headers:t}).then(t=>t.data),rt=(t,e)=>n.a.get(i+"/api/tool/durationData",{params:e},{headers:t}).then(t=>t.data),nt=(t,e)=>n.a.post(i+"/api/tool/add_duration",e,t).then(t=>t.data),it=(t,e)=>n.a.post(i+"/api/tool/update_duration",e,t).then(t=>t.data),ot=(t,e)=>n.a.post(i+"/api/tool/del_duration",e,t).then(t=>t.data),st=(t,e)=>n.a.post(i+"/api/tool/enable_duration",e,t).then(t=>t.data),dt=(t,e)=>n.a.post(i+"/api/tool/disable_duration",e,t).then(t=>t.data),pt=(t,e)=>n.a.get(i+"/api/tool/duration_verify",{params:e},{headers:t}).then(t=>t.data),lt=(t,e)=>n.a.get(i+"/api/base/getdata",{params:e},{headers:t}).then(t=>t.data),ut=(t,e)=>n.a.post(i+"/api/base/addData",e,t).then(t=>t.data),mt=(t,e)=>n.a.post(i+"/api/base/updateData",e,t).then(t=>t.data),ct=(t,e)=>n.a.post(i+"/api/base/enablebase",e,t).then(t=>t.data),ht=(t,e)=>n.a.post(i+"/api/base/disablebase",e,t).then(t=>t.data),gt=(t,e)=>n.a.post(i+"/api/base/delbasedata",e,t).then(t=>t.data)},"5f66":function(t,e,a){"use strict";a.r(e);var r=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("el-row",{staticClass:"member-manage"},[a("p",{staticStyle:{color:"#999"}},[t._v("*注"),a("strong",[t._v(": ")]),t._v("自动化测试结果会发送给所有项目成员")]),a("div",{staticStyle:{"margin-bottom":"20px","font-size":"20px"}},[a("div",[a("div",{staticStyle:{display:"inline"}},[t._v("测试报告发送账号： ")]),t.reportFrom?t._e():a("div",{staticStyle:{display:"inline"}},[t._v("未添加账号")]),t.reportFrom?a("div",{staticStyle:{display:"inline"}},[t._v(t._s(t.reportFrom))]):t._e(),t._v(" "),a("i",{staticClass:"el-icon-edit",staticStyle:{cursor:"pointer",display:"inline"},on:{click:function(e){t.editFormVisible=!0}}}),t._v(" "),t.reportFrom?a("i",{staticClass:"el-icon-delete",staticStyle:{cursor:"pointer",display:"inline"},on:{click:function(e){return t.DelEmail()}}}):t._e()])]),a("el-dialog",{staticStyle:{width:"60%",left:"20%"},attrs:{title:"编辑",visible:t.editFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(e){t.editFormVisible=e}}},[a("el-form",{ref:"editForm",attrs:{model:t.editForm,"label-width":"100px",rules:t.editFormRules}},[a("el-form-item",{attrs:{label:"发送人邮箱:",prop:"reportFrom"}},[a("el-input",{attrs:{"auto-complete":"off"},model:{value:t.editForm.reportFrom,callback:function(e){t.$set(t.editForm,"reportFrom","string"===typeof e?e.trim():e)},expression:"editForm.reportFrom"}})],1),a("el-form-item",{attrs:{label:"用户名:",prop:"mailUser"}},[a("el-input",{attrs:{"auto-complete":"off"},model:{value:t.editForm.mailUser,callback:function(e){t.$set(t.editForm,"mailUser","string"===typeof e?e.trim():e)},expression:"editForm.mailUser"}})],1),a("el-form-item",{attrs:{label:"口令:",prop:"mailPass"}},[a("el-input",{attrs:{"auto-complete":"off"},model:{value:t.editForm.mailPass,callback:function(e){t.$set(t.editForm,"mailPass","string"===typeof e?e.trim():e)},expression:"editForm.mailPass"}})],1),a("el-form-item",{attrs:{label:"邮箱服务器:",prop:"mailSmtp"}},[a("el-input",{attrs:{"auto-complete":"off"},model:{value:t.editForm.mailSmtp,callback:function(e){t.$set(t.editForm,"mailSmtp","string"===typeof e?e.trim():e)},expression:"editForm.mailSmtp"}})],1)],1),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{nativeOn:{click:function(e){t.editFormVisible=!1}}},[t._v("取消")]),a("el-button",{attrs:{type:"primary",loading:t.editLoading},nativeOn:{click:function(e){return t.editSubmit(e)}}},[t._v("提交")])],1)],1),a("el-col",{attrs:{span:24}},[a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.listLoading,expression:"listLoading"}],staticStyle:{width:"100%"},attrs:{data:t.memberData,"highlight-current-row":""}},[a("el-table-column",{attrs:{prop:"username",label:"姓名","min-width":"30%",sortable:""}}),a("el-table-column",{attrs:{prop:"permissionType",label:"权限","min-width":"30%",sortable:""}}),a("el-table-column",{attrs:{prop:"userPhone",label:"手机号","min-width":"20%",sortable:""}}),a("el-table-column",{attrs:{prop:"userEmail",label:"邮箱地址","min-width":"20%",sortable:""}})],1),a("el-pagination",{staticStyle:{float:"right"},attrs:{layout:"prev, pager, next","page-size":20,"page-count":t.total},on:{"current-change":t.handleCurrentChange}})],1)],1)},n=[],i=a("2d92"),o={data(){return{memberData:[],total:0,page:1,listLoading:!1,reportFrom:"",editFormVisible:!1,editLoading:!1,editFormRules:{reportFrom:[{required:!0,message:"请输入发送人",trigger:"blur"},{min:1,max:100,message:"长度在 1 到 100 个字符",trigger:"blur"}],mailUser:[{required:!0,message:"请输入用户名",trigger:"blur"},{min:1,max:100,message:"长度在 1 到 100 个字符",trigger:"blur"}],mailPass:[{required:!0,message:"请输入口令",trigger:"blur"},{min:1,max:100,message:"长度在 1 到 100 个字符",trigger:"blur"}],mailSmtp:[{required:!1,message:"请输入邮件服务器",trigger:"blur"},{min:1,max:100,message:"长度在 1 到 100 个字符",trigger:"blur"}]},editForm:{}}},methods:{handleCurrentChange(t){this.page=t,this.getProjectMember()},getProjectMember(){this.listLoading=!0;let t=this,e={project_id:this.$route.params.project_id,page:t.page},a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(i["M"])(a,e).then(e=>{let{msg:a,code:r,data:n}=e;t.listLoading=!1,"0"===r?(t.total=n.total,t.memberData=n.data):t.$message.error({message:a,center:!0})})},getEmailConfig(){let t=this,e={project_id:this.$route.params.project_id},a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(i["H"])(a,e).then(e=>{let{msg:a,code:r,data:n}=e;t.listLoading=!1,"0"===r?(console.log(n),n?(t.reportFrom=n.reportFrom,t.editForm=n):(t.reportFrom="",t.editForm={})):t.$message.error({message:a,center:!0})})},DelEmail(){let t=this,e={project_id:Number(this.$route.params.project_id)},a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(i["q"])(a,e).then(e=>{let{msg:a,code:r,data:n}=e;t.listLoading=!1,"0"===r?(t.$message.success({message:"删除成功",center:!0}),t.getEmailConfig()):t.$message.error({message:a,center:!0})})},editSubmit:function(){let t=this;this.$refs.editForm.validate(e=>{e&&this.$confirm("确认提交吗？","提示",{}).then(()=>{t.editLoading=!0;let e={project_id:Number(this.$route.params.project_id),reportFrom:this.editForm.reportFrom,mailUser:this.editForm.mailUser,mailPass:this.editForm.mailPass,mailSmtp:this.editForm.mailSmtp},a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(i["h"])(a,e).then(e=>{let{msg:a,code:r,data:n}=e;t.editLoading=!1,"0"===r?(t.$message({message:"修改成功",center:!0,type:"success"}),t.$refs["editForm"].resetFields(),t.editFormVisible=!1,t.getEmailConfig()):t.$message.error({message:a,center:!0})})})})}},mounted(){this.getProjectMember(),this.getEmailConfig()}},s=o,d=(a("d534"),a("2877")),p=Object(d["a"])(s,r,n,!1,null,"5c721dca",null);e["default"]=p.exports},"9a51":function(t,e,a){},d534:function(t,e,a){"use strict";var r=a("9a51"),n=a.n(r);n.a}}]);