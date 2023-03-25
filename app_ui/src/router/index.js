import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/feed",
    name: "feed",
    component: () => import(/* webpackChunkName "login" */ "../views/FeedView.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import(/* webpackChunkName "login" */ "../views/LogIn.vue"),
  },
  {
    path: "/signup",
    name: "signup",
    component: () => import(/*webpackChunkName "signin" */ "../views/SignUp.vue"),
  },
  {
    path: "/about/:user_name", //<str:user_name>
    name: "about",
    props: true,
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    path: "/userlist/:type/:user_name",
    name: "userlist",
    props: true,
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ "../views/UserList.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
