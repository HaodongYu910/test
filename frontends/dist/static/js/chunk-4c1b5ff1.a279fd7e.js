(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-4c1b5ff1"],{"0ee8":function(t,e,s){"use strict";var l=s("e9fb"),i=s.n(l);i.a},2087:function(t,e,s){},7159:function(t,e,s){t.exports=s.p+"static/img/img.132d6025.jpg"},b4a8:function(t,e,s){"use strict";var l=s("ba7f"),i=s.n(l);i.a},ba7f:function(t,e,s){},bfe9:function(t,e,s){"use strict";s.r(e);var l=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"wrapper"},[s("v-head"),s("v-sidebar"),s("div",{staticClass:"content-box",class:{"content-collapse":t.collapse}},[s("v-tags"),s("div",{staticClass:"content"},[s("transition",{attrs:{name:"move",mode:"out-in"}},[s("keep-alive",{attrs:{include:t.tagsList}},[s("router-view")],1)],1)],1)],1)],1)},i=[],a=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"header"},[s("div",{staticClass:"collapse-btn",on:{click:t.collapseChage}},[s("i",{staticClass:"el-icon-menu"})]),s("div",{staticClass:"logo"},[t._v("Biomind Test Platform")]),s("div",{staticClass:"header-right"},[s("div",{staticClass:"header-user-con"},[s("div",{staticClass:"btn-fullscreen",on:{click:t.handleFullScreen}},[s("el-tooltip",{attrs:{effect:"dark",content:t.fullscreen?"取消全屏":"全屏",placement:"bottom"}},[s("i",{staticClass:"el-icon-rank"})])],1),s("div",{staticClass:"btn-bell"},[s("el-tooltip",{attrs:{effect:"dark",content:t.message?"有"+t.message+"条未读消息":"消息中心",placement:"bottom"}},[s("router-link",{attrs:{to:"/tabs"}},[s("i",{staticClass:"el-icon-bell"})])],1),t.message?s("span",{staticClass:"btn-bell-badge"}):t._e()],1),t._m(0),s("el-dropdown",{staticClass:"user-name",attrs:{trigger:"click"},on:{command:t.handleCommand}},[s("span",{staticClass:"el-dropdown-link"},[t._v(" "+t._s(t.username)+" "),s("i",{staticClass:"el-icon-caret-bottom"})]),s("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},[s("a",{attrs:{href:"",target:"_blank"}},[s("el-dropdown-item",[t._v("设置")])],1),s("el-dropdown-item",{attrs:{divided:"",command:"loginout"}},[t._v("退出登录")])],1)],1)],1)])])},n=[function(){var t=this,e=t.$createElement,l=t._self._c||e;return l("div",{staticClass:"user-avator"},[l("img",{attrs:{src:s("7159")}})])}],o=s("2b0e");const c=new o["default"];var r=c,u={data(){return{collapse:!1,fullscreen:!1,name:"linxin",message:2}},computed:{username(){let t=localStorage.getItem("ms_username");return t||this.name}},methods:{handleCommand(t){"loginout"==t&&(localStorage.removeItem("ms_username"),this.$router.push("/login"))},collapseChage(){this.collapse=!this.collapse,r.$emit("collapse",this.collapse)},handleFullScreen(){let t=document.documentElement;this.fullscreen?document.exitFullscreen?document.exitFullscreen():document.webkitCancelFullScreen?document.webkitCancelFullScreen():document.mozCancelFullScreen?document.mozCancelFullScreen():document.msExitFullscreen&&document.msExitFullscreen():t.requestFullscreen?t.requestFullscreen():t.webkitRequestFullScreen?t.webkitRequestFullScreen():t.mozRequestFullScreen?t.mozRequestFullScreen():t.msRequestFullscreen&&t.msRequestFullscreen(),this.fullscreen=!this.fullscreen}},mounted(){document.body.clientWidth<1500&&this.collapseChage()}},d=u,m=(s("0ee8"),s("2877")),h=Object(m["a"])(d,a,n,!1,null,"40171712",null),p=h.exports,g=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"sidebar"},[s("el-menu",{staticClass:"sidebar-el-menu",attrs:{"default-active":t.onRoutes,collapse:t.collapse,"background-color":"#324157","text-color":"#bfcbd9","active-text-color":"#20a0ff","unique-opened":"",router:""}},[t._l(t.items,(function(e){return[e.subs?[s("el-submenu",{key:e.index,attrs:{index:e.index}},[s("template",{slot:"title"},[s("i",{class:e.icon}),s("span",{attrs:{slot:"title"},slot:"title"},[t._v(t._s(e.title))])]),t._l(e.subs,(function(e){return[e.subs?s("el-submenu",{key:e.index,attrs:{index:e.index}},[s("template",{slot:"title"},[t._v(t._s(e.title))]),t._l(e.subs,(function(e,l){return s("el-menu-item",{key:l,attrs:{index:e.index}},[t._v(" "+t._s(e.title)+" ")])}))],2):s("el-menu-item",{key:e.index,attrs:{index:e.index}},[t._v(" "+t._s(e.title)+" ")])]}))],2)]:[s("el-menu-item",{key:e.index,attrs:{index:e.index}},[s("i",{class:e.icon}),s("span",{attrs:{slot:"title"},slot:"title"},[t._v(t._s(e.title))])])]]}))],2)],1)},f=[],b={data(){return{collapse:!1,items:[{icon:"el-icon-s-home",index:"home",title:"系统首页"},{icon:"el-icon-s-platform",index:"project",title:"项目",subs:[{index:"project",title:"项目列表"},{index:"host",title:"Host配置"},{index:"data",title:"自动化测试报告"}]},{icon:"el-icon-s-help",index:"3",title:"测试工具",subs:[{index:"data",title:"测试数据"},{index:"dicom",title:"dicom工具"},{index:"stress",title:"性能工具"}]},{icon:"el-icon-message",index:"4",title:"邮件管理",subs:[{index:"testreport",title:"邮件配置"}]},{icon:"el-icon-s-tools",index:"5",title:"系统设置",subs:[{index:"qrcode",title:"用户配置"},{index:"mailconfig",title:"其他配置"}]},{icon:"el-icon-message-solid",index:"tabs",title:"消息中心"}]}},computed:{onRoutes(){return this.$route.path.replace("/","")}},created(){r.$on("collapse",t=>{this.collapse=t})}},v=b,x=(s("b4a8"),Object(m["a"])(v,g,f,!1,null,"3bcb0c4c",null)),_=x.exports,C=function(){var t=this,e=t.$createElement,s=t._self._c||e;return t.showTags?s("div",{staticClass:"tags"},[s("ul",t._l(t.tagsList,(function(e,l){return s("li",{key:l,staticClass:"tags-li",class:{active:t.isActive(e.path)}},[s("router-link",{staticClass:"tags-li-title",attrs:{to:e.path}},[t._v(" "+t._s(e.title)+" ")]),s("span",{staticClass:"tags-li-icon",on:{click:function(e){return t.closeTags(l)}}},[s("i",{staticClass:"el-icon-close"})])],1)})),0),s("div",{staticClass:"tags-close-box"},[s("el-dropdown",{on:{command:t.handleTags}},[s("el-button",{attrs:{size:"mini",type:"primary"}},[t._v(" 标签选项"),s("i",{staticClass:"el-icon-arrow-down el-icon--right"})]),s("el-dropdown-menu",{attrs:{slot:"dropdown",size:"small"},slot:"dropdown"},[s("el-dropdown-item",{attrs:{command:"other"}},[t._v("关闭其他")]),s("el-dropdown-item",{attrs:{command:"all"}},[t._v("关闭所有")])],1)],1)],1)]):t._e()},w=[],k={data(){return{tagsList:[]}},methods:{isActive(t){return t===this.$route.fullPath},closeTags(t){const e=this.tagsList.splice(t,1)[0],s=this.tagsList[t]?this.tagsList[t]:this.tagsList[t-1];s?e.path===this.$route.fullPath&&this.$router.push(s.path):this.$router.push("/")},closeAll(){this.tagsList=[],this.$router.push("/")},closeOther(){const t=this.tagsList.filter(t=>t.path===this.$route.fullPath);this.tagsList=t},setTags(t){const e=this.tagsList.some(e=>e.path===t.fullPath);e||(this.tagsList.length>=8&&this.tagsList.shift(),this.tagsList.push({title:t.meta.title,path:t.fullPath,name:t.matched[1].components.default.name})),r.$emit("tags",this.tagsList)},handleTags(t){"other"===t?this.closeOther():this.closeAll()}},computed:{showTags(){return this.tagsList.length>0}},watch:{$route(t,e){this.setTags(t)}},created(){this.setTags(this.$route),r.$on("close_current_tags",()=>{for(let t=0,e=this.tagsList.length;t<e;t++){const s=this.tagsList[t];s.path===this.$route.fullPath&&(t<e-1?this.$router.push(this.tagsList[t+1].path):t>0?this.$router.push(this.tagsList[t-1].path):this.$router.push("/"),this.tagsList.splice(t,1))}})}},$=k,L=(s("c5f3"),Object(m["a"])($,C,w,!1,null,null,null)),F=L.exports,S={data(){return{tagsList:[],collapse:!1}},components:{vHead:p,vSidebar:_,vTags:F},created(){r.$on("collapse",t=>{this.collapse=t}),r.$on("tags",t=>{let e=[];for(let s=0,l=t.length;s<l;s++)t[s].name&&e.push(t[s].name);this.tagsList=e})}},T=S,q=Object(m["a"])(T,l,i,!1,null,null,null);e["default"]=q.exports},c5f3:function(t,e,s){"use strict";var l=s("2087"),i=s.n(l);i.a},e9fb:function(t,e,s){}}]);