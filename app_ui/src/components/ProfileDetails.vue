<template>
  <!-- <div class="row">
    <img src="../../../api/static/coverphoto.jpg" alt="" class="col-sm-2" height="250rem" />
    <div class="col-sm-3 align-self-center text-center">
      <a href="#" class="h4">Total posts</a>
      <p>30</p>
    </div>
    <div class="col-sm-3 align-self-center text-center">
      <a href="#" class="h4">Follwed</a>
      <p>15</p>
    </div>
    <div class="col-sm-3 align-self-center text-center">
      <a href="#" class="h4">Follwed by</a>
      <p>20</p>
    </div>
  </div> -->

  <div class="card">
    <div class="card-body d-flex justify-content-between align-items-center">
      <div>
        <h5 class="card-title">{{ userInfo.user_name }}</h5>
        <template v-if="userInfo.user_name !== this.$store.state.user.user_name">
          <button v-if="!updated_already_follow" @click="follow(userInfo.user_name)">Follow</button>
          <button v-else @click="unfollow(userInfo.user_name)">Unfollow</button>
        </template>
        <p class="card-text">
          <router-link
            :to="{ name: 'userlist', params: { user_name: userInfo.user_name, type: 'follower' } }"
            class="btn btn-primary"
            >Followers: {{ this.updated_follower }}
          </router-link>
        </p>
        <p class="card-text">
          <router-link
            :to="{ name: 'userlist', params: { user_name: userInfo.user_name, type: 'follow' } }"
            class="btn btn-primary"
            >Following: {{ this.updated_following }}
          </router-link>
        </p>
      </div>
      <img
        class="img-fluid img-thumbnail rounded-circle"
        :src="this.updated_userInfo.img_path"
        alt="User profile image"
        style="width: 100px; height: 100px"
      />
    </div>
  </div>
</template>

<script>
  export default {
    name: "ProfileDetails",
    props: {
      userInfo: {
        type: Object,
        required: true,
        // default: { user_name: "ashraf2" },
      },
      following: {
        type: Number,
        default: 0,
      },
      follower: {
        type: Number,
        default: 0,
      },
      already_follow: {
        type: Boolean,
        default: false,
      },
    },
    data() {
      return {
        updated_userInfo: this.userInfo,
        updated_follower: this.follower,
        updated_following: this.following,
        updated_already_follow: this.already_follow,
      };
    },
    methods: {
      follow(user_name) {
        // logic to follow user
        let formData = new FormData();
        formData.append("current_user", this.$store.state.user.user_name);
        formData.append("user", user_name);
        fetch(this.$store.state.base_url + "/api/follow", {
          method: "post",
          body: formData,
          headers: { "Authentication-Token": this.$store.state.authentication_token },
        }).then((resp) => {
          console.log(resp.json());
        });
        this.updated_already_follow = true;
        this.updated_follower = this.updated_follower + 1;
        this.$store.dispatch("follow");

        this.$forceUpdate();
      },
      unfollow(user_name) {
        // logic to unfollow user
        let formData = new FormData();
        formData.append("current_user", this.$store.state.user.user_name);
        formData.append("user", user_name);
        fetch(`${this.$store.state.base_url}/api/unfollow`, {
          method: "post",
          body: formData,
          headers: { "Authentication-Token": this.$store.state.authentication_token },
        }).then((resp) => {
          console.log(resp.json());
        });
        this.updated_already_follow = false;
        this.updated_follower = this.updated_follower - 1;
        this.$store.dispatch("unfollow");
        this.$forceUpdate();
        // const user = this.users.find((user) => user.id === id);
        // user.following = false;
      },
    },
  };
</script>
