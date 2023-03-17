import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import AddListFormView from '../views/AddListFormView.vue';
import EditListFormView from '../views/EditListFormView.vue';
import AddCardFormView from '../views/AddCardFormView.vue';
import EditCardFormView from '../views/EditCardFormView.vue';
import SummaryView from '../views/SummaryView.vue';

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    beforeEnter: routeGuard
  },
  {
    path: '/summary',
    name: 'summary',
    component: SummaryView,
    beforeEnter: routeGuard
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    beforeEnter: loginGuard
  },
  {
    path: '/list',
    name: 'add-list',
    component: AddListFormView,
    beforeEnter: routeGuard

  },
  {
    path: '/list/edit/:list_id',
    name: 'edit-list',
    component: EditListFormView,
    beforeEnter: routeGuard

  },
  {
    path: '/card/add/:list_id',
    name: 'add-card',
    component: AddCardFormView,
    beforeEnter: routeGuard

  },
  {
    path: '/card/edit/:card_id',
    name: 'edit-card',
    component: EditCardFormView,
    beforeEnter: routeGuard

  }
  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  // }
]

const router = new VueRouter({
  base: process.env.BASE_URL,
  routes
})

import store from "../store";

function routeGuard(to, from, next) {
  let isAuthenticated = store.getters.isAuthenticated;

  if (isAuthenticated) {
    next(); // allow to enter route
  }
  else {
    next('/login');
    return false; // go to '/login';
  }
}

function loginGuard(to, from, next) {
  let isAuthenticated = store.getters.isAuthenticated;

  if (isAuthenticated) {
    next('/');
    return false;
  } else {
    next();
  }
}


// router.beforeEach((to, from) => {
//   if (to.matched.some((record) => record.meta.requiresAuth)) {
//     console.log(from);
//     if (store.getters.isAuthenticated) {
//       return true;
//     }
//   } else {
//     return false;
//   }
// });

export default router
