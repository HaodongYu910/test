(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-40c23cf7"],{"2d92":function(e,t,a){"use strict";a.d(t,"qb",(function(){return o})),a.d(t,"Q",(function(){return s})),a.d(t,"v",(function(){return i})),a.d(t,"G",(function(){return l})),a.d(t,"K",(function(){return d})),a.d(t,"tb",(function(){return p})),a.d(t,"k",(function(){return u})),a.d(t,"R",(function(){return c})),a.d(t,"P",(function(){return h})),a.d(t,"u",(function(){return m})),a.d(t,"F",(function(){return f})),a.d(t,"J",(function(){return g})),a.d(t,"sb",(function(){return b})),a.d(t,"j",(function(){return v})),a.d(t,"S",(function(){return _})),a.d(t,"T",(function(){return y})),a.d(t,"O",(function(){return w})),a.d(t,"t",(function(){return k})),a.d(t,"i",(function(){return T})),a.d(t,"U",(function(){return x})),a.d(t,"W",(function(){return j})),a.d(t,"V",(function(){return S})),a.d(t,"g",(function(){return D})),a.d(t,"N",(function(){return R})),a.d(t,"h",(function(){return I})),a.d(t,"rb",(function(){return O})),a.d(t,"s",(function(){return C})),a.d(t,"I",(function(){return $})),a.d(t,"mb",(function(){return A})),a.d(t,"ub",(function(){return L})),a.d(t,"l",(function(){return E})),a.d(t,"L",(function(){return F})),a.d(t,"z",(function(){return P})),a.d(t,"jb",(function(){return N})),a.d(t,"lb",(function(){return z})),a.d(t,"kb",(function(){return q})),a.d(t,"q",(function(){return J})),a.d(t,"xb",(function(){return H})),a.d(t,"B",(function(){return B})),a.d(t,"d",(function(){return V})),a.d(t,"ob",(function(){return U})),a.d(t,"m",(function(){return W})),a.d(t,"e",(function(){return X})),a.d(t,"nb",(function(){return G})),a.d(t,"X",(function(){return K})),a.d(t,"pb",(function(){return M})),a.d(t,"w",(function(){return Q})),a.d(t,"vb",(function(){return Y})),a.d(t,"o",(function(){return Z})),a.d(t,"E",(function(){return ee})),a.d(t,"ab",(function(){return te})),a.d(t,"D",(function(){return ae})),a.d(t,"x",(function(){return re})),a.d(t,"ib",(function(){return ne})),a.d(t,"hb",(function(){return oe})),a.d(t,"eb",(function(){return se})),a.d(t,"A",(function(){return ie})),a.d(t,"bb",(function(){return le})),a.d(t,"cb",(function(){return de})),a.d(t,"p",(function(){return pe})),a.d(t,"wb",(function(){return ue})),a.d(t,"y",(function(){return ce})),a.d(t,"r",(function(){return he})),a.d(t,"M",(function(){return me})),a.d(t,"H",(function(){return fe})),a.d(t,"db",(function(){return ge})),a.d(t,"fb",(function(){return be})),a.d(t,"gb",(function(){return ve})),a.d(t,"Z",(function(){return _e})),a.d(t,"Y",(function(){return ye})),a.d(t,"n",(function(){return we})),a.d(t,"f",(function(){return ke})),a.d(t,"c",(function(){return Te})),a.d(t,"b",(function(){return xe})),a.d(t,"a",(function(){return je})),a.d(t,"C",(function(){return Se}));var r=a("bc3a"),n=a.n(r);a("c896");const o="http://192.168.1.121:9000",s=(e,t)=>n.a.get(o+"/api/project/project_list",{params:t,headers:e}).then(e=>e.data),i=(e,t)=>n.a.post(o+"/api/project/del_project",t,{headers:e}).then(e=>e.data),l=(e,t)=>n.a.post(o+"/api/project/disable_project",t,{headers:e}).then(e=>e.data),d=(e,t)=>n.a.post(o+"/api/project/enable_project",t,{headers:e}).then(e=>e.data),p=(e,t)=>n.a.post(o+"/api/project/update_project",t,{headers:e}).then(e=>e.data),u=(e,t)=>n.a.post(o+"/api/project/add_project",t,{headers:e}).then(e=>e.data),c=(e,t)=>n.a.get(o+"/api/title/project_info",{params:t,headers:e}).then(e=>e.data),h=(e,t)=>n.a.get(o+"/api/global/host_total",{params:t,headers:e}).then(e=>e.data),m=(e,t)=>n.a.post(o+"/api/global/del_host",t,{headers:e}).then(e=>e.data),f=(e,t)=>n.a.post(o+"/api/global/disable_host",t,{headers:e}).then(e=>e.data),g=(e,t)=>n.a.post(o+"/api/global/enable_host",t,{headers:e}).then(e=>e.data),b=(e,t)=>n.a.post(o+"/api/global/update_host",t,{headers:e}).then(e=>e.data),v=(e,t)=>n.a.post(o+"/api/global/add_host",t,{headers:e}).then(e=>e.data),_=(e,t)=>n.a.get(o+"/api/dynamic/dynamic",{params:t,headers:e}).then(e=>e.data),y=(e,t)=>n.a.get(o+"/api/member/project_member",{params:t,headers:e}).then(e=>e.data),w=(e,t)=>n.a.get(o+"/api/member/get_email",{params:t,headers:e}).then(e=>e.data),k=(e,t)=>n.a.post(o+"/api/member/del_email",t,{headers:e}).then(e=>e.data),T=(e,t)=>n.a.post(o+"/api/member/email_config",t,{headers:e}).then(e=>e.data),x=(e,t)=>n.a.get(o+"/api/report/auto_test_report",{params:t,headers:e}).then(e=>e.data),j=(e,t)=>n.a.get(o+"/api/report/test_time",{params:t,headers:e}).then(e=>e.data),S=(e,t)=>n.a.get(o+"/api/report/lately_ten",{params:t,headers:e}).then(e=>e.data),D=(e,t)=>n.a.post(o+"/api/api/add_api",t,{headers:e}).then(e=>e.data),R=(e,t)=>n.a.get(o+"/api/api/group",{params:t,headers:e}).then(e=>e.data),I=(e,t)=>n.a.post(o+"/api/api/add_group",t,{headers:e}).then(e=>e.data),O=(e,t)=>n.a.post(o+"/api/api/update_name_group",t,{headers:e}).then(e=>e.data),C=(e,t)=>n.a.post(o+"/api/api/del_group",t,{headers:e}).then(e=>e.data),$=(e,t)=>n.a.post(o+"/api/download",t,{headers:e}).then(e=>e.data),A=(e,t)=>n.a.post(o+"/api/user/login",t,e).then(e=>e.data),L=(e,t)=>n.a.post(o+"/api/risk/update",t,{headers:e}).then(e=>e.data),E=(e,t)=>n.a.post(o+"/api/risk/add",t,{headers:e}).then(e=>e.data),F=(e,t)=>n.a.post(o+"/api/risk/add",t,{headers:e}).then(e=>e.data),P=(e,t)=>n.a.post(o+"/api/risk/del",t,e).then(e=>e.data),N=(e,t)=>n.a.get(o+"/api/risk ",{params:t},e).then(e=>e.data),z=(e,t)=>n.a.get(o+"/api/todo ",{params:t},e).then(e=>e.data),q=(e,t)=>n.a.get(o+"/api/report ",{params:t},e).then(e=>e.data),J=(e,t)=>n.a.post(o+"/api/addreport",t,e).then(e=>e.data),H=(e,t)=>n.a.post(o+"/api/updatereport",t,e).then(e=>e.data),B=(e,t)=>n.a.post(o+"/api/delreport",t,e).then(e=>e.data),V=(e,t)=>n.a.post(o+"/api/send",t,e).then(e=>e.data),U=(e,t)=>n.a.get(o+"/api/stress/list",{params:t},{headers:e}).then(e=>e.data),W=(e,t)=>n.a.post(o+"/api/stress/add",t,e).then(e=>e.data),X=(e,t)=>n.a.get(o+"/api/stress/stressDetail ",{params:t},e).then(e=>e.data),G=(e,t)=>n.a.post(o+"/api/stress/stresstool",t,e).then(e=>e.data),K=(e,t)=>n.a.get(o+"/api/stress/version",{params:t},{headers:e}).then(e=>e.data),M=(e,t)=>n.a.post(o+"/api/stress/stresssave",t,e).then(e=>e.data),Q=(e,t)=>n.a.post(o+"/api/tool/del_dicomData",t,e).then(e=>e.data),Y=(e,t)=>n.a.post(o+"/api/dicom/update",t,e).then(e=>e.data),Z=(e,t)=>n.a.post(o+"/api/tool/add_dicomData",t,e).then(e=>e.data),ee=(e,t)=>n.a.post(o+"/api/tool/dicomdetail",t,e).then(e=>e.data),te=(e,t)=>n.a.get(o+"/api/tool/dicomData",{params:t},{headers:e}).then(e=>e.data),ae=(e,t)=>n.a.post(o+"/api/tool/dicomcsv",t,e).then(e=>e.data),re=(e,t)=>n.a.post(o+"/api/tool/delreport",t,e).then(e=>e.data),ne=(e,t)=>n.a.get(o+"/api/stress/stressversion",{params:t},{headers:e}).then(e=>e.data),oe=(e,t)=>n.a.post(o+"/api/stress/stressresult",t,e).then(e=>e.data),se=(e,t)=>n.a.post(o+"/api/stress/stressfigure",t,e).then(e=>e.data),ie=(e,t)=>n.a.post(o+"/api/tool/delete_patients",t,e).then(e=>e.data),le=(e,t)=>n.a.get(o+"/api/tool/getduration",{params:t},{headers:e}).then(e=>e.data),de=(e,t)=>n.a.get(o+"/api/tool/durationData",{params:t},{headers:e}).then(e=>e.data),pe=(e,t)=>n.a.post(o+"/api/tool/add_duration",t,e).then(e=>e.data),ue=(e,t)=>n.a.post(o+"/api/tool/update_duration",t,e).then(e=>e.data),ce=(e,t)=>n.a.post(o+"/api/tool/del_duration",t,e).then(e=>e.data),he=(e,t)=>n.a.post(o+"/api/tool/anonymization",t,e).then(e=>e.data),me=(e,t)=>n.a.post(o+"/api/tool/enable_duration",t,e).then(e=>e.data),fe=(e,t)=>n.a.post(o+"/api/tool/disable_duration",t,e).then(e=>e.data),ge=(e,t)=>n.a.get(o+"/api/tool/duration_verify",{params:t},{headers:e}).then(e=>e.data),be=(e,t)=>n.a.get(o+"/api/tool/somkerecord",{params:t},{headers:e}).then(e=>e.data),ve=(e,t)=>n.a.post(o+"/api/tool/somke",t,e).then(e=>e.data),_e=(e,t)=>n.a.post(o+"/api/tool/dicomSend",t,e).then(e=>e.data),ye=(e,t)=>n.a.get(o+"/api/base/getdata",{params:t},{headers:e}).then(e=>e.data),we=(e,t)=>n.a.post(o+"/api/base/addData",t,e).then(e=>e.data),ke=(e,t)=>n.a.post(o+"/api/base/updateData",t,e).then(e=>e.data),Te=(e,t)=>n.a.post(o+"/api/base/enablebase",t,e).then(e=>e.data),xe=(e,t)=>n.a.post(o+"/api/base/disablebase",t,e).then(e=>e.data),je=(e,t)=>n.a.post(o+"/api/base/delbasedata",t,e).then(e=>e.data),Se=(e,t)=>n.a.get(o+"/api/base/dicom",{params:t},{headers:e}).then(e=>e.data)},"41d3":function(e,t,a){},"488b":function(e,t,a){"use strict";a.r(t);var r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("section",[a("el-row",{attrs:{gutter:20}},[a("el-col",{attrs:{span:12}},[a("div",{style:{height:"400px"},attrs:{id:"myChart"}})]),a("el-col",{attrs:{span:7}},[a("div",{style:{height:"400px"},attrs:{id:"singleTestChart"}})])],1),e._m(0),a("el-row",[a("el-col",{attrs:{span:4}},[a("el-select",{staticStyle:{"padding-left":"50px","padding-bottom":"10px"},attrs:{placeholder:"请选择测试时间"},model:{value:e.time,callback:function(t){e.time=t},expression:"time"}},e._l(e.options,(function(e){return a("el-option",{key:e.startTime,attrs:{label:e.startTime,value:e.startTime}})})),1)],1),a("el-col",{attrs:{span:4}},[a("div",[a("p",[e._v("测试耗时： "+e._s(e.elapsedTime)+"s")])])]),a("el-col",{attrs:{span:16}},[a("div",[a("p",[e._v("测试地址： "+e._s(e.host))])])])],1),a("div",{staticStyle:{"padding-left":"50px",width:"96%"}},[a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.listLoading,expression:"listLoading"}],attrs:{data:e.tableData,"row-style":e.tableRowStyle}},[a("el-table-column",{attrs:{type:"expand"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-form",{staticClass:"demo-table-expand",attrs:{"label-position":"left",inline:""}},[a("el-form-item",{attrs:{label:"名称: "}},[a("span",[e._v(e._s(t.row.name))])]),a("el-form-item"),a("el-form-item",{attrs:{label:"接口地址： "}},[a("span",[e._v(e._s(t.row.apiAddress))])]),a("el-form-item",{attrs:{label:"请求方式： "}},[a("span",[e._v(e._s(t.row.requestType))])]),a("el-form-item",{attrs:{label:"测试结果： "}},[a("span",[e._v(e._s(t.row.result))])]),a("el-form-item"),a("el-form-item",{attrs:{label:"请求头： "}},[a("span",{staticStyle:{"word-break":"break-all",overflow:"auto","overflow-x":"hidden"}},[e._v(e._s(t.row.header))])]),a("el-form-item",{attrs:{label:"返回头： "}},[a("span",{staticStyle:{"word-break":"break-all",overflow:"auto","overflow-x":"hidden"}},[e._v(e._s(t.row.responseHeader))])]),a("el-form-item",{attrs:{label:"请求参数： "}},[a("span",{staticStyle:{"word-break":"break-all",overflow:"auto","overflow-x":"hidden"}},[e._v(e._s(t.row.parameter))])]),a("el-form-item",{attrs:{label:"返回结果： "}},[a("span",{staticStyle:{"word-break":"break-all",overflow:"auto","overflow-x":"hidden"}},[e._v(e._s(t.row.responseData))])])],1)]}}])}),a("el-table-column",{attrs:{type:"index",label:"#",width:"100"}}),a("el-table-column",{attrs:{prop:"name",label:"接口名称","min-width":"29",sortable:"","show-overflow-tooltip":""}}),a("el-table-column",{attrs:{prop:"automationTestCase",label:"用例名称","min-width":"29%",sortable:"","show-overflow-tooltip":""}}),a("el-table-column",{attrs:{prop:"apiAddress",label:"请求地址","min-width":"20%",sortable:"","show-overflow-tooltip":""}}),a("el-table-column",{attrs:{prop:"examineType",label:"校验方式","min-width":"12%",sortable:"","show-overflow-tooltip":""},scopedSlots:e._u([{key:"default",fn:function(t){return["no_check"===t.row.examineType?a("a",[e._v("不校验")]):e._e(),"only_check_status"===t.row.examineType?a("a",[e._v("校验http状态")]):e._e(),"json"===t.row.examineType?a("a",[e._v("JSON校验")]):e._e(),"entirely_check"===t.row.examineType?a("a",[e._v("完全校验")]):e._e(),"Regular_check"===t.row.examineType?a("a",[e._v("正则校验")]):e._e()]}}])}),a("el-table-column",{attrs:{prop:"result",label:"结果","min-width":"10%",filters:e.resultFilter,"filter-method":e.filterHandler},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v(" "+e._s(t.row.result?t.row.result:"NotRun")+" ")]}}])})],1)],1),a("div",{staticStyle:{"margin-top":"5%"}})],1)},n=[function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("p",{staticStyle:{"padding-left":"50px",color:"#999"}},[e._v("*注"),a("strong",[e._v(": ")]),e._v("只保留最近十次的测试记录")])}],o=a("313e"),s=a.n(o),i=a("2d92"),l={data(){return{tableData:[],listLoading:!1,resultFilter:[{text:"ERROR",value:"ERROR"},{text:"FAIL",value:"FAIL"},{text:"NotRun",value:"NotRun"},{text:"PASS",value:"PASS"}],time:"",elapsedTime:"",host:"",options:[],pass:"",fail:"",error:"",latelyTenPass:[],latelyTenFail:[],latelyTenError:[]}},mounted(){this.getTenTestTime(),this.getLatelyTenTestResult()},methods:{getTestResult(){this.listLoading=!0;let e=this,t={project_id:this.$route.params.project_id,time:this.time.toString()},a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(i["U"])(a,t).then(t=>{let{msg:a,code:r,data:n}=t;e.listLoading=!1,"0"===r?(e.total=n.total,e.pass=n.pass,e.fail=n.fail,e.not_run=n.NotRun,e.error=n.error,e.tableData=n.data,e.singleTestDraw()):e.$message.error({message:a,center:!0})})},drawLine(){let e=s.a.init(document.getElementById("myChart")),t={title:{text:"近十次测试结果",left:"center",top:20,textStyle:{color:"#ccc"}},tooltip:{trigger:"axis",axisPointer:{type:"cross",crossStyle:{color:"#999"}}},toolbox:{feature:{dataView:{show:!0,readOnly:!1},magicType:{show:!0,type:["line","bar"]},restore:{show:!0},saveAsImage:{show:!0}}},legend:{data:["通过率","失败率","错误率"]},xAxis:[{type:"category",data:["1","2","3","4","5","6","7","8","9","10"],axisPointer:{type:"shadow"}}],yAxis:[{type:"value",name:"百分比",min:0,max:100,interval:20,axisLabel:{formatter:"{value} %"}}],series:[{name:"失败率",type:"bar",data:this.latelyTenFail},{name:"错误率",type:"line",data:this.latelyTenError},{name:"通过率",type:"bar",data:this.latelyTenPass}]};e.setOption(t)},singleTestDraw(){let e=s.a.init(document.getElementById("singleTestChart")),t={title:{text:"比例图",x:"center"},tooltip:{trigger:"item",formatter:"{a} <br/>{b} : {c} ({d}%)"},legend:{type:"scroll",orient:"vertical",right:10,top:20,bottom:20},toolbox:{feature:{dataView:{show:!0,readOnly:!1},magicType:{show:!0,type:["line","bar"]},restore:{show:!0},saveAsImage:{show:!0}}},series:[{type:"pie",radius:"50%",center:["50%","50%"],data:[{value:this.error,name:"ERROR"},{value:this.fail,name:"FAIL"},{value:this.pass,name:"PASS"}],itemStyle:{emphasis:{shadowBlur:10,shadowOffsetX:0,shadowColor:"rgba(0, 0, 0, 0.5)"}}}]};e.setOption(t)},tableRowStyle(e){return"ERROR"===e.result||"FAIL"===e.result?"background-color: #DC143C;":"TimeOut"===e.result?"background-color: #FFE4C4;":void 0},filterHandler(e,t,a){return t.result===e},getTenTestTime(){let e=this,t={project_id:this.$route.params.project_id},a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(i["W"])(a,t).then(t=>{let{msg:a,code:r,data:n}=t;"0"===r?(e.options=n,n.length&&(e.time=n[0].startTime,e.elapsedTime=n[0].elapsedTime,e.host=n[0].host,e.getTestResult())):e.$message.error({message:a,center:!0})})},changeHost(){for(let e=0;e<this.options.length;e++)this.options[e]["startTime"]===this.time&&(this.host=this.options[e].host,this.elapsedTime=this.options[e].elapsedTime)},getLatelyTenTestResult(){let e=this,t={project_id:this.$route.params.project_id},a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(i["V"])(a,t).then(t=>{let{msg:a,code:r,data:n}=t;"0"===r?(console.log(n),n.forEach(t=>{e.latelyTenPass.push(100*t.pass),e.latelyTenFail.push(100*t.fail),e.latelyTenError.push(100*t.error)}),e.drawLine()):e.$message.error({message:a,center:!0})})}},watch:{time(){this.getTestResult(),this.changeHost()}}},d=l,p=(a("b00c"),a("2877")),u=Object(p["a"])(d,r,n,!1,null,"49e6deb6",null);t["default"]=u.exports},b00c:function(e,t,a){"use strict";var r=a("cae7"),n=a.n(r);n.a},c896:function(e,t,a){"use strict";var r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("div",{staticClass:"crumbs"},[a("el-breadcrumb",{attrs:{separator:"/"}},[a("el-breadcrumb-item",[a("i",{staticClass:"el-icon-lx-calendar"}),e._v(" 测试工具")]),a("el-breadcrumb-item",[e._v("推送工具")])],1)],1),a("div",{staticClass:"container"},[a("div",{staticClass:"form-box"},[a("el-form",{ref:"form",attrs:{model:e.form,"status-icon":"",rules:e.rules,"label-width":"80px"}},[a("el-form-item",{attrs:{label:"推送ID",prop:"pushID"}},[a("el-col",{attrs:{span:10}},[a("el-input",{attrs:{id:"pushID"},model:{value:e.form.pushID,callback:function(t){e.$set(e.form,"pushID",t)},expression:"form.pushID"}})],1)],1),a("el-form-item",{attrs:{label:"推送环境",prop:"environment"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.form.environment,callback:function(t){e.$set(e.form,"environment",t)},expression:"form.environment"}},[a("el-option",{key:"test",attrs:{label:"测试环境",value:"test"}}),a("el-option",{key:"online",attrs:{label:"线上环境",value:"online"}})],1)],1),a("el-form-item",{attrs:{label:"推送类型",prop:"types"}},[a("el-cascader",{attrs:{options:e.types},on:{change:function(t){return e.changeLang("form")}},model:{value:e.form.types,callback:function(t){e.$set(e.form,"types",t)},expression:"form.types"}})],1),a("el-form-item",{attrs:{label:"选择语言",prop:"languages"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.form.languages,callback:function(t){e.$set(e.form,"languages",t)},expression:"form.languages"}},e._l(e.languages,(function(e,t){return a("el-option",{key:e.key,attrs:{label:e.value,value:e.key}})})),1)],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.onSubmit("form")}}},[e._v("确定推送")]),a("el-button",{on:{click:function(t){return e.resetForm("form")}}},[e._v("重置")])],1)],1)],1)])])},n=[],o={name:"baseform",data:function(){return{types:[{value:"bishijie",label:"Boimind",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"replay",label:"币圈"},{value:"monitor",label:"盯盘"}]},{value:"coinness",label:"coinness",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"monitor",label:"盯盘"}]}],languages:[],form:{pushID:"",environment:"",types:[],languages:[]},rules:{pushID:[{required:!0,message:"请输入推送ID",trigger:"blur"}],environment:[{required:!0,message:"请选择推送环境",trigger:"blur"}],types:[{required:!0,message:"请选择推送类型",trigger:"blur"}],languages:[{required:!0,message:"请选择语言",trigger:"blur"}]}}},methods:{onSubmit(e){this.$refs[e].validate(e=>{if(!e)return console.log("error submit"),!1;console.log("语言："+this.form.languages),console.log("pushID："+this.form.pushID),console.log("APP："+this.form.types[0]),console.log("推送类型："+this.form.types[1]),console.log("environment："+this.form.environment),this.$ajax.post("/bishijie/push",{id:this.form.pushID,service:this.form.environment,system:this.form.types[0],module:this.form.types[1],lang:this.form.languages,rid:""}).then(e=>{"0"==e.data.code?null==e.data.data||e.data.data[0]?this.$message.success("push成功！"):this.$message.error(e.data.data[1]):this.$message.error(e.data.msg)}).catch((function(e){console.log(e)}))})},resetForm(e){this.$refs[e].resetFields()},changeLang(e){this.languages=[],this.form.languages="";var t=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"}],a=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"},{key:"en_go",value:"English"},{key:"ko_kr",value:"한글"}],r=this.form.types[0].toLowerCase();"bishijie"==r?this.languages=t:"coinness"==r&&(this.languages=a)}}},s=o,i=(a("cd97"),a("2877")),l=Object(i["a"])(s,r,n,!1,null,"6d8efc95",null);l.exports},cae7:function(e,t,a){},cd97:function(e,t,a){"use strict";var r=a("41d3"),n=a.n(r);n.a}}]);