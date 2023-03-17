import Vuex from 'vuex';
import Vue from 'vue';
// import createPersistedState from "vuex-persistedstate";
import auth from './modules/auth';
import lists from './modules/lists';


// Load Vuex
Vue.use(Vuex);
// Create store
export default new Vuex.Store({
  modules: {
    auth,
    lists
  },
  // plugins: [createPersistedState()]
});
