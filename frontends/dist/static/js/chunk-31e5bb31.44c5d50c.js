(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-31e5bb31"],{"2d92":function(t,a,e){"use strict";e.d(a,"ub",(function(){return s})),e.d(a,"U",(function(){return o})),e.d(a,"v",(function(){return r})),e.d(a,"H",(function(){return d})),e.d(a,"M",(function(){return p})),e.d(a,"xb",(function(){return h})),e.d(a,"k",(function(){return c})),e.d(a,"V",(function(){return u})),e.d(a,"T",(function(){return l})),e.d(a,"u",(function(){return m})),e.d(a,"G",(function(){return b})),e.d(a,"L",(function(){return g})),e.d(a,"wb",(function(){return f})),e.d(a,"j",(function(){return j})),e.d(a,"W",(function(){return y})),e.d(a,"X",(function(){return _})),e.d(a,"S",(function(){return v})),e.d(a,"t",(function(){return w})),e.d(a,"i",(function(){return B})),e.d(a,"Y",(function(){return L})),e.d(a,"ab",(function(){return x})),e.d(a,"Z",(function(){return C})),e.d(a,"g",(function(){return D})),e.d(a,"Q",(function(){return O})),e.d(a,"h",(function(){return k})),e.d(a,"vb",(function(){return A})),e.d(a,"s",(function(){return S})),e.d(a,"K",(function(){return z})),e.d(a,"qb",(function(){return I})),e.d(a,"yb",(function(){return N})),e.d(a,"l",(function(){return T})),e.d(a,"N",(function(){return P})),e.d(a,"A",(function(){return E})),e.d(a,"nb",(function(){return G})),e.d(a,"pb",(function(){return Y})),e.d(a,"ob",(function(){return H})),e.d(a,"q",(function(){return J})),e.d(a,"Cb",(function(){return M})),e.d(a,"C",(function(){return U})),e.d(a,"d",(function(){return V})),e.d(a,"sb",(function(){return X})),e.d(a,"m",(function(){return Z})),e.d(a,"zb",(function(){return q})),e.d(a,"w",(function(){return F})),e.d(a,"e",(function(){return K})),e.d(a,"rb",(function(){return Q})),e.d(a,"bb",(function(){return R})),e.d(a,"tb",(function(){return W})),e.d(a,"x",(function(){return $})),e.d(a,"Ab",(function(){return tt})),e.d(a,"o",(function(){return at})),e.d(a,"F",(function(){return et})),e.d(a,"eb",(function(){return it})),e.d(a,"E",(function(){return nt})),e.d(a,"y",(function(){return st})),e.d(a,"mb",(function(){return ot})),e.d(a,"lb",(function(){return rt})),e.d(a,"ib",(function(){return dt})),e.d(a,"B",(function(){return pt})),e.d(a,"fb",(function(){return ht})),e.d(a,"gb",(function(){return ct})),e.d(a,"p",(function(){return ut})),e.d(a,"Bb",(function(){return lt})),e.d(a,"z",(function(){return mt})),e.d(a,"r",(function(){return bt})),e.d(a,"P",(function(){return gt})),e.d(a,"J",(function(){return ft})),e.d(a,"hb",(function(){return jt})),e.d(a,"jb",(function(){return yt})),e.d(a,"kb",(function(){return _t})),e.d(a,"db",(function(){return vt})),e.d(a,"cb",(function(){return wt})),e.d(a,"n",(function(){return Bt})),e.d(a,"f",(function(){return Lt})),e.d(a,"c",(function(){return xt})),e.d(a,"b",(function(){return Ct})),e.d(a,"a",(function(){return Dt})),e.d(a,"D",(function(){return Ot})),e.d(a,"R",(function(){return kt}));var i=e("bc3a"),n=e.n(i);const s="http://192.168.1.121:9000",o=(t,a)=>n.a.get(s+"/api/project/project_list",{params:a,headers:t}).then(t=>t.data),r=(t,a)=>n.a.post(s+"/api/project/del_project",a,{headers:t}).then(t=>t.data),d=(t,a)=>n.a.post(s+"/api/project/disable_project",a,{headers:t}).then(t=>t.data),p=(t,a)=>n.a.post(s+"/api/project/enable_project",a,{headers:t}).then(t=>t.data),h=(t,a)=>n.a.post(s+"/api/project/update_project",a,{headers:t}).then(t=>t.data),c=(t,a)=>n.a.post(s+"/api/project/add_project",a,{headers:t}).then(t=>t.data),u=(t,a)=>n.a.get(s+"/api/title/project_info",{params:a,headers:t}).then(t=>t.data),l=(t,a)=>n.a.get(s+"/api/global/host_total",{params:a,headers:t}).then(t=>t.data),m=(t,a)=>n.a.post(s+"/api/global/del_host",a,{headers:t}).then(t=>t.data),b=(t,a)=>n.a.post(s+"/api/global/disable_host",a,{headers:t}).then(t=>t.data),g=(t,a)=>n.a.post(s+"/api/global/enable_host",a,{headers:t}).then(t=>t.data),f=(t,a)=>n.a.post(s+"/api/global/update_host",a,{headers:t}).then(t=>t.data),j=(t,a)=>n.a.post(s+"/api/global/add_host",a,{headers:t}).then(t=>t.data),y=(t,a)=>n.a.get(s+"/api/dynamic/dynamic",{params:a,headers:t}).then(t=>t.data),_=(t,a)=>n.a.get(s+"/api/member/project_member",{params:a,headers:t}).then(t=>t.data),v=(t,a)=>n.a.get(s+"/api/member/get_email",{params:a,headers:t}).then(t=>t.data),w=(t,a)=>n.a.post(s+"/api/member/del_email",a,{headers:t}).then(t=>t.data),B=(t,a)=>n.a.post(s+"/api/member/email_config",a,{headers:t}).then(t=>t.data),L=(t,a)=>n.a.get(s+"/api/report/auto_test_report",{params:a,headers:t}).then(t=>t.data),x=(t,a)=>n.a.get(s+"/api/report/test_time",{params:a,headers:t}).then(t=>t.data),C=(t,a)=>n.a.get(s+"/api/report/lately_ten",{params:a,headers:t}).then(t=>t.data),D=(t,a)=>n.a.post(s+"/api/api/add_api",a,{headers:t}).then(t=>t.data),O=(t,a)=>n.a.get(s+"/api/api/group",{params:a,headers:t}).then(t=>t.data),k=(t,a)=>n.a.post(s+"/api/api/add_group",a,{headers:t}).then(t=>t.data),A=(t,a)=>n.a.post(s+"/api/api/update_name_group",a,{headers:t}).then(t=>t.data),S=(t,a)=>n.a.post(s+"/api/api/del_group",a,{headers:t}).then(t=>t.data),z=(t,a)=>n.a.post(s+"/api/download",a,{headers:t}).then(t=>t.data),I=(t,a)=>n.a.post(s+"/api/user/login",a,t).then(t=>t.data),N=(t,a)=>n.a.post(s+"/api/risk/update",a,{headers:t}).then(t=>t.data),T=(t,a)=>n.a.post(s+"/api/risk/add",a,{headers:t}).then(t=>t.data),P=(t,a)=>n.a.post(s+"/api/risk/add",a,{headers:t}).then(t=>t.data),E=(t,a)=>n.a.post(s+"/api/risk/del",a,t).then(t=>t.data),G=(t,a)=>n.a.get(s+"/api/risk ",{params:a},t).then(t=>t.data),Y=(t,a)=>n.a.get(s+"/api/todo ",{params:a},t).then(t=>t.data),H=(t,a)=>n.a.get(s+"/api/report ",{params:a},t).then(t=>t.data),J=(t,a)=>n.a.post(s+"/api/addreport",a,t).then(t=>t.data),M=(t,a)=>n.a.post(s+"/api/updatereport",a,t).then(t=>t.data),U=(t,a)=>n.a.post(s+"/api/delreport",a,t).then(t=>t.data),V=(t,a)=>n.a.post(s+"/api/send",a,t).then(t=>t.data),X=(t,a)=>n.a.get(s+"/api/stress/list",{params:a},{headers:t}).then(t=>t.data),Z=(t,a)=>n.a.post(s+"/api/stress/add",a,t).then(t=>t.data),q=(t,a)=>n.a.post(s+"/api/stress/update",a,t).then(t=>t.data),F=(t,a)=>n.a.post(s+"/api/stress/del",a,t).then(t=>t.data),K=(t,a)=>n.a.get(s+"/api/stress/Detail ",{params:a},t).then(t=>t.data),Q=(t,a)=>n.a.post(s+"/api/stress/tool",a,t).then(t=>t.data),R=(t,a)=>n.a.get(s+"/api/stress/version",{params:a},{headers:t}).then(t=>t.data),W=(t,a)=>n.a.post(s+"/api/stress/save",a,t).then(t=>t.data),$=(t,a)=>n.a.post(s+"/api/tool/del_dicomData",a,t).then(t=>t.data),tt=(t,a)=>n.a.post(s+"/api/dicom/update",a,t).then(t=>t.data),at=(t,a)=>n.a.post(s+"/api/tool/add_dicomData",a,t).then(t=>t.data),et=(t,a)=>n.a.post(s+"/api/tool/dicomdetail",a,t).then(t=>t.data),it=(t,a)=>n.a.get(s+"/api/tool/dicomData",{params:a},{headers:t}).then(t=>t.data),nt=(t,a)=>n.a.post(s+"/api/tool/dicomcsv",a,t).then(t=>t.data),st=(t,a)=>n.a.post(s+"/api/tool/delreport",a,t).then(t=>t.data),ot=(t,a)=>n.a.get(s+"/api/stress/version",{params:a},{headers:t}).then(t=>t.data),rt=(t,a)=>n.a.post(s+"/api/stress/result",a,t).then(t=>t.data),dt=(t,a)=>n.a.post(s+"/api/stress/figure",a,t).then(t=>t.data),pt=(t,a)=>n.a.post(s+"/api/tool/delete_patients",a,t).then(t=>t.data),ht=(t,a)=>n.a.get(s+"/api/tool/getduration",{params:a},{headers:t}).then(t=>t.data),ct=(t,a)=>n.a.get(s+"/api/tool/durationData",{params:a},{headers:t}).then(t=>t.data),ut=(t,a)=>n.a.post(s+"/api/tool/add_duration",a,t).then(t=>t.data),lt=(t,a)=>n.a.post(s+"/api/tool/update_duration",a,t).then(t=>t.data),mt=(t,a)=>n.a.post(s+"/api/tool/del_duration",a,t).then(t=>t.data),bt=(t,a)=>n.a.post(s+"/api/tool/anonymization",a,t).then(t=>t.data),gt=(t,a)=>n.a.post(s+"/api/tool/enable_duration",a,t).then(t=>t.data),ft=(t,a)=>n.a.post(s+"/api/tool/disable_duration",a,t).then(t=>t.data),jt=(t,a)=>n.a.get(s+"/api/tool/duration_verify",{params:a},{headers:t}).then(t=>t.data),yt=(t,a)=>n.a.get(s+"/api/tool/somkerecord",{params:a},{headers:t}).then(t=>t.data),_t=(t,a)=>n.a.post(s+"/api/tool/somke",a,t).then(t=>t.data),vt=(t,a)=>n.a.post(s+"/api/tool/dicomSend",a,t).then(t=>t.data),wt=(t,a)=>n.a.get(s+"/api/base/getdata",{params:a},{headers:t}).then(t=>t.data),Bt=(t,a)=>n.a.post(s+"/api/base/addData",a,t).then(t=>t.data),Lt=(t,a)=>n.a.post(s+"/api/base/updateData",a,t).then(t=>t.data),xt=(t,a)=>n.a.post(s+"/api/base/enablebase",a,t).then(t=>t.data),Ct=(t,a)=>n.a.post(s+"/api/base/disablebase",a,t).then(t=>t.data),Dt=(t,a)=>n.a.post(s+"/api/base/delbasedata",a,t).then(t=>t.data),Ot=(t,a)=>n.a.get(s+"/api/base/dicom",{params:a},{headers:t}).then(t=>t.data),kt=(t,a)=>n.a.get(s+"/api/dictionary/list",{params:a},{headers:t}).then(t=>t.data)},"48d1":function(t,a,e){},7159:function(t,a,e){t.exports=e.p+"static/img/img.132d6025.jpg"},e2ad:function(t,a,e){"use strict";e.r(a);var i=function(){var t=this,a=t.$createElement,i=t._self._c||a;return i("div",[i("el-row",{attrs:{gutter:20}},[i("el-col",{attrs:{span:9}},[i("el-card",{staticClass:"mgb20",staticStyle:{height:"252px"},attrs:{shadow:"hover"}},[i("div",{staticClass:"user-info"},[i("img",{staticClass:"user-avator",attrs:{src:e("7159"),alt:""}}),i("div",{staticClass:"user-info-cont"},[i("div",{staticClass:"user-info-name"},[t._v(t._s(t.name))]),i("div",[t._v(t._s(t.role))])])]),i("div",{staticClass:"user-info-list"},[t._v("上次登录时间："),i("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(t._f("dateformat")(t.date_joined,"YYYY-MM-DD HH:mm:ss")))])]),i("div",{staticClass:"user-info-list"},[t._v("上次登录地点："),i("span",[t._v("北京")])])]),i("el-card",{staticStyle:{height:"350px"},attrs:{shadow:"hover"}},[i("el-row",{attrs:{gutter:20}},[i("el-col",{attrs:{span:12}},[i("el-card",{attrs:{shadow:"hover"}},[i("div",{staticClass:"mybar",staticStyle:{width:"250px",height:"310px",margin:"0 auto"},attrs:{id:"bishijieBar"}})])],1)],1)],1)],1),i("el-col",{attrs:{span:15}},[i("el-row",{staticClass:"mgb20",attrs:{gutter:20}},[i("el-col",{attrs:{span:8}},[i("el-card",{attrs:{shadow:"hover","body-style":{padding:"0px"}}},[i("div",{staticClass:"grid-content grid-con-1"},[i("i",{staticClass:"el-icon-lx-read grid-con-icon"}),i("div",{staticClass:"grid-cont-right"},[i("div",[t._v("待处理Bug")]),i("div",{staticClass:"grid-num"},[t._v(t._s(t.bug))])])])])],1),i("el-col",{attrs:{span:8}},[i("el-card",{attrs:{shadow:"hover","body-style":{padding:"0px"}}},[i("div",{staticClass:"grid-content grid-con-2"},[i("i",{staticClass:"el-icon-lx-text grid-con-icon"}),i("div",{staticClass:"grid-cont-right"},[i("div",{staticClass:"grid-num"},[t._v(t._s(t.todo))]),i("div",[t._v("待处理任务")])])])])],1),i("el-col",{attrs:{span:8}},[i("el-card",{attrs:{shadow:"hover","body-style":{padding:"0px"}}},[i("div",{staticClass:"grid-content grid-con-3"},[i("i",{staticClass:"el-icon-lx-warn grid-con-icon"}),i("div",{staticClass:"grid-cont-right"},[i("div",{staticClass:"grid-num"},[t._v(t._s(t.online))]),i("div",[t._v("待处理线上问题")])])])])],1)],1),i("el-card",{attrs:{shadow:"hover"}},[i("div",{staticClass:"myLine",staticStyle:{width:"100%",height:"350px",margin:"0 auto"},attrs:{id:"bishijieLine"}})])],1)],1)],1)},n=[],s=e("313e"),o=e.n(s),r=e("2d92"),d={name:"dashboard",date_joined:"2019-06-06",data(){return{name:localStorage.getItem("ms_username"),date_joined:localStorage.getItem("date_joined"),bishijieBar:{},bishijieLine:{},coinnessBar:{},coinnessLine:{},bishijieBarData:[],bishijieLineData:[],coinnessBarData:[],coinnessLineData:[],twoData:[],bishijieBaroption:{backgroundColor:"#2c343c",title:{text:"Boimind-Bug解决数量状态图",left:"center",top:20,textStyle:{color:"#ccc"}},tooltip:{trigger:"item",formatter:"{a} <br/>{b} : {c} ({d}%)"},series:[{name:"Bug状态",type:"pie",radius:"55%",center:["50%","60%"],data:[],itemStyle:{emphasis:{shadowBlur:10,shadowOffsetX:0,shadowColor:"rgba(0, 0, 0, 0.5)"},normal:{label:{show:function(t){if(0==t)return!1}(),formatter:"{b} : {c} ({d}%)"},labelLine:{show:function(t){if(0==t)return!1}()}}}}]},coinnessBaroption:{backgroundColor:"#ccc",title:{text:"CoinNess-Bug解决数量状态图",left:"center",top:20,textStyle:{color:"#ccc"}},tooltip:{trigger:"item",formatter:"{a} <br/>{b} : {c} ({d}%)"},series:[{name:"Bug状态",type:"pie",radius:"55%",center:["50%","60%"],data:[],itemStyle:{emphasis:{shadowBlur:10,shadowOffsetX:0,shadowColor:"rgba(0, 0, 0, 0.5)"},normal:{label:{show:function(t){if(0==t)return!1}(),formatter:"{b} : {c} ({d}%)"},labelLine:{show:function(t){if(0==t)return!1}()}}}}]},bishijieLineoption:{title:{text:"Boimind-创建与解决问题对比图"},tooltip:{trigger:"axis",padding:25},legend:{data:["创建问题","解决问题"],padding:25},toolbox:{show:!0,feature:{dataZoom:{yAxisIndex:"none"},dataView:{readOnly:!0},magicType:{type:["line","bar"]},restore:{},saveAsImage:{}}},xAxis:{type:"category",boundaryGap:!1,data:[]},yAxis:{type:"value",axisLabel:{formatter:"{value} 个"}},series:[{name:"创建问题",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"解决问题",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}}]},coinnessLineoption:{title:{text:"CoinNess-创建与解决问题对比图"},tooltip:{trigger:"axis",padding:25},legend:{data:["创建问题","解决问题"],padding:25},toolbox:{show:!0,feature:{dataZoom:{yAxisIndex:"none"},dataView:{readOnly:!0},magicType:{type:["line","bar"]},restore:{},saveAsImage:{}}},xAxis:{type:"category",boundaryGap:!1,data:[]},yAxis:{type:"value",axisLabel:{formatter:"{value} 个"}},series:[{name:"创建问题",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}},{name:"解决问题",type:"line",data:[],markPoint:{data:[{type:"max",name:"最大值"},{type:"min",name:"最小值"}]}}]}}},components:{},mounted(){this.drawbishijieBar(),this.drawCoinNessBar(),this.drawbishijieLine(),this.drawCoinNessLine()},computed:{role(){return"admin"===this.name?"超级管理员":"普通用户"}},created(){this.getbishijieData(),this.getCoinnessData(),this.getData()},watch:{bishijieBaroption:{handler(t,a){this.bishijieBar?t?this.bishijieBar.setOption(t):this.bishijieBar.setOption(a):this.drawbishijieBar()},deep:!0},bishijieLineoption:{handler(t,a){this.bishijieBar?t?this.bishijieLine.setOption(t):this.bishijieLine.setOption(a):this.drawbishijieLine()},deep:!0},coinnessBaroption:{handler(t,a){this.coinnessBar?t?this.coinnessBar.setOption(t):this.coinnessBar.setOption(a):this.drawCoinNessBar()},deep:!0},coinnessLineoption:{handler(t,a){this.coinnessBar?t?this.coinnessLine.setOption(t):this.coinnessLine.setOption(a):this.drawCoinNessLine()},deep:!0}},todoData:[],methods:{getData(){let t={user:"yinhang"},a={"Content-Type":"application/x-www-form-urlencoded"};Object(r["pb"])(a,t).then(t=>{let{code:a,msg:e,data:i}=t;0!=t.length?(this.totalData=i.total,this.bug=this.totalData[0],this.todo=this.totalData[1],this.online=this.totalData[2],console.log(this.bug)):this.todoData=null})},getbishijieData(){let t={project:"BUG",service:"Boimind-APP-缺陷",sprint_version:"",starttime:"",days:7,status:"",component:"",priority:""},a={"Content-Type":"application/json"};Object(r["ib"])(a,t).then(t=>{let{code:a,msg:e,data:i}=t;this.bishijieLineData=i.figure_list,this.bishijieLineoption.xAxis.data=this.bishijieLineData[0],this.bishijieLineoption.series[0].data=this.bishijieLineData[1],this.bishijieLineoption.series[1].data=this.bishijieLineData[2],this.bishijieBarData=i.solution_state.sort((function(t,a){return t.value-a.value})),this.bishijieBaroption.series[0].data=this.bishijieBarData})},getCoinnessData(){let t={project:"BUG",service:"CoinNess-APP-缺陷",sprint_version:"",starttime:"",days:7,status:"",component:"",priority:""},a={"Content-Type":"application/json"};Object(r["ib"])(a,t).then(t=>{let{code:a,msg:e,data:i}=t;this.coinnessLineData=i.figure_list,this.coinnessLineoption.xAxis.data=this.coinnessLineData[0],this.coinnessLineoption.series[0].data=this.coinnessLineData[1],this.coinnessLineoption.series[1].data=this.coinnessLineData[2],this.coinnessBarData=i.solution_state.sort((function(t,a){return t.value-a.value})),this.coinnessBaroption.series[0].data=this.coinnessBarData})},drawbishijieBar(){this.bishijieBar=o.a.init(document.getElementById("bishijieBar")),this.bishijieBar.setOption(this.bishijieBaroption,!0),setTimeout(()=>{window.onresize=bishijieBar.resize},200)},drawCoinNessBar(){this.coinnessBar=o.a.init(document.getElementById("coinnessBar")),this.coinnessBar.setOption(this.coinnessBaroption,!0),setTimeout(()=>{window.onresize=coinnessBar.resize},200)},drawbishijieLine(){this.bishijieLine=o.a.init(document.getElementById("bishijieLine")),this.bishijieLine.setOption(this.bishijieLineoption),setTimeout(()=>{window.onresize=bishijieLine.resize},200)},drawCoinNessLine(){this.coinnessLine=o.a.init(document.getElementById("coinnessLine")),this.coinnessLine.setOption(this.coinnessLineoption),setTimeout(()=>{window.onresize=coinnessLine.resize},200)}}},p=d,h=(e("f5c4"),e("2877")),c=Object(h["a"])(p,i,n,!1,null,"1d691bae",null);a["default"]=c.exports},f5c4:function(t,a,e){"use strict";var i=e("48d1"),n=e.n(i);n.a}}]);