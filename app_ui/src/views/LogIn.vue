<template>
  <div class="container">
    <div class="display-4 mt-5">Provide details to login!</div>
    <div class="card mt-3">
      <div class="card-body">
        <form @submit.prevent="login">
          <div class="mb-3 mt-3">
            <label for="user_name" class="form-label"> <h4>User Name</h4></label>
            <input type="user_name" class="form-control" name="user_name" v-model.lazy="data.user_name" required />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label"> <h4>Password</h4></label>
            <input :type="type" class="form-control" v-model.lazy="data.password" name="password" required />
            <input type="checkbox" class="from-check-input" name="toggle" @click="toggle" />
            <label for="toggle" class="form-check-label">show password</label>
          </div>

          <button class="btn btn-info btn-lg rounded-pill">Login</button>
        </form>

        <p class="mt-2">
          Not registered yet?
          <router-link :to="{ name: 'signup' }">Sign Up!</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        data: { user_name: null, password: null },
        type: "password",
      };
    },
    methods: {
      toggle() {
        if (this.type === "password") {
          this.type = "type";
        } else {
          this.type = "password";
        }
      },
      login() {
        console.log("looging");
        let formData = new FormData();
        formData.append("user_name", this.data.user_name);
        formData.append("password", this.data.password);

        fetch(this.$store.state.base_url + `/api/user/${this.data.user_name}`, {
          method: "get",
          // body: formData,
        })
          .then((r) => {
            if (!r.ok) {
              console.log(r);
              throw new Error(`Error status : ${r.status}`);
            }
            return r.json();
          })
          .then((d) => {
            this.$store.dispatch("userInfo", d);
            this.$router.push({ path: "/feed" });
          })
          .catch((err) => console.log(err));
      },
    },
  };
</script>

<style></style>
