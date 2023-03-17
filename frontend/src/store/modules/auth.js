//store/modules/auth.js

import axios from "axios";

const state = {
    user: localStorage.getItem('token')
};
const getters = {
    isAuthenticated: state => { if (state.user == null) { return false } else { return true } }
};
const actions = {
    async Logout({ commit }) {
        let user = null;
        localStorage.removeItem("token");
        commit('Logout', user);
    },

    async Login({ commit }, data) {

        let result = await axios.post('login', data);

        localStorage.setItem('token', result['data']['response']['user']['authentication_token'])

        commit('Login', true)
    }
};
const mutations = {
    Logout(state) {
        state.user = null
    },
    Login(state, result) {
        state.user = result
    }
};
export default {
    state,
    getters,
    actions,
    mutations
};