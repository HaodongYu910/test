(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-b8818bd8"],{"0290":function(t,a,e){"use strict";e.r(a);var r=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{staticClass:"login-wrap"},[e("div",{staticClass:"ms-login"},[e("div",{staticClass:"ms-title"},[t._v("Biomind Test Platform")]),e("el-form",{ref:"ruleForm",staticClass:"ms-content",attrs:{model:t.ruleForm,rules:t.rules,"label-width":"0px"}},[e("el-form-item",{attrs:{prop:"username"}},[e("el-input",{attrs:{placeholder:"username"},model:{value:t.ruleForm.username,callback:function(a){t.$set(t.ruleForm,"username",a)},expression:"ruleForm.username"}},[e("el-button",{attrs:{slot:"prepend",icon:"el-icon-user-solid"},slot:"prepend"})],1)],1),e("el-form-item",{attrs:{prop:"password"}},[e("el-input",{attrs:{type:"password",placeholder:"password"},nativeOn:{keyup:function(a){return!a.type.indexOf("key")&&t._k(a.keyCode,"enter",13,a.key,"Enter")?null:t.submitForm("ruleForm")}},model:{value:t.ruleForm.password,callback:function(a){t.$set(t.ruleForm,"password",a)},expression:"ruleForm.password"}},[e("el-button",{attrs:{slot:"prepend",icon:"el-icon-s-goods"},slot:"prepend"})],1)],1),e("div",{staticClass:"login-btn"},[e("el-button",{attrs:{type:"primary"},on:{click:function(a){return t.submitForm("ruleForm")}}},[t._v("登录")])],1)],1)],1)])},n=[],o=e("2d92"),s={data:function(){return{ruleForm:{username:"",password:""},rules:{username:[{required:!0,message:"请输入用户名",trigger:"blur"}],password:[{required:!0,message:"请输入密码",trigger:"blur"}]}}},methods:{submitForm(t){this.$refs[t].validate(t=>{if(!t)return!1;{let t={username:this.ruleForm.username,password:this.ruleForm.password},a={"Content-Type":"application/json"};Object(o["db"])(a,t).then(t=>{let{msg:a,code:e,data:r}=t;console.log("code:"+e),"0"===e?(sessionStorage.setItem("username",JSON.stringify(r.first_name)),sessionStorage.setItem("token",JSON.stringify(r.key)),this.$message.success("登录成功"),localStorage.setItem("ms_username",this.ruleForm.username),localStorage.setItem("date_joined",JSON.stringify(r.date_joined)),this.$router.push("/")):this.$message.error(a)})}})}}},d=s,i=(e("ea20"),e("2877")),u=Object(i["a"])(d,r,n,!1,null,"0d1738ad",null);a["default"]=u.exports},"2d92":function(t,a,e){"use strict";e.d(a,"fb",(function(){return o})),e.d(a,"J",(function(){return s})),e.d(a,"s",(function(){return d})),e.d(a,"z",(function(){return i})),e.d(a,"D",(function(){return u})),e.d(a,"ib",(function(){return p})),e.d(a,"j",(function(){return l})),e.d(a,"K",(function(){return c})),e.d(a,"I",(function(){return h})),e.d(a,"r",(function(){return m})),e.d(a,"y",(function(){return f})),e.d(a,"C",(function(){return b})),e.d(a,"hb",(function(){return g})),e.d(a,"i",(function(){return _})),e.d(a,"L",(function(){return j})),e.d(a,"M",(function(){return k})),e.d(a,"H",(function(){return w})),e.d(a,"q",(function(){return v})),e.d(a,"h",(function(){return y})),e.d(a,"N",(function(){return F})),e.d(a,"P",(function(){return C})),e.d(a,"O",(function(){return O})),e.d(a,"f",(function(){return S})),e.d(a,"G",(function(){return $})),e.d(a,"g",(function(){return x})),e.d(a,"gb",(function(){return J})),e.d(a,"p",(function(){return I})),e.d(a,"B",(function(){return D})),e.d(a,"db",(function(){return N})),e.d(a,"jb",(function(){return q})),e.d(a,"k",(function(){return E})),e.d(a,"E",(function(){return T})),e.d(a,"u",(function(){return B})),e.d(a,"ab",(function(){return P})),e.d(a,"Z",(function(){return z})),e.d(a,"cb",(function(){return A})),e.d(a,"bb",(function(){return G})),e.d(a,"n",(function(){return H})),e.d(a,"lb",(function(){return K})),e.d(a,"w",(function(){return L})),e.d(a,"d",(function(){return M})),e.d(a,"eb",(function(){return Q})),e.d(a,"Q",(function(){return R})),e.d(a,"x",(function(){return U})),e.d(a,"mb",(function(){return V})),e.d(a,"o",(function(){return W})),e.d(a,"Y",(function(){return X})),e.d(a,"W",(function(){return Y})),e.d(a,"X",(function(){return Z})),e.d(a,"V",(function(){return tt})),e.d(a,"v",(function(){return at})),e.d(a,"S",(function(){return et})),e.d(a,"T",(function(){return rt})),e.d(a,"m",(function(){return nt})),e.d(a,"kb",(function(){return ot})),e.d(a,"t",(function(){return st})),e.d(a,"F",(function(){return dt})),e.d(a,"A",(function(){return it})),e.d(a,"U",(function(){return ut})),e.d(a,"R",(function(){return pt})),e.d(a,"l",(function(){return lt})),e.d(a,"e",(function(){return ct})),e.d(a,"c",(function(){return ht})),e.d(a,"b",(function(){return mt})),e.d(a,"a",(function(){return ft}));var r=e("bc3a"),n=e.n(r);const o="http://192.168.2.38:9000",s=(t,a)=>n.a.get(o+"/api/project/project_list",{params:a,headers:t}).then(t=>t.data),d=(t,a)=>n.a.post(o+"/api/project/del_project",a,{headers:t}).then(t=>t.data),i=(t,a)=>n.a.post(o+"/api/project/disable_project",a,{headers:t}).then(t=>t.data),u=(t,a)=>n.a.post(o+"/api/project/enable_project",a,{headers:t}).then(t=>t.data),p=(t,a)=>n.a.post(o+"/api/project/update_project",a,{headers:t}).then(t=>t.data),l=(t,a)=>n.a.post(o+"/api/project/add_project",a,{headers:t}).then(t=>t.data),c=(t,a)=>n.a.get(o+"/api/title/project_info",{params:a,headers:t}).then(t=>t.data),h=(t,a)=>n.a.get(o+"/api/global/host_total",{params:a,headers:t}).then(t=>t.data),m=(t,a)=>n.a.post(o+"/api/global/del_host",a,{headers:t}).then(t=>t.data),f=(t,a)=>n.a.post(o+"/api/global/disable_host",a,{headers:t}).then(t=>t.data),b=(t,a)=>n.a.post(o+"/api/global/enable_host",a,{headers:t}).then(t=>t.data),g=(t,a)=>n.a.post(o+"/api/global/update_host",a,{headers:t}).then(t=>t.data),_=(t,a)=>n.a.post(o+"/api/global/add_host",a,{headers:t}).then(t=>t.data),j=(t,a)=>n.a.get(o+"/api/dynamic/dynamic",{params:a,headers:t}).then(t=>t.data),k=(t,a)=>n.a.get(o+"/api/member/project_member",{params:a,headers:t}).then(t=>t.data),w=(t,a)=>n.a.get(o+"/api/member/get_email",{params:a,headers:t}).then(t=>t.data),v=(t,a)=>n.a.post(o+"/api/member/del_email",a,{headers:t}).then(t=>t.data),y=(t,a)=>n.a.post(o+"/api/member/email_config",a,{headers:t}).then(t=>t.data),F=(t,a)=>n.a.get(o+"/api/report/auto_test_report",{params:a,headers:t}).then(t=>t.data),C=(t,a)=>n.a.get(o+"/api/report/test_time",{params:a,headers:t}).then(t=>t.data),O=(t,a)=>n.a.get(o+"/api/report/lately_ten",{params:a,headers:t}).then(t=>t.data),S=(t,a)=>n.a.post(o+"/api/api/add_api",a,{headers:t}).then(t=>t.data),$=(t,a)=>n.a.get(o+"/api/api/group",{params:a,headers:t}).then(t=>t.data),x=(t,a)=>n.a.post(o+"/api/api/add_group",a,{headers:t}).then(t=>t.data),J=(t,a)=>n.a.post(o+"/api/api/update_name_group",a,{headers:t}).then(t=>t.data),I=(t,a)=>n.a.post(o+"/api/api/del_group",a,{headers:t}).then(t=>t.data),D=(t,a)=>n.a.post(o+"/api/download",a,{headers:t}).then(t=>t.data),N=(t,a)=>n.a.post(o+"/api/user/login",a,t).then(t=>t.data),q=(t,a)=>n.a.post(o+"/api/risk/update",a,{headers:t}).then(t=>t.data),E=(t,a)=>n.a.post(o+"/api/risk/add",a,{headers:t}).then(t=>t.data),T=(t,a)=>n.a.post(o+"/api/risk/add",a,{headers:t}).then(t=>t.data),B=(t,a)=>n.a.post(o+"/api/risk/del",a,t).then(t=>t.data),P=(t,a)=>n.a.get(o+"/api/risk ",{params:a},t).then(t=>t.data),z=(t,a)=>n.a.post(o+"/api/jira/figure ",a,t).then(t=>t.data),A=(t,a)=>n.a.get(o+"/api/todo ",{params:a},t).then(t=>t.data),G=(t,a)=>n.a.get(o+"/api/report ",{params:a},t).then(t=>t.data),H=(t,a)=>n.a.post(o+"/api/addreport",a,t).then(t=>t.data),K=(t,a)=>n.a.post(o+"/api/updatereport",a,t).then(t=>t.data),L=(t,a)=>n.a.post(o+"/api/delreport",a,t).then(t=>t.data),M=(t,a)=>n.a.post(o+"/api/send",a,t).then(t=>t.data),Q=(t,a)=>n.a.post(o+"/api/tool/stresstool",a,t).then(t=>t.data),R=(t,a)=>n.a.get(o+"/api/tool/version",{params:a},{headers:t}).then(t=>t.data),U=(t,a)=>n.a.post(o+"/api/tool/del_stressdata",a,t).then(t=>t.data),V=(t,a)=>n.a.post(o+"/api/tool/update_stressdata",a,t).then(t=>t.data),W=(t,a)=>n.a.post(o+"/api/tool/add_stressdata",a,t).then(t=>t.data),X=(t,a)=>n.a.get(o+"/api/tool/stressversion",{params:a},{headers:t}).then(t=>t.data),Y=(t,a)=>n.a.get(o+"/api/tool/stressdata",{params:a},{headers:t}).then(t=>t.data),Z=(t,a)=>n.a.post(o+"/api/tool/stressresult",a,t).then(t=>t.data),tt=(t,a)=>n.a.post(o+"/api/tool/stressfigure",a,t).then(t=>t.data),at=(t,a)=>n.a.post(o+"/api/tool/delete_patients",a,t).then(t=>t.data),et=(t,a)=>n.a.get(o+"/api/tool/getduration",{params:a},{headers:t}).then(t=>t.data),rt=(t,a)=>n.a.get(o+"/api/tool/durationData",{params:a},{headers:t}).then(t=>t.data),nt=(t,a)=>n.a.post(o+"/api/tool/add_duration",a,t).then(t=>t.data),ot=(t,a)=>n.a.post(o+"/api/tool/update_duration",a,t).then(t=>t.data),st=(t,a)=>n.a.post(o+"/api/tool/del_duration",a,t).then(t=>t.data),dt=(t,a)=>n.a.post(o+"/api/tool/enable_duration",a,t).then(t=>t.data),it=(t,a)=>n.a.post(o+"/api/tool/disable_duration",a,t).then(t=>t.data),ut=(t,a)=>n.a.get(o+"/api/tool/duration_verify",{params:a},{headers:t}).then(t=>t.data),pt=(t,a)=>n.a.get(o+"/api/base/getdata",{params:a},{headers:t}).then(t=>t.data),lt=(t,a)=>n.a.post(o+"/api/base/addData",a,t).then(t=>t.data),ct=(t,a)=>n.a.post(o+"/api/base/updateData",a,t).then(t=>t.data),ht=(t,a)=>n.a.post(o+"/api/base/enablebase",a,t).then(t=>t.data),mt=(t,a)=>n.a.post(o+"/api/base/disablebase",a,t).then(t=>t.data),ft=(t,a)=>n.a.post(o+"/api/base/delbasedata",a,t).then(t=>t.data)},ac19:function(t,a,e){},ea20:function(t,a,e){"use strict";var r=e("ac19"),n=e.n(r);n.a}}]);