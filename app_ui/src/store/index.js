import { createStore } from "vuex";
import { VuexPersistence } from "vuex-persist";

export default createStore({
  state: {
    base_url: "http://127.0.0.1:5000",
  },
  getters: {},
  mutations: {
    userInfo(state, data) {
      state.user = data;
      state["authentication_token"] = data.authentication_token;
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
    editBlog(state, obj) {
      state.user.blogs[obj["index"]] = obj["data"];
    },
    deleteBlog(state, index) {
      state.user.blogs.splice(index, 1);
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
    editBlog(context, obj) {
      context.commit("editBlog", obj);
    },
    deleteBlog(context, index) {
      context.commit("deleteBlog", index);
    },
  },
  modules: {},
  plugins: [new VuexPersistence().plugin],
});
