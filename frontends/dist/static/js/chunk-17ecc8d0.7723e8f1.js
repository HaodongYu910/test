(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-17ecc8d0"],{"0d93":function(t,e,a){},"2d92":function(t,e,a){"use strict";a.d(e,"nb",(function(){return r})),a.d(e,"O",(function(){return s})),a.d(e,"t",(function(){return o})),a.d(e,"E",(function(){return l})),a.d(e,"I",(function(){return d})),a.d(e,"qb",(function(){return p})),a.d(e,"k",(function(){return u})),a.d(e,"P",(function(){return c})),a.d(e,"N",(function(){return m})),a.d(e,"s",(function(){return h})),a.d(e,"D",(function(){return f})),a.d(e,"H",(function(){return g})),a.d(e,"pb",(function(){return b})),a.d(e,"j",(function(){return y})),a.d(e,"Q",(function(){return v})),a.d(e,"R",(function(){return _})),a.d(e,"M",(function(){return w})),a.d(e,"r",(function(){return x})),a.d(e,"i",(function(){return k})),a.d(e,"S",(function(){return L})),a.d(e,"U",(function(){return S})),a.d(e,"T",(function(){return j})),a.d(e,"g",(function(){return D})),a.d(e,"L",(function(){return O})),a.d(e,"h",(function(){return P})),a.d(e,"ob",(function(){return B})),a.d(e,"q",(function(){return I})),a.d(e,"G",(function(){return A})),a.d(e,"kb",(function(){return C})),a.d(e,"rb",(function(){return z})),a.d(e,"l",(function(){return $})),a.d(e,"J",(function(){return N})),a.d(e,"x",(function(){return T})),a.d(e,"hb",(function(){return J})),a.d(e,"jb",(function(){return E})),a.d(e,"ib",(function(){return F})),a.d(e,"p",(function(){return q})),a.d(e,"ub",(function(){return G})),a.d(e,"z",(function(){return V})),a.d(e,"d",(function(){return Z})),a.d(e,"mb",(function(){return H})),a.d(e,"e",(function(){return K})),a.d(e,"lb",(function(){return M})),a.d(e,"V",(function(){return Q})),a.d(e,"u",(function(){return R})),a.d(e,"sb",(function(){return U})),a.d(e,"n",(function(){return W})),a.d(e,"C",(function(){return X})),a.d(e,"Y",(function(){return Y})),a.d(e,"B",(function(){return tt})),a.d(e,"v",(function(){return et})),a.d(e,"gb",(function(){return at})),a.d(e,"fb",(function(){return nt})),a.d(e,"cb",(function(){return it})),a.d(e,"y",(function(){return rt})),a.d(e,"Z",(function(){return st})),a.d(e,"ab",(function(){return ot})),a.d(e,"o",(function(){return lt})),a.d(e,"tb",(function(){return dt})),a.d(e,"w",(function(){return pt})),a.d(e,"K",(function(){return ut})),a.d(e,"F",(function(){return ct})),a.d(e,"bb",(function(){return mt})),a.d(e,"db",(function(){return ht})),a.d(e,"eb",(function(){return ft})),a.d(e,"X",(function(){return gt})),a.d(e,"W",(function(){return bt})),a.d(e,"m",(function(){return yt})),a.d(e,"f",(function(){return vt})),a.d(e,"c",(function(){return _t})),a.d(e,"b",(function(){return wt})),a.d(e,"a",(function(){return xt})),a.d(e,"A",(function(){return kt}));var n=a("bc3a"),i=a.n(n);a("c896");const r="http://192.168.2.38:9000",s=(t,e)=>i.a.get(r+"/api/project/project_list",{params:e,headers:t}).then(t=>t.data),o=(t,e)=>i.a.post(r+"/api/project/del_project",e,{headers:t}).then(t=>t.data),l=(t,e)=>i.a.post(r+"/api/project/disable_project",e,{headers:t}).then(t=>t.data),d=(t,e)=>i.a.post(r+"/api/project/enable_project",e,{headers:t}).then(t=>t.data),p=(t,e)=>i.a.post(r+"/api/project/update_project",e,{headers:t}).then(t=>t.data),u=(t,e)=>i.a.post(r+"/api/project/add_project",e,{headers:t}).then(t=>t.data),c=(t,e)=>i.a.get(r+"/api/title/project_info",{params:e,headers:t}).then(t=>t.data),m=(t,e)=>i.a.get(r+"/api/global/host_total",{params:e,headers:t}).then(t=>t.data),h=(t,e)=>i.a.post(r+"/api/global/del_host",e,{headers:t}).then(t=>t.data),f=(t,e)=>i.a.post(r+"/api/global/disable_host",e,{headers:t}).then(t=>t.data),g=(t,e)=>i.a.post(r+"/api/global/enable_host",e,{headers:t}).then(t=>t.data),b=(t,e)=>i.a.post(r+"/api/global/update_host",e,{headers:t}).then(t=>t.data),y=(t,e)=>i.a.post(r+"/api/global/add_host",e,{headers:t}).then(t=>t.data),v=(t,e)=>i.a.get(r+"/api/dynamic/dynamic",{params:e,headers:t}).then(t=>t.data),_=(t,e)=>i.a.get(r+"/api/member/project_member",{params:e,headers:t}).then(t=>t.data),w=(t,e)=>i.a.get(r+"/api/member/get_email",{params:e,headers:t}).then(t=>t.data),x=(t,e)=>i.a.post(r+"/api/member/del_email",e,{headers:t}).then(t=>t.data),k=(t,e)=>i.a.post(r+"/api/member/email_config",e,{headers:t}).then(t=>t.data),L=(t,e)=>i.a.get(r+"/api/report/auto_test_report",{params:e,headers:t}).then(t=>t.data),S=(t,e)=>i.a.get(r+"/api/report/test_time",{params:e,headers:t}).then(t=>t.data),j=(t,e)=>i.a.get(r+"/api/report/lately_ten",{params:e,headers:t}).then(t=>t.data),D=(t,e)=>i.a.post(r+"/api/api/add_api",e,{headers:t}).then(t=>t.data),O=(t,e)=>i.a.get(r+"/api/api/group",{params:e,headers:t}).then(t=>t.data),P=(t,e)=>i.a.post(r+"/api/api/add_group",e,{headers:t}).then(t=>t.data),B=(t,e)=>i.a.post(r+"/api/api/update_name_group",e,{headers:t}).then(t=>t.data),I=(t,e)=>i.a.post(r+"/api/api/del_group",e,{headers:t}).then(t=>t.data),A=(t,e)=>i.a.post(r+"/api/download",e,{headers:t}).then(t=>t.data),C=(t,e)=>i.a.post(r+"/api/user/login",e,t).then(t=>t.data),z=(t,e)=>i.a.post(r+"/api/risk/update",e,{headers:t}).then(t=>t.data),$=(t,e)=>i.a.post(r+"/api/risk/add",e,{headers:t}).then(t=>t.data),N=(t,e)=>i.a.post(r+"/api/risk/add",e,{headers:t}).then(t=>t.data),T=(t,e)=>i.a.post(r+"/api/risk/del",e,t).then(t=>t.data),J=(t,e)=>i.a.get(r+"/api/risk ",{params:e},t).then(t=>t.data),E=(t,e)=>i.a.get(r+"/api/todo ",{params:e},t).then(t=>t.data),F=(t,e)=>i.a.get(r+"/api/report ",{params:e},t).then(t=>t.data),q=(t,e)=>i.a.post(r+"/api/addreport",e,t).then(t=>t.data),G=(t,e)=>i.a.post(r+"/api/updatereport",e,t).then(t=>t.data),V=(t,e)=>i.a.post(r+"/api/delreport",e,t).then(t=>t.data),Z=(t,e)=>i.a.post(r+"/api/send",e,t).then(t=>t.data),H=(t,e)=>i.a.get(r+"/api/stress/list",{params:e},{headers:t}).then(t=>t.data),K=(t,e)=>i.a.get(r+"/api/stress/stressDetail ",{params:e},t).then(t=>t.data),M=(t,e)=>i.a.post(r+"/api/stress/stresstool",e,t).then(t=>t.data),Q=(t,e)=>i.a.get(r+"/api/stress/version",{params:e},{headers:t}).then(t=>t.data),R=(t,e)=>i.a.post(r+"/api/tool/del_dicomData",e,t).then(t=>t.data),U=(t,e)=>i.a.post(r+"/api/tool/update_dicomData",e,t).then(t=>t.data),W=(t,e)=>i.a.post(r+"/api/tool/add_dicomData",e,t).then(t=>t.data),X=(t,e)=>i.a.post(r+"/api/tool/dicomdetail",e,t).then(t=>t.data),Y=(t,e)=>i.a.get(r+"/api/tool/dicomData",{params:e},{headers:t}).then(t=>t.data),tt=(t,e)=>i.a.post(r+"/api/tool/dicomcsv",e,t).then(t=>t.data),et=(t,e)=>i.a.post(r+"/api/tool/delreport",e,t).then(t=>t.data),at=(t,e)=>i.a.get(r+"/api/stress/stressversion",{params:e},{headers:t}).then(t=>t.data),nt=(t,e)=>i.a.post(r+"/api/stress/stressresult",e,t).then(t=>t.data),it=(t,e)=>i.a.post(r+"/api/stress/stressfigure",e,t).then(t=>t.data),rt=(t,e)=>i.a.post(r+"/api/tool/delete_patients",e,t).then(t=>t.data),st=(t,e)=>i.a.get(r+"/api/tool/getduration",{params:e},{headers:t}).then(t=>t.data),ot=(t,e)=>i.a.get(r+"/api/tool/durationData",{params:e},{headers:t}).then(t=>t.data),lt=(t,e)=>i.a.post(r+"/api/tool/add_duration",e,t).then(t=>t.data),dt=(t,e)=>i.a.post(r+"/api/tool/update_duration",e,t).then(t=>t.data),pt=(t,e)=>i.a.post(r+"/api/tool/del_duration",e,t).then(t=>t.data),ut=(t,e)=>i.a.post(r+"/api/tool/enable_duration",e,t).then(t=>t.data),ct=(t,e)=>i.a.post(r+"/api/tool/disable_duration",e,t).then(t=>t.data),mt=(t,e)=>i.a.get(r+"/api/tool/duration_verify",{params:e},{headers:t}).then(t=>t.data),ht=(t,e)=>i.a.get(r+"/api/tool/somkerecord",{params:e},{headers:t}).then(t=>t.data),ft=(t,e)=>i.a.post(r+"/api/tool/somke",e,t).then(t=>t.data),gt=(t,e)=>i.a.post(r+"/api/tool/dicomSend",e,t).then(t=>t.data),bt=(t,e)=>i.a.get(r+"/api/base/getdata",{params:e},{headers:t}).then(t=>t.data),yt=(t,e)=>i.a.post(r+"/api/base/addData",e,t).then(t=>t.data),vt=(t,e)=>i.a.post(r+"/api/base/updateData",e,t).then(t=>t.data),_t=(t,e)=>i.a.post(r+"/api/base/enablebase",e,t).then(t=>t.data),wt=(t,e)=>i.a.post(r+"/api/base/disablebase",e,t).then(t=>t.data),xt=(t,e)=>i.a.post(r+"/api/base/delbasedata",e,t).then(t=>t.data),kt=(t,e)=>i.a.get(r+"/api/base/dicom",{params:e},{headers:t}).then(t=>t.data)},"41d3":function(t,e,a){},4657:function(t,e,a){"use strict";var n=a("0d93"),i=a.n(n);i.a},"9bde":function(t,e,a){"use strict";a.r(e);var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"app-container"},[a("div",{staticClass:"filter-container"},[a("el-col",{staticClass:"toolbar",staticStyle:{"padding-bottom":"0px"},attrs:{span:100}},[a("el-card",{staticStyle:{width:"100%",height:"800px"},attrs:{shadow:"hover"}},[a("el-row",{attrs:{gutter:50}},[a("el-col",{attrs:{span:30}},[a("el-card",{attrs:{shadow:"hover"}},[a("div",{staticClass:"myLine",staticStyle:{width:"1500px",height:"600px",margin:"0 auto"},attrs:{id:"predictionLine"}})])],1)],1)],1),a("el-card",{staticStyle:{width:"100%",height:"800px"},attrs:{shadow:"hover"}},[a("el-row",{attrs:{gutter:50}},[a("el-col",{attrs:{span:30}},[a("el-card",{attrs:{shadow:"hover"}},[a("div",{staticClass:"myLine",staticStyle:{width:"1500px",height:"600px",margin:"0 auto"},attrs:{id:"jobLine"}})])],1)],1)],1),a("el-card",{staticStyle:{width:"100%",height:"800px"},attrs:{shadow:"hover"}},[a("el-row",{attrs:{gutter:50}},[a("el-col",{attrs:{span:30}},[a("el-card",{attrs:{shadow:"hover"}},[a("div",{staticClass:"myLine",staticStyle:{width:"750px",height:"600px",margin:"0 auto"},attrs:{id:"lungLine"}})])],1)],1)],1),a("el-col",{staticClass:"toolbar",staticStyle:{"padding-bottom":"0px"},attrs:{span:24}},[a("el-form",{attrs:{inline:!0,model:t.filters},nativeOn:{submit:function(t){t.preventDefault()}}},[a("el-select",{attrs:{placeholder:"请选择服务器"},nativeOn:{click:function(e){return t.gethost()}},model:{value:t.filters.server,callback:function(e){t.$set(t.filters,"server",e)},expression:"filters.server"}},t._l(t.tags,(function(t,e){return a("el-option",{key:t.host,attrs:{label:t.name,value:t.host}})})),1),a("el-select",{attrs:{placeholder:"当前版本"},nativeOn:{click:function(e){return t.getversion()}},model:{value:t.filters.version,callback:function(e){t.$set(t.filters,"version",e)},expression:"filters.version"}},t._l(t.versions,(function(t,e){return a("el-option",{key:t.version,attrs:{label:t.version,value:t.version}})})),1),a("el-select",{attrs:{placeholder:"以前版本"},nativeOn:{click:function(e){return t.getversion()}},model:{value:t.filters.checkversion,callback:function(e){t.$set(t.filters,"checkversion",e)},expression:"filters.checkversion"}},t._l(t.versions,(function(t,e){return a("el-option",{key:t.version,attrs:{label:t.version,value:t.version}})})),1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:t.getDurationlist}},[t._v("查询")])],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:t.handleAdd}},[t._v("生成报告")])],1)],1)],1),a("span",{staticStyle:{"margin-left":"10px"}},[t._v("prediction time")]),a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.listLoading,expression:"listLoading"}],staticStyle:{width:"100%"},attrs:{data:t.prediction},on:{"selection-change":t.selsChange}},[a("el-table-column",{attrs:{prop:"modelname",label:"modelname","min-width":"8%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.modelname))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"prediction_count","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.count))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"avg pred time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{class:t.valuestatus(e.row.avg),staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.avg))])]}}])}),a("el-table-column",{attrs:{label:"median pred time /s","min-width":"10%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{class:t.valuestatus(e.row.median),staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.median))])]}}])}),a("el-table-column",{attrs:{label:"min pred time /s","min-width":"10%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{class:t.valuestatus(e.row.min),staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.min))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"max pred time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{class:t.valuestatus(e.row.max),staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.max))])]}}])}),a("el-table-column",{attrs:{prop:"status",label:"coef. of variation","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.coef))])]}}])}),a("el-table-column",{attrs:{label:"rate of success","min-width":"8%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.rate))])]}}])})],1),a("span",{staticStyle:{"margin-left":"10px"}},[t._v("job time")]),a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.listLoading,expression:"listLoading"}],staticStyle:{width:"100%"},attrs:{data:t.job,"highlight-current-row":""},on:{"selection-change":t.selsChange}},[a("el-table-column",{attrs:{prop:"version",label:"modelname","min-width":"8%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.modelname))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"job_count","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.count))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"avg job time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{class:t.valuestatus(e.row.avg),staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.avg))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"avg single job time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{class:t.valuestatus(e.row.single),staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.single))])]}}])}),a("el-table-column",{attrs:{label:"median job time /s","min-width":"10%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{class:t.valuestatus(e.row.median),staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.median)+" 秒")])]}}])}),a("el-table-column",{attrs:{label:"min job time /s","min-width":"10%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{class:t.valuestatus(e.row.min),staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.min))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"max job time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{class:t.valuestatus(e.row.max),staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.max))])]}}])}),a("el-table-column",{attrs:{prop:"status",label:"coef. of variation","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.coef))])]}}])})],1),a("span",{staticStyle:{"margin-left":"10px"}},[t._v("Lung prediction time")]),a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.listLoading,expression:"listLoading"}],staticStyle:{width:"100%"},attrs:{data:t.lung,"highlight-current-row":""},on:{"selection-change":t.selsChange}},[a("el-table-column",{attrs:{prop:"version",label:"slicenumber","min-width":"6%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.slicenumber))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"avg pred time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{class:t.valuestatus(e.row.avg),staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.avg))])]}}])}),a("el-table-column",{attrs:{label:"median pred time /s","min-width":"10%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{class:t.valuestatus(e.row.median),staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.median))])]}}])}),a("el-table-column",{attrs:{label:"min pred time /s","min-width":"10%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{class:t.valuestatus(e.row.min),staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.min))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"max pred time /s","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{class:t.valuestatus(e.row.max),staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.max))])]}}])}),a("el-table-column",{attrs:{prop:"type",label:"coef. of variation","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.coef))])]}}])}),a("el-table-column",{attrs:{label:"rate of success","min-width":"8%",sortable:""},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.rate))])]}}])})],1)],1)],1)])},i=[],r=a("2d92"),s=a("313e"),o=a.n(s),l={data(){return{filters:{diseases:""},durationlist:[],total:0,page:1,listLoading:!1,sels:[],predictionLine:{},jobLine:{},lungLine:{},predictionLineData:[],jobLineData:[],lungData:[],twoData:[],predictionLineoption:{title:{text:"模型预测时间对比图"},tooltip:{trigger:"axis",padding:25},legend:{data:["aibrainct","aibrainmri","aicardiomodel","archcta","bodypart","brainct","braincta","brainctp","brainmra","headcta","postsurgery"],padding:25},toolbox:{show:!0,feature:{dataZoom:{yAxisIndex:"none"},dataView:{readOnly:!0},magicType:{type:["line","bar"]},restore:{},saveAsImage:{}}},xAxis:{type:"category",boundaryGap:!1,data:[]},yAxis:{type:"value",axisLabel:{formatter:"{value} 秒"}},series:[{name:"aibrainct",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"aibrainmri",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"aicardiomodel",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"archcta",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"bodypart",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"brainct",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"braincta",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"brainctp",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"brainmra",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"headcta",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"lungct",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"postsurgery",type:"line",data:[],markPoint:{}}]},jobLineoption:{title:{text:"Job时间对比图"},tooltip:{trigger:"axis",padding:25},legend:{data:["aibrainct","aibrainmri","aicardiomodel","archcta","bodypart","brainct","braincta","brainctp","brainmra","headcta","postsurgery"],padding:25},toolbox:{show:!0,feature:{dataZoom:{yAxisIndex:"none"},dataView:{readOnly:!0},magicType:{type:["line","bar"]},restore:{},saveAsImage:{}}},xAxis:{type:"category",boundaryGap:!1,data:[]},yAxis:{type:"value",axisLabel:{formatter:"{value} 秒"}},series:[{name:"aibrainct",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"aibrainmri",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"aicardiomodel",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"archcta",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"bodypart",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"brainct",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"braincta",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"brainctp",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"brainmra",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"headcta",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"lungct",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"postsurgery",type:"line",data:[],markPoint:{}}]},lungLineoption:{title:{text:"Lung层厚预测时间对比图"},tooltip:{trigger:"axis",padding:25},legend:{data:["1.0","1.25","1.5","5.0","10.0"],padding:25},toolbox:{show:!0,feature:{dataZoom:{yAxisIndex:"none"},dataView:{readOnly:!0},magicType:{type:["line","bar"]},restore:{},saveAsImage:{}}},xAxis:{type:"category",boundaryGap:!1,data:[]},yAxis:{type:"value",axisLabel:{formatter:"{value} 秒"}},series:[{name:"1.0",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"1.25",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"1.5",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"5.0",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"10.0",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}}]}}},components:{},mounted(){this.drawpredictionLine(),this.drawjobLine(),this.drawlungLine(),this.gethost(),this.getBase()},created(){this.getreportData(),this.getData()},watch:{predictionLineoption:{handler(t,e){this.reportBar?t?this.predictionLine.setOption(t):this.predictionLine.setOption(e):this.drawpredictionLine()},deep:!0},jobLineoption:{handler(t,e){this.coinnessBar?t?this.jobLine.setOption(t):this.jobLine.setOption(e):this.drawjobLine()},deep:!0},lungLineoption:{handler(t,e){this.lungBar?t?this.lungLine.setOption(t):this.lungLine.setOption(e):this.drawlungLine()},deep:!0}},methods:{valuestatus:function(t){switch(t=/-/g.test(t)?/\+/g.test(t)?2:1:0,console.log(t),t){case 0:return"statuscssa";case 1:return"statuscssb";case 2:return"statuscssc"}},getversion(){this.listLoading=!0;const t=this,e={},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(r["gb"])(a,e).then(e=>{t.listLoading=!1;const{msg:a,code:n,data:i}=e;if("0"===n){t.total=i.total,t.list=i.data;var r=JSON.stringify(t.list);this.versions=JSON.parse(r)}else t.$message.error({message:a,center:!0})})},gethost(){this.listLoading=!0;const t=this,e={},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(r["N"])(a,e).then(e=>{t.listLoading=!1;const{msg:a,code:n,data:i}=e;if("0"===n){t.total=i.total,t.list=i.data;var r=JSON.stringify(t.list);this.tags=JSON.parse(r)}else t.$message.error({message:a,center:!0})})},getDurationlist(){this.listLoading=!0;const t=this,e={version:this.filters.version,checkversion:this.filters.checkversion,server:this.filters.server},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(r["fb"])(a,e).then(e=>{t.listLoading=!1;const{msg:a,code:n,data:i}=e;"0"===n?(t.prediction=i.predictionresult,t.job=i.jobresult,t.lung=i.lungresult):t.$message.error({message:a,center:!0})})},selsChange:function(t){this.sels=t},getreportData(){let t={version:"Boimind",type:"prediction"},e={"Content-Type":"application/json"};Object(r["cb"])(e,t).then(t=>{let{code:e,msg:a,data:n}=t;this.predictionLineData=n.predictionFigure,this.jobLineData=n.jobFigure,this.lungLineData=n.lungFigure,this.predictionLineoption.xAxis.data=this.predictionLineData[0],this.jobLineoption.xAxis.data=this.jobLineData[0],this.lungLineoption.xAxis.data=this.lungLineData[0];for(var i=0;i<this.predictionLineData.length;i++)this.predictionLineoption.series[i].data=this.predictionLineData[i+1],this.jobLineoption.series[i].data=this.jobLineData[i+1];this.lungLineoption.series[0].data=this.lungLineData[1],this.lungLineoption.series[1].data=this.lungLineData[2],this.lungLineoption.series[2].data=this.lungLineData[3],this.lungLineoption.series[3].data=this.lungLineData[4],this.lungLineoption.series[4].data=this.lungLineData[5],this.reportBarData=n.solution_state.sort((function(t,e){return t.value-e.value})),this.reportBaroption.series[0].data=this.reportBarData})},drawreportBar(){this.reportBar=o.a.init(document.getElementById("reportBar")),this.reportBar.setOption(this.reportBaroption,!0),setTimeout(()=>{window.onresize=reportBar.resize},200)},drawCoinNessBar(){this.coinnessBar=o.a.init(document.getElementById("coinnessBar")),this.coinnessBar.setOption(this.coinnessBaroption,!0),setTimeout(()=>{window.onresize=coinnessBar.resize},200)},drawpredictionLine(){this.predictionLine=o.a.init(document.getElementById("predictionLine")),this.predictionLine.setOption(this.predictionLineoption),setTimeout(()=>{window.onresize=predictionLine.resize},200)},drawjobLine(){this.jobLine=o.a.init(document.getElementById("jobLine")),this.jobLine.setOption(this.jobLineoption),setTimeout(()=>{window.onresize=jobLine.resize},200)},drawlungLine(){this.lungLine=o.a.init(document.getElementById("lungLine")),this.lungLine.setOption(this.lungLineoption),setTimeout(()=>{window.onresize=lungLine.resize},200)}}},d=l,p=(a("4657"),a("2877")),u=Object(p["a"])(d,n,i,!1,null,"47785a4f",null);e["default"]=u.exports},c896:function(t,e,a){"use strict";var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("div",{staticClass:"crumbs"},[a("el-breadcrumb",{attrs:{separator:"/"}},[a("el-breadcrumb-item",[a("i",{staticClass:"el-icon-lx-calendar"}),t._v(" 测试工具")]),a("el-breadcrumb-item",[t._v("推送工具")])],1)],1),a("div",{staticClass:"container"},[a("div",{staticClass:"form-box"},[a("el-form",{ref:"form",attrs:{model:t.form,"status-icon":"",rules:t.rules,"label-width":"80px"}},[a("el-form-item",{attrs:{label:"推送ID",prop:"pushID"}},[a("el-col",{attrs:{span:10}},[a("el-input",{attrs:{id:"pushID"},model:{value:t.form.pushID,callback:function(e){t.$set(t.form,"pushID",e)},expression:"form.pushID"}})],1)],1),a("el-form-item",{attrs:{label:"推送环境",prop:"environment"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:t.form.environment,callback:function(e){t.$set(t.form,"environment",e)},expression:"form.environment"}},[a("el-option",{key:"test",attrs:{label:"测试环境",value:"test"}}),a("el-option",{key:"online",attrs:{label:"线上环境",value:"online"}})],1)],1),a("el-form-item",{attrs:{label:"推送类型",prop:"types"}},[a("el-cascader",{attrs:{options:t.types},on:{change:function(e){return t.changeLang("form")}},model:{value:t.form.types,callback:function(e){t.$set(t.form,"types",e)},expression:"form.types"}})],1),a("el-form-item",{attrs:{label:"选择语言",prop:"languages"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:t.form.languages,callback:function(e){t.$set(t.form,"languages",e)},expression:"form.languages"}},t._l(t.languages,(function(t,e){return a("el-option",{key:t.key,attrs:{label:t.value,value:t.key}})})),1)],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:function(e){return t.onSubmit("form")}}},[t._v("确定推送")]),a("el-button",{on:{click:function(e){return t.resetForm("form")}}},[t._v("重置")])],1)],1)],1)])])},i=[],r={name:"baseform",data:function(){return{types:[{value:"bishijie",label:"Boimind",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"replay",label:"币圈"},{value:"monitor",label:"盯盘"}]},{value:"coinness",label:"coinness",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"monitor",label:"盯盘"}]}],languages:[],form:{pushID:"",environment:"",types:[],languages:[]},rules:{pushID:[{required:!0,message:"请输入推送ID",trigger:"blur"}],environment:[{required:!0,message:"请选择推送环境",trigger:"blur"}],types:[{required:!0,message:"请选择推送类型",trigger:"blur"}],languages:[{required:!0,message:"请选择语言",trigger:"blur"}]}}},methods:{onSubmit(t){this.$refs[t].validate(t=>{if(!t)return console.log("error submit"),!1;console.log("语言："+this.form.languages),console.log("pushID："+this.form.pushID),console.log("APP："+this.form.types[0]),console.log("推送类型："+this.form.types[1]),console.log("environment："+this.form.environment),this.$ajax.post("/bishijie/push",{id:this.form.pushID,service:this.form.environment,system:this.form.types[0],module:this.form.types[1],lang:this.form.languages,rid:""}).then(t=>{"0"==t.data.code?null==t.data.data||t.data.data[0]?this.$message.success("push成功！"):this.$message.error(t.data.data[1]):this.$message.error(t.data.msg)}).catch((function(t){console.log(t)}))})},resetForm(t){this.$refs[t].resetFields()},changeLang(t){this.languages=[],this.form.languages="";var e=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"}],a=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"},{key:"en_go",value:"English"},{key:"ko_kr",value:"한글"}],n=this.form.types[0].toLowerCase();"bishijie"==n?this.languages=e:"coinness"==n&&(this.languages=a)}}},s=r,o=(a("cd97"),a("2877")),l=Object(o["a"])(s,n,i,!1,null,"6d8efc95",null);l.exports},cd97:function(t,e,a){"use strict";var n=a("41d3"),i=a.n(n);i.a}}]);