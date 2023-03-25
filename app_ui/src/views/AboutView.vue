<template>
  <div class="container">
    <h1>This is an about page</h1>
    <ProfileDetails :userInfo="userInfo" :follower="follower" :following="following" :already_follow="already_follow" />
    <div v-for="blog in userInfo.blogs" :key="blog.blog_id">
      <BlogCard :blog="blog" />
    </div>
  </div>
</template>
<script>
  import ProfileDetails from "@/components/ProfileDetails.vue";
  import BlogCard from "@/components/BlogCard.vue";
  export default {
    components: { ProfileDetails, BlogCard },
    props: { user_name: { type: String } },
    data() {
      return { userInfo: {}, follower: 0, following: 0, already_follow: false };
    },
    created() {
      this.getUserInfo();
    },
    methods: {
      getUserInfo() {
        if (this.$store.state.user.user_name !== this.user_name) {
          let formData = new FormData();
          formData.append("current_user", this.$store.state.user.user_name);
          formData.append("user", this.user_name);
          fetch(this.$store.state.base_url + `/api/user`, {
            method: "post",
            body: formData,
            headers: { "Authentication-Token": this.$store.state.authentication_token },
          })
            .then((res) => {
              return res.json();
            })
            .then((data) => {
              // console.log(data);
              this.userInfo = data.user;
              this.following = data.following;
              this.follower = data.follower;
              this.already_follow = data.already_follow;
            })
            .catch((e) => {
              console.log(e);
            });
        } else {
          this.userInfo = this.$store.state.user;
          this.following = this.$store.state.following;
          this.follower = this.$store.state.follower;
        }
      },
    },
  };
</script>
