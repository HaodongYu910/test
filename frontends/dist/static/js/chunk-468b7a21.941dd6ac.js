(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-468b7a21"],{"20fc":function(t,e){t.exports="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHkAAAABCAYAAAD6iwHlAAAAAXNSR0IArs4c6QAAAN5JREFUGBm1kN1NxEAMhMfjDYLjHdqhNEqhE6qgCh4BAcdlzeeNKIFIiT07P14nHh6fx6vu/KKT729v8ufjLaeG96uvPJ23fFf6epyzPtNzy6y8ZH3b23CW6WXXpNfFZafAw5E1Jy9VuxXN92emIvKy787cbHRqHec7vAOeeY6ihiuU2os5YaEpvB02e0iRjc7CS68eoBqHD4wm4P+0U6TgRwdX2Mmi74z2cA+iySwyu+Jv3NrDQx6X43ztEqpsDL/8PSe09OBjRuOVszB51GCn4qctTe+37gP6ryfi6Rcrv2ESgTsI2AAAAABJRU5ErkJggg=="},"2d92":function(t,e,a){"use strict";a.d(e,"fb",(function(){return r})),a.d(e,"J",(function(){return i})),a.d(e,"s",(function(){return o})),a.d(e,"z",(function(){return d})),a.d(e,"D",(function(){return p})),a.d(e,"ib",(function(){return l})),a.d(e,"j",(function(){return c})),a.d(e,"K",(function(){return u})),a.d(e,"I",(function(){return h})),a.d(e,"r",(function(){return m})),a.d(e,"y",(function(){return g})),a.d(e,"C",(function(){return b})),a.d(e,"hb",(function(){return f})),a.d(e,"i",(function(){return _})),a.d(e,"L",(function(){return v})),a.d(e,"M",(function(){return w})),a.d(e,"H",(function(){return x})),a.d(e,"q",(function(){return y})),a.d(e,"h",(function(){return j})),a.d(e,"N",(function(){return A})),a.d(e,"P",(function(){return C})),a.d(e,"O",(function(){return D})),a.d(e,"f",(function(){return S})),a.d(e,"G",(function(){return F})),a.d(e,"g",(function(){return k})),a.d(e,"gb",(function(){return H})),a.d(e,"p",(function(){return B})),a.d(e,"B",(function(){return P})),a.d(e,"db",(function(){return $})),a.d(e,"jb",(function(){return E})),a.d(e,"k",(function(){return L})),a.d(e,"E",(function(){return T})),a.d(e,"u",(function(){return M})),a.d(e,"ab",(function(){return N})),a.d(e,"Z",(function(){return O})),a.d(e,"cb",(function(){return q})),a.d(e,"bb",(function(){return z})),a.d(e,"n",(function(){return R})),a.d(e,"lb",(function(){return X})),a.d(e,"w",(function(){return I})),a.d(e,"d",(function(){return J})),a.d(e,"eb",(function(){return V})),a.d(e,"Q",(function(){return Y})),a.d(e,"x",(function(){return U})),a.d(e,"mb",(function(){return K})),a.d(e,"o",(function(){return G})),a.d(e,"Y",(function(){return Q})),a.d(e,"W",(function(){return W})),a.d(e,"X",(function(){return Z})),a.d(e,"V",(function(){return tt})),a.d(e,"v",(function(){return et})),a.d(e,"S",(function(){return at})),a.d(e,"T",(function(){return nt})),a.d(e,"m",(function(){return st})),a.d(e,"kb",(function(){return rt})),a.d(e,"t",(function(){return it})),a.d(e,"F",(function(){return ot})),a.d(e,"A",(function(){return dt})),a.d(e,"U",(function(){return pt})),a.d(e,"R",(function(){return lt})),a.d(e,"l",(function(){return ct})),a.d(e,"e",(function(){return ut})),a.d(e,"c",(function(){return ht})),a.d(e,"b",(function(){return mt})),a.d(e,"a",(function(){return gt}));var n=a("bc3a"),s=a.n(n);const r="http://192.168.2.38:9000",i=(t,e)=>s.a.get(r+"/api/project/project_list",{params:e,headers:t}).then(t=>t.data),o=(t,e)=>s.a.post(r+"/api/project/del_project",e,{headers:t}).then(t=>t.data),d=(t,e)=>s.a.post(r+"/api/project/disable_project",e,{headers:t}).then(t=>t.data),p=(t,e)=>s.a.post(r+"/api/project/enable_project",e,{headers:t}).then(t=>t.data),l=(t,e)=>s.a.post(r+"/api/project/update_project",e,{headers:t}).then(t=>t.data),c=(t,e)=>s.a.post(r+"/api/project/add_project",e,{headers:t}).then(t=>t.data),u=(t,e)=>s.a.get(r+"/api/title/project_info",{params:e,headers:t}).then(t=>t.data),h=(t,e)=>s.a.get(r+"/api/global/host_total",{params:e,headers:t}).then(t=>t.data),m=(t,e)=>s.a.post(r+"/api/global/del_host",e,{headers:t}).then(t=>t.data),g=(t,e)=>s.a.post(r+"/api/global/disable_host",e,{headers:t}).then(t=>t.data),b=(t,e)=>s.a.post(r+"/api/global/enable_host",e,{headers:t}).then(t=>t.data),f=(t,e)=>s.a.post(r+"/api/global/update_host",e,{headers:t}).then(t=>t.data),_=(t,e)=>s.a.post(r+"/api/global/add_host",e,{headers:t}).then(t=>t.data),v=(t,e)=>s.a.get(r+"/api/dynamic/dynamic",{params:e,headers:t}).then(t=>t.data),w=(t,e)=>s.a.get(r+"/api/member/project_member",{params:e,headers:t}).then(t=>t.data),x=(t,e)=>s.a.get(r+"/api/member/get_email",{params:e,headers:t}).then(t=>t.data),y=(t,e)=>s.a.post(r+"/api/member/del_email",e,{headers:t}).then(t=>t.data),j=(t,e)=>s.a.post(r+"/api/member/email_config",e,{headers:t}).then(t=>t.data),A=(t,e)=>s.a.get(r+"/api/report/auto_test_report",{params:e,headers:t}).then(t=>t.data),C=(t,e)=>s.a.get(r+"/api/report/test_time",{params:e,headers:t}).then(t=>t.data),D=(t,e)=>s.a.get(r+"/api/report/lately_ten",{params:e,headers:t}).then(t=>t.data),S=(t,e)=>s.a.post(r+"/api/api/add_api",e,{headers:t}).then(t=>t.data),F=(t,e)=>s.a.get(r+"/api/api/group",{params:e,headers:t}).then(t=>t.data),k=(t,e)=>s.a.post(r+"/api/api/add_group",e,{headers:t}).then(t=>t.data),H=(t,e)=>s.a.post(r+"/api/api/update_name_group",e,{headers:t}).then(t=>t.data),B=(t,e)=>s.a.post(r+"/api/api/del_group",e,{headers:t}).then(t=>t.data),P=(t,e)=>s.a.post(r+"/api/download",e,{headers:t}).then(t=>t.data),$=(t,e)=>s.a.post(r+"/api/user/login",e,t).then(t=>t.data),E=(t,e)=>s.a.post(r+"/api/risk/update",e,{headers:t}).then(t=>t.data),L=(t,e)=>s.a.post(r+"/api/risk/add",e,{headers:t}).then(t=>t.data),T=(t,e)=>s.a.post(r+"/api/risk/add",e,{headers:t}).then(t=>t.data),M=(t,e)=>s.a.post(r+"/api/risk/del",e,t).then(t=>t.data),N=(t,e)=>s.a.get(r+"/api/risk ",{params:e},t).then(t=>t.data),O=(t,e)=>s.a.post(r+"/api/jira/figure ",e,t).then(t=>t.data),q=(t,e)=>s.a.get(r+"/api/todo ",{params:e},t).then(t=>t.data),z=(t,e)=>s.a.get(r+"/api/report ",{params:e},t).then(t=>t.data),R=(t,e)=>s.a.post(r+"/api/addreport",e,t).then(t=>t.data),X=(t,e)=>s.a.post(r+"/api/updatereport",e,t).then(t=>t.data),I=(t,e)=>s.a.post(r+"/api/delreport",e,t).then(t=>t.data),J=(t,e)=>s.a.post(r+"/api/send",e,t).then(t=>t.data),V=(t,e)=>s.a.post(r+"/api/tool/stresstool",e,t).then(t=>t.data),Y=(t,e)=>s.a.get(r+"/api/tool/version",{params:e},{headers:t}).then(t=>t.data),U=(t,e)=>s.a.post(r+"/api/tool/del_stressdata",e,t).then(t=>t.data),K=(t,e)=>s.a.post(r+"/api/tool/update_stressdata",e,t).then(t=>t.data),G=(t,e)=>s.a.post(r+"/api/tool/add_stressdata",e,t).then(t=>t.data),Q=(t,e)=>s.a.get(r+"/api/tool/stressversion",{params:e},{headers:t}).then(t=>t.data),W=(t,e)=>s.a.get(r+"/api/tool/stressdata",{params:e},{headers:t}).then(t=>t.data),Z=(t,e)=>s.a.post(r+"/api/tool/stressresult",e,t).then(t=>t.data),tt=(t,e)=>s.a.post(r+"/api/tool/stressfigure",e,t).then(t=>t.data),et=(t,e)=>s.a.post(r+"/api/tool/delete_patients",e,t).then(t=>t.data),at=(t,e)=>s.a.get(r+"/api/tool/getduration",{params:e},{headers:t}).then(t=>t.data),nt=(t,e)=>s.a.get(r+"/api/tool/durationData",{params:e},{headers:t}).then(t=>t.data),st=(t,e)=>s.a.post(r+"/api/tool/add_duration",e,t).then(t=>t.data),rt=(t,e)=>s.a.post(r+"/api/tool/update_duration",e,t).then(t=>t.data),it=(t,e)=>s.a.post(r+"/api/tool/del_duration",e,t).then(t=>t.data),ot=(t,e)=>s.a.post(r+"/api/tool/enable_duration",e,t).then(t=>t.data),dt=(t,e)=>s.a.post(r+"/api/tool/disable_duration",e,t).then(t=>t.data),pt=(t,e)=>s.a.get(r+"/api/tool/duration_verify",{params:e},{headers:t}).then(t=>t.data),lt=(t,e)=>s.a.get(r+"/api/base/getdata",{params:e},{headers:t}).then(t=>t.data),ct=(t,e)=>s.a.post(r+"/api/base/addData",e,t).then(t=>t.data),ut=(t,e)=>s.a.post(r+"/api/base/updateData",e,t).then(t=>t.data),ht=(t,e)=>s.a.post(r+"/api/base/enablebase",e,t).then(t=>t.data),mt=(t,e)=>s.a.post(r+"/api/base/disablebase",e,t).then(t=>t.data),gt=(t,e)=>s.a.post(r+"/api/base/delbasedata",e,t).then(t=>t.data)},ab57:function(t,e,a){"use strict";a.r(e);var n=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"wid-2000 ",attrs:{for:"pc"}},[n("el-container",{staticStyle:{height:"2000px",border:"1px solid #eee"}},[n("el-container",[n("el-header",{staticStyle:{"text-align":"center",color:"#FFFFFF","font-size":"24px"}},[n("el-dropdown",[n("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},[n("el-dropdown-item",[t._v("查看")]),n("el-dropdown-item",[t._v("新增")]),n("el-dropdown-item",[t._v("删除")])],1)],1),n("span",[t._v("Boimind【】& CoinNess【】质量分析报告")])],1),n("el-main",[n("div",[n("p",{staticClass:"bug-exp-step p-t-20 p-b-10"},[n("img",{attrs:{src:a("20fc")}}),n("span",{staticClass:"bug-ex-item"},[t._v("项目描述")]),n("img",{staticClass:"img-revers",attrs:{src:a("20fc")}})])]),n("el-input",{attrs:{type:"textarea",rows:5,placeholder:"请输入内容"},model:{value:t.textarea,callback:function(e){t.textarea=e},expression:"textarea"}}),n("p",{staticClass:"bug-exp-step p-t-20 p-b-10"},[n("img",{attrs:{src:a("20fc")}}),n("span",{staticClass:"bug-ex-item"},[t._v("2 需求上线情况")]),n("img",{attrs:{src:a("20fc")}})]),n("el-table",{staticStyle:{width:"100%"},attrs:{data:t.tableData,border:""}},[n("el-table-column",{attrs:{prop:"business",label:"问题ID",width:"180"}}),n("el-table-column",{attrs:{prop:"product",label:"问题内容"}}),n("el-table-column",{attrs:{prop:"pm",label:"经办人",width:"180"}}),n("el-table-column",{attrs:{prop:"测试人员",label:"缺陷等级"}}),n("el-table-column",{attrs:{prop:"online",label:"解决状态",width:"180"}})],1),n("p",{staticClass:"bug-exp-step p-t-20 p-b-10"},[n("img",{attrs:{src:a("20fc")}}),n("span",{staticClass:"bug-ex-item"},[t._v("3 Case执行情况")]),n("img",{staticClass:"img-revers",attrs:{src:a("20fc")}})]),n("el-table",{staticStyle:{width:"100%"},attrs:{data:t.tableData,border:""}},[n("el-table-column",{attrs:{prop:"project",label:"项目列",width:"180"}}),n("el-table-column",{attrs:{prop:"param",label:"相关参数"}}),n("el-table-column",{attrs:{prop:"device",label:"覆盖设备",width:"180"}}),n("el-table-column",{attrs:{prop:"check",label:"验收负责人"}})],1),n("p",{staticClass:"bug-exp-step p-t-20 p-b-10"},[n("img",{attrs:{src:a("20fc")}}),n("span",{staticClass:"bug-ex-item"},[t._v("4 Bug明细")]),n("img",{staticClass:"img-revers",attrs:{src:a("20fc")}})]),n("el-table",{staticStyle:{width:"100%"},attrs:{data:t.tableData,border:""}},[n("el-table-column",{attrs:{prop:"priority",label:"方向/优先级",width:"180"}}),n("el-table-column",{attrs:{prop:"Highest",label:"Highest"}}),n("el-table-column",{attrs:{prop:"High",label:"High",width:"180"}}),n("el-table-column",{attrs:{prop:"Medium",label:"Medium"}}),n("el-table-column",{attrs:{prop:"Low",label:"Low",width:"180"}}),n("el-table-column",{attrs:{prop:"Lowest",label:"Lowest"}})],1),n("p",{staticClass:"bug-exp-step p-t-20 p-b-10"},[n("img",{attrs:{src:a("20fc")}}),n("span",{staticClass:"bug-ex-item"},[t._v("5 性能/压力测试")]),n("img",{staticClass:"img-revers",attrs:{src:a("20fc")}})])],1)],1)],1)],1)},s=[],r=a("2d92"),i={name:"basetable",data(){return{textarea:"1.Boimind x.x.x & CoinNess x.x.x 版本已于x月x日测试完成\n2.Android已提交给渠道同学、iOS已提交App Store等待审核；\n3.当前版本共消化 糖果红包权益、快讯+图片、热门频道、行情侧需求、广告也无需求、平台基础需求等；\n4.本版本共 328个 bug，己解决 307个 ，部分Server Bug 与 P3Bug待到下版本修复。",tableData:[{business:"1.糖果红包积分权益",product:"1.糖果红包积分权益\n2.积分权益后台\n3.数据需求",pm:"王晓东",qa:"李兰兰",online:"已上线",status:" ",project:"用例执行情况",product:"用例执行情况",param:"Boimind：\n总共执行用例数：1453\n通过数：1281\n未通过：172\n\nCoinNess:\n总共执行用例数：433\n通过数：372\n未通过：61",device:"Android：三星S7、vivo X9i、红米note 4x、\n小米 MI 5、华为 P10、华为 P10 Plus、华为Mate 9、\nvivo X20、一加 5T、华为mate10、小米 MI 5等\n\niOS：iPhone SE、5s、6s plus、6s、7 plus、8 plus、iPhoneX，\niPhone XS max",check:"尹航\n李虎\n刘畅\n柯尊森\n李兰兰\n蒋银山\n",priority:"Boimind",Highest:"12",High:"32",Medium:"23",Low:"4",Lowest:"1"},{business:"1.糖果红包积分权益",product:"1.糖果红包积分权益\n2.积分权益后台\n3.数据需求",pm:"王晓东",qa:"李兰兰",online:"已上线",status:" ",project:"",product:"",parameter:"",device:"",check:"",priority:"Boimind",Highest:"12",High:"32",Medium:"23",Low:"4",Lowest:"1"},{business:"1.糖果红包积分权益",product:"1.糖果红包积分权益\n2.积分权益后台\n3.数据需求",pm:"王晓东",qa:"李兰兰",online:"已上线",status:" ",project:"",product:"",param:"",device:"",check:"",priority:"Boimind",Highest:"12",High:"32",Medium:"23",Low:"4",Lowest:"1"},{business:"1.糖果红包积分权益",product:"1.糖果红包积分权益\n2.积分权益后台\n3.数据需求",pm:"王晓东",qa:"李兰兰",online:"已上线",status:" ",project:"",product:"",param:"",device:"",check:"",priority:"Boimind",Highest:"12",High:"32",Medium:"23",Low:"4",Lowest:"1"}],form:{title:"",test_version:"",cns_version:""}}},created(){this.getData()},computed:{data(){return this.tableData.filter(t=>{let e=!1;for(let a=0;a<this.del_list.length;a++)if(t.name===this.del_list[a].name){e=!0;break}if(!e&&t.address.indexOf(this.select_cate)>-1&&(t.name.indexOf(this.select_word)>-1||t.address.indexOf(this.select_word)>-1))return t})}},methods:{showRisk(t,e){this.$router.push({path:"/risk",query:{project_id:e.project_id,project:e.project}})},handleSizeChange(t){this.pageSize=t,console.log(`每页 ${t} 条`),this.getData()},handleCurrentChange(t){this.currentPage=t,console.log(`这是第${t}页`),this.getData()},getData(t,e){let a={page:this.currentPage,page_size:this.pageSize,name:t,version:e},n={"Content-Type":"application/x-www-form-urlencoded"};Object(r["bb"])(n,a).then(t=>{let{msg:e,data:a,code:n}=t;this.currentTotal=a.total,this.tableData=a.data})},search(){this.is_search=!0},dateFormatter(t,e){console.log("格式化日期");var a=t[e.property];return void 0==a?"":moment(data).format("YYYY-MM-DD")},filterTag(t,e){return e.tag===t},handleAdd(){this.dialogFormVisible=!0,this.addForm={id:null,test_version:null,cns_version:null,receiver:null,is_send:null,send_time:null,email_cc:null,title:null,template:null}},addreportconfig(t){console.log(t),this.$refs[t].validate(t=>{if(!t)return console.log("error submit!!"),!1;{let t={test_version:this.addForm.test_version,cns_version:this.addForm.cns_version,receiver:this.addForm.receiver,type:this.addForm.type,send_time:this.addForm.send_time,email_cc:this.addForm.email_cc,title:this.addForm.title,template:this.addForm.template};console.log(t);let e={"Content-Type":"application/json"};addTestProject(e,t).then(t=>{let{msg:e,code:a,data:n}=t;console.log("code:"+a),"0"==a?(this.$message.success("添加成功"),this.dialogFormVisible=!1,this.getData()):this.$message.error(e)})}})},handleEdit(t,e){this.idx=t;const a=this.tableData[t];this.editform={id:a.id,test_version:a.test_version,cns_version:a.cns_version,title:a.title,receiver:a.receiver,type:a.type,send_time:a.send_time,email_cc:a.email_cc,template:""},this.editVisible=!0},handleEdit(t,e){this.idx=t;const a=this.tableData[t];this.editform={id:a.id,test_version:a.test_version,cns_version:a.cns_version,title:a.title,receiver:a.receiver,type:a.type,send_time:a.send_time,email_cc:a.email_cc,template:""},this.editVisible=!0},handleDelete(t,e){this.idx=t;const a=this.tableData[t];let n=[a.id],s={ids:n},r={"Content-Type":"application/json"};deleteTestProject(r,s).then(t=>{let{msg:e,code:a,data:n}=t;"0"==a?null==n||n[0]?(this.$message.success("删除成功！"),this.getData()):this.$message.error(n[1]):this.$message.error(e)})},handleSend(t,e){this.idx=t;const a=this.tableData[t];let n=a.id,s={id:n,type:1,start_time:"",endtime:""},i={"Content-Type":"application/json"};Object(r["d"])(i,s).then(t=>{let{msg:e,code:a,data:n}=t;"0"==a?null==n||n[0]?(this.$message.success("发送成功！"),this.getData()):this.$message.error(n[1]):this.$message.error(e)})},handleSelectionChange(t){this.multipleSelection=t},searchProject(t){let e=this.searchform.select_app,a=this.searchform.select_version,n=/^\d+\.\d+\.\d+$/;if("undefined"==typeof e&&"undefined"==typeof a)return void alert("请输入要搜索的版本号或者版本号");let s=typeof a;"undefined"==s||null==s||""==s||n.test(a)?this.getData(e,a):alert("请输入格式为x.x.x的版本号")},saveEdit(t){let e={id:t.id,test_version:t.test_version,cns_version:t.cns_version,receiver:t.receiver,type:t.type,send_time:t.send_time,email_cc:t.email_cc,title:t.title,template:""},a={"Content-Type":"application/json"};Object(r["lb"])(a,e).then(t=>{let{msg:e,code:a,data:n}=t;"0"==a?null==n||n[0]?(this.$message.success("编辑成功"),this.editVisible=!1,this.getData()):this.$message.error(n[1]):this.$message.error(e)})}}},o=i,d=(a("c718"),a("2877")),p=Object(d["a"])(o,n,s,!1,null,null,null);e["default"]=p.exports},c718:function(t,e,a){"use strict";var n=a("cfd1"),s=a.n(n);s.a},cfd1:function(t,e,a){}}]);