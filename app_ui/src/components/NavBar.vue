<!-- <template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <router-link
        :to="{ name: 'about', params: { user_name: this.$store.state.user.user_name } }"
        type="button"
        class="navbar-brand"
      >
        Welcome {{ this.$store.state.user.user_name }}
      </router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-around" id="navbarSupportedContent">
        <AddBlog />
        <UserSearch />
        <a class="btn btn-primary">Logout <i class="bi bi-box-arrow-right"></i></a>
      </div>
    </div>
  </nav>
</template> -->
<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <router-link
        :to="{ name: 'about', params: { user_name: this.$store.state.user.user_name } }"
        type="button"
        class="navbar-brand"
      >
        Welcome {{ this.$store.state.user.user_name }}
      </router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
        <ul class="navbar-nav">
          <li class="nav-item">
            <AddBlog />
          </li>
          <li class="nav-item ms-2">
            <UserSearch />
          </li>
          <li class="nav-item ms-2">
            <button class="btn btn-primary" title="Export data" @click="exportData">
              <i class="bi bi-cloud-arrow-down-fill"></i>
            </button>
          </li>
          <li class="nav-item mx-2">
            <a class="btn btn-primary" title="Logout" @click="logOut"> <i class="bi bi-box-arrow-right"></i></a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
  // import TrackerModal from "@/components/TrackerModal";
  import UserSearch from "./UserSearch.vue";
  import AddBlog from "./AddBlog.vue";
  export default {
    name: "NavBar",
    components: { UserSearch, AddBlog },
    data() {
      return {
        user_name: "",
        users: [],
      };
    },
    methods: {
      redirect() {
        this.$router.push({ name: "about", params: { user_name: this.user_name } });
      },
      exportData() {
        const formData = new FormData();
        formData.append("email", this.$store.state.user.email);
        formData.append("user_name", this.$store.state.user.user_name);
        fetch(`${this.$store.state.base_url}/api/export`, {
          method: "post",
          body: formData,
          headers: { "Authentication-Token": this.$store.state.authentication_token },
        });
      },
      logOut() {
        fetch(`${this.$store.state.base_url}/logout`, {
          method: "post",
          body: JSON.stringify({ email: this.$store.state.user.email }),
        }).then((r) => {
          console.log(`logout ${r}`);
          localStorage.clear();
          this.$router.push({ name: "login" });
        });
      },
      find(user_name) {
        // console.log(user_name);
        if (user_name.length > 0) {
          fetch(`${this.$store.state.base_url}/api/search/${user_name}`, {
            method: "get",
            headers: { "Authentication-Token": this.$store.state.authentication_token },
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
    },
  };
</script>
