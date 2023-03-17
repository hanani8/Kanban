//store/modules/auth.js

import axios from "axios";

const state = {
    lists: [],
    card: {},
    list: {}
};

const actions = {

    async getLists({ commit }) {

        let result = await axios.get('lists', {
            headers: {
                'Authentication-Token': localStorage.getItem('token')
            }
        });

        commit('SetLists', result)
    },

    async createList({ dispatch }, data) {

        console.log(data);

        let result = await axios.post('list', data, {
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('token')
            }
        })

        console.log(result);

        dispatch('getLists');
    },

    async getList({ commit }, id) {

        console.log(id);

        let result = await axios.get(`list/${id}`, {
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('token')
            }
        })

        commit('SetList', result);
    },

    async putList({ dispatch }, { id, data }) {
        let result = await axios.put(`list/${id}`, data, {
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('token')
            }
        })

        console.log(result);


        dispatch('getLists');
    },

    async deleteList({ dispatch }, id) {
        let result = await axios.delete(`list/${id}`, {
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('token')
            }
        })

        console.log(result);


        dispatch('getLists');
    },

    async createCard({ dispatch }, data) {

        console.log(data);

        let result = await axios.post('card', data, {
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('token')
            }
        })

        console.log(result);

        dispatch('getLists');
    },

    async getCard({ commit }, id) {

        console.log(id);

        let result = await axios.get(`card/${id}`, {
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('token')
            }
        })

        commit('SetCard', result);
    },

    async putCard({ dispatch }, { id, data }) {
        console.log(data);

        let result = await axios.put(`card/${id}`, data, {
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('token')
            }
        })

        console.log(result);

        dispatch('getCard', id);
    },

    async deleteCard({ dispatch }, id) {

        let result = await axios.delete(`card/${id}`, {
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('token')
            }
        })

        console.log(result);

        dispatch('getLists');
    },

    async markAsCompleted({ dispatch }, id) {
        const data = {
            "completed": true
        }
        let result = await axios.patch(`card/${id}`, data, {
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('token')
            }
        })

        console.log(result);

        dispatch('getLists');

    },

    async moveCard({ dispatch }, object) {
        const { card_id, list_id } = object;
        const data = {
            "list_id": list_id
        };

        let result = await axios.patch(`card/${card_id}`, data, {
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('token')
            }
        });

        console.log(result);

        dispatch('getLists');
    },

    async exportCard(state, card_id) {

        let result = await axios.get(`export/card/${card_id}`, {
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('token')
            }
        })

        console.log(result);
    },

    async exportList(state, list_id) {
        let result = await axios.get(`export/list/${list_id}`, {
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('token')
            }
        })

        console.log(result);
    }
};
const mutations = {
    SetLists(state, result) {
        state.lists = result['data']
    },

    SetCard(state, result) {
        state.card = result['data'];
    },
    SetList(state, result) {
        state.list = result['data'];
    }
};

const getters = {
    lists: state => state.lists,
    list: state => state.list,
    card: state => state.card,
    summaryOfLists: (state) => {
        let summaryOfLists = [];
        for (let list of state.lists) {
            let summaryOfList = {
                "completed": 0,
                "total": 0,
                "deadline_passed": 0,
                "id": list.id,
                "title": list.title,

            }

            let charts = new Map();

            console.log(list.cards);

            for (let card of list.cards) {

                summaryOfList.total += 1;

                let completed_at;
                let completed_at_date;
                let completed_at_month;
                let completed_at_string;

                if (card.completed_at != null) {
                    completed_at = new Date(card.completed_at);
                    completed_at_date = completed_at.getDate();
                    completed_at_month = completed_at.getMonth();
                    completed_at_string = completed_at_date + "/" + completed_at_month;
                    if (charts.get(completed_at_string) == null) {
                        charts.set(completed_at_string, 1);

                    } else {
                        charts.set(completed_at_string, charts.get(completed_at_string) + 1);
                    }
                }



                if (card.completed) {
                    summaryOfList.completed += 1;
                } else {
                    const card_deadline = new Date(card.deadline);
                    const current_date = new Date();
                    if (card_deadline < current_date) {
                        summaryOfList.deadline_passed += 1;
                    }
                }

            }
            summaryOfList.charts = charts;
            summaryOfLists.push(summaryOfList);
        }
        console.log(summaryOfLists);
        return summaryOfLists;
    }

}

export default {
    state,
    getters,
    actions,
    mutations
};