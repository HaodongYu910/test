(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-26b31d64"],{"2d92":function(t,e,a){"use strict";a.d(e,"Z",(function(){return o})),a.d(e,"E",(function(){return n})),a.d(e,"n",(function(){return i})),a.d(e,"u",(function(){return l})),a.d(e,"y",(function(){return d})),a.d(e,"cb",(function(){return p})),a.d(e,"f",(function(){return c})),a.d(e,"F",(function(){return u})),a.d(e,"D",(function(){return m})),a.d(e,"m",(function(){return h})),a.d(e,"t",(function(){return f})),a.d(e,"x",(function(){return g})),a.d(e,"bb",(function(){return b})),a.d(e,"e",(function(){return y})),a.d(e,"G",(function(){return v})),a.d(e,"H",(function(){return _})),a.d(e,"C",(function(){return k})),a.d(e,"l",(function(){return F})),a.d(e,"d",(function(){return w})),a.d(e,"I",(function(){return S})),a.d(e,"K",(function(){return x})),a.d(e,"J",(function(){return $})),a.d(e,"b",(function(){return O})),a.d(e,"B",(function(){return j})),a.d(e,"c",(function(){return z})),a.d(e,"ab",(function(){return T})),a.d(e,"k",(function(){return C})),a.d(e,"w",(function(){return D})),a.d(e,"X",(function(){return L})),a.d(e,"db",(function(){return N})),a.d(e,"g",(function(){return J})),a.d(e,"z",(function(){return A})),a.d(e,"p",(function(){return V})),a.d(e,"U",(function(){return q})),a.d(e,"T",(function(){return I})),a.d(e,"W",(function(){return R})),a.d(e,"V",(function(){return E})),a.d(e,"i",(function(){return B})),a.d(e,"fb",(function(){return M})),a.d(e,"r",(function(){return P})),a.d(e,"a",(function(){return G})),a.d(e,"Y",(function(){return H})),a.d(e,"L",(function(){return K})),a.d(e,"s",(function(){return Q})),a.d(e,"gb",(function(){return U})),a.d(e,"S",(function(){return W})),a.d(e,"Q",(function(){return X})),a.d(e,"R",(function(){return Y})),a.d(e,"q",(function(){return Z})),a.d(e,"N",(function(){return tt})),a.d(e,"O",(function(){return et})),a.d(e,"h",(function(){return at})),a.d(e,"eb",(function(){return rt})),a.d(e,"o",(function(){return st})),a.d(e,"A",(function(){return ot})),a.d(e,"v",(function(){return nt})),a.d(e,"P",(function(){return it})),a.d(e,"M",(function(){return lt}));var r=a("bc3a"),s=a.n(r);const o="http://192.168.2.38:9000",n=(t,e)=>s.a.get(o+"/api/project/project_list",{params:e,headers:t}).then(t=>t.data),i=(t,e)=>s.a.post(o+"/api/project/del_project",e,{headers:t}).then(t=>t.data),l=(t,e)=>s.a.post(o+"/api/project/disable_project",e,{headers:t}).then(t=>t.data),d=(t,e)=>s.a.post(o+"/api/project/enable_project",e,{headers:t}).then(t=>t.data),p=(t,e)=>s.a.post(o+"/api/project/update_project",e,{headers:t}).then(t=>t.data),c=(t,e)=>s.a.post(o+"/api/project/add_project",e,{headers:t}).then(t=>t.data),u=(t,e)=>s.a.get(o+"/api/title/project_info",{params:e,headers:t}).then(t=>t.data),m=(t,e)=>s.a.get(o+"/api/global/host_total",{params:e,headers:t}).then(t=>t.data),h=(t,e)=>s.a.post(o+"/api/global/del_host",e,{headers:t}).then(t=>t.data),f=(t,e)=>s.a.post(o+"/api/global/disable_host",e,{headers:t}).then(t=>t.data),g=(t,e)=>s.a.post(o+"/api/global/enable_host",e,{headers:t}).then(t=>t.data),b=(t,e)=>s.a.post(o+"/api/global/update_host",e,{headers:t}).then(t=>t.data),y=(t,e)=>s.a.post(o+"/api/global/add_host",e,{headers:t}).then(t=>t.data),v=(t,e)=>s.a.get(o+"/api/dynamic/dynamic",{params:e,headers:t}).then(t=>t.data),_=(t,e)=>s.a.get(o+"/api/member/project_member",{params:e,headers:t}).then(t=>t.data),k=(t,e)=>s.a.get(o+"/api/member/get_email",{params:e,headers:t}).then(t=>t.data),F=(t,e)=>s.a.post(o+"/api/member/del_email",e,{headers:t}).then(t=>t.data),w=(t,e)=>s.a.post(o+"/api/member/email_config",e,{headers:t}).then(t=>t.data),S=(t,e)=>s.a.get(o+"/api/report/auto_test_report",{params:e,headers:t}).then(t=>t.data),x=(t,e)=>s.a.get(o+"/api/report/test_time",{params:e,headers:t}).then(t=>t.data),$=(t,e)=>s.a.get(o+"/api/report/lately_ten",{params:e,headers:t}).then(t=>t.data),O=(t,e)=>s.a.post(o+"/api/api/add_api",e,{headers:t}).then(t=>t.data),j=(t,e)=>s.a.get(o+"/api/api/group",{params:e,headers:t}).then(t=>t.data),z=(t,e)=>s.a.post(o+"/api/api/add_group",e,{headers:t}).then(t=>t.data),T=(t,e)=>s.a.post(o+"/api/api/update_name_group",e,{headers:t}).then(t=>t.data),C=(t,e)=>s.a.post(o+"/api/api/del_group",e,{headers:t}).then(t=>t.data),D=(t,e)=>s.a.post(o+"/api/download",e,{headers:t}).then(t=>t.data),L=(t,e)=>s.a.post(o+"/api/user/login",e,t).then(t=>t.data),N=(t,e)=>s.a.post(o+"/api/risk/update",e,{headers:t}).then(t=>t.data),J=(t,e)=>s.a.post(o+"/api/risk/add",e,{headers:t}).then(t=>t.data),A=(t,e)=>s.a.post(o+"/api/risk/add",e,{headers:t}).then(t=>t.data),V=(t,e)=>s.a.post(o+"/api/risk/del",e,t).then(t=>t.data),q=(t,e)=>s.a.get(o+"/api/risk ",{params:e},t).then(t=>t.data),I=(t,e)=>s.a.post(o+"/api/jira/figure ",e,t).then(t=>t.data),R=(t,e)=>s.a.get(o+"/api/todo ",{params:e},t).then(t=>t.data),E=(t,e)=>s.a.get(o+"/api/report ",{params:e},t).then(t=>t.data),B=(t,e)=>s.a.post(o+"/api/addreport",e,t).then(t=>t.data),M=(t,e)=>s.a.post(o+"/api/updatereport",e,t).then(t=>t.data),P=(t,e)=>s.a.post(o+"/api/delreport",e,t).then(t=>t.data),G=(t,e)=>s.a.post(o+"/api/send",e,t).then(t=>t.data),H=(t,e)=>s.a.post(o+"/api/tool/stresstool",e,t).then(t=>t.data),K=(t,e)=>s.a.get(o+"/api/tool/version",{params:e},{headers:t}).then(t=>t.data),Q=(t,e)=>s.a.post(o+"/api/tool/delete_stressdata",e,t).then(t=>t.data),U=(t,e)=>s.a.post(o+"/api/tool/update_stressdata",e,t).then(t=>t.data),W=(t,e)=>s.a.get(o+"/api/tool/stressversion",{params:e},{headers:t}).then(t=>t.data),X=(t,e)=>s.a.get(o+"/api/tool/stressdata",{params:e},{headers:t}).then(t=>t.data),Y=(t,e)=>s.a.post(o+"/api/tool/stressresult",e,t).then(t=>t.data),Z=(t,e)=>s.a.post(o+"/api/tool/delete_patients",e,t).then(t=>t.data),tt=(t,e)=>s.a.get(o+"/api/tool/getduration",{params:e},{headers:t}).then(t=>t.data),et=(t,e)=>s.a.get(o+"/api/tool/durationData",{params:e},{headers:t}).then(t=>t.data),at=(t,e)=>s.a.post(o+"/api/tool/add_duration",e,t).then(t=>t.data),rt=(t,e)=>s.a.post(o+"/api/tool/update_duration",e,t).then(t=>t.data),st=(t,e)=>s.a.post(o+"/api/tool/del_duration",e,t).then(t=>t.data),ot=(t,e)=>s.a.post(o+"/api/tool/enable_duration",e,t).then(t=>t.data),nt=(t,e)=>s.a.post(o+"/api/tool/disable_duration",e,t).then(t=>t.data),it=(t,e)=>s.a.get(o+"/api/tool/duration_verify",{params:e},{headers:t}).then(t=>t.data),lt=(t,e)=>s.a.get(o+"/api/base/getdata",{params:e},{headers:t}).then(t=>t.data)},3155:function(t,e,a){"use strict";a.r(e);var r=function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("div",{staticClass:"app-container"},[r("div",{staticClass:"filter-container"},[r("el-col",{staticClass:"toolbar",staticStyle:{"padding-bottom":"0px"},attrs:{span:100}},[r("aside",[r("a",{attrs:{href:"http://192.168.2.38:9000/",target:"_blank"}},[t._v("删除dicom数据 ")])]),r("el-form",{ref:"form",attrs:{model:t.form,"status-icon":"",rules:t.rules,"label-width":"100px"}},[r("el-row",[r("el-col",{attrs:{span:5}},[r("el-form-item",{attrs:{label:"测试服务器",prop:"server_ip"}},[r("el-select",{attrs:{placeholder:"请选择"},nativeOn:{click:function(e){return t.gethost()}},model:{value:t.form.server_ip,callback:function(e){t.$set(t.form,"server_ip",e)},expression:"form.server_ip"}},t._l(t.tags,(function(t,e){return r("el-option",{key:t.host,attrs:{label:t.name,value:t.host}})})),1)],1)],1),r("el-col",{attrs:{span:5}},[r("el-form-item",{attrs:{label:"删除数据",prop:"deldata"}},[r("el-input",{attrs:{id:"deldata",placeholder:"删除数据"},model:{value:t.form.deldata,callback:function(e){t.$set(t.form,"deldata",e)},expression:"form.deldata"}})],1)],1),r("el-col",{attrs:{span:5}},[r("el-form-item",{attrs:{label:"数据类型",prop:"testtype"}},[r("el-select",{attrs:{placeholder:"请选择"},model:{value:t.form.testtype,callback:function(e){t.$set(t.form,"testtype",e)},expression:"form.testtype"}},[r("el-option",{key:"",attrs:{label:"患者姓名",value:"CTA"}}),r("el-option",{key:"CTP",attrs:{label:"患者编号",value:"CTP"}}),r("el-option",{key:"Lung",attrs:{label:"预测结果",value:"Lung"}}),r("el-option",{key:"MRA",attrs:{label:"检查类型",value:"MRA"}})],1)],1)],1),r("el-col",{attrs:{span:4}},[r("el-form-item",{attrs:{label:"模糊搜索",prop:"fuzzy"}},[r("el-select",{attrs:{clearable:"",placeholder:"请选择"},model:{value:t.form.fuzzy,callback:function(e){t.$set(t.form,"fuzzy",e)},expression:"form.fuzzy"}},[r("el-option",{key:"True",attrs:{label:"是",value:"True"}}),r("el-option",{key:"False",attrs:{label:"否",value:"False"}})],1)],1)],1),r("el-col",{attrs:{span:4}},[r("el-form-item",[r("el-button",{attrs:{type:"primary"},on:{click:function(e){return t.deldicom("form")}}},[t._v("删除")])],1)],1)],1)],1),r("div",[r("el-table",{staticStyle:{width:"50%"},attrs:{data:t.tableData}},[r("el-table-column",{attrs:{label:"结果显示",width:"180"},scopedSlots:t._u([{key:"default",fn:function(e){return[r("el-popover",{attrs:{trigger:"hover",placement:"top"}},[r("p",[t._v("标签: "+t._s(e.row.name))]),r("div",{staticClass:"name-wrapper",attrs:{slot:"reference"},slot:"reference"},[r("el-tag",{attrs:{size:"medium"}},[t._v(t._s(e.row.name))])],1)])]}}])}),r("el-table-column",{attrs:{fixed:"right",label:""},scopedSlots:t._u([{key:"default",fn:function(e){return[r("el-button",{attrs:{size:"mini",type:"danger"},on:{click:function(a){return t.deleteTag(e.$index,e.row)}}},[t._v("开始/关闭 ")])]}}])})],1)],1),r("aside",[r("a",{attrs:{href:"http://192.168.2.38:9000/",target:"_blank"}},[t._v("匿名发送dicom数据 ")])]),r("el-col",{staticClass:"toolbar",staticStyle:{"padding-bottom":"0px"},attrs:{span:24}},[r("el-form",{attrs:{inline:!0,model:t.filters},nativeOn:{submit:function(t){t.preventDefault()}}},[r("el-form-item",[r("el-input",{attrs:{placeholder:"名称"},nativeOn:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.getDurationlist(e)}},model:{value:t.filters.name,callback:function(e){t.$set(t.filters,"name",e)},expression:"filters.name"}})],1),r("el-form-item",[r("el-button",{attrs:{type:"primary"},on:{click:t.getDurationlist}},[t._v("查询")])],1),r("el-form-item",[r("el-button",{attrs:{type:"primary"},on:{click:t.handleAdd}},[t._v("新增")])],1)],1)],1),r("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.listLoading,expression:"listLoading"}],staticStyle:{width:"200%"},attrs:{data:t.durationlist,"highlight-current-row":""},on:{"selection-change":t.selsChange}},[r("el-table-column",{attrs:{type:"selection","min-width":"5%"}}),r("el-table-column",{attrs:{prop:"type",label:"服务器","min-width":"20%"},scopedSlots:t._u([{key:"default",fn:function(e){return[e.row.server?r("router-link",{staticStyle:{"text-decoration":"none",color:"#000000"},attrs:{to:{name:"持续化数据详情",params:{id:e.row.id}}}},[r("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.server)+"："+t._s(e.row.port))])]):t._e()]}}])}),r("el-table-column",{attrs:{prop:"type",label:"匿名名称","min-width":"12%"},scopedSlots:t._u([{key:"default",fn:function(e){return[r("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.keyword))])]}}])}),r("el-table-column",{attrs:{prop:"type",label:"发送类型","min-width":"25%"},scopedSlots:t._u([{key:"default",fn:function(e){return[r("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.dicom))])]}}])}),r("el-table-column",{attrs:{label:"共计发送","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[r("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.all)+" 个")])]}}])}),r("el-table-column",{attrs:{label:"成功接收","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[r("span",{staticStyle:{"margin-left":"10px",color:"#00A600"}},[t._v(t._s(e.row.sent)+" 个")])]}}])}),r("el-table-column",{attrs:{label:"未确认","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[r("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.notsent)+" 个")])]}}])}),r("el-table-column",{attrs:{label:"AI预测成功","min-width":"12%"},scopedSlots:t._u([{key:"default",fn:function(e){return[r("span",{staticStyle:{"margin-left":"10px",color:"#02C874"}},[t._v(t._s(e.row.ai_true)+" 个")])]}}])}),r("el-table-column",{attrs:{label:"AI预测失败","min-width":"12%"},scopedSlots:t._u([{key:"default",fn:function(e){return[r("span",{staticStyle:{"margin-left":"10px",color:"#FF0000"}},[t._v(t._s(e.row.ai_false)+" 个")])]}}])}),r("el-table-column",{attrs:{label:"AI未预测","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(e){return[r("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.notai)+" 个")])]}}])}),r("el-table-column",{attrs:{prop:"sendstatus",label:"运行状态","min-width":"10%"},scopedSlots:t._u([{key:"default",fn:function(t){return[r("img",{directives:[{name:"show",rawName:"v-show",value:t.row.sendstatus,expression:"scope.row.sendstatus"}],staticStyle:{width:"18px",height:"18px","margin-right":"5px","margin-bottom":"5px"},attrs:{src:a("9742")}}),r("img",{directives:[{name:"show",rawName:"v-show",value:!t.row.sendstatus,expression:"!scope.row.sendstatus"}],staticStyle:{width:"15px",height:"15px","margin-right":"5px","margin-bottom":"5px"},attrs:{src:a("c392")}})]}}])}),r("el-table-column",{attrs:{label:"操作","min-width":"30%"},scopedSlots:t._u([{key:"default",fn:function(e){return[r("el-button",{attrs:{type:"info",size:"small"},on:{click:function(a){return t.handleChangeStatus(e.$index,e.row)}}},[t._v(" "+t._s(!1===e.row.sendstatus?"启用":"停用")+" ")]),r("el-button",{attrs:{type:"danger",size:"small"},on:{click:function(a){return t.showDetail(e.$index,e.row)}}},[t._v("数据")]),r("el-button",{attrs:{type:"warning",size:"small"},on:{click:function(a){return t.handleEdit(e.$index,e.row)}}},[t._v("修改 ")])]}}])})],1),r("el-col",{staticClass:"toolbar",attrs:{span:24}},[r("el-button",{attrs:{type:"danger",disabled:0===this.sels.length},on:{click:t.batchRemove}},[t._v("删除")]),r("el-pagination",{staticStyle:{float:"right"},attrs:{layout:"prev, pager, next","page-size":20,"page-count":t.total},on:{"current-change":t.handleCurrentChange}})],1),r("el-dialog",{staticStyle:{width:"75%",left:"12.5%"},attrs:{title:"修改",visible:t.editFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(e){t.editFormVisible=e}}},[r("el-form",{ref:"editForm",attrs:{model:t.editForm,"label-width":"80px",rules:t.editFormRules}},[r("el-row",[r("el-col",{attrs:{span:8}},[r("el-form-item",{attrs:{label:"数据类型",prop:"senddata"}},[r("el-select",{attrs:{multiple:"",placeholder:"请选择"},nativeOn:{click:function(e){return t.getBase()}},model:{value:t.editForm.senddata,callback:function(e){t.$set(t.editForm,"senddata",e)},expression:"editForm.senddata"}},t._l(t.tags,(function(t,e){return r("el-option",{key:t.remarks,attrs:{label:t.remarks,value:t.remarks}})})),1)],1)],1),r("el-col",{attrs:{span:6}},[r("el-form-item",{attrs:{label:"匿名名称",prop:"keyword"}},[r("el-input",{attrs:{id:"key_word",placeholder:"数据名称"},model:{value:t.editForm.keyword,callback:function(e){t.$set(t.editForm,"keyword",e)},expression:"editForm.keyword"}})],1)],1),r("el-col",{attrs:{span:6}},[r("el-form-item",{attrs:{label:"发送数据",prop:"keyword"}},[r("el-input",{attrs:{id:"sendcount",placeholder:"共/个"},model:{value:t.editForm.sendcount,callback:function(e){t.$set(t.editForm,"sendcount",e)},expression:"editForm.sendcount"}})],1)],1),r("el-col",{attrs:{span:6}},[r("el-form-item",{attrs:{label:"持续时间",prop:"loop_time"}},[r("el-input",{attrs:{id:"looptime",placeholder:"小时"},model:{value:t.editForm.loop_time,callback:function(e){t.$set(t.editForm,"loop_time",e)},expression:"editForm.loop_time"}})],1)],1),r("el-col",{attrs:{span:12}},[r("el-form-item",{attrs:{label:"定时器",prop:"timer"}},[r("el-input",{attrs:{id:"timer",placeholder:"30 09 * * *  表示每天9：30执行"},model:{value:t.editForm.timer,callback:function(e){t.$set(t.editForm,"timer",e)},expression:"editForm.timer"}})],1)],1),r("el-col",{attrs:{span:4}},[r("el-form-item",{attrs:{label:"",prop:"keyword"}},[r("el-button",{attrs:{type:"primary",loading:t.editLoading},nativeOn:{click:function(e){return t.editSubmit(e)}}},[t._v("保存")])],1)],1)],1)],1)],1),r("el-dialog",{staticStyle:{width:"75%",left:"12.5%"},attrs:{title:"新增",visible:t.addFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(e){t.addFormVisible=e}}},[r("el-form",{ref:"addForm",attrs:{model:t.addForm,"label-width":"80px",rules:t.addFormRules}},[r("el-form",{attrs:{inline:!0,model:t.filters},nativeOn:{submit:function(t){t.preventDefault()}}},[r("el-row",[r("el-col",{attrs:{span:5}},[r("el-form-item",{attrs:{label:"发送服务器",prop:"sendserver"}},[r("el-select",{attrs:{placeholder:"请选择"},nativeOn:{click:function(e){return t.gethost()}},model:{value:t.addForm.sendserver,callback:function(e){t.$set(t.addForm,"sendserver",e)},expression:"addForm.sendserver"}},t._l(t.tags,(function(t,e){return r("el-option",{key:t.host,attrs:{label:t.name,value:t.host}})})),1)],1)],1),r("el-col",{attrs:{span:3}},[r("el-form-item",{attrs:{label:"端口号",prop:"port"}},[r("el-input",{attrs:{id:"port",placeholder:""},model:{value:t.addForm.port,callback:function(e){t.$set(t.addForm,"port",e)},expression:"addForm.port"}})],1)],1),r("el-col",{attrs:{span:6}},[r("el-form-item",{attrs:{label:"数据类型",prop:"senddata"}},[r("el-select",{attrs:{multiple:"",placeholder:"请选择"},nativeOn:{click:function(e){return t.getBase()}},model:{value:t.addForm.senddata,callback:function(e){t.$set(t.addForm,"senddata",e)},expression:"addForm.senddata"}},t._l(t.tags,(function(t,e){return r("el-option",{key:t.remarks,attrs:{label:t.remarks,value:t.remarks}})})),1)],1)],1),r("el-col",{attrs:{span:4}},[r("el-form-item",{attrs:{label:"匿名名称",prop:"keyword"}},[r("el-input",{attrs:{id:"keyword",placeholder:"数据名称"},model:{value:t.addForm.keyword,callback:function(e){t.$set(t.addForm,"keyword",e)},expression:"addForm.keyword"}})],1)],1),r("el-col",{attrs:{span:3}},[r("el-form-item",{attrs:{label:"持续时间",prop:"loop_time"}},[r("el-input",{attrs:{id:"loop_time",placeholder:"小时"},model:{value:t.addForm.loop_time,callback:function(e){t.$set(t.addForm,"loop_time",e)},expression:"addForm.loop_time"}})],1)],1),r("el-col",{attrs:{span:3}},[r("el-form-item",{attrs:{label:"发送数量",prop:"count"}},[r("el-input",{attrs:{id:"sendcount",placeholder:"共/个"},model:{value:t.addForm.sendcount,callback:function(e){t.$set(t.addForm,"sendcount",e)},expression:"addForm.sendcount"}})],1)],1),r("el-col",{attrs:{span:10}},[r("el-form-item",{attrs:{label:"定时器",prop:"timer"}},[r("el-input",{attrs:{id:"timer",placeholder:"30 09 * * *  表示每天9：30执行"},model:{value:t.addForm.timer,callback:function(e){t.$set(t.addForm,"timer",e)},expression:"addForm.timer"}})],1)],1),r("el-col",{attrs:{span:4}},[r("el-form-item",{attrs:{label:"DDS服务",prop:"fuzzy"}},[r("el-select",{attrs:{clearable:"",placeholder:"请选择"},model:{value:t.addForm.dds,callback:function(e){t.$set(t.addForm,"dds",e)},expression:"addForm.dds"}},[r("el-option",{key:"True",attrs:{label:"是",value:"True"}}),r("el-option",{key:"False",attrs:{label:"否",value:"False"}})],1)],1)],1),r("el-col",{attrs:{span:4}},[r("el-form-item",{attrs:{label:"",prop:"save"}},[r("el-button",{attrs:{type:"primary"},on:{click:function(e){return t.addSubmit("form")}}},[t._v("保存")])],1)],1)],1)],1)],1)],1)],1)],1)])},s=[],o=a("2d92"),n={data(){return{form:{server_ip:"",fuzzy:"是",testtype:"患者编号",deldata:""},rules:{server_ip:[{required:!0,message:"请输入测试服务器",trigger:"blur"}],version:[{required:!0,message:"请输入版本号",trigger:"change"},{pattern:/^\d+\.\d+\.\d+$/,message:"请输入合法的版本号（x.x.x）"}]},filters:{diseases:""},durationlist:{},total:0,page:1,listLoading:!1,sels:[],editFormVisible:!1,editLoading:!1,editFormRules:{diseases:[{required:!0,message:"请输入名称",trigger:"blur"},{min:1,max:50,message:"长度在 1 到 50 个字符",trigger:"blur"}],type:[{required:!0,message:"请选择类型",trigger:"blur"}],description:[{required:!1,message:"请输入描述",trigger:"blur"},{max:1024,message:"不能超过1024个字符",trigger:"blur"}]},editForm:{loop_time:"",port:"4242"},addForm:{port:"4242"},addFormVisible:!1,addLoading:!1,addFormRules:{diseases:[{required:!0,message:"请输入名称",trigger:"blur"},{min:1,max:50,message:"长度在 1 到 50 个字符",trigger:"blur"}],type:[{required:!0,message:"请选择类型",trigger:"blur"}],version:[{required:!0,message:"请输入版本号",trigger:"change"},{pattern:/^\d+\.\d+\.\d+$/,message:"请输入合法的版本号（x.x.x）"}]},addForm:{diseases:"",version:"",type:"",description:""}}},mounted(){this.getDurationlist(),this.gethost(),this.durationVerifyData()},methods:{showDetail(t,e){this.$router.push({path:"/durationData",query:{id:e.id,name:e.server_ip}})},deldicom(t){this.tableData=null,this.$refs[t].validate(t=>{if(!t)return console.log("error submit"),!1;{const t={server_ip:this.form.server_ip,deldata:this.form.deldata,testtype:this.form.testtype,fuzzy:this.form.fuzzy},e={"Content-Type":"application/json"};Object(o["q"])(e,t).then(t=>{console.log(this.form.testtype);const{msg:e,code:a,data:r}=t;if("0"==a){var s=r[0];if(null==r||0!=s){for(var o=r[1],n=[],i=0;i<o.length;i++)n.push({name:o[i]});var l=JSON.stringify(n);this.tableData=JSON.parse(l)}else this.$message.error(r[1])}else this.$message.error(e)})}})},getversion(){const t={type:"1"},e={"Content-Type":"application/json"};Object(o["L"])(e,t).then(t=>{console.log(t);const{msg:e,code:a,data:r}=t;if("0"==a){var s=r.data;console.log(s);var o=JSON.stringify(s);this.tags=JSON.parse(o)}else this.$message.error(e)})},durationVerifyData(){const t={},e={"Content-Type":"application/json"};durationverifydata(e,t).then(t=>{console.log(t);const{msg:e,code:a,data:r}=t;if("0"==a){var s=r.data;console.log(s);var o=JSON.stringify(s);this.tags=JSON.parse(o)}else this.$message.error(e)})},getBase(){this.listLoading=!0;const t=this,e={selecttype:"dicom"},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["M"])(a,e).then(e=>{t.listLoading=!1;const{msg:a,code:r,data:s}=e;if("0"===r){t.total=s.total,t.list=s.data;var o=JSON.stringify(t.list);this.tags=JSON.parse(o)}else t.$message.error({message:a,center:!0})})},gethost(){this.listLoading=!0;const t=this,e={},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["D"])(a,e).then(e=>{t.listLoading=!1;const{msg:a,code:r,data:s}=e;if("0"===r){t.total=s.total,t.list=s.data;var o=JSON.stringify(t.list);this.tags=JSON.parse(o)}else t.$message.error({message:a,center:!0})})},getDurationlist(){this.listLoading=!0;const t=this,e={},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["N"])(a,e).then(e=>{t.listLoading=!1;const{msg:a,code:r,data:s}=e;"0"===r?(t.total=s.total,t.durationlist=s.data):t.$message.error({message:a,center:!0})})},handleDel:function(t,e){this.$confirm("确认删除该记录吗?","提示",{type:"warning"}).then(()=>{this.listLoading=!0;const t=this,a={ids:[e.id]},r={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["o"])(r,a).then(e=>{const{msg:a,code:r,data:s}=e;"0"===r?t.$message({message:"删除成功",center:!0,type:"success"}):t.$message.error({message:a,center:!0}),t.getDurationlist()})})},handleCurrentChange(t){this.page=t,this.handleDel()},handleEdit:function(t,e){this.editFormVisible=!0,this.editForm=Object.assign({},e)},handleChangeStatus:function(t,e){let a=this;this.listLoading=!0;let r={id:e.id},s={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};e.sendstatus?Object(o["v"])(s,r).then(t=>{let{msg:r,code:s,data:o}=t;a.listLoading=!1,"0"===s?(a.$message({message:"停止成功",center:!0,type:"success"}),e.sendstatus=!e.sendstatus):a.$message.error({message:r,center:!0})}):Object(o["A"])(s,r).then(t=>{let{msg:r,code:s,data:o}=t;a.listLoading=!1,"0"===s?(a.$message({message:"启用成功",center:!0,type:"success"}),e.sendstatus=!e.sendstatus):a.$message.error({message:r,center:!0})})},handleAdd:function(){this.addFormVisible=!0,this.addForm={server:null,port:4242,loop_time:"",keyword:null,dicom:null,dds:!1,sendstatus:!1,status:!1}},editSubmit:function(){const t=this;this.$refs.editForm.validate(e=>{e&&this.$confirm("确认提交吗？","提示",{}).then(()=>{t.editLoading=!0;const e={id:t.editForm.id,loop_time:t.editForm.loop_time,keyword:this.editForm.keyword,dicom:this.editForm.senddata,sendcount:this.editForm.sendcount,timer:this.editForm.timer},a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["eb"])(a,e).then(e=>{const{msg:a,code:r,data:s}=e;t.editLoading=!1,"0"===r?(t.$message({message:"修改成功",center:!0,type:"success"}),t.$refs["editForm"].resetFields(),t.editFormVisible=!1,t.getDurationlist()):t.$message.error({message:a,center:!0})})})})},addSubmit:function(){this.$refs.addForm.validate(t=>{if(t){const t=this;this.$confirm("确认提交吗？","提示",{}).then(()=>{t.addLoading=!0;const e=JSON.stringify({server:t.addForm.sendserver,port:t.addForm.port,loop_time:t.addForm.loop_time,keyword:this.addForm.keyword,dicom:this.addForm.senddata,sendcount:this.addForm.sendcount,timer:this.addForm.timer,dds:this.addForm.dds,sendstatus:!1,status:!1}),a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["h"])(a,e).then(e=>{const{msg:a,code:r,data:s}=e;t.addLoading=!1,"0"===r?(t.$message({message:"添加成功",center:!0,type:"success"}),t.$refs["addForm"].resetFields(),t.addFormVisible=!1,t.getDurationlist()):"999997"===r?t.$message.error({message:a,center:!0}):(t.$message.error({message:a,center:!0}),t.$refs["addForm"].resetFields(),t.addFormVisible=!1,t.getDurationlist())})})}})},selsChange:function(t){this.sels=t},cancelEdit(t){t.title=t.originalTitle,t.edit=!1,this.$message({message:"The title has been restored to the original value",type:"warning"})},confirmEdit(t){t.edit=!1,t.originalTitle=t.title,this.$message({message:"The title has been edited",type:"success"})},batchRemove:function(){const t=this.sels.map(t=>t.id);this.$confirm("确认删除选中记录吗？","提示",{type:"warning"}).then(()=>{this.listLoading=!0;const e=this,a={ids:t},r={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["o"])(r,a).then(t=>{const{msg:a,code:r,data:s}=t;"0"===r?e.$message({message:"删除成功",center:!0,type:"success"}):e.$message.error({message:a,center:!0}),e.getDurationlist()})})}}},i=n,l=(a("f640"),a("2877")),d=Object(l["a"])(i,r,s,!1,null,"63bc5d4d",null);e["default"]=d.exports},7364:function(t,e,a){},9742:function(t,e,a){t.exports=a.p+"static/img/qidong.d51313a5.png"},c392:function(t,e,a){t.exports=a.p+"static/img/ting-zhi.7cb414cc.png"},f640:function(t,e,a){"use strict";var r=a("7364"),s=a.n(r);s.a}}]);