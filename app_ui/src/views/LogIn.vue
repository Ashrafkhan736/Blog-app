<template>
  <div class="container">
    <div class="display-4 mt-5">Provide details to login!</div>
    <div class="card mt-3">
      <div class="card-body">
        <form @submit.prevent="login">
          <div class="mb-3 mt-3">
            <label for="email" class="form-label"> <h4>Email</h4></label>
            <input type="email" class="form-control" name="email" v-model.lazy="data.email" required />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label"> <h4>Password</h4></label>
            <input :type="this.type" class="form-control" v-model.lazy="data.password" name="password" required />
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
        data: { email: null, password: null },
        type: "password",
      };
    },
    methods: {
      toggle() {
        if (this.type === "password") {
          this.type = "text";
        } else {
          this.type = "password";
        }
      },
      login() {
        console.log("loging");
        let formData = new FormData();
        formData.append("email", this.data.email);
        formData.append("password", this.data.password);

        fetch(this.$store.state.base_url + "/login?include_auth_token", {
          method: "post",
          body: JSON.stringify(this.data),
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((r) => {
            if (!r.ok) {
              console.log(r);
              throw new Error(`Error status : ${r.status}`);
            }
            return r.json();
          })
          .then((d) => {
            console.log(d.response.user);
            this.$store.dispatch("userInfo", d.response.user);
            this.$router.push({ path: "/feed" });
          })
          .catch((err) => console.log(err));
      },
    },
  };
</script>

<style></style>
