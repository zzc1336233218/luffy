// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import settings from "./settings";
Vue.config.productionTip = false

Vue.prototype.$settings = settings;

// elementUI 导入
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

// 调用插件
Vue.use(ElementUI);

import axios from 'axios'; // 从node_modules目录中导入包
// 允许ajax发送请求时附带cookie
axios.defaults.withCredentials = false;  // 阻止ajax附带cookie

Vue.prototype.$axios = axios; // 把对象挂载vue中

//导入css
import "../static/css/reset.css";

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
