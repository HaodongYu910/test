(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-79bd94c8"],{"2d92":function(e,t,a){"use strict";a.d(t,"qb",(function(){return s})),a.d(t,"Q",(function(){return l})),a.d(t,"v",(function(){return i})),a.d(t,"G",(function(){return n})),a.d(t,"K",(function(){return u})),a.d(t,"tb",(function(){return d})),a.d(t,"k",(function(){return p})),a.d(t,"R",(function(){return c})),a.d(t,"P",(function(){return m})),a.d(t,"u",(function(){return f})),a.d(t,"F",(function(){return h})),a.d(t,"J",(function(){return b})),a.d(t,"sb",(function(){return v})),a.d(t,"j",(function(){return g})),a.d(t,"S",(function(){return y})),a.d(t,"T",(function(){return _})),a.d(t,"O",(function(){return k})),a.d(t,"t",(function(){return w})),a.d(t,"i",(function(){return x})),a.d(t,"U",(function(){return F})),a.d(t,"W",(function(){return T})),a.d(t,"V",(function(){return $})),a.d(t,"g",(function(){return S})),a.d(t,"N",(function(){return q})),a.d(t,"h",(function(){return C})),a.d(t,"rb",(function(){return L})),a.d(t,"s",(function(){return P})),a.d(t,"I",(function(){return j})),a.d(t,"mb",(function(){return D})),a.d(t,"ub",(function(){return R})),a.d(t,"l",(function(){return A})),a.d(t,"L",(function(){return I})),a.d(t,"z",(function(){return E})),a.d(t,"jb",(function(){return O})),a.d(t,"lb",(function(){return z})),a.d(t,"kb",(function(){return G})),a.d(t,"q",(function(){return H})),a.d(t,"xb",(function(){return N})),a.d(t,"B",(function(){return V})),a.d(t,"d",(function(){return J})),a.d(t,"ob",(function(){return M})),a.d(t,"m",(function(){return U})),a.d(t,"e",(function(){return W})),a.d(t,"nb",(function(){return B})),a.d(t,"X",(function(){return K})),a.d(t,"pb",(function(){return Q})),a.d(t,"w",(function(){return X})),a.d(t,"vb",(function(){return Y})),a.d(t,"o",(function(){return Z})),a.d(t,"E",(function(){return ee})),a.d(t,"ab",(function(){return te})),a.d(t,"D",(function(){return ae})),a.d(t,"x",(function(){return re})),a.d(t,"ib",(function(){return oe})),a.d(t,"hb",(function(){return se})),a.d(t,"eb",(function(){return le})),a.d(t,"A",(function(){return ie})),a.d(t,"bb",(function(){return ne})),a.d(t,"cb",(function(){return ue})),a.d(t,"p",(function(){return de})),a.d(t,"wb",(function(){return pe})),a.d(t,"y",(function(){return ce})),a.d(t,"r",(function(){return me})),a.d(t,"M",(function(){return fe})),a.d(t,"H",(function(){return he})),a.d(t,"db",(function(){return be})),a.d(t,"fb",(function(){return ve})),a.d(t,"gb",(function(){return ge})),a.d(t,"Z",(function(){return ye})),a.d(t,"Y",(function(){return _e})),a.d(t,"n",(function(){return ke})),a.d(t,"f",(function(){return we})),a.d(t,"c",(function(){return xe})),a.d(t,"b",(function(){return Fe})),a.d(t,"a",(function(){return Te})),a.d(t,"C",(function(){return $e}));var r=a("bc3a"),o=a.n(r);a("c896");const s="http://192.168.1.121:9000",l=(e,t)=>o.a.get(s+"/api/project/project_list",{params:t,headers:e}).then(e=>e.data),i=(e,t)=>o.a.post(s+"/api/project/del_project",t,{headers:e}).then(e=>e.data),n=(e,t)=>o.a.post(s+"/api/project/disable_project",t,{headers:e}).then(e=>e.data),u=(e,t)=>o.a.post(s+"/api/project/enable_project",t,{headers:e}).then(e=>e.data),d=(e,t)=>o.a.post(s+"/api/project/update_project",t,{headers:e}).then(e=>e.data),p=(e,t)=>o.a.post(s+"/api/project/add_project",t,{headers:e}).then(e=>e.data),c=(e,t)=>o.a.get(s+"/api/title/project_info",{params:t,headers:e}).then(e=>e.data),m=(e,t)=>o.a.get(s+"/api/global/host_total",{params:t,headers:e}).then(e=>e.data),f=(e,t)=>o.a.post(s+"/api/global/del_host",t,{headers:e}).then(e=>e.data),h=(e,t)=>o.a.post(s+"/api/global/disable_host",t,{headers:e}).then(e=>e.data),b=(e,t)=>o.a.post(s+"/api/global/enable_host",t,{headers:e}).then(e=>e.data),v=(e,t)=>o.a.post(s+"/api/global/update_host",t,{headers:e}).then(e=>e.data),g=(e,t)=>o.a.post(s+"/api/global/add_host",t,{headers:e}).then(e=>e.data),y=(e,t)=>o.a.get(s+"/api/dynamic/dynamic",{params:t,headers:e}).then(e=>e.data),_=(e,t)=>o.a.get(s+"/api/member/project_member",{params:t,headers:e}).then(e=>e.data),k=(e,t)=>o.a.get(s+"/api/member/get_email",{params:t,headers:e}).then(e=>e.data),w=(e,t)=>o.a.post(s+"/api/member/del_email",t,{headers:e}).then(e=>e.data),x=(e,t)=>o.a.post(s+"/api/member/email_config",t,{headers:e}).then(e=>e.data),F=(e,t)=>o.a.get(s+"/api/report/auto_test_report",{params:t,headers:e}).then(e=>e.data),T=(e,t)=>o.a.get(s+"/api/report/test_time",{params:t,headers:e}).then(e=>e.data),$=(e,t)=>o.a.get(s+"/api/report/lately_ten",{params:t,headers:e}).then(e=>e.data),S=(e,t)=>o.a.post(s+"/api/api/add_api",t,{headers:e}).then(e=>e.data),q=(e,t)=>o.a.get(s+"/api/api/group",{params:t,headers:e}).then(e=>e.data),C=(e,t)=>o.a.post(s+"/api/api/add_group",t,{headers:e}).then(e=>e.data),L=(e,t)=>o.a.post(s+"/api/api/update_name_group",t,{headers:e}).then(e=>e.data),P=(e,t)=>o.a.post(s+"/api/api/del_group",t,{headers:e}).then(e=>e.data),j=(e,t)=>o.a.post(s+"/api/download",t,{headers:e}).then(e=>e.data),D=(e,t)=>o.a.post(s+"/api/user/login",t,e).then(e=>e.data),R=(e,t)=>o.a.post(s+"/api/risk/update",t,{headers:e}).then(e=>e.data),A=(e,t)=>o.a.post(s+"/api/risk/add",t,{headers:e}).then(e=>e.data),I=(e,t)=>o.a.post(s+"/api/risk/add",t,{headers:e}).then(e=>e.data),E=(e,t)=>o.a.post(s+"/api/risk/del",t,e).then(e=>e.data),O=(e,t)=>o.a.get(s+"/api/risk ",{params:t},e).then(e=>e.data),z=(e,t)=>o.a.get(s+"/api/todo ",{params:t},e).then(e=>e.data),G=(e,t)=>o.a.get(s+"/api/report ",{params:t},e).then(e=>e.data),H=(e,t)=>o.a.post(s+"/api/addreport",t,e).then(e=>e.data),N=(e,t)=>o.a.post(s+"/api/updatereport",t,e).then(e=>e.data),V=(e,t)=>o.a.post(s+"/api/delreport",t,e).then(e=>e.data),J=(e,t)=>o.a.post(s+"/api/send",t,e).then(e=>e.data),M=(e,t)=>o.a.get(s+"/api/stress/list",{params:t},{headers:e}).then(e=>e.data),U=(e,t)=>o.a.post(s+"/api/stress/add",t,e).then(e=>e.data),W=(e,t)=>o.a.get(s+"/api/stress/stressDetail ",{params:t},e).then(e=>e.data),B=(e,t)=>o.a.post(s+"/api/stress/stresstool",t,e).then(e=>e.data),K=(e,t)=>o.a.get(s+"/api/stress/version",{params:t},{headers:e}).then(e=>e.data),Q=(e,t)=>o.a.post(s+"/api/stress/stresssave",t,e).then(e=>e.data),X=(e,t)=>o.a.post(s+"/api/tool/del_dicomData",t,e).then(e=>e.data),Y=(e,t)=>o.a.post(s+"/api/dicom/update",t,e).then(e=>e.data),Z=(e,t)=>o.a.post(s+"/api/tool/add_dicomData",t,e).then(e=>e.data),ee=(e,t)=>o.a.post(s+"/api/tool/dicomdetail",t,e).then(e=>e.data),te=(e,t)=>o.a.get(s+"/api/tool/dicomData",{params:t},{headers:e}).then(e=>e.data),ae=(e,t)=>o.a.post(s+"/api/tool/dicomcsv",t,e).then(e=>e.data),re=(e,t)=>o.a.post(s+"/api/tool/delreport",t,e).then(e=>e.data),oe=(e,t)=>o.a.get(s+"/api/stress/stressversion",{params:t},{headers:e}).then(e=>e.data),se=(e,t)=>o.a.post(s+"/api/stress/stressresult",t,e).then(e=>e.data),le=(e,t)=>o.a.post(s+"/api/stress/stressfigure",t,e).then(e=>e.data),ie=(e,t)=>o.a.post(s+"/api/tool/delete_patients",t,e).then(e=>e.data),ne=(e,t)=>o.a.get(s+"/api/tool/getduration",{params:t},{headers:e}).then(e=>e.data),ue=(e,t)=>o.a.get(s+"/api/tool/durationData",{params:t},{headers:e}).then(e=>e.data),de=(e,t)=>o.a.post(s+"/api/tool/add_duration",t,e).then(e=>e.data),pe=(e,t)=>o.a.post(s+"/api/tool/update_duration",t,e).then(e=>e.data),ce=(e,t)=>o.a.post(s+"/api/tool/del_duration",t,e).then(e=>e.data),me=(e,t)=>o.a.post(s+"/api/tool/anonymization",t,e).then(e=>e.data),fe=(e,t)=>o.a.post(s+"/api/tool/enable_duration",t,e).then(e=>e.data),he=(e,t)=>o.a.post(s+"/api/tool/disable_duration",t,e).then(e=>e.data),be=(e,t)=>o.a.get(s+"/api/tool/duration_verify",{params:t},{headers:e}).then(e=>e.data),ve=(e,t)=>o.a.get(s+"/api/tool/somkerecord",{params:t},{headers:e}).then(e=>e.data),ge=(e,t)=>o.a.post(s+"/api/tool/somke",t,e).then(e=>e.data),ye=(e,t)=>o.a.post(s+"/api/tool/dicomSend",t,e).then(e=>e.data),_e=(e,t)=>o.a.get(s+"/api/base/getdata",{params:t},{headers:e}).then(e=>e.data),ke=(e,t)=>o.a.post(s+"/api/base/addData",t,e).then(e=>e.data),we=(e,t)=>o.a.post(s+"/api/base/updateData",t,e).then(e=>e.data),xe=(e,t)=>o.a.post(s+"/api/base/enablebase",t,e).then(e=>e.data),Fe=(e,t)=>o.a.post(s+"/api/base/disablebase",t,e).then(e=>e.data),Te=(e,t)=>o.a.post(s+"/api/base/delbasedata",t,e).then(e=>e.data),$e=(e,t)=>o.a.get(s+"/api/base/dicom",{params:t},{headers:e}).then(e=>e.data)},3034:function(e,t,a){"use strict";a.r(t);var r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("section",[a("router-link",{staticStyle:{"text-decoration":"none",color:"aliceblue"},attrs:{to:{name:"接口列表",params:{project_id:this.$route.params.project_id}}}},[a("el-button",{staticClass:"return-list"},[a("i",{staticClass:"el-icon-d-arrow-left",staticStyle:{"margin-right":"5px"}}),e._v("接口列表")])],1),a("router-link",{staticStyle:{"text-decoration":"none",color:"aliceblue"},attrs:{to:{name:"接口列表",params:{project_id:this.$route.params.project_id}}}},[a("el-button",{staticClass:"return-list",staticStyle:{float:"right"}},[e._v("取消")])],1),a("el-button",{staticClass:"return-list",staticStyle:{float:"right","margin-right":"15px"},attrs:{type:"primary"},nativeOn:{click:function(t){return e.addApiInfo(t)}}},[e._v("保存")]),a("el-form",{ref:"form",attrs:{model:e.form,rules:e.FormRules}},[a("div",{staticStyle:{border:"1px solid #e6e6e6","margin-bottom":"10px",padding:"15px"}},[a("el-form-item",{attrs:{label:"接口分组:","label-width":"83px",prop:"apiGroupLevelFirst_id"}},[a("el-select",{attrs:{placeholder:"请选择分组"},model:{value:e.form.apiGroupLevelFirst_id,callback:function(t){e.$set(e.form,"apiGroupLevelFirst_id",t)},expression:"form.apiGroupLevelFirst_id"}},e._l(e.group,(function(e,t){return a("el-option",{key:t+"",attrs:{label:e.name,value:e.id}})})),1)],1),a("el-row",{attrs:{gutter:10}},[a("el-col",{attrs:{span:8}},[a("el-form-item",{attrs:{label:"接口名称:","label-width":"83px",prop:"name"}},[a("el-input",{attrs:{placeholder:"名称","auto-complete":""},model:{value:e.form.name,callback:function(t){e.$set(e.form,"name","string"===typeof t?t.trim():t)},expression:"form.name"}})],1)],1),a("el-col",{attrs:{span:10}},[a("el-form-item",{attrs:{label:"状态:","label-width":"72px"}},[a("el-select",{attrs:{placeholder:"接口状态"},model:{value:e.form.status,callback:function(t){e.$set(e.form,"status",t)},expression:"form.status"}},e._l(e.status,(function(e,t){return a("el-option",{key:t+"",attrs:{label:e.label,value:e.value}})})),1)],1)],1)],1),a("el-row",{attrs:{gutter:10}},[a("el-col",{attrs:{span:4}},[a("el-form-item",{attrs:{label:"URL:","label-width":"83px"}},[a("el-select",{attrs:{placeholder:"请求方式"},on:{change:e.checkRequest},model:{value:e.form.requestType,callback:function(t){e.$set(e.form,"requestType",t)},expression:"form.requestType"}},e._l(e.request,(function(e,t){return a("el-option",{key:t+"",attrs:{label:e.label,value:e.value}})})),1)],1)],1),a("el-col",{attrs:{span:2}},[a("el-form-item",[a("el-select",{attrs:{placeholder:"HTTP协议"},model:{value:e.form.httpType,callback:function(t){e.$set(e.form,"httpType",t)},expression:"form.httpType"}},e._l(e.Http,(function(e,t){return a("el-option",{key:t+"",attrs:{label:e.label,value:e.value}})})),1)],1)],1),a("el-col",{attrs:{span:18}},[a("el-form-item",{attrs:{prop:"apiAddress"}},[a("el-input",{attrs:{placeholder:"地址","auto-complete":""},model:{value:e.form.apiAddress,callback:function(t){e.$set(e.form,"apiAddress","string"===typeof t?t.trim():t)},expression:"form.apiAddress"}})],1)],1)],1)],1),a("el-row",{attrs:{span:24}},[a("el-collapse",{on:{change:e.handleChange},model:{value:e.activeNames,callback:function(t){e.activeNames=t},expression:"activeNames"}},[a("el-collapse-item",{attrs:{title:"请求头部",name:"1"}},[a("el-table",{attrs:{data:e.form.headDict,"highlight-current-row":""}},[a("el-table-column",{attrs:{prop:"name",label:"标签","min-width":"20%",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-select",{attrs:{placeholder:"head标签",filterable:""},model:{value:t.row.name,callback:function(a){e.$set(t.row,"name",a)},expression:"scope.row.name"}},e._l(e.header,(function(e,t){return a("el-option",{key:t+"",attrs:{label:e.label,value:e.value}})})),1),a("el-input",{staticClass:"selectInput",attrs:{value:t.row.name,placeholder:"请输入内容"},model:{value:t.row.name,callback:function(a){e.$set(t.row,"name","string"===typeof a?a.trim():a)},expression:"scope.row.name"}})]}}])}),a("el-table-column",{attrs:{prop:"value",label:"内容","min-width":"40%",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-input",{attrs:{value:t.row.value,placeholder:"请输入内容"},model:{value:t.row.value,callback:function(a){e.$set(t.row,"value","string"===typeof a?a.trim():a)},expression:"scope.row.value"}})]}}])}),a("el-table-column",{attrs:{label:"操作","min-width":"10%"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("i",{staticClass:"el-icon-delete",staticStyle:{"font-size":"30px",cursor:"pointer"},on:{click:function(a){return e.delHead(t.$index)}}})]}}])}),a("el-table-column",{attrs:{label:"","min-width":"10%"},scopedSlots:e._u([{key:"default",fn:function(t){return[t.$index===e.form.headDict.length-1?a("el-button",{staticClass:"el-icon-plus",attrs:{size:"mini"},on:{click:e.addHead}}):e._e()]}}])})],1)],1),a("el-collapse-item",{attrs:{title:"请求参数",name:"2"}},[a("div",{staticStyle:{margin:"5px"}},[a("el-row",{attrs:{span:24}},[a("el-col",{attrs:{span:4}},[a("el-radio",{attrs:{label:"form-data"},model:{value:e.radio,callback:function(t){e.radio=t},expression:"radio"}},[e._v("表单(form-data)")])],1),e.request3?a("el-col",{attrs:{span:4}},[a("el-radio",{attrs:{label:"raw"},model:{value:e.radio,callback:function(t){e.radio=t},expression:"radio"}},[e._v("源数据(raw)")])],1):e._e(),e.request3?a("el-col",{attrs:{span:16}},[a("el-checkbox",{directives:[{name:"show",rawName:"v-show",value:e.ParameterTyep,expression:"ParameterTyep"}],attrs:{label:"3"},model:{value:e.radioType,callback:function(t){e.radioType=t},expression:"radioType"}},[e._v("表单转源数据")])],1):e._e()],1)],1),a("el-table",{class:e.ParameterTyep?"parameter-a":"parameter-b",attrs:{data:e.form.requestList,"highlight-current-row":""}},[a("el-table-column",{attrs:{prop:"name",label:"参数名","min-width":"25%",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-input",{attrs:{value:t.row.name,placeholder:"请输入参数值"},model:{value:t.row.name,callback:function(a){e.$set(t.row,"name","string"===typeof a?a.trim():a)},expression:"scope.row.name"}})]}}])}),a("el-table-column",{attrs:{prop:"value",label:"参数值","min-width":"30%",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-input",{attrs:{value:t.row.value,placeholder:"请输入参数值"},model:{value:t.row.value,callback:function(a){e.$set(t.row,"value","string"===typeof a?a.trim():a)},expression:"scope.row.value"}})]}}])}),a("el-table-column",{attrs:{prop:"_type",label:"参数类型","min-width":"14%",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-select",{attrs:{placeholder:"请求方式"},model:{value:t.row._type,callback:function(a){e.$set(t.row,"_type",a)},expression:"scope.row._type"}},e._l(e.paramTyep,(function(e,t){return a("el-option",{key:t+"",attrs:{label:e.label,value:e.value}})})),1)]}}])}),a("el-table-column",{attrs:{prop:"description",label:"参数说明","min-width":"14%",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-input",{attrs:{value:t.row.desc,placeholder:"请输入参数说明"},model:{value:t.row.description,callback:function(a){e.$set(t.row,"description","string"===typeof a?a.trim():a)},expression:"scope.row.description"}})]}}])}),a("el-table-column",{attrs:{label:"操作","min-width":"13%"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("i",{staticClass:"el-icon-delete",staticStyle:{"font-size":"30px",cursor:"pointer"},on:{click:function(a){return e.delParameter(t.$index)}}}),a("el-button",{staticStyle:{"margin-bottom":"5px"},attrs:{type:"primary",size:"mini"},on:{click:function(a){return e.handleParameterEdit(t.$index,t.row)}}},[e._v("更多设置")])]}}])}),a("el-table-column",{attrs:{label:"","min-width":"4%"},scopedSlots:e._u([{key:"default",fn:function(t){return[t.$index===e.form.requestList.length-1?a("el-button",{staticClass:"el-icon-plus",attrs:{size:"mini"},on:{click:e.addParameter}}):e._e()]}}])})],1),[a("el-input",{class:e.ParameterTyep?"parameter-b":"parameter-a",attrs:{type:"textarea",rows:5,placeholder:"请输入内容"},model:{value:e.parameterRaw,callback:function(t){e.parameterRaw="string"===typeof t?t.trim():t},expression:"parameterRaw"}})]],2),a("el-dialog",{attrs:{title:"更多设置",visible:e.addParameterFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(t){e.addParameterFormVisible=t}}},[a("el-form",{ref:"editForm",attrs:{model:e.editForm,"label-width":"60px",rules:e.FormRules}},[a("el-form-item",{attrs:{label:"参数名","label-width":"83px"}},[a("el-input",{attrs:{"auto-complete":"off",placeholder:"请输入参数名称"},model:{value:e.editForm.name,callback:function(t){e.$set(e.editForm,"name","string"===typeof t?t.trim():t)},expression:"editForm.name"}})],1),a("el-form-item",{attrs:{label:"参数值","label-width":"83px"}},[a("el-input",{attrs:{"auto-complete":"off",placeholder:"请输入参数值"},model:{value:e.editForm.value,callback:function(t){e.$set(e.editForm,"value","string"===typeof t?t.trim():t)},expression:"editForm.value"}})],1),a("el-form-item",{attrs:{label:"必填?","label-width":"83px",prop:"required"}},[a("el-select",{attrs:{placeholder:"必填？"},model:{value:e.editForm.required,callback:function(t){e.$set(e.editForm,"required",t)},expression:"editForm.required"}},e._l(e.required4,(function(e,t){return a("el-option",{key:t+"",attrs:{label:e.label,value:e.value}})})),1)],1),a("el-form-item",{attrs:{label:"输入限制",prop:"version","label-width":"83px"}},[a("el-input",{attrs:{"auto-complete":"off",placeholder:"请输入输入限制"},model:{value:e.editForm.restrict,callback:function(t){e.$set(e.editForm,"restrict","string"===typeof t?t.trim():t)},expression:"editForm.restrict"}})],1),a("el-form-item",{attrs:{label:"描述",prop:"description","label-width":"83px"}},[a("el-input",{attrs:{type:"textarea",rows:7,placeholder:"请输入描述"},model:{value:e.editForm.description,callback:function(t){e.$set(e.editForm,"description","string"===typeof t?t.trim():t)},expression:"editForm.description"}})],1)],1),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{nativeOn:{click:function(t){e.addParameterFormVisible=!1}}},[e._v("取消")]),a("el-button",{attrs:{type:"primary"},nativeOn:{click:function(t){return e.editParameterSubmit(t)}}},[e._v("保存")])],1)],1),a("el-collapse-item",{attrs:{title:"返回参数",name:"3"}},[a("el-table",{attrs:{data:e.form.responseList,"highlight-current-row":""}},[a("el-table-column",{attrs:{prop:"name",label:"参数名","min-width":"25%",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-input",{attrs:{value:t.row.name,placeholder:"请输入参数值"},model:{value:t.row.name,callback:function(a){e.$set(t.row,"name","string"===typeof a?a.trim():a)},expression:"scope.row.name"}})]}}])}),a("el-table-column",{attrs:{prop:"value",label:"参数值","min-width":"30%",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-input",{attrs:{value:t.row.value,placeholder:"请输入参数值"},model:{value:t.row.value,callback:function(a){e.$set(t.row,"value","string"===typeof a?a.trim():a)},expression:"scope.row.value"}})]}}])}),a("el-table-column",{attrs:{prop:"_type",label:"参数类型","min-width":"14%",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-select",{attrs:{placeholder:"请求方式"},model:{value:t.row._type,callback:function(a){e.$set(t.row,"_type",a)},expression:"scope.row._type"}},e._l(e.paramTyep,(function(e,t){return a("el-option",{key:t+"",attrs:{label:e.label,value:e.value}})})),1)]}}])}),a("el-table-column",{attrs:{prop:"description",label:"参数说明","min-width":"14%",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-input",{attrs:{value:t.row.desc,placeholder:"请输入参数说明"},model:{value:t.row.description,callback:function(a){e.$set(t.row,"description","string"===typeof a?a.trim():a)},expression:"scope.row.description"}})]}}])}),a("el-table-column",{attrs:{label:"操作","min-width":"13%"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("i",{staticClass:"el-icon-delete",staticStyle:{"font-size":"30px",cursor:"pointer"},on:{click:function(a){return e.delResponse(t.$index)}}}),a("el-button",{staticStyle:{"margin-bottom":"5px"},attrs:{type:"primary",size:"mini"},on:{click:function(a){return e.handleResponseEdit(t.$index,t.row)}}},[e._v("更多设置")])]}}])}),a("el-table-column",{attrs:{label:"","min-width":"4%"},scopedSlots:e._u([{key:"default",fn:function(t){return[t.$index===e.form.responseList.length-1?a("el-button",{staticClass:"el-icon-plus",attrs:{size:"mini"},on:{click:e.addResponse}}):e._e()]}}])})],1)],1),a("el-dialog",{attrs:{title:"更多设置",visible:e.addResponseFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(t){e.addResponseFormVisible=t}}},[a("el-form",{ref:"editForm",attrs:{model:e.editForm,"label-width":"60px",rules:e.FormRules}},[a("el-form-item",{attrs:{label:"参数名",prop:"name","label-width":"83px"}},[a("el-input",{attrs:{"auto-complete":"off",placeholder:"请输入参数名称"},model:{value:e.editForm.name,callback:function(t){e.$set(e.editForm,"name","string"===typeof t?t.trim():t)},expression:"editForm.name"}})],1),a("el-form-item",{attrs:{label:"参数值",prop:"name","label-width":"83px"}},[a("el-input",{attrs:{"auto-complete":"off",placeholder:"请输入参数值"},model:{value:e.editForm.value,callback:function(t){e.$set(e.editForm,"value","string"===typeof t?t.trim():t)},expression:"editForm.value"}})],1),a("el-form-item",{attrs:{label:"必填?","label-width":"83px",prop:"required"}},[a("el-select",{attrs:{placeholder:"必填？"},model:{value:e.editForm.required,callback:function(t){e.$set(e.editForm,"required",t)},expression:"editForm.required"}},e._l(e.required4,(function(e,t){return a("el-option",{key:t+"",attrs:{label:e.label,value:e.value}})})),1)],1),a("el-form-item",{attrs:{label:"描述",prop:"description","label-width":"83px"}},[a("el-input",{attrs:{type:"textarea",rows:7,placeholder:"请输入描述"},model:{value:e.editForm.description,callback:function(t){e.$set(e.editForm,"description","string"===typeof t?t.trim():t)},expression:"editForm.description"}})],1)],1),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{nativeOn:{click:function(t){e.addResponseFormVisible=!1}}},[e._v("取消")]),a("el-button",{attrs:{type:"primary"},nativeOn:{click:function(t){return e.editResponseSubmit(t)}}},[e._v("保存")])],1)],1),a("el-collapse-item",{attrs:{title:"普通mock",name:"4"}},[a("el-card",{staticClass:"box-card"},[a("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[a("el-select",{attrs:{placeholder:"HTTP状态"},model:{value:e.form.mockCode,callback:function(t){e.$set(e.form,"mockCode",t)},expression:"form.mockCode"}},e._l(e.httpCode,(function(e,t){return a("el-option",{key:t+"",attrs:{label:e.label,value:e.value}})})),1)],1),a("el-input",{attrs:{type:"textarea",rows:8,placeholder:"请输入mock内容"},model:{value:e.form.data,callback:function(t){e.$set(e.form,"data","string"===typeof t?t.trim():t)},expression:"form.data"}})],1)],1)],1)],1)],1)],1)},o=[],s=a("2d92"),l={data(){return{request:[{value:"GET",label:"GET"},{value:"POST",label:"POST"},{value:"PUT",label:"PUT"},{value:"DELETE",label:"DELETE"}],Http:[{value:"HTTP",label:"HTTP"},{value:"HTTPS",label:"HTTPS"}],paramTyep:[{value:"Int",label:"Int"},{value:"String",label:"String"}],checkHeadList:[],checkParameterList:[],ParameterTyep:!0,group:[],radio:"form-data",secondGroup:[],status:[{value:!0,label:"启用"},{value:!1,label:"禁用"}],header:[{value:"Accept",label:"Accept"},{value:"Accept-Charset",label:"Accept-Charset"},{value:"Accept-Encoding",label:"Accept-Encoding"},{value:"Accept-Language",label:"Accept-Language"},{value:"Accept-Ranges",label:"Accept-Ranges"},{value:"Authorization",label:"Authorization"},{value:"Cache-Control",label:"Cache-Control"},{value:"Connection",label:"Connection"},{value:"Cookie",label:"Cookie"},{value:"Content-Length",label:"Content-Length"},{value:"Content-Type",label:"Content-Type"},{value:"Content-MD5",label:"Content-MD5"},{value:"Date",label:"Date"},{value:"Expect",label:"Expect"},{value:"From",label:"From"},{value:"Host",label:"Host"},{value:"If-Match",label:"If-Match"},{value:"If-Modified-Since",label:"If-Modified-Since"},{value:"If-None-Match",label:"If-None-Match"},{value:"If-Range",label:"If-Range"},{value:"If-Unmodified-Since",label:"If-Unmodified-Since"},{value:"Max-Forwards",label:"Max-Forwards"},{value:"Origin",label:"Origin"},{value:"Pragma",label:"Pragma"},{value:"Proxy-Authorization",label:"Proxy-Authorization"},{value:"Range",label:"Range"},{value:"Referer",label:"Referer"},{value:"TE",label:"TE"},{value:"Upgrade",label:"Upgrade"},{value:"User-Agent",label:"User-Agent"},{value:"Via",label:"Via"},{value:"Warning",label:"Warning"}],header4:"",addParameterFormVisible:!1,addResponseFormVisible:!1,required4:[{value:!0,label:"是"},{value:!1,label:"否"}],httpCode:[{value:"",label:""},{value:"200",label:"200"},{value:"404",label:"404"},{value:"400",label:"400"},{value:"500",label:"500"},{value:"502",label:"502"},{value:"302",label:"302"}],radioType:"",result:!0,activeNames:["1","2","3","4"],id:"",parameterRaw:"",request3:!0,form:{apiGroupLevelFirst_id:"",name:"",status:!0,requestType:"POST",httpType:"HTTP",apiAddress:"",headDict:[{name:"",value:""},{name:"",value:""}],requestList:[{name:"",value:"",_type:"String",required:!0,restrict:"",description:""},{name:"",value:"",_type:"String",required:!0,restrict:"",description:""}],requestParameterType:"",responseList:[{name:"",value:"",_type:"String",required:!0,description:""},{name:"",value:"",_type:"String",required:!0,description:""}],mockCode:"",data:""},FormRules:{name:[{required:!0,message:"请输入名称",trigger:"blur"},{max:50,message:"不能超过50个字",trigger:"blur"}],apiAddress:[{required:!0,message:"请输入地址",trigger:"blur"}],required:[{type:"boolean",required:!0,message:"请选择状态",trigger:"blur"}],apiGroupLevelFirst_id:[{type:"number",required:!0,message:"请选择分组",trigger:"blur"}]},editForm:{name:"",value:"",required:"",restrict:"",description:""}}},methods:{checkRequest(){let e=this.form.requestType;this.request3="GET"!==e&&"DELETE"!==e},isJsonString(e){try{if("object"===typeof JSON.parse(e))return!0}catch(t){}return!1},addApiInfo:function(){this.form.data&&this.form.mockCode?this.isJsonString(this.form.data)?this.addApi():this.$message({message:"mock格式错误",center:!0,type:"error"}):this.form.data||this.form.mockCode?this.$message({message:"HTTP状态或mock为空",center:!0,type:"warning"}):this.addApi()},addApi:function(){this.$refs.form.validate(e=>{if(e){let e=this;console.log(this.form.requestList),this.$confirm("确认提交吗？","提示",{}).then(()=>{e.form.parameterType=e.radio;let t=e.form.parameterType,a={};"form-data"===t?!0===e.radioType?(t="raw",e.form.requestList.forEach(e=>{e.name&&(a[e.name]=e.value)}),a=JSON.stringify(a)):a=e.form.requestList:a=e.parameterRaw,console.log(a);let r={project_id:Number(e.$route.params.project_id),apiGroupLevelFirst_id:Number(e.form.apiGroupLevelFirst_id),name:e.form.name,httpType:e.form.httpType,requestType:e.form.requestType,apiAddress:e.form.apiAddress,status:e.form.status,headDict:e.form.headDict,requestParameterType:t,requestList:a,responseList:e.form.responseList,mockCode:e.form.mockCode,data:e.form.data,description:""},o={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};e.parameterRaw&&"raw"===t?e.isJsonString(e.parameterRaw)?Object(s["g"])(o,r).then(t=>{let{msg:a,code:r,data:o}=t;"0"===r?(e.$router.push({name:"分组接口列表",params:{project_id:e.$route.params.project_id,firstGroup:e.form.apiGroupLevelFirst_id}}),e.$message({message:"保存成功",center:!0,type:"success"})):e.$message.error({message:a,center:!0})}):e.$message({message:"源数据格式错误",center:!0,type:"error"}):Object(s["g"])(o,r).then(t=>{let{msg:a,code:r,data:o}=t;"0"===r?(e.$router.push({name:"分组接口列表",params:{project_id:e.$route.params.project_id,firstGroup:e.form.apiGroupLevelFirst_id}}),e.$message({message:"保存成功",center:!0,type:"success"})):e.$message.error({message:a,center:!0})})})}})},editParameterSubmit:function(){this.$refs.editForm.validate(e=>{e&&(this.form.requestList[this.id]=this.editForm,this.addParameterFormVisible=!1)})},handleParameterEdit:function(e,t){this.addParameterFormVisible=!0,this.id=e,this.editForm=Object.assign({},t)},editResponseSubmit:function(){this.$refs.editForm.validate(e=>{e&&(this.form.responseList[this.id]=this.editForm,this.addResponseFormVisible=!1)})},handleResponseEdit:function(e,t){this.addResponseFormVisible=!0,this.id=e,this.editForm=Object.assign({},t)},getApiGroup(){let e=this,t={project_id:this.$route.params.project_id},a={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};Object(s["N"])(a,t).then(t=>{let{msg:a,code:r,data:o}=t;"0"===r?(e.group=o,e.form.apiGroupLevelFirst_id=e.group[0].id):e.$message.error({message:a,center:!0})})},addHead(){let e={name:"",value:""};this.form.headDict.push(e)},delHead(e){this.form.headDict.splice(e,1),0===this.form.headDict.length&&this.form.headDict.push({name:"",value:""})},addParameter(){let e={name:"",value:"",_type:"String",required:!0,restrict:"",description:""};this.form.requestList.push(e)},delParameter(e){this.form.requestList.splice(e,1),0===this.form.requestList.length&&this.form.requestList.push({name:"",value:"",_type:"String",required:!0,restrict:"",description:""})},addResponse(){let e={name:"",value:"",_type:"String",required:!0,description:""};this.form.responseList.push(e)},delResponse(e){this.form.responseList.splice(e,1),0===this.form.responseList.length&&this.form.responseList.push({name:"",value:"",_type:"String",required:!0,description:""})},changeParameterType(){"form-data"===this.radio?this.ParameterTyep=!0:this.ParameterTyep=!1},showData(){this.result=!0},showHead(){this.result=!1},handleChange(e){},onSubmit(){console.log("submit!")},fastAdd(){let e=this.$route.params.formData,t=this.$route.params._type,a=this.$route.params._typeData;e&&(this.form.requestList=[],this.form.requestType=e.request4.toUpperCase(),this.form.httpType=e.Http4,this.form.apiAddress=e.addr,this.form.headDict=e.head,this.form.parameterRaw=e.parameterRaw,e.parameter.forEach(e=>{e["_type"]="String",e["required"]=!0,e["restrict"]="",e["description"]="",this.form.requestList.push(e)}),this.form.mockCode=e.statusCode,this.form.data=JSON.stringify(e.resultData)),t&&(this.radio=t),a&&(this.radioType=a)}},watch:{radio(){this.changeParameterType()}},mounted(){this.getApiGroup(),this.fastAdd()}},i=l,n=(a("c042"),a("e640"),a("2877")),u=Object(n["a"])(i,r,o,!1,null,"58a229fd",null);t["default"]=u.exports},"41d3":function(e,t,a){},c042:function(e,t,a){"use strict";var r=a("fc29"),o=a.n(r);o.a},c896:function(e,t,a){"use strict";var r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("div",{staticClass:"crumbs"},[a("el-breadcrumb",{attrs:{separator:"/"}},[a("el-breadcrumb-item",[a("i",{staticClass:"el-icon-lx-calendar"}),e._v(" 测试工具")]),a("el-breadcrumb-item",[e._v("推送工具")])],1)],1),a("div",{staticClass:"container"},[a("div",{staticClass:"form-box"},[a("el-form",{ref:"form",attrs:{model:e.form,"status-icon":"",rules:e.rules,"label-width":"80px"}},[a("el-form-item",{attrs:{label:"推送ID",prop:"pushID"}},[a("el-col",{attrs:{span:10}},[a("el-input",{attrs:{id:"pushID"},model:{value:e.form.pushID,callback:function(t){e.$set(e.form,"pushID",t)},expression:"form.pushID"}})],1)],1),a("el-form-item",{attrs:{label:"推送环境",prop:"environment"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.form.environment,callback:function(t){e.$set(e.form,"environment",t)},expression:"form.environment"}},[a("el-option",{key:"test",attrs:{label:"测试环境",value:"test"}}),a("el-option",{key:"online",attrs:{label:"线上环境",value:"online"}})],1)],1),a("el-form-item",{attrs:{label:"推送类型",prop:"types"}},[a("el-cascader",{attrs:{options:e.types},on:{change:function(t){return e.changeLang("form")}},model:{value:e.form.types,callback:function(t){e.$set(e.form,"types",t)},expression:"form.types"}})],1),a("el-form-item",{attrs:{label:"选择语言",prop:"languages"}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.form.languages,callback:function(t){e.$set(e.form,"languages",t)},expression:"form.languages"}},e._l(e.languages,(function(e,t){return a("el-option",{key:e.key,attrs:{label:e.value,value:e.key}})})),1)],1),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.onSubmit("form")}}},[e._v("确定推送")]),a("el-button",{on:{click:function(t){return e.resetForm("form")}}},[e._v("重置")])],1)],1)],1)])])},o=[],s={name:"baseform",data:function(){return{types:[{value:"bishijie",label:"Boimind",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"replay",label:"币圈"},{value:"monitor",label:"盯盘"}]},{value:"coinness",label:"coinness",children:[{value:"news",label:"快讯"},{value:"shendu",label:"深度"},{value:"monitor",label:"盯盘"}]}],languages:[],form:{pushID:"",environment:"",types:[],languages:[]},rules:{pushID:[{required:!0,message:"请输入推送ID",trigger:"blur"}],environment:[{required:!0,message:"请选择推送环境",trigger:"blur"}],types:[{required:!0,message:"请选择推送类型",trigger:"blur"}],languages:[{required:!0,message:"请选择语言",trigger:"blur"}]}}},methods:{onSubmit(e){this.$refs[e].validate(e=>{if(!e)return console.log("error submit"),!1;console.log("语言："+this.form.languages),console.log("pushID："+this.form.pushID),console.log("APP："+this.form.types[0]),console.log("推送类型："+this.form.types[1]),console.log("environment："+this.form.environment),this.$ajax.post("/bishijie/push",{id:this.form.pushID,service:this.form.environment,system:this.form.types[0],module:this.form.types[1],lang:this.form.languages,rid:""}).then(e=>{"0"==e.data.code?null==e.data.data||e.data.data[0]?this.$message.success("push成功！"):this.$message.error(e.data.data[1]):this.$message.error(e.data.msg)}).catch((function(e){console.log(e)}))})},resetForm(e){this.$refs[e].resetFields()},changeLang(e){this.languages=[],this.form.languages="";var t=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"}],a=[{key:"zh_cn",value:"简体中文"},{key:"zh_tw",value:"繁体"},{key:"en_go",value:"English"},{key:"ko_kr",value:"한글"}],r=this.form.types[0].toLowerCase();"bishijie"==r?this.languages=t:"coinness"==r&&(this.languages=a)}}},l=s,i=(a("cd97"),a("2877")),n=Object(i["a"])(l,r,o,!1,null,"6d8efc95",null);n.exports},cd97:function(e,t,a){"use strict";var r=a("41d3"),o=a.n(r);o.a},cfff:function(e,t,a){},e640:function(e,t,a){"use strict";var r=a("cfff"),o=a.n(r);o.a},fc29:function(e,t,a){}}]);