import { createStore } from "vuex";
import { VuexPersistence } from "vuex-persist";

export default createStore({
  state: {
    base_url: "http://127.0.0.1:5000",
  },
  getters: {},
  mutations: {
    userInfo(state, data) {
      state.user = data.user;
      state.following = data.following;
      state.follower = data.follower;
    },
    follow(state) {
      state.following += 1;
    },
    unfollow(state) {
      state.following -= 1;
    },
    addBlog(state, data) {
      state.user.blogs.push(data);
    },
  },
  actions: {
    userInfo(context, data) {
      context.commit("userInfo", data);
    },
    follow(context) {
      context.commit("follow");
    },
    unfollow(context) {
      context.commit("unfollow");
    },
    addBlog(context, data) {
      context.commit("addBlog", data);
    },
  },
  modules: {},
  plugins: [new VuexPersistence().plugin],
});
