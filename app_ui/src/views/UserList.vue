<template>
  <div>
    <ul class="list-group">
      <li class="list-group-items" v-for="(user, index) in users" :key="index">
        <router-link :to="{ name: 'about', params: { user_name: user.user_name } }">{{ user.user_name }}</router-link>
        <template v-if="user.user_name !== this.$store.state.user.user_name">
          <button v-if="!user.already_follow" @click="follow(user.user_name)">Follow</button>
          <button v-else @click="unfollow(user.user_name)">Unfollow</button>
        </template>
      </li>
    </ul>
  </div>
</template>

<script>
  export default {
    props: { user_name: { type: String, required: true }, type: { type: String, required: true } },
    data() {
      return {
        users: [
          // { id: 1, username: "user1", following: false },
          // { id: 2, username: "user2", following: true },
          // { id: 3, username: "user3", following: false },
        ],
      };
    },
    methods: {
      follow(user_name) {
        // logic to follow user
        let formData = new FormData();
        formData.append("current_user", this.$store.state.user.user_name);
        formData.append("user", user_name);
        fetch(this.$store.state.base_url + "/api/follow", { method: "post", body: formData }).then((resp) => {
          console.log(resp.json());
          const user = this.users.find((user) => user.user_name === user_name);
          user.already_follow = true;
          this.$store.dispatch("follow");
        });
      },
      unfollow(user_name) {
        // logic to unfollow user
        let formData = new FormData();
        formData.append("current_user", this.$store.state.user.user_name);
        formData.append("user", user_name);
        fetch(this.$store.state.base_url + "/api/unfollow", { method: "post", body: formData }).then((resp) => {
          console.log(resp.json());
          const user = this.users.find((user) => user.user_name === user_name);
          user.already_follow = false;
          this.$store.dispatch("unfollow");
        });

        // const user = this.users.find((user) => user.id === id);
        // user.following = false;
      },
    },
    mounted() {
      let formData = new FormData();
      formData.append("current_user", this.$store.state.user.user_name);
      formData.append("user", this.user_name);
      if (this.type === "follow") {
        fetch(`http://127.0.0.1:5000/api/showfollow`, {
          method: "post",
          headers: { "Authentication-Token": this.$store.state.authentication_token },
          body: formData,
        })
          .then((res) => {
            return res.json();
          })
          .then((data) => {
            console.log(data);
            this.users = data;
          });
      } else {
        fetch(`http://127.0.0.1:5000/api/showfollower`, {
          method: "post",
          headers: { "Authentication-Token": this.$store.state.authentication_token },
          body: formData,
        })
          .then((res) => {
            return res.json();
          })
          .then((data) => {
            console.log(data);
            this.users = data;
          });
      }
    },
  };
</script>
