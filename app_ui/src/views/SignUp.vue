<template>
  <div class="container">
    <h1 class="display-4 mt-5">Set up your user name to proceed further</h1>
    <div class="card mt-3">
      <div class="card-body">
        <form @submit.prevent="signup">
          <div class="mb-3">
            <label for="user_name" class="form-label">
              <h4>User name</h4>
            </label>
            <input v-model="data.user_name" type="text" class="form-control" name="user_name" required />
          </div>
          <div class="mb-3">
            <label for="email" class="form-label"> <h4>Email</h4></label>
            <input v-model="data.email" type="email" name="email" class="form-control" required />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label"> <h4>Password</h4> </label>
            <input v-model="data.password" :type="this.type" class="form-control" name="password" required /><input
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
        data: {
          user_name: null,
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
        console.log("singing");
        let formData = new FormData();
        formData.append("user_name", this.data.user_name);
        formData.append("password", this.data.password);
        formData.append("email", this.data.email);

        fetch(this.$store.state.base_url + "/api/user", {
          method: "put",
          body: formData,
        })
          .then((r) => r.json())
          .then((d) => {
            console.log(d);
            this.$router.push({ path: "/login" });
          })
          .catch((e) => console.log(e));
      },
    },
  };
</script>

<style></style>
