<template>
  <div>
    <form class="d-flex" @submit.prevent="redirect()">
      <input
        type="text"
        class="form-control me-2"
        v-model.trim="user_name"
        ref="input"
        placeholder="Enter username"
        @input="find(user_name)"
        @focus="showResults()"
      />
      <button class="btn btn-outline-success" type="submit">Search</button>
      <!-- <button @click="redirect()">search</button> -->
    </form>
    <template v-if="showPopoverElement">
      <div
        ref="popover"
        class="popover bs-popover-right"
        role="tooltip"
        :style="{ top: popoverTop + 'px', left: popoverLeft + 'px' }"
      >
        <div class="arrow"></div>
        <div class="popover-body">
          <ul @blur="hideResults()">
            <li v-for="(user, index) in users" :key="index" @click="selectResult(user)">
              {{ user }}
            </li>
          </ul>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
  export default {
    name: "UserSearch",
    data() {
      return {
        user_name: "",
        users: [],
        showPopoverElement: false,
        popoverTop: 0,
        popoverLeft: 0,
      };
    },

    methods: {
      redirect() {
        this.$router.push({ name: "about", params: { user_name: this.user_name } });
      },
      find(user_name) {
        // console.log(user_name);
        if (user_name.length > 0) {
          fetch(`http://127.0.0.1:5000/api/search/${user_name}`, { method: "get" })
            .then((res) => {
              return res.json();
            })
            .then((data) => {
              console.log(data);
              this.users = data;
            });
        }
      },
      showResults() {
        console.log("show");
        this.showPopoverElement = true;
        const form = this.$el.querySelector("form");
        const formRect = form.getBoundingClientRect();
        this.popoverTop = formRect.bottom;
        this.popoverLeft = formRect.left;
      },
      hideResults(event) {
        if (event.target !== this.$refs.input && event.target !== this.$refs.popover) {
          this.showPopoverElement = false;
        }
      },
      selectResult(result) {
        this.user_name = result;
        console.log("selected");
      },
    },
    mounted() {
      document.addEventListener("click", this.hideResults);
    },
    beforeDestroy() {
      document.removeEventListener("click", this.hideResults);
    },
  };
</script>
