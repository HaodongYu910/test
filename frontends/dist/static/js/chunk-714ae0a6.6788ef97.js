(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-714ae0a6"],{"2d92":function(e,t,a){"use strict";a.d(t,"hb",(function(){return o})),a.d(t,"K",(function(){return n})),a.d(t,"s",(function(){return i})),a.d(t,"A",(function(){return l})),a.d(t,"E",(function(){return d})),a.d(t,"kb",(function(){return p})),a.d(t,"j",(function(){return c})),a.d(t,"L",(function(){return u})),a.d(t,"J",(function(){return m})),a.d(t,"r",(function(){return h})),a.d(t,"z",(function(){return f})),a.d(t,"D",(function(){return g})),a.d(t,"jb",(function(){return b})),a.d(t,"i",(function(){return y})),a.d(t,"M",(function(){return v})),a.d(t,"N",(function(){return _})),a.d(t,"I",(function(){return k})),a.d(t,"q",(function(){return F})),a.d(t,"h",(function(){return w})),a.d(t,"O",(function(){return S})),a.d(t,"Q",(function(){return x})),a.d(t,"P",(function(){return $})),a.d(t,"f",(function(){return O})),a.d(t,"H",(function(){return j})),a.d(t,"g",(function(){return D})),a.d(t,"ib",(function(){return z})),a.d(t,"p",(function(){return C})),a.d(t,"C",(function(){return N})),a.d(t,"eb",(function(){return T})),a.d(t,"lb",(function(){return J})),a.d(t,"k",(function(){return L})),a.d(t,"F",(function(){return I})),a.d(t,"u",(function(){return V})),a.d(t,"bb",(function(){return A})),a.d(t,"ab",(function(){return q})),a.d(t,"db",(function(){return R})),a.d(t,"cb",(function(){return E})),a.d(t,"n",(function(){return P})),a.d(t,"nb",(function(){return B})),a.d(t,"w",(function(){return U})),a.d(t,"d",(function(){return G})),a.d(t,"gb",(function(){return H})),a.d(t,"fb",(function(){return K})),a.d(t,"R",(function(){return M})),a.d(t,"x",(function(){return Q})),a.d(t,"ob",(function(){return W})),a.d(t,"o",(function(){return X})),a.d(t,"Z",(function(){return Y})),a.d(t,"X",(function(){return Z})),a.d(t,"Y",(function(){return ee})),a.d(t,"W",(function(){return te})),a.d(t,"v",(function(){return ae})),a.d(t,"T",(function(){return se})),a.d(t,"U",(function(){return re})),a.d(t,"m",(function(){return oe})),a.d(t,"mb",(function(){return ne})),a.d(t,"t",(function(){return ie})),a.d(t,"G",(function(){return le})),a.d(t,"B",(function(){return de})),a.d(t,"V",(function(){return pe})),a.d(t,"S",(function(){return ce})),a.d(t,"l",(function(){return ue})),a.d(t,"e",(function(){return me})),a.d(t,"c",(function(){return he})),a.d(t,"b",(function(){return fe})),a.d(t,"a",(function(){return ge})),a.d(t,"y",(function(){return be}));var s=a("bc3a"),r=a.n(s);const o="http://192.168.2.38:9000",n=(e,t)=>r.a.get(o+"/api/project/project_list",{params:t,headers:e}).then(e=>e.data),i=(e,t)=>r.a.post(o+"/api/project/del_project",t,{headers:e}).then(e=>e.data),l=(e,t)=>r.a.post(o+"/api/project/disable_project",t,{headers:e}).then(e=>e.data),d=(e,t)=>r.a.post(o+"/api/project/enable_project",t,{headers:e}).then(e=>e.data),p=(e,t)=>r.a.post(o+"/api/project/update_project",t,{headers:e}).then(e=>e.data),c=(e,t)=>r.a.post(o+"/api/project/add_project",t,{headers:e}).then(e=>e.data),u=(e,t)=>r.a.get(o+"/api/title/project_info",{params:t,headers:e}).then(e=>e.data),m=(e,t)=>r.a.get(o+"/api/global/host_total",{params:t,headers:e}).then(e=>e.data),h=(e,t)=>r.a.post(o+"/api/global/del_host",t,{headers:e}).then(e=>e.data),f=(e,t)=>r.a.post(o+"/api/global/disable_host",t,{headers:e}).then(e=>e.data),g=(e,t)=>r.a.post(o+"/api/global/enable_host",t,{headers:e}).then(e=>e.data),b=(e,t)=>r.a.post(o+"/api/global/update_host",t,{headers:e}).then(e=>e.data),y=(e,t)=>r.a.post(o+"/api/global/add_host",t,{headers:e}).then(e=>e.data),v=(e,t)=>r.a.get(o+"/api/dynamic/dynamic",{params:t,headers:e}).then(e=>e.data),_=(e,t)=>r.a.get(o+"/api/member/project_member",{params:t,headers:e}).then(e=>e.data),k=(e,t)=>r.a.get(o+"/api/member/get_email",{params:t,headers:e}).then(e=>e.data),F=(e,t)=>r.a.post(o+"/api/member/del_email",t,{headers:e}).then(e=>e.data),w=(e,t)=>r.a.post(o+"/api/member/email_config",t,{headers:e}).then(e=>e.data),S=(e,t)=>r.a.get(o+"/api/report/auto_test_report",{params:t,headers:e}).then(e=>e.data),x=(e,t)=>r.a.get(o+"/api/report/test_time",{params:t,headers:e}).then(e=>e.data),$=(e,t)=>r.a.get(o+"/api/report/lately_ten",{params:t,headers:e}).then(e=>e.data),O=(e,t)=>r.a.post(o+"/api/api/add_api",t,{headers:e}).then(e=>e.data),j=(e,t)=>r.a.get(o+"/api/api/group",{params:t,headers:e}).then(e=>e.data),D=(e,t)=>r.a.post(o+"/api/api/add_group",t,{headers:e}).then(e=>e.data),z=(e,t)=>r.a.post(o+"/api/api/update_name_group",t,{headers:e}).then(e=>e.data),C=(e,t)=>r.a.post(o+"/api/api/del_group",t,{headers:e}).then(e=>e.data),N=(e,t)=>r.a.post(o+"/api/download",t,{headers:e}).then(e=>e.data),T=(e,t)=>r.a.post(o+"/api/user/login",t,e).then(e=>e.data),J=(e,t)=>r.a.post(o+"/api/risk/update",t,{headers:e}).then(e=>e.data),L=(e,t)=>r.a.post(o+"/api/risk/add",t,{headers:e}).then(e=>e.data),I=(e,t)=>r.a.post(o+"/api/risk/add",t,{headers:e}).then(e=>e.data),V=(e,t)=>r.a.post(o+"/api/risk/del",t,e).then(e=>e.data),A=(e,t)=>r.a.get(o+"/api/risk ",{params:t},e).then(e=>e.data),q=(e,t)=>r.a.post(o+"/api/jira/figure ",t,e).then(e=>e.data),R=(e,t)=>r.a.get(o+"/api/todo ",{params:t},e).then(e=>e.data),E=(e,t)=>r.a.get(o+"/api/report ",{params:t},e).then(e=>e.data),P=(e,t)=>r.a.post(o+"/api/addreport",t,e).then(e=>e.data),B=(e,t)=>r.a.post(o+"/api/updatereport",t,e).then(e=>e.data),U=(e,t)=>r.a.post(o+"/api/delreport",t,e).then(e=>e.data),G=(e,t)=>r.a.post(o+"/api/send",t,e).then(e=>e.data),H=(e,t)=>r.a.get(o+"/api/stress/list",{params:t},{headers:e}).then(e=>e.data),K=(e,t)=>r.a.post(o+"/api/stress/stresstool",t,e).then(e=>e.data),M=(e,t)=>r.a.get(o+"/api/stress/version",{params:t},{headers:e}).then(e=>e.data),Q=(e,t)=>r.a.post(o+"/api/stress/del_stressdata",t,e).then(e=>e.data),W=(e,t)=>r.a.post(o+"/api/stress/update_stressdata",t,e).then(e=>e.data),X=(e,t)=>r.a.post(o+"/api/stress/add_stressdata",t,e).then(e=>e.data),Y=(e,t)=>r.a.get(o+"/api/stress/stressversion",{params:t},{headers:e}).then(e=>e.data),Z=(e,t)=>r.a.get(o+"/api/stress/stressdata",{params:t},{headers:e}).then(e=>e.data),ee=(e,t)=>r.a.post(o+"/api/tool/stressresult",t,e).then(e=>e.data),te=(e,t)=>r.a.post(o+"/api/stress/stressfigure",t,e).then(e=>e.data),ae=(e,t)=>r.a.post(o+"/api/tool/delete_patients",t,e).then(e=>e.data),se=(e,t)=>r.a.get(o+"/api/tool/getduration",{params:t},{headers:e}).then(e=>e.data),re=(e,t)=>r.a.get(o+"/api/tool/durationData",{params:t},{headers:e}).then(e=>e.data),oe=(e,t)=>r.a.post(o+"/api/tool/add_duration",t,e).then(e=>e.data),ne=(e,t)=>r.a.post(o+"/api/tool/update_duration",t,e).then(e=>e.data),ie=(e,t)=>r.a.post(o+"/api/tool/del_duration",t,e).then(e=>e.data),le=(e,t)=>r.a.post(o+"/api/tool/enable_duration",t,e).then(e=>e.data),de=(e,t)=>r.a.post(o+"/api/tool/disable_duration",t,e).then(e=>e.data),pe=(e,t)=>r.a.get(o+"/api/tool/duration_verify",{params:t},{headers:e}).then(e=>e.data),ce=(e,t)=>r.a.get(o+"/api/base/getdata",{params:t},{headers:e}).then(e=>e.data),ue=(e,t)=>r.a.post(o+"/api/base/addData",t,e).then(e=>e.data),me=(e,t)=>r.a.post(o+"/api/base/updateData",t,e).then(e=>e.data),he=(e,t)=>r.a.post(o+"/api/base/enablebase",t,e).then(e=>e.data),fe=(e,t)=>r.a.post(o+"/api/base/disablebase",t,e).then(e=>e.data),ge=(e,t)=>r.a.post(o+"/api/base/delbasedata",t,e).then(e=>e.data),be=(e,t)=>r.a.get(o+"/api/base/dicom",{params:t},{headers:e}).then(e=>e.data)},3155:function(e,t,a){"use strict";a.r(t);var s=function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",{staticClass:"app-container"},[s("div",{staticClass:"filter-container"},[s("el-col",{staticClass:"toolbar",staticStyle:{"padding-bottom":"0px"},attrs:{span:100}},[s("aside",[s("a",{attrs:{href:"http://192.168.2.38:9000/",target:"_blank"}},[e._v("删除dicom数据 ")])]),s("el-form",{ref:"form",attrs:{model:e.form,"status-icon":"",rules:e.rules,"label-width":"100px"}},[s("el-row",[s("el-col",{attrs:{span:5}},[s("el-form-item",{attrs:{label:"测试服务器",prop:"server_ip"}},[s("el-select",{attrs:{placeholder:"请选择"},nativeOn:{click:function(t){return e.gethost()}},model:{value:e.form.server_ip,callback:function(t){e.$set(e.form,"server_ip",t)},expression:"form.server_ip"}},e._l(e.tags,(function(e,t){return s("el-option",{key:e.host,attrs:{label:e.name,value:e.host}})})),1)],1)],1),s("el-col",{attrs:{span:5}},[s("el-form-item",{attrs:{label:"删除数据",prop:"deldata"}},[s("el-input",{attrs:{id:"deldata",placeholder:"删除数据"},model:{value:e.form.deldata,callback:function(t){e.$set(e.form,"deldata",t)},expression:"form.deldata"}})],1)],1),s("el-col",{attrs:{span:5}},[s("el-form-item",{attrs:{label:"数据类型",prop:"testtype"}},[s("el-select",{attrs:{placeholder:"请选择"},model:{value:e.form.testtype,callback:function(t){e.$set(e.form,"testtype",t)},expression:"form.testtype"}},[s("el-option",{key:"PatientName",attrs:{label:"患者姓名",value:"PatientName"}}),s("el-option",{key:"PatientID",attrs:{label:"患者编号",value:"PatientID"}}),s("el-option",{key:"ai",attrs:{label:"预测结果",value:"ai"}}),s("el-option",{key:"StudyInstanceUID",attrs:{label:"StudyInstanceUID",value:"StudyInstanceUID"}})],1)],1)],1),s("el-col",{attrs:{span:4}},[s("el-form-item",{attrs:{label:"模糊搜索",prop:"fuzzy"}},[s("el-select",{attrs:{clearable:"",placeholder:"请选择"},model:{value:e.form.fuzzy,callback:function(t){e.$set(e.form,"fuzzy",t)},expression:"form.fuzzy"}},[s("el-option",{key:"True",attrs:{label:"是",value:"True"}}),s("el-option",{key:"False",attrs:{label:"否",value:"False"}})],1)],1)],1),s("el-col",{attrs:{span:4}},[s("el-form-item",[s("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.deldicom("form")}}},[e._v("删除")])],1)],1)],1)],1),s("div",[s("el-table",{staticStyle:{width:"50%"},attrs:{data:e.tableData}},[s("el-table-column",{attrs:{label:"结果显示",width:"180"},scopedSlots:e._u([{key:"default",fn:function(t){return[s("el-popover",{attrs:{trigger:"hover",placement:"top"}},[s("p",[e._v("标签: "+e._s(t.row.name))]),s("div",{staticClass:"name-wrapper",attrs:{slot:"reference"},slot:"reference"},[s("el-tag",{attrs:{size:"medium"}},[e._v(e._s(t.row.name))])],1)])]}}])}),s("el-table-column",{attrs:{fixed:"right",label:""},scopedSlots:e._u([{key:"default",fn:function(t){return[s("el-button",{attrs:{size:"mini",type:"danger"},on:{click:function(a){return e.deleteTag(t.$index,t.row)}}},[e._v("开始/关闭 ")])]}}])})],1)],1),s("aside",[s("a",{attrs:{href:"http://192.168.2.38:9000/",target:"_blank"}},[e._v("匿名发送dicom数据 ")])]),s("el-col",{staticClass:"toolbar",staticStyle:{"padding-bottom":"0px"},attrs:{span:24}},[s("el-form",{attrs:{inline:!0,model:e.filters},nativeOn:{submit:function(e){e.preventDefault()}}},[s("el-form-item",[s("el-input",{attrs:{placeholder:"名称"},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.getDurationlist(t)}},model:{value:e.filters.name,callback:function(t){e.$set(e.filters,"name",t)},expression:"filters.name"}})],1),s("el-form-item",[s("el-button",{attrs:{type:"primary"},on:{click:e.getDurationlist}},[e._v("查询")])],1),s("el-form-item",[s("el-button",{attrs:{type:"primary"},on:{click:e.handleAdd}},[e._v("新增")])],1)],1)],1),s("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.listLoading,expression:"listLoading"}],staticStyle:{width:"200%"},attrs:{data:e.durationlist,"highlight-current-row":""},on:{"selection-change":e.selsChange}},[s("el-table-column",{attrs:{type:"selection","min-width":"5%"}}),s("el-table-column",{attrs:{prop:"type",label:"服务器","min-width":"20%"},scopedSlots:e._u([{key:"default",fn:function(t){return[t.row.server?s("router-link",{staticStyle:{"text-decoration":"none",color:"#000000"},attrs:{to:{name:"持续化数据详情",params:{id:t.row.id}}}},[s("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.server)+"："+e._s(t.row.port))])]):e._e()]}}])}),s("el-table-column",{attrs:{prop:"type",label:"匿名名称","min-width":"12%"},scopedSlots:e._u([{key:"default",fn:function(t){return[s("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.keyword))])]}}])}),s("el-table-column",{attrs:{prop:"type",label:"发送类型","min-width":"25%"},scopedSlots:e._u([{key:"default",fn:function(t){return[s("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.dicom))])]}}])}),s("el-table-column",{attrs:{label:"预发送数量","min-width":"10%"},scopedSlots:e._u([{key:"default",fn:function(t){return[s("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.sendcount)+" 个")])]}}])}),s("el-table-column",{attrs:{label:"实际已发送","min-width":"12%"},scopedSlots:e._u([{key:"default",fn:function(t){return[s("span",{staticStyle:{"margin-left":"10px",color:"#FF0000"}},[e._v(e._s(t.row.send))])]}}])}),s("el-table-column",{attrs:{label:"结束时间","min-width":"10%"},scopedSlots:e._u([{key:"default",fn:function(t){return[s("span",{staticStyle:{"margin-left":"10px",color:"#00A600"}},[e._v(e._s(t.row.end_time))])]}}])}),s("el-table-column",{attrs:{label:"延时时间","min-width":"10%"},scopedSlots:e._u([{key:"default",fn:function(t){return[s("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.sleeptime)+" 秒 ")])]}}])}),s("el-table-column",{attrs:{label:"延时数量","min-width":"10%"},scopedSlots:e._u([{key:"default",fn:function(t){return[s("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.sleepcount)+" 个 ")])]}}])}),s("el-table-column",{attrs:{label:"series延时","min-width":"10%"},scopedSlots:e._u([{key:"default",fn:function(t){return[s("span",{staticStyle:{"margin-left":"10px"}},[e._v(e._s(t.row.series))])]}}])}),s("el-table-column",{attrs:{label:"DDS","min-width":"12%"},scopedSlots:e._u([{key:"default",fn:function(t){return[s("span",{staticStyle:{"margin-left":"10px",color:"#02C874"}},[e._v(e._s(t.row.dds))])]}}])}),s("el-table-column",{attrs:{prop:"sendstatus",label:"运行状态","min-width":"10%"},scopedSlots:e._u([{key:"default",fn:function(e){return[s("img",{directives:[{name:"show",rawName:"v-show",value:e.row.sendstatus,expression:"scope.row.sendstatus"}],staticStyle:{width:"18px",height:"18px","margin-right":"5px","margin-bottom":"5px"},attrs:{src:a("9742")}}),s("img",{directives:[{name:"show",rawName:"v-show",value:!e.row.sendstatus,expression:"!scope.row.sendstatus"}],staticStyle:{width:"15px",height:"15px","margin-right":"5px","margin-bottom":"5px"},attrs:{src:a("c392")}})]}}])}),s("el-table-column",{attrs:{label:"操作","min-width":"30%"},scopedSlots:e._u([{key:"default",fn:function(t){return[s("el-button",{attrs:{type:"info",size:"small"},on:{click:function(a){return e.handleChangeStatus(t.$index,t.row)}}},[e._v(" "+e._s(!1===t.row.sendstatus?"启用":"停用")+" ")]),s("el-button",{attrs:{type:"danger",size:"small"},on:{click:function(a){return e.showDetail(t.$index,t.row)}}},[e._v("数据")]),s("el-button",{attrs:{type:"warning",size:"small"},on:{click:function(a){return e.handleEdit(t.$index,t.row)}}},[e._v("修改 ")])]}}])})],1),s("el-col",{staticClass:"toolbar",attrs:{span:24}},[s("el-button",{attrs:{type:"danger",disabled:0===this.sels.length},on:{click:e.batchRemove}},[e._v("删除")]),s("el-pagination",{staticStyle:{float:"right"},attrs:{layout:"prev, pager, next","page-size":20,"page-count":e.total},on:{"current-change":e.handleCurrentChange}})],1),s("el-dialog",{staticStyle:{width:"75%",left:"12.5%"},attrs:{title:"修改",visible:e.editFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(t){e.editFormVisible=t}}},[s("el-form",{ref:"editForm",attrs:{model:e.editForm,"label-width":"80px",rules:e.editFormRules}},[s("el-row",[s("el-col",{attrs:{span:8}},[s("el-form-item",{attrs:{label:"数据类型",prop:"senddata"}},[s("el-select",{attrs:{multiple:"",placeholder:"请选择"},nativeOn:{click:function(t){return e.getBase()}},model:{value:e.editForm.senddata,callback:function(t){e.$set(e.editForm,"senddata",t)},expression:"editForm.senddata"}},e._l(e.tags,(function(e,t){return s("el-option",{key:e.remarks,attrs:{label:e.remarks,value:e.remarks}})})),1)],1)],1),s("el-col",{attrs:{span:6}},[s("el-form-item",{attrs:{label:"匿名名称",prop:"keyword"}},[s("el-input",{attrs:{id:"key_word",placeholder:"数据名称"},model:{value:e.editForm.keyword,callback:function(t){e.$set(e.editForm,"keyword",t)},expression:"editForm.keyword"}})],1)],1),s("el-col",{attrs:{span:6}},[s("el-form-item",{attrs:{label:"发送数据",prop:"keyword"}},[s("el-input",{attrs:{id:"sendcount",placeholder:"共/个"},model:{value:e.editForm.sendcount,callback:function(t){e.$set(e.editForm,"sendcount",t)},expression:"editForm.sendcount"}})],1)],1),s("el-col",{attrs:{span:6}},[s("el-form-item",{attrs:{label:"持续时间",prop:"loop_time"}},[s("el-input",{attrs:{id:"looptime",placeholder:"小时"},model:{value:e.editForm.loop_time,callback:function(t){e.$set(e.editForm,"loop_time",t)},expression:"editForm.loop_time"}})],1)],1),s("el-col",{attrs:{span:4}},[s("el-form-item",{attrs:{label:"延时时间",prop:"sleeptime"}},[s("el-input",{attrs:{id:"sleeptime",placeholder:"秒"},model:{value:e.editForm.sleeptime,callback:function(t){e.$set(e.editForm,"sleeptime",t)},expression:"editForm.sleeptime"}})],1)],1),s("el-col",{attrs:{span:4}},[s("el-form-item",{attrs:{label:"延时数量",prop:"sleepcount"}},[s("el-input",{attrs:{id:"sleepcount",placeholder:"张"},model:{value:e.editForm.sleepcount,callback:function(t){e.$set(e.editForm,"sleepcount",t)},expression:"editForm.sleepcount"}})],1)],1),s("el-col",{attrs:{span:3}},[s("el-form-item",{attrs:{label:"series",prop:"series"}},[s("el-switch",{attrs:{"active-color":"#13ce66","inactive-color":"#ff4949"},model:{value:e.editForm.series,callback:function(t){e.$set(e.editForm,"series",t)},expression:"editForm.series"}})],1)],1),s("el-col",{attrs:{span:4}},[s("el-form-item",{attrs:{label:"",prop:"keyword"}},[s("el-button",{attrs:{type:"primary",loading:e.editLoading},nativeOn:{click:function(t){return e.editSubmit(t)}}},[e._v("保存")])],1)],1)],1)],1)],1),s("el-dialog",{staticStyle:{width:"75%",left:"12.5%"},attrs:{title:"新增",visible:e.addFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(t){e.addFormVisible=t}}},[s("el-form",{ref:"addForm",attrs:{model:e.addForm,"label-width":"80px",rules:e.addFormRules}},[s("el-form",{attrs:{inline:!0,model:e.filters},nativeOn:{submit:function(e){e.preventDefault()}}},[s("el-row",[s("el-col",{attrs:{span:5}},[s("el-form-item",{attrs:{label:"发送服务器",prop:"sendserver"}},[s("el-select",{attrs:{placeholder:"请选择"},nativeOn:{click:function(t){return e.gethost()}},model:{value:e.addForm.sendserver,callback:function(t){e.$set(e.addForm,"sendserver",t)},expression:"addForm.sendserver"}},e._l(e.tags,(function(e,t){return s("el-option",{key:e.host,attrs:{label:e.name,value:e.host}})})),1)],1)],1),s("el-col",{attrs:{span:3}},[s("el-form-item",{attrs:{label:"端口号",prop:"port"}},[s("el-input",{attrs:{id:"port",placeholder:""},model:{value:e.addForm.port,callback:function(t){e.$set(e.addForm,"port",t)},expression:"addForm.port"}})],1)],1),s("el-col",{attrs:{span:6}},[s("el-form-item",{attrs:{label:"数据类型",prop:"senddata"}},[s("el-select",{attrs:{multiple:"",placeholder:"请选择"},nativeOn:{click:function(t){return e.getBase()}},model:{value:e.addForm.senddata,callback:function(t){e.$set(e.addForm,"senddata",t)},expression:"addForm.senddata"}},e._l(e.tags,(function(e,t){return s("el-option",{key:e.remarks,attrs:{label:e.remarks,value:e.remarks}})})),1)],1)],1),s("el-col",{attrs:{span:4}},[s("el-form-item",{attrs:{label:"匿名名称",prop:"keyword"}},[s("el-input",{attrs:{id:"keyword",placeholder:"数据名称"},model:{value:e.addForm.keyword,callback:function(t){e.$set(e.addForm,"keyword",t)},expression:"addForm.keyword"}})],1)],1),s("el-col",{attrs:{span:3}},[s("el-form-item",{attrs:{label:"持续时间",prop:"loop_time"}},[s("el-input",{attrs:{id:"loop_time",placeholder:"小时"},model:{value:e.addForm.loop_time,callback:function(t){e.$set(e.addForm,"loop_time",t)},expression:"addForm.loop_time"}})],1)],1),s("el-col",{attrs:{span:3}},[s("el-form-item",{attrs:{label:"发送数量",prop:"count"}},[s("el-input",{attrs:{id:"sendcount",placeholder:"共/个"},model:{value:e.addForm.sendcount,callback:function(t){e.$set(e.addForm,"sendcount",t)},expression:"addForm.sendcount"}})],1)],1),s("el-col",{attrs:{span:4}},[s("el-form-item",{attrs:{label:"延时时间",prop:"sleeptime"}},[s("el-input",{attrs:{id:"sleeptime",placeholder:"秒"},model:{value:e.addForm.sleeptime,callback:function(t){e.$set(e.addForm,"sleeptime",t)},expression:"addForm.sleeptime"}})],1)],1),s("el-col",{attrs:{span:4}},[s("el-form-item",{attrs:{label:"延时数量",prop:"sleepcount"}},[s("el-input",{attrs:{id:"sleepcount",placeholder:"张"},model:{value:e.addForm.sleepcount,callback:function(t){e.$set(e.addForm,"sleepcount",t)},expression:"addForm.sleepcount"}})],1)],1),s("el-col",{attrs:{span:3}},[s("el-form-item",{attrs:{label:"series",prop:"series"}},[s("el-switch",{attrs:{"active-color":"#13ce66","inactive-color":"#ff4949"},model:{value:e.addForm.series,callback:function(t){e.$set(e.addForm,"series",t)},expression:"addForm.series"}})],1)],1),s("el-col",{attrs:{span:6}},[s("el-form-item",{attrs:{label:"",prop:"dds"}},[s("el-input",{attrs:{id:"dds",placeholder:"DDS服务"},model:{value:e.addForm.dds,callback:function(t){e.$set(e.addForm,"dds",t)},expression:"addForm.dds"}})],1)],1),s("el-col",{attrs:{span:4}},[s("el-form-item",{attrs:{label:"",prop:"save"}},[s("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.addSubmit("form")}}},[e._v("保存")])],1)],1)],1)],1)],1)],1)],1)],1)])},r=[],o=a("2d92"),n={data(){return{form:{server_ip:"",fuzzy:"是",testtype:"PatientID",deldata:""},rules:{server_ip:[{required:!0,message:"请输入测试服务器",trigger:"blur"}],version:[{required:!0,message:"请输入版本号",trigger:"change"},{pattern:/^\d+\.\d+\.\d+$/,message:"请输入合法的版本号（x.x.x）"}]},filters:{diseases:""},durationlist:{},total:0,page:1,listLoading:!0,sels:[],editFormVisible:!1,editLoading:!1,editFormRules:{diseases:[{required:!0,message:"请输入名称",trigger:"blur"},{min:1,max:50,message:"长度在 1 到 50 个字符",trigger:"blur"}],type:[{required:!0,message:"请选择类型",trigger:"blur"}],description:[{required:!1,message:"请输入描述",trigger:"blur"},{max:1024,message:"不能超过1024个字符",trigger:"blur"}]},editForm:{loop_time:"",port:"4242"},addForm:{port:"4242"},addFormVisible:!1,addLoading:!1,addFormRules:{diseases:[{required:!0,message:"请输入名称",trigger:"blur"},{min:1,max:50,message:"长度在 1 到 50 个字符",trigger:"blur"}],type:[{required:!0,message:"请选择类型",trigger:"blur"}],version:[{required:!0,message:"请输入版本号",trigger:"change"},{pattern:/^\d+\.\d+\.\d+$/,message:"请输入合法的版本号（x.x.x）"}]},addForm:{diseases:"",version:"",type:"",description:""}}},mounted(){this.getDurationlist(),this.gethost(),this.durationVerifyData()},methods:{showDetail(e,t){this.$router.push({path:"/durationData",query:{id:t.id,name:t.server_ip}})},deldicom(e){this.tableData=null,this.$refs[e].validate(e=>{if(!e)return console.log("error submit"),!1;{const e={server_ip:this.form.server_ip,deldata:this.form.deldata,testtype:this.form.testtype,fuzzy:this.form.fuzzy},t={"Content-Type":"application/json"};Object(o["v"])(t,e).then(e=>{console.log(this.form.testtype);const{msg:t,code:a,data:s}=e;if("0"==a){var r=s[0];if(null==s||0!=r){for(var o=s[1],n=[],i=0;i<o.length;i++)n.push({name:o[i]});var l=JSON.stringify(n);this.tableData=JSON.parse(l)}else this.$message.error(s[1])}else this.$message.error(t)})}})},getversion(){const e={type:"1"},t={"Content-Type":"application/json"};Object(o["R"])(t,e).then(e=>{console.log(e);const{msg:t,code:a,data:s}=e;if("0"==a){var r=s.data;console.log(r);var o=JSON.stringify(r);this.tags=JSON.parse(o)}else this.$message.error(t)})},durationVerifyData(){const e={},t={"Content-Type":"application/json"};durationverifydata(t,e).then(e=>{console.log(e);const{msg:t,code:a,data:s}=e;if("0"==a){var r=s.data;console.log(r);var o=JSON.stringify(r);this.tags=JSON.parse(o)}else this.$message.error(t)})},getBase(){this.listLoading=!0;const e=this,t={selecttype:"dicom"},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["S"])(a,t).then(t=>{e.listLoading=!1;const{msg:a,code:s,data:r}=t;if("0"===s){e.total=r.total,e.list=r.data;var o=JSON.stringify(e.list);this.tags=JSON.parse(o)}else e.$message.error({message:a,center:!0})})},gethost(){this.listLoading=!0;const e=this,t={},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["J"])(a,t).then(t=>{e.listLoading=!1;const{msg:a,code:s,data:r}=t;if("0"===s){e.total=r.total,e.list=r.data;var o=JSON.stringify(e.list);this.tags=JSON.parse(o)}else e.$message.error({message:a,center:!0})})},getDurationlist(){this.listLoading=!0;const e=this,t={},a={Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["T"])(a,t).then(t=>{e.listLoading=!1;const{msg:a,code:s,data:r}=t;"0"===s?(e.total=r.total,e.durationlist=r.data):e.$message.error({message:a,center:!0})})},handleDel:function(e,t){this.$confirm("确认删除该记录吗?","提示",{type:"warning"}).then(()=>{this.listLoading=!0;const e=this,a={ids:[t.id]},s={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["t"])(s,a).then(t=>{const{msg:a,code:s,data:r}=t;"0"===s?e.$message({message:"删除成功",center:!0,type:"success"}):e.$message.error({message:a,center:!0}),e.getDurationlist()})})},handleCurrentChange(e){this.page=e,this.handleDel()},handleEdit:function(e,t){this.editFormVisible=!0,this.editForm=Object.assign({},t)},handleChangeStatus:function(e,t){let a=this;this.listLoading=!0;let s={id:t.id},r={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};t.sendstatus?Object(o["B"])(r,s).then(e=>{let{msg:s,code:r,data:o}=e;a.listLoading=!1,"0"===r?(a.$message({message:"停止成功",center:!0,type:"success"}),t.sendstatus=!t.sendstatus):a.$message.error({message:s,center:!0})}):Object(o["G"])(r,s).then(e=>{let{msg:s,code:r,data:o}=e;a.listLoading=!1,"0"===r?(a.$message({message:"启用成功",center:!0,type:"success"}),t.sendstatus=!t.sendstatus):a.$message.error({message:s,center:!0})})},handleAdd:function(){this.addFormVisible=!0,this.addForm={server:null,port:4242,loop_time:"",keyword:null,dicom:null,dds:null,sendstatus:!1,status:!1,sleepcount:null,sleeptime:0,series:!1}},editSubmit:function(){const e=this;this.$refs.editForm.validate(t=>{t&&this.$confirm("确认提交吗？","提示",{}).then(()=>{e.editLoading=!0;const t={id:e.editForm.id,loop_time:e.editForm.loop_time,keyword:this.editForm.keyword,dicom:this.editForm.senddata,sendcount:this.editForm.sendcount,sleepcount:this.editForm.sleepcount,sleeptime:this.editForm.sleeptime,series:this.editForm.series},a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["mb"])(a,t).then(t=>{const{msg:a,code:s,data:r}=t;e.editLoading=!1,"0"===s?(e.$message({message:"修改成功",center:!0,type:"success"}),e.$refs["editForm"].resetFields(),e.editFormVisible=!1,e.getDurationlist()):e.$message.error({message:a,center:!0})})})})},addSubmit:function(){this.$refs.addForm.validate(e=>{if(e){const e=this;this.$confirm("确认提交吗？","提示",{}).then(()=>{e.addLoading=!0;const t=JSON.stringify({server:e.addForm.sendserver,port:e.addForm.port,loop_time:e.addForm.loop_time,keyword:this.addForm.keyword,dicom:this.addForm.senddata,sendcount:this.addForm.sendcount,dds:this.addForm.dds,sleepcount:this.addForm.sleepcount,sleeptime:this.addForm.sleeptime,series:this.addForm.series,sendstatus:!1,status:!1}),a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["m"])(a,t).then(t=>{const{msg:a,code:s,data:r}=t;e.addLoading=!1,"0"===s?(e.$message({message:"添加成功",center:!0,type:"success"}),e.$refs["addForm"].resetFields(),e.addFormVisible=!1,e.getDurationlist()):"999997"===s?e.$message.error({message:a,center:!0}):(e.$message.error({message:a,center:!0}),e.$refs["addForm"].resetFields(),e.addFormVisible=!1,e.getDurationlist())})})}})},selsChange:function(e){this.sels=e},cancelEdit(e){e.title=e.originalTitle,e.edit=!1,this.$message({message:"The title has been restored to the original value",type:"warning"})},confirmEdit(e){e.edit=!1,e.originalTitle=e.title,this.$message({message:"The title has been edited",type:"success"})},batchRemove:function(){const e=this.sels.map(e=>e.id);this.$confirm("确认删除选中记录吗？","提示",{type:"warning"}).then(()=>{this.listLoading=!0;const t=this,a={ids:e},s={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(o["t"])(s,a).then(e=>{const{msg:a,code:s,data:r}=e;"0"===s?t.$message({message:"删除成功",center:!0,type:"success"}):t.$message.error({message:a,center:!0}),t.getDurationlist()})})}}},i=n,l=(a("ff44"),a("2877")),d=Object(l["a"])(i,s,r,!1,null,"4a8c7f6c",null);t["default"]=d.exports},"40b6":function(e,t,a){},9742:function(e,t,a){e.exports=a.p+"static/img/qidong.d51313a5.png"},c392:function(e,t,a){e.exports=a.p+"static/img/ting-zhi.7cb414cc.png"},ff44:function(e,t,a){"use strict";var s=a("40b6"),r=a.n(s);r.a}}]);