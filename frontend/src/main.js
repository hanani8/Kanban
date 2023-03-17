import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store';
import axios from 'axios';
import './registerServiceWorker'
import VueSimpleAlert from "vue-simple-alert";

axios.defaults.withCredentials = true
axios.defaults.baseURL = 'http://localhost:5000/api/';

Vue.config.productionTip = false
Vue.use(VueSimpleAlert);


new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')

axios.interceptors.response.use(undefined, function (error) {
  if (error) {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {

      originalRequest._retry = true;
      store.dispatch('LogOut')
      return router.push('/login')
    }
  }
})