<template>
  <!-- <div class="home">
      <img alt="Vue logo" src="../assets/logo.png">
      <HelloWorld msg="Welcome to Your Vue.js App"/>
    </div> -->
  <NavBar />
  <div class="container p-3">
    <!-- <label for="search">Username</label>
    <input @input="find(username)" v-model.trim="username" type="text" id="search" /> -->
    <h3 class="text-start">My Feed:</h3>
    <div v-if="feed.length > 0" v-for="blog in feed" :key="blog.blog_id">
      <BlogCard :blog="blog" />
    </div>
    <div v-else>
      <img class="img-fluid max-width-100" src="/img/monsters-inc-sully.gif" alt="No feed" />
      <p>Sorry, you have no feed. Follow some users to see their posts.</p>
    </div>
  </div>
</template>

<script>
  // @ is an alias to /src
  import HelloWorld from "@/components/HelloWorld.vue";
  import BlogCard from "@/components/BlogCard.vue";
  import NavBar from "@/components/NavBar.vue";
  export default {
    name: "HomeView",
    components: {
      HelloWorld,
      BlogCard,
      NavBar,
    },
    data() {
      return { feed: [], username: "" };
    },

    created() {
      this.getFeed();
    },
    methods: {
      find(username) {
        // console.log(username);
        if (username.length > 0) {
          fetch(`http://127.0.0.1:5000/api/search/${username}`, {
            method: "get",
            headers: { "Authentication-Token": this.$store.state.authentication_token },
          })
            .then((res) => {
              return res.json();
            })
            .then((data) => {
              console.log(data);
            });
        }
      },
      getFeed() {
        fetch(this.$store.state.base_url + `/api/feed/${this.$store.state.user.user_name}`, {
          method: "get",
          headers: { "Authentication-Token": this.$store.state.authentication_token },
        })
          .then((res) => {
            // console.log(res);
            return res.json();
          })
          .then((data) => {
            // console.log(data);
            this.feed = data;
          });
      },
    },
  };
</script>
