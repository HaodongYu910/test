(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-673974a0"],{"2d92":function(t,e,a){"use strict";a.d(e,"hb",(function(){return s})),a.d(e,"K",(function(){return i})),a.d(e,"s",(function(){return o})),a.d(e,"A",(function(){return l})),a.d(e,"E",(function(){return d})),a.d(e,"kb",(function(){return p})),a.d(e,"j",(function(){return u})),a.d(e,"L",(function(){return c})),a.d(e,"J",(function(){return h})),a.d(e,"r",(function(){return m})),a.d(e,"z",(function(){return f})),a.d(e,"D",(function(){return g})),a.d(e,"jb",(function(){return b})),a.d(e,"i",(function(){return _})),a.d(e,"M",(function(){return y})),a.d(e,"N",(function(){return v})),a.d(e,"I",(function(){return w})),a.d(e,"q",(function(){return x})),a.d(e,"h",(function(){return S})),a.d(e,"O",(function(){return k})),a.d(e,"Q",(function(){return L})),a.d(e,"P",(function(){return B})),a.d(e,"f",(function(){return j})),a.d(e,"H",(function(){return O})),a.d(e,"g",(function(){return D})),a.d(e,"ib",(function(){return C})),a.d(e,"p",(function(){return N})),a.d(e,"C",(function(){return A})),a.d(e,"eb",(function(){return I})),a.d(e,"lb",(function(){return z})),a.d(e,"k",(function(){return T})),a.d(e,"F",(function(){return J})),a.d(e,"u",(function(){return $})),a.d(e,"bb",(function(){return E})),a.d(e,"ab",(function(){return G})),a.d(e,"db",(function(){return P})),a.d(e,"cb",(function(){return Z})),a.d(e,"n",(function(){return U})),a.d(e,"nb",(function(){return V})),a.d(e,"w",(function(){return W})),a.d(e,"d",(function(){return X})),a.d(e,"gb",(function(){return q})),a.d(e,"fb",(function(){return M})),a.d(e,"R",(function(){return Y})),a.d(e,"x",(function(){return F})),a.d(e,"ob",(function(){return H})),a.d(e,"o",(function(){return K})),a.d(e,"Z",(function(){return Q})),a.d(e,"X",(function(){return R})),a.d(e,"Y",(function(){return tt})),a.d(e,"W",(function(){return et})),a.d(e,"v",(function(){return at})),a.d(e,"T",(function(){return nt})),a.d(e,"U",(function(){return rt})),a.d(e,"m",(function(){return st})),a.d(e,"mb",(function(){return it})),a.d(e,"t",(function(){return ot})),a.d(e,"G",(function(){return lt})),a.d(e,"B",(function(){return dt})),a.d(e,"V",(function(){return pt})),a.d(e,"S",(function(){return ut})),a.d(e,"l",(function(){return ct})),a.d(e,"e",(function(){return ht})),a.d(e,"c",(function(){return mt})),a.d(e,"b",(function(){return ft})),a.d(e,"a",(function(){return gt})),a.d(e,"y",(function(){return bt}));var n=a("bc3a"),r=a.n(n);const s="http://192.168.2.38:9000",i=(t,e)=>r.a.get(s+"/api/project/project_list",{params:e,headers:t}).then(t=>t.data),o=(t,e)=>r.a.post(s+"/api/project/del_project",e,{headers:t}).then(t=>t.data),l=(t,e)=>r.a.post(s+"/api/project/disable_project",e,{headers:t}).then(t=>t.data),d=(t,e)=>r.a.post(s+"/api/project/enable_project",e,{headers:t}).then(t=>t.data),p=(t,e)=>r.a.post(s+"/api/project/update_project",e,{headers:t}).then(t=>t.data),u=(t,e)=>r.a.post(s+"/api/project/add_project",e,{headers:t}).then(t=>t.data),c=(t,e)=>r.a.get(s+"/api/title/project_info",{params:e,headers:t}).then(t=>t.data),h=(t,e)=>r.a.get(s+"/api/global/host_total",{params:e,headers:t}).then(t=>t.data),m=(t,e)=>r.a.post(s+"/api/global/del_host",e,{headers:t}).then(t=>t.data),f=(t,e)=>r.a.post(s+"/api/global/disable_host",e,{headers:t}).then(t=>t.data),g=(t,e)=>r.a.post(s+"/api/global/enable_host",e,{headers:t}).then(t=>t.data),b=(t,e)=>r.a.post(s+"/api/global/update_host",e,{headers:t}).then(t=>t.data),_=(t,e)=>r.a.post(s+"/api/global/add_host",e,{headers:t}).then(t=>t.data),y=(t,e)=>r.a.get(s+"/api/dynamic/dynamic",{params:e,headers:t}).then(t=>t.data),v=(t,e)=>r.a.get(s+"/api/member/project_member",{params:e,headers:t}).then(t=>t.data),w=(t,e)=>r.a.get(s+"/api/member/get_email",{params:e,headers:t}).then(t=>t.data),x=(t,e)=>r.a.post(s+"/api/member/del_email",e,{headers:t}).then(t=>t.data),S=(t,e)=>r.a.post(s+"/api/member/email_config",e,{headers:t}).then(t=>t.data),k=(t,e)=>r.a.get(s+"/api/report/auto_test_report",{params:e,headers:t}).then(t=>t.data),L=(t,e)=>r.a.get(s+"/api/report/test_time",{params:e,headers:t}).then(t=>t.data),B=(t,e)=>r.a.get(s+"/api/report/lately_ten",{params:e,headers:t}).then(t=>t.data),j=(t,e)=>r.a.post(s+"/api/api/add_api",e,{headers:t}).then(t=>t.data),O=(t,e)=>r.a.get(s+"/api/api/group",{params:e,headers:t}).then(t=>t.data),D=(t,e)=>r.a.post(s+"/api/api/add_group",e,{headers:t}).then(t=>t.data),C=(t,e)=>r.a.post(s+"/api/api/update_name_group",e,{headers:t}).then(t=>t.data),N=(t,e)=>r.a.post(s+"/api/api/del_group",e,{headers:t}).then(t=>t.data),A=(t,e)=>r.a.post(s+"/api/download",e,{headers:t}).then(t=>t.data),I=(t,e)=>r.a.post(s+"/api/user/login",e,t).then(t=>t.data),z=(t,e)=>r.a.post(s+"/api/risk/update",e,{headers:t}).then(t=>t.data),T=(t,e)=>r.a.post(s+"/api/risk/add",e,{headers:t}).then(t=>t.data),J=(t,e)=>r.a.post(s+"/api/risk/add",e,{headers:t}).then(t=>t.data),$=(t,e)=>r.a.post(s+"/api/risk/del",e,t).then(t=>t.data),E=(t,e)=>r.a.get(s+"/api/risk ",{params:e},t).then(t=>t.data),G=(t,e)=>r.a.post(s+"/api/jira/figure ",e,t).then(t=>t.data),P=(t,e)=>r.a.get(s+"/api/todo ",{params:e},t).then(t=>t.data),Z=(t,e)=>r.a.get(s+"/api/report ",{params:e},t).then(t=>t.data),U=(t,e)=>r.a.post(s+"/api/addreport",e,t).then(t=>t.data),V=(t,e)=>r.a.post(s+"/api/updatereport",e,t).then(t=>t.data),W=(t,e)=>r.a.post(s+"/api/delreport",e,t).then(t=>t.data),X=(t,e)=>r.a.post(s+"/api/send",e,t).then(t=>t.data),q=(t,e)=>r.a.get(s+"/api/stress/list",{params:e},{headers:t}).then(t=>t.data),M=(t,e)=>r.a.post(s+"/api/stress/stresstool",e,t).then(t=>t.data),Y=(t,e)=>r.a.get(s+"/api/stress/version",{params:e},{headers:t}).then(t=>t.data),F=(t,e)=>r.a.post(s+"/api/stress/del_stressdata",e,t).then(t=>t.data),H=(t,e)=>r.a.post(s+"/api/stress/update_stressdata",e,t).then(t=>t.data),K=(t,e)=>r.a.post(s+"/api/stress/add_stressdata",e,t).then(t=>t.data),Q=(t,e)=>r.a.get(s+"/api/stress/stressversion",{params:e},{headers:t}).then(t=>t.data),R=(t,e)=>r.a.get(s+"/api/stress/stressdata",{params:e},{headers:t}).then(t=>t.data),tt=(t,e)=>r.a.post(s+"/api/tool/stressresult",e,t).then(t=>t.data),et=(t,e)=>r.a.post(s+"/api/stress/stressfigure",e,t).then(t=>t.data),at=(t,e)=>r.a.post(s+"/api/tool/delete_patients",e,t).then(t=>t.data),nt=(t,e)=>r.a.get(s+"/api/tool/getduration",{params:e},{headers:t}).then(t=>t.data),rt=(t,e)=>r.a.get(s+"/api/tool/durationData",{params:e},{headers:t}).then(t=>t.data),st=(t,e)=>r.a.post(s+"/api/tool/add_duration",e,t).then(t=>t.data),it=(t,e)=>r.a.post(s+"/api/tool/update_duration",e,t).then(t=>t.data),ot=(t,e)=>r.a.post(s+"/api/tool/del_duration",e,t).then(t=>t.data),lt=(t,e)=>r.a.post(s+"/api/tool/enable_duration",e,t).then(t=>t.data),dt=(t,e)=>r.a.post(s+"/api/tool/disable_duration",e,t).then(t=>t.data),pt=(t,e)=>r.a.get(s+"/api/tool/duration_verify",{params:e},{headers:t}).then(t=>t.data),ut=(t,e)=>r.a.get(s+"/api/base/getdata",{params:e},{headers:t}).then(t=>t.data),ct=(t,e)=>r.a.post(s+"/api/base/addData",e,t).then(t=>t.data),ht=(t,e)=>r.a.post(s+"/api/base/updateData",e,t).then(t=>t.data),mt=(t,e)=>r.a.post(s+"/api/base/enablebase",e,t).then(t=>t.data),ft=(t,e)=>r.a.post(s+"/api/base/disablebase",e,t).then(t=>t.data),gt=(t,e)=>r.a.post(s+"/api/base/delbasedata",e,t).then(t=>t.data),bt=(t,e)=>r.a.get(s+"/api/base/dicom",{params:e},{headers:t}).then(t=>t.data)},"5e41":function(t,e,a){},"9bde":function(t,e,a){"use strict";a.r(e);var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"app-container"},[a("div",{staticClass:"filter-container"},[a("el-col",{staticClass:"toolbar",staticStyle:{"padding-bottom":"0px"},attrs:{span:100}},[a("aside",[a("a",{attrs:{href:"http://192.168.2.38:3000/d/Ss3q6hSZk/docker-and-os-metrics-test?orgId=1&refresh=5s&from=now-5m&to=now&var-host_name=192.168.2.60&var-gpu_exporter_port=9445&var-node_exporter_port=9100&var-cadvisor_port=8080",target:"_blank"}},[t._v("Stress Monitor ")])]),a("el-col",{staticClass:"toolbar",staticStyle:{"padding-bottom":"0px"},attrs:{span:24}},[a("el-form",{attrs:{inline:!0,model:t.filters},nativeOn:{submit:function(t){t.preventDefault()}}},[a("el-select",{attrs:{placeholder:"请选择服务器"},nativeOn:{click:function(e){return t.gethost()}},model:{value:t.filters.server,callback:function(e){t.$set(t.filters,"server",e)},expression:"filters.server"}},t._l(t.tags,(function(t,e){return a("el-option",{key:t.host,attrs:{label:t.name,value:t.host}})})),1),a("el-select",{attrs:{placeholder:"当前版本"},nativeOn:{click:function(e){return t.getversion()}},model:{value:t.filters.version,callback:function(e){t.$set(t.filters,"version",e)},expression:"filters.version"}},t._l(t.versions,(function(t,e){return a("el-option",{key:t.version,attrs:{label:t.version,value:t.version}})})),1),a("el-select",{attrs:{placeholder:"以前版本"},nativeOn:{click:function(e){return t.getversion()}},model:{value:t.filters.checkversion,callback:function(e){t.$set(t.filters,"checkversion",e)},expression:"filters.checkversion"}},t._l(t.versions,(function(t,e){return a("el-option",{key:t.version,attrs:{label:t.version,value:t.version}})})),1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:t.getDurationlist}},[t._v("查询")])],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:t.handleAdd}},[t._v("生成报告")])],1)],1)],1),a("el-card",{staticStyle:{height:"350px"},attrs:{shadow:"hover"}},[a("el-row",{attrs:{gutter:20}},[a("el-col",{attrs:{span:12}},[a("el-card",{attrs:{shadow:"hover"}},[a("div",{staticClass:"mybar",staticStyle:{width:"250px",height:"310px",margin:"0 auto"},attrs:{id:"reportBar"}})])],1)],1)],1),a("span",{staticStyle:{"margin-left":"10px"}},[t._v("prediction time")]),a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.listLoading,expression:"listLoading"}],staticStyle:{width:"100%"},attrs:{data:t.prediction},on:{"selection-change":t.selsChange}},[a("el-table-column",{attrs:{prop:"modelname",label:"modelname","min-width":"8%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.modelname))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"prediction_count","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.count))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"avg pred time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.avg))])]}}])}),a("el-table-column",{attrs:{label:"median pred time /s","min-width":"10%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.median))])]}}])}),a("el-table-column",{attrs:{label:"min pred time /s","min-width":"10%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.min))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"max pred time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.max))])]}}])}),a("el-table-column",{attrs:{prop:"status",label:"coef. of variation","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.coef))])]}}])}),a("el-table-column",{attrs:{label:"rate of success","min-width":"8%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.rate))])]}}])})],1),a("span",{staticStyle:{"margin-left":"10px"}},[t._v("job time")]),a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.listLoading,expression:"listLoading"}],staticStyle:{width:"100%"},attrs:{data:t.job,"highlight-current-row":""},on:{"selection-change":t.selsChange}},[a("el-table-column",{attrs:{prop:"version",label:"modelname","min-width":"8%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.modelname))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"job_count","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.count))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"avg job time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.avg))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"avg single job time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.single))])]}}])}),a("el-table-column",{attrs:{label:"median job time /s","min-width":"10%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.median)+" 秒")])]}}])}),a("el-table-column",{attrs:{label:"min job time /s","min-width":"10%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.min))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"max job time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.max))])]}}])}),a("el-table-column",{attrs:{prop:"status",label:"coef. of variation","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.coef))])]}}])})],1),a("span",{staticStyle:{"margin-left":"10px"}},[t._v("Lung prediction time")]),a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.listLoading,expression:"listLoading"}],staticStyle:{width:"100%"},attrs:{data:t.lung,"highlight-current-row":""},on:{"selection-change":t.selsChange}},[a("el-table-column",{attrs:{prop:"version",label:"slicenumber","min-width":"6%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.slicenumber))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"avg pred time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.avg))])]}}])}),a("el-table-column",{attrs:{label:"median pred time /s","min-width":"10%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.median))])]}}])}),a("el-table-column",{attrs:{label:"min pred time /s","min-width":"10%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.min))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"max pred time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.max))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"coef. of variation","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.coef))])]}}])}),a("el-table-column",{attrs:{label:"rate of success","min-width":"8%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.rate))])]}}])})],1)],1)],1)])},r=[],s=a("2d92"),i=a("313e"),o=a.n(i),l={data(){return{filters:{diseases:""},durationlist:[],total:0,page:1,listLoading:!1,sels:[],reportBar:{},reportLine:{},coinnessBar:{},coinnessLine:{},reportBarData:[],reportLineData:[],coinnessBarData:[],coinnessLineData:[],twoData:[],reportBaroption:{backgroundColor:"#2c343c",title:{text:"Boimind-Bug解决数量状态图",left:"center",top:20,textStyle:{color:"#ccc"}},tooltip:{trigger:"item",formatter:"{a} <br/>{b} : {c} ({d}%)"},series:[{name:"Bug状态",type:"pie",radius:"55%",center:["50%","60%"],data:[],itemStyle:{emphasis:{shadowBlur:10,shadowOffsetX:0,shadowColor:"rgba(0, 0, 0, 0.5)"},normal:{label:{show:function(t){if(0==t)return!1}(),formatter:"{b} : {c} ({d}%)"},labelLine:{show:function(t){if(0==t)return!1}()}}}}]},coinnessBaroption:{backgroundColor:"#2c343c",title:{text:"CoinNess-Bug解决数量状态图",left:"center",top:20,textStyle:{color:"#ccc"}},tooltip:{trigger:"item",formatter:"{a} <br/>{b} : {c} ({d}%)"},series:[{name:"Bug状态",type:"pie",radius:"55%",center:["50%","60%"],data:[],itemStyle:{emphasis:{shadowBlur:10,shadowOffsetX:0,shadowColor:"rgba(0, 0, 0, 0.5)"},normal:{label:{show:function(t){if(0==t)return!1}(),formatter:"{b} : {c} ({d}%)"},labelLine:{show:function(t){if(0==t)return!1}()}}}}]},reportLineoption:{title:{text:"Boimind-创建与解决问题对比图"},tooltip:{trigger:"axis",padding:25},legend:{data:["创建问题","解决问题"],padding:25},toolbox:{show:!0,feature:{dataZoom:{yAxisIndex:"none"},dataView:{readOnly:!0},magicType:{type:["line","bar"]},restore:{},saveAsImage:{}}},xAxis:{type:"category",boundaryGap:!1,data:[]},yAxis:{type:"value",axisLabel:{formatter:"{value} 个"}},series:[{name:"创建问题",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"解决问题",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}}]},coinnessLineoption:{title:{text:"CoinNess-创建与解决问题对比图"},tooltip:{trigger:"axis",padding:25},legend:{data:["创建问题","解决问题"],padding:25},toolbox:{show:!0,feature:{dataZoom:{yAxisIndex:"none"},dataView:{readOnly:!0},magicType:{type:["line","bar"]},restore:{},saveAsImage:{}}},xAxis:{type:"category",boundaryGap:!1,data:[]},yAxis:{type:"value",axisLabel:{formatter:"{value} 个"}},series:[{name:"创建问题",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"解决问题",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}}]}}},components:{},mounted(){this.drawreportBar(),this.drawCoinNessBar(),this.drawreportLine(),this.drawCoinNessLine()},computed:{role(){return"admin"===this.name?"超级管理员":"普通用户"}},created(){this.getreportData(),this.getCoinnessData(),this.getData()},watch:{reportBaroption:{handler(t,e){this.reportBar?t?this.reportBar.setOption(t):this.reportBar.setOption(e):this.drawreportBar()},deep:!0},reportLineoption:{handler(t,e){this.reportBar?t?this.reportLine.setOption(t):this.reportLine.setOption(e):this.drawreportLine()},deep:!0},coinnessBaroption:{handler(t,e){this.coinnessBar?t?this.coinnessBar.setOption(t):this.coinnessBar.setOption(e):this.drawCoinNessBar()},deep:!0},coinnessLineoption:{handler(t,e){this.coinnessBar?t?this.coinnessLine.setOption(t):this.coinnessLine.setOption(e):this.drawCoinNessLine()},deep:!0}},mounted(){this.getDurationlist(),this.gethost(),this.getBase()},methods:{getversion(){this.listLoading=!0;const t=this,e={},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(s["Z"])(a,e).then(e=>{t.listLoading=!1;const{msg:a,code:n,data:r}=e;if("0"===n){t.total=r.total,t.list=r.data;var s=JSON.stringify(t.list);this.versions=JSON.parse(s)}else t.$message.error({message:a,center:!0})})},gethost(){this.listLoading=!0;const t=this,e={},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(s["J"])(a,e).then(e=>{t.listLoading=!1;const{msg:a,code:n,data:r}=e;if("0"===n){t.total=r.total,t.list=r.data;var s=JSON.stringify(t.list);this.tags=JSON.parse(s)}else t.$message.error({message:a,center:!0})})},getDurationlist(){this.listLoading=!0;const t=this,e={version:this.filters.version,checkversion:this.filters.checkversion,server:this.filters.server},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(s["Y"])(a,e).then(e=>{t.listLoading=!1;const{msg:a,code:n,data:r}=e;"0"===n?(t.prediction=r.predictionresult,t.job=r.jobresult,t.lung=r.lungresult):t.$message.error({message:a,center:!0})})},selsChange:function(t){this.sels=t},getreportData(){let t={checkversion:"BUG",version:"Boimind"},e={"Content-Type":"application/json"};Object(s["W"])(e,t).then(t=>{let{code:e,msg:a,data:n}=t;this.reportLineData=n.figure_list,this.reportLineoption.xAxis.data=this.reportLineData[0],this.reportLineoption.series[0].data=this.reportLineData[1],this.reportLineoption.series[1].data=this.reportLineData[2],this.reportBarData=n.solution_state.sort((function(t,e){return t.value-e.value})),this.reportBaroption.series[0].data=this.reportBarData})},getCoinnessData(){let t={checkversion:"BUG",version:"Boimind"},e={"Content-Type":"application/json"};Object(s["W"])(e,t).then(t=>{let{code:e,msg:a,data:n}=t;this.coinnessLineData=n.figure_list,this.coinnessLineoption.xAxis.data=this.coinnessLineData[0],this.coinnessLineoption.series[0].data=this.coinnessLineData[1],this.coinnessLineoption.series[1].data=this.coinnessLineData[2],this.coinnessBarData=n.solution_state.sort((function(t,e){return t.value-e.value})),this.coinnessBaroption.series[0].data=this.coinnessBarData})},drawreportBar(){this.reportBar=o.a.init(document.getElementById("reportBar")),this.reportBar.setOption(this.reportBaroption,!0),setTimeout(()=>{window.onresize=reportBar.resize},200)},drawCoinNessBar(){this.coinnessBar=o.a.init(document.getElementById("coinnessBar")),this.coinnessBar.setOption(this.coinnessBaroption,!0),setTimeout(()=>{window.onresize=coinnessBar.resize},200)},drawreportLine(){this.reportLine=o.a.init(document.getElementById("reportLine")),this.reportLine.setOption(this.reportLineoption),setTimeout(()=>{window.onresize=reportLine.resize},200)},drawCoinNessLine(){this.coinnessLine=o.a.init(document.getElementById("coinnessLine")),this.coinnessLine.setOption(this.coinnessLineoption),setTimeout(()=>{window.onresize=coinnessLine.resize},200)}}},d=l,p=(a("f558"),a("2877")),u=Object(p["a"])(d,n,r,!1,null,"d400e2d6",null);e["default"]=u.exports},f558:function(t,e,a){"use strict";var n=a("5e41"),r=a.n(n);r.a}}]);