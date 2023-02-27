<template>
  <div class="d-flex flex-column justify-content-center text-center bg-dark text-light">
    <div class="display-3">Welcome to Self Quantified Tracker App</div>
    <div class="my-5">
      <router-link :to="{ name: 'signup' }" type="button" class="btn btn-info me-5 rounded-pill">Sign up</router-link>
      <router-link :to="{ name: 'login' }" type="button" class="btn btn-info ms-5 rounded-pill">Log in</router-link>
    </div>
    <!-- <img alt="Vue logo" src="../assets/logo.png" /> -->
  </div>
</template>

<script>
  // @ is an alias to /src

  export default {
    // name: "HomeView",
    // components: {
    //   HelloWorld,
    // },
  };
</script>
<style scoped>
  .d-flex {
    height: 100vh;
    width: 100vw;
  }
</style>
