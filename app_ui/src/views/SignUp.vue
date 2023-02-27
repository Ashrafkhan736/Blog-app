<template>
  <div class="container">
    <h1 class="display-4 mt-5">Set up your user name to proceed further</h1>
    <div class="card mt-3">
      <div class="card-body">
        <form @submit.prevent="signup">
          <div class="mb-3">
            <label for="username" class="form-label">
              <h4>User name</h4>
            </label>
            <input
              v-model="formData.username"
              type="text"
              class="form-control"
              name="username"
              required
            />
          </div>
          <div class="mb-3">
            <label for="email" class="form-label"> <h4>Email</h4></label>
            <input
              v-model="formData.email"
              type="email"
              name="email"
              class="form-control"
              required
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label"> <h4>Password</h4> </label>
            <input
              v-model="formData.password"
              type="password"
              class="form-control"
              name="password"
              required
            /><input
              type="checkbox"
              class="from-check-input"
              name="toggle"
              @click="toggle"
            />
            <label for="toggle" class="form-check-label">show password</label>
          </div>

          <button class="btn btn-info rounded-pill">Sign-up</button>
        </form>
        <p class="mt-2" style="color: black">
          Already registered?
          <router-link :to="{ name: 'login' }">Login Here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        username: null,
        password: null,
        email: null,
      },
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
    signup() {
      console.log("singing"),
        fetch(this.$store.state.base_url + "/api/user", {
          method: "put",
          // mode: "cors",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.formData),
        })
          .then((r) => r.json())
          .then((d) => console.log(d))
          .catch((e) => console.log(e));
    },
  },
};
</script>

<style></style>
