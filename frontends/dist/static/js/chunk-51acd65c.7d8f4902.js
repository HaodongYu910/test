(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-51acd65c"],{4779:function(t,e,a){"use strict";var l=a("8ecd"),o=a.n(l);o.a},"8ecd":function(t,e,a){},aa99:function(t,e,a){"use strict";a.r(e);var l=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("section",[a("el-button",{staticClass:"return-list",on:{click:t.back}},[a("i",{staticClass:"el-icon-d-arrow-left",staticStyle:{"margin-right":"5px"}}),t._v("用例列表")]),a("div",{staticClass:"number-pass",staticStyle:{"background-color":"#43CD80"}},[a("div",{staticStyle:{"font-size":"40px","padding-top":"15px"}},[t._v(t._s(t.pass))]),a("div",[t._v("Passed")])]),a("div",{staticClass:"number-fail",staticStyle:{"background-color":"#DC143C"}},[a("div",{staticStyle:{"font-size":"40px","padding-top":"15px"}},[t._v(t._s(t.fail))]),a("div",[t._v("Failed")])]),a("div",{staticClass:"number-error",staticStyle:{"background-color":"#DC143C"}},[a("div",{staticStyle:{"font-size":"40px","padding-top":"15px"}},[t._v(t._s(t.error))]),a("div",[t._v("Error")])]),a("div",{staticClass:"number-total"},[a("div",{staticStyle:{"font-size":"40px","padding-top":"15px"}},[t._v(t._s(t.total))]),a("div",[t._v("Total")])]),a("div",[a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.listLoading,expression:"listLoading"}],attrs:{data:t.tableData,"row-style":t.tableRowStyle},on:{"expand-change":t.showJson}},[a("el-table-column",{attrs:{type:"expand"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("el-form",{staticClass:"demo-table-expand",attrs:{"label-position":"left",inline:""}},[a("el-form-item",{attrs:{label:"名称: "}},[a("span",[t._v(t._s(e.row.name))])]),a("el-form-item"),a("el-form-item",{attrs:{label:"测试环境： "}},[a("span",[t._v(t._s(e.row.host))])]),a("el-form-item",{attrs:{label:"接口地址： "}},[a("span",[t._v(t._s(e.row.apiAddress))])]),a("el-form-item",{attrs:{label:"请求方式： "}},[a("span",[t._v(t._s(e.row.requestType))])]),a("el-form-item",{attrs:{label:"测试结果： "}},[a("span",[t._v(t._s(e.row.result))])]),a("el-form-item",{attrs:{label:"请求参数： "}},[a("span",{staticStyle:{"word-break":"break-all",overflow:"auto","overflow-x":"hidden"}},[t._v(t._s(e.row.parameter))])]),a("el-form-item",{attrs:{label:"测试时间"}},[a("span",[t._v(t._s(e.row.testTime))])]),a("el-form-item",{attrs:{label:"返回结果： "}},[a("span",[a("pre",{directives:[{name:"highlightA",rawName:"v-highlightA"}],staticStyle:{"word-break":"break-all",overflow:"auto","overflow-x":"hidden"}},[a("code",[t._v(t._s(e.row.responseData))])])])])],1)]}}])}),a("el-table-column",{attrs:{type:"index",label:"#",width:"100"}}),a("el-table-column",{attrs:{prop:"name",label:"接口名称","min-width":"27%",sortable:"","show-overflow-tooltip":""}}),a("el-table-column",{attrs:{prop:"automationTestCase",label:"用例名称","min-width":"29%",sortable:"","show-overflow-tooltip":""}}),a("el-table-column",{attrs:{prop:"apiAddress",label:"请求地址","min-width":"20%",sortable:"","show-overflow-tooltip":""}}),a("el-table-column",{attrs:{prop:"examineType",label:"校验方式","min-width":"13%",sortable:"","show-overflow-tooltip":""},scopedSlots:t._u([{key:"default",fn:function(e){return["no_check"===e.row.examineType?a("a",[t._v("不校验")]):t._e(),"only_check_status"===e.row.examineType?a("a",[t._v("校验http状态")]):t._e(),"json"===e.row.examineType?a("a",[t._v("JSON校验")]):t._e(),"entirely_check"===e.row.examineType?a("a",[t._v("完全校验")]):t._e(),"Regular_check"===e.row.examineType?a("a",[t._v("正则校验")]):t._e()]}}])}),a("el-table-column",{attrs:{prop:"result",label:"结果","min-width":"11%",filters:t.resultFilter,"filter-method":t.filterHandler},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v(" "+t._s(e.row.result?e.row.result:"NotRun")+" ")]}}])})],1)],1)],1)},o=[],r=a("2d92"),s=a("1157"),i=a.n(s),n={name:"test-report",data(){return{pass:"",fail:"",not_run:"",error:"",total:"",listLoading:!1,resultFilter:[{text:"ERROR",value:"ERROR"},{text:"FAIL",value:"FAIL"},{text:"NotRun",value:"NotRun"},{text:"PASS",value:"PASS"}],tableData:[]}},methods:{back(){this.$router.go(-1)},tableRowStyle(t){return"ERROR"===t.result||"FAIL"===t.result?"background-color: #DC143C;":"TimeOut"===t.result?"background-color: #FFE4C4;":void 0},filterHandler(t,e,a){return e.result===t},getTestResult(){this.listLoading=!0;let t=this;i.a.ajax({type:"get",url:r["Z"]+"/api/automation/test_report",async:!0,data:{project_id:this.$route.params.project_id},headers:{Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))},timeout:5e3,success:function(e){t.listLoading=!1,"0"===e.code?(t.total=e.data.total,t.pass=e.data.pass,t.fail=e.data.fail,t.not_run=e.data.NotRun,t.error=e.data.error,t.tableData=e.data.data,t.tableData.forEach(t=>{t["responseData"]=JSON.parse(t["responseData"].replace(/'/g,'"').replace(/None/g,"null").replace(/True/g,"true").replace(/False/g,"false"))})):t.$message.error({message:e.msg,center:!0})}})}},mounted(){this.getTestResult()}},d=n,p=(a("4779"),a("2877")),c=Object(p["a"])(d,l,o,!1,null,"20125906",null);e["default"]=c.exports}}]);