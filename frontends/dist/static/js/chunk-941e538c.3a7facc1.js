(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-941e538c"],{"2d92":function(t,e,a){"use strict";a.d(e,"eb",(function(){return s})),a.d(e,"J",(function(){return o})),a.d(e,"s",(function(){return i})),a.d(e,"z",(function(){return l})),a.d(e,"D",(function(){return d})),a.d(e,"hb",(function(){return p})),a.d(e,"j",(function(){return u})),a.d(e,"K",(function(){return c})),a.d(e,"I",(function(){return m})),a.d(e,"r",(function(){return f})),a.d(e,"y",(function(){return h})),a.d(e,"C",(function(){return g})),a.d(e,"gb",(function(){return b})),a.d(e,"i",(function(){return v})),a.d(e,"L",(function(){return _})),a.d(e,"M",(function(){return y})),a.d(e,"H",(function(){return k})),a.d(e,"q",(function(){return w})),a.d(e,"h",(function(){return S})),a.d(e,"N",(function(){return x})),a.d(e,"P",(function(){return j})),a.d(e,"O",(function(){return O})),a.d(e,"f",(function(){return $})),a.d(e,"G",(function(){return L})),a.d(e,"g",(function(){return z})),a.d(e,"fb",(function(){return C})),a.d(e,"p",(function(){return N})),a.d(e,"B",(function(){return J})),a.d(e,"cb",(function(){return D})),a.d(e,"ib",(function(){return T})),a.d(e,"k",(function(){return A})),a.d(e,"E",(function(){return q})),a.d(e,"u",(function(){return I})),a.d(e,"Z",(function(){return W})),a.d(e,"Y",(function(){return B})),a.d(e,"bb",(function(){return F})),a.d(e,"ab",(function(){return R})),a.d(e,"n",(function(){return H})),a.d(e,"kb",(function(){return V})),a.d(e,"w",(function(){return E})),a.d(e,"d",(function(){return M})),a.d(e,"db",(function(){return P})),a.d(e,"Q",(function(){return X})),a.d(e,"x",(function(){return Z})),a.d(e,"lb",(function(){return G})),a.d(e,"o",(function(){return K})),a.d(e,"X",(function(){return Q})),a.d(e,"V",(function(){return U})),a.d(e,"W",(function(){return Y})),a.d(e,"v",(function(){return tt})),a.d(e,"S",(function(){return et})),a.d(e,"T",(function(){return at})),a.d(e,"m",(function(){return rt})),a.d(e,"jb",(function(){return nt})),a.d(e,"t",(function(){return st})),a.d(e,"F",(function(){return ot})),a.d(e,"A",(function(){return it})),a.d(e,"U",(function(){return lt})),a.d(e,"R",(function(){return dt})),a.d(e,"l",(function(){return pt})),a.d(e,"e",(function(){return ut})),a.d(e,"c",(function(){return ct})),a.d(e,"b",(function(){return mt})),a.d(e,"a",(function(){return ft}));var r=a("bc3a"),n=a.n(r);const s="http://192.168.2.38:9000",o=(t,e)=>n.a.get(s+"/api/project/project_list",{params:e,headers:t}).then(t=>t.data),i=(t,e)=>n.a.post(s+"/api/project/del_project",e,{headers:t}).then(t=>t.data),l=(t,e)=>n.a.post(s+"/api/project/disable_project",e,{headers:t}).then(t=>t.data),d=(t,e)=>n.a.post(s+"/api/project/enable_project",e,{headers:t}).then(t=>t.data),p=(t,e)=>n.a.post(s+"/api/project/update_project",e,{headers:t}).then(t=>t.data),u=(t,e)=>n.a.post(s+"/api/project/add_project",e,{headers:t}).then(t=>t.data),c=(t,e)=>n.a.get(s+"/api/title/project_info",{params:e,headers:t}).then(t=>t.data),m=(t,e)=>n.a.get(s+"/api/global/host_total",{params:e,headers:t}).then(t=>t.data),f=(t,e)=>n.a.post(s+"/api/global/del_host",e,{headers:t}).then(t=>t.data),h=(t,e)=>n.a.post(s+"/api/global/disable_host",e,{headers:t}).then(t=>t.data),g=(t,e)=>n.a.post(s+"/api/global/enable_host",e,{headers:t}).then(t=>t.data),b=(t,e)=>n.a.post(s+"/api/global/update_host",e,{headers:t}).then(t=>t.data),v=(t,e)=>n.a.post(s+"/api/global/add_host",e,{headers:t}).then(t=>t.data),_=(t,e)=>n.a.get(s+"/api/dynamic/dynamic",{params:e,headers:t}).then(t=>t.data),y=(t,e)=>n.a.get(s+"/api/member/project_member",{params:e,headers:t}).then(t=>t.data),k=(t,e)=>n.a.get(s+"/api/member/get_email",{params:e,headers:t}).then(t=>t.data),w=(t,e)=>n.a.post(s+"/api/member/del_email",e,{headers:t}).then(t=>t.data),S=(t,e)=>n.a.post(s+"/api/member/email_config",e,{headers:t}).then(t=>t.data),x=(t,e)=>n.a.get(s+"/api/report/auto_test_report",{params:e,headers:t}).then(t=>t.data),j=(t,e)=>n.a.get(s+"/api/report/test_time",{params:e,headers:t}).then(t=>t.data),O=(t,e)=>n.a.get(s+"/api/report/lately_ten",{params:e,headers:t}).then(t=>t.data),$=(t,e)=>n.a.post(s+"/api/api/add_api",e,{headers:t}).then(t=>t.data),L=(t,e)=>n.a.get(s+"/api/api/group",{params:e,headers:t}).then(t=>t.data),z=(t,e)=>n.a.post(s+"/api/api/add_group",e,{headers:t}).then(t=>t.data),C=(t,e)=>n.a.post(s+"/api/api/update_name_group",e,{headers:t}).then(t=>t.data),N=(t,e)=>n.a.post(s+"/api/api/del_group",e,{headers:t}).then(t=>t.data),J=(t,e)=>n.a.post(s+"/api/download",e,{headers:t}).then(t=>t.data),D=(t,e)=>n.a.post(s+"/api/user/login",e,t).then(t=>t.data),T=(t,e)=>n.a.post(s+"/api/risk/update",e,{headers:t}).then(t=>t.data),A=(t,e)=>n.a.post(s+"/api/risk/add",e,{headers:t}).then(t=>t.data),q=(t,e)=>n.a.post(s+"/api/risk/add",e,{headers:t}).then(t=>t.data),I=(t,e)=>n.a.post(s+"/api/risk/del",e,t).then(t=>t.data),W=(t,e)=>n.a.get(s+"/api/risk ",{params:e},t).then(t=>t.data),B=(t,e)=>n.a.post(s+"/api/jira/figure ",e,t).then(t=>t.data),F=(t,e)=>n.a.get(s+"/api/todo ",{params:e},t).then(t=>t.data),R=(t,e)=>n.a.get(s+"/api/report ",{params:e},t).then(t=>t.data),H=(t,e)=>n.a.post(s+"/api/addreport",e,t).then(t=>t.data),V=(t,e)=>n.a.post(s+"/api/updatereport",e,t).then(t=>t.data),E=(t,e)=>n.a.post(s+"/api/delreport",e,t).then(t=>t.data),M=(t,e)=>n.a.post(s+"/api/send",e,t).then(t=>t.data),P=(t,e)=>n.a.post(s+"/api/tool/stresstool",e,t).then(t=>t.data),X=(t,e)=>n.a.get(s+"/api/tool/version",{params:e},{headers:t}).then(t=>t.data),Z=(t,e)=>n.a.post(s+"/api/tool/del_stressdata",e,t).then(t=>t.data),G=(t,e)=>n.a.post(s+"/api/tool/update_stressdata",e,t).then(t=>t.data),K=(t,e)=>n.a.post(s+"/api/tool/add_stressdata",e,t).then(t=>t.data),Q=(t,e)=>n.a.get(s+"/api/tool/stressversion",{params:e},{headers:t}).then(t=>t.data),U=(t,e)=>n.a.get(s+"/api/tool/stressdata",{params:e},{headers:t}).then(t=>t.data),Y=(t,e)=>n.a.post(s+"/api/tool/stressresult",e,t).then(t=>t.data),tt=(t,e)=>n.a.post(s+"/api/tool/delete_patients",e,t).then(t=>t.data),et=(t,e)=>n.a.get(s+"/api/tool/getduration",{params:e},{headers:t}).then(t=>t.data),at=(t,e)=>n.a.get(s+"/api/tool/durationData",{params:e},{headers:t}).then(t=>t.data),rt=(t,e)=>n.a.post(s+"/api/tool/add_duration",e,t).then(t=>t.data),nt=(t,e)=>n.a.post(s+"/api/tool/update_duration",e,t).then(t=>t.data),st=(t,e)=>n.a.post(s+"/api/tool/del_duration",e,t).then(t=>t.data),ot=(t,e)=>n.a.post(s+"/api/tool/enable_duration",e,t).then(t=>t.data),it=(t,e)=>n.a.post(s+"/api/tool/disable_duration",e,t).then(t=>t.data),lt=(t,e)=>n.a.get(s+"/api/tool/duration_verify",{params:e},{headers:t}).then(t=>t.data),dt=(t,e)=>n.a.get(s+"/api/base/getdata",{params:e},{headers:t}).then(t=>t.data),pt=(t,e)=>n.a.post(s+"/api/base/addData",e,t).then(t=>t.data),ut=(t,e)=>n.a.post(s+"/api/base/updateData",e,t).then(t=>t.data),ct=(t,e)=>n.a.post(s+"/api/base/enablebase",e,t).then(t=>t.data),mt=(t,e)=>n.a.post(s+"/api/base/disablebase",e,t).then(t=>t.data),ft=(t,e)=>n.a.post(s+"/api/base/delbasedata",e,t).then(t=>t.data)},a05f:function(t,e,a){"use strict";a.r(e);var r=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"app-container"},[a("div",{staticClass:"filter-container"},[a("el-col",{staticClass:"toolbar",staticStyle:{"padding-bottom":"0px"},attrs:{span:100}},[a("aside",[a("a",{attrs:{href:"http://192.168.2.38:3000/d/Ss3q6hSZk/docker-and-os-metrics-test?orgId=1&refresh=5s&from=now-5m&to=now&var-host_name=192.168.2.60&var-gpu_exporter_port=9445&var-node_exporter_port=9100&var-cadvisor_port=8080",target:"_blank"}},[t._v("Stress Monitor ")])]),a("el-form",{ref:"form",attrs:{model:t.form,"status-icon":"",rules:t.rules,"label-width":"100px"}},[a("el-row",[a("el-col",{attrs:{span:3}},[a("el-form-item",{attrs:{label:"服务器",prop:"loadserver"}},[a("el-select",{attrs:{placeholder:"请选择"},nativeOn:{click:function(e){return t.gethost()}},model:{value:t.form.loadserver,callback:function(e){t.$set(t.form,"loadserver",e)},expression:"form.loadserver"}},t._l(t.tags,(function(t,e){return a("el-option",{key:t.host,attrs:{label:t.name,value:t.host}})})),1)],1)],1),a("el-col",{attrs:{span:3}},[a("el-form-item",{attrs:{label:"测试版本",prop:"version"}},[a("el-input",{attrs:{id:"version",placeholder:"测试版本"},model:{value:t.form.version,callback:function(e){t.$set(t.form,"version",e)},expression:"form.version"}})],1)],1),a("el-col",{attrs:{span:3}},[a("el-form-item",{attrs:{label:"压测时间",prop:"loop_time"}},[a("el-input",{attrs:{id:"loop_time",placeholder:"测试小时"},model:{value:t.form.loop_time,callback:function(e){t.$set(t.form,"loop_time",e)},expression:"form.loop_time"}})],1)],1),a("el-col",{attrs:{span:3}},[a("el-form-item",{attrs:{label:"线程数",prop:"loop_time"}},[a("el-input",{attrs:{id:"thread",placeholder:"个"},model:{value:t.form.thread,callback:function(e){t.$set(t.form,"thread",e)},expression:"form.thread"}})],1)],1),a("el-col",{attrs:{span:3}},[a("el-form-item",{attrs:{label:"循环次数",prop:"loop"}},[a("el-input",{attrs:{id:"loop",placeholder:"个"},model:{value:t.form.loop,callback:function(e){t.$set(t.form,"loop",e)},expression:"form.loop"}})],1)],1),a("el-col",{attrs:{span:3}},[a("el-form-item",{attrs:{label:"并发",prop:"synchronizing"}},[a("el-input",{attrs:{id:"synchronizing",placeholder:"个"},model:{value:t.form.synchronizing,callback:function(e){t.$set(t.form,"synchronizing",e)},expression:"form.synchronizing"}})],1)],1),a("el-col",{attrs:{span:3}},[a("el-form-item",{attrs:{label:"dicom发送",prop:"loadserver"}},[a("el-switch",{attrs:{"active-color":"#13ce66","inactive-color":"#ff4949"},model:{value:t.form.switch,callback:function(e){t.$set(t.form,"switch",e)},expression:"form.switch"}})],1)],1),a("el-col",{attrs:{span:4}},[a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:function(e){return t.stressrun("form")}}},[t._v("执行")])],1)],1)],1)],1),a("el-row",[a("el-checkbox-group",{attrs:{size:"small"},model:{value:t.form.testdata,callback:function(e){t.$set(t.form,"testdata",e)},expression:"form.testdata"}},t._l(t.dibase,(function(e,r){return a("el-checkbox-button",{key:e.remarks,attrs:{label:e.remarks}},[t._v(t._s(e.remarks))])})),1)],1),a("aside",[a("a",{attrs:{href:"http://192.168.2.38:9000/",target:"_blank"}},[t._v("测试结果 ")])]),a("el-col",{staticClass:"toolbar",staticStyle:{"padding-bottom":"0px"},attrs:{span:24}},[a("el-form",{attrs:{inline:!0,model:t.filters},nativeOn:{submit:function(t){t.preventDefault()}}},[a("el-select",{attrs:{placeholder:"请选择服务器"},nativeOn:{click:function(e){return t.gethost()}},model:{value:t.filters.server,callback:function(e){t.$set(t.filters,"server",e)},expression:"filters.server"}},t._l(t.tags,(function(t,e){return a("el-option",{key:t.host,attrs:{label:t.name,value:t.host}})})),1),a("el-select",{attrs:{placeholder:"当前版本"},nativeOn:{click:function(e){return t.getversion()}},model:{value:t.filters.version,callback:function(e){t.$set(t.filters,"version",e)},expression:"filters.version"}},t._l(t.versions,(function(t,e){return a("el-option",{key:t.version,attrs:{label:t.version,value:t.version}})})),1),a("el-select",{attrs:{placeholder:"以前版本"},nativeOn:{click:function(e){return t.getversion()}},model:{value:t.filters.checkversion,callback:function(e){t.$set(t.filters,"checkversion",e)},expression:"filters.checkversion"}},t._l(t.versions,(function(t,e){return a("el-option",{key:t.version,attrs:{label:t.version,value:t.version}})})),1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:t.getDurationlist}},[t._v("查询")])],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:t.handleAdd}},[t._v("生成报告")])],1)],1)],1),a("span",{staticStyle:{"margin-left":"10px"}},[t._v("prediction time")]),a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.listLoading,expression:"listLoading"}],staticStyle:{width:"100%"},attrs:{data:t.prediction},on:{"selection-change":t.selsChange}},[a("el-table-column",{attrs:{prop:"modelname",label:"modelname","min-width":"8%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.modelname))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"prediction_count","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.count))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"avg pred time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.avg))])]}}])}),a("el-table-column",{attrs:{label:"median pred time /s","min-width":"10%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.median))])]}}])}),a("el-table-column",{attrs:{label:"min pred time /s","min-width":"10%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.min))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"max pred time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.max))])]}}])}),a("el-table-column",{attrs:{prop:"status",label:"coef. of variation","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.coef))])]}}])}),a("el-table-column",{attrs:{label:"rate of success","min-width":"8%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.rate))])]}}])})],1),a("span",{staticStyle:{"margin-left":"10px"}},[t._v("job time")]),a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.listLoading,expression:"listLoading"}],staticStyle:{width:"100%"},attrs:{data:t.job,"highlight-current-row":""},on:{"selection-change":t.selsChange}},[a("el-table-column",{attrs:{prop:"version",label:"modelname","min-width":"8%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.modelname))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"job_count","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.count))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"avg job time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.avg))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"avg single job time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.single))])]}}])}),a("el-table-column",{attrs:{label:"median job time /s","min-width":"10%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.median)+" 秒")])]}}])}),a("el-table-column",{attrs:{label:"min job time /s","min-width":"10%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.min))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"max job time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.max))])]}}])}),a("el-table-column",{attrs:{prop:"status",label:"coef. of variation","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.coef))])]}}])})],1),a("span",{staticStyle:{"margin-left":"10px"}},[t._v("Lung prediction time")]),a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.listLoading,expression:"listLoading"}],staticStyle:{width:"100%"},attrs:{data:t.lung,"highlight-current-row":""},on:{"selection-change":t.selsChange}},[a("el-table-column",{attrs:{prop:"version",label:"slicenumber","min-width":"6%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.slicenumber))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"avg pred time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.avg))])]}}])}),a("el-table-column",{attrs:{label:"median pred time /s","min-width":"10%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.median))])]}}])}),a("el-table-column",{attrs:{label:"min pred time /s","min-width":"10%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.min))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"max pred time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.max))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"coef. of variation","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.coef))])]}}])}),a("el-table-column",{attrs:{label:"rate of success","min-width":"8%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.rate))])]}}])})],1)],1)],1)])},n=[],s=a("2d92"),o={data(){return{cities:["lung","swi","svd"],form:{version:"",loadserver:"192.168.1.208",loop_time:"",thread:4,synchronizing:0,testdata:["Lung","Brain","SWI","SVD","Tumor","Heart","CT_Hematoma","CTA","CTP"],switch:!1},rules:{server:[{required:!0,message:"请输入测试服务器",trigger:"blur"}],version:[{required:!0,message:"请输入测试版本",trigger:"blur"}]},filters:{diseases:""},durationlist:[],total:0,page:1,listLoading:!1,sels:[],editFormVisible:!1,editLoading:!1,options:[{label:"Web",value:"Web"},{label:"App",value:"App"}],editFormRules:{diseases:[{required:!0,message:"请输入名称",trigger:"blur"},{min:1,max:50,message:"长度在 1 到 50 个字符",trigger:"blur"}],type:[{required:!0,message:"请选择类型",trigger:"blur"}],version:[{required:!0,message:"请输入版本号",trigger:"change"},{pattern:/^\d+\.\d+\.\d+$/,message:"请输入合法的版本号（x.x.x）"}],description:[{required:!1,message:"请输入描述",trigger:"blur"},{max:1024,message:"不能超过1024个字符",trigger:"blur"}]},filters:{checkversion:"2.11.0",version:"2.10.0RC9",server:"192.168.1.208"},addForm:{diseases:"",version:"",type:"",description:""}}},mounted(){this.getDurationlist(),this.gethost(),this.getBase()},methods:{stressrun(t){this.tableData=null,this.$refs[t].validate(t=>{if(t){const t={version:this.form.version,loadserver:this.form.loadserver,loop_time:this.form.loop_time,thread:this.form.thread,testdata:this.form.testdata,switch:this.form.switch,loop:this.form.loop,synchronizing:this.form.synchronizing},e={"Content-Type":"application/json"};Object(s["db"])(e,t).then(t=>{console.log(this.form.testtype);const{msg:e,code:a,data:r}=t;"0"===a?self.$message({message:"修改成功",center:!0,type:"success"}):self.$message.error({message:e,center:!0})})}})},getversion(){this.listLoading=!0;const t=this,e={},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(s["X"])(a,e).then(e=>{t.listLoading=!1;const{msg:a,code:r,data:n}=e;if("0"===r){t.total=n.total,t.list=n.data;var s=JSON.stringify(t.list);this.versions=JSON.parse(s)}else t.$message.error({message:a,center:!0})})},getBase(){this.listLoading=!0;const t=this,e={selecttype:"dicom",status:1},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(s["R"])(a,e).then(e=>{t.listLoading=!1;const{msg:a,code:r,data:n}=e;if("0"===r){t.total=n.total,t.list=n.data;var s=JSON.stringify(t.list);this.dibase=JSON.parse(s)}else t.$message.error({message:a,center:!0})})},gethost(){this.listLoading=!0;const t=this,e={},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(s["I"])(a,e).then(e=>{t.listLoading=!1;const{msg:a,code:r,data:n}=e;if("0"===r){t.total=n.total,t.list=n.data;var s=JSON.stringify(t.list);this.tags=JSON.parse(s)}else t.$message.error({message:a,center:!0})})},getDurationlist(){this.listLoading=!0;const t=this,e={version:this.filters.version,checkversion:this.filters.checkversion,server:this.filters.server},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(s["W"])(a,e).then(e=>{t.listLoading=!1;const{msg:a,code:r,data:n}=e;"0"===r?(t.prediction=n.predictionresult,t.job=n.jobresult,t.lung=n.lungresult):t.$message.error({message:a,center:!0})})},selsChange:function(t){this.sels=t}}},i=o,l=(a("a9ae"),a("2877")),d=Object(l["a"])(i,r,n,!1,null,"17f21e4c",null);e["default"]=d.exports},a9ae:function(t,e,a){"use strict";var r=a("f023"),n=a.n(r);n.a},f023:function(t,e,a){}}]);