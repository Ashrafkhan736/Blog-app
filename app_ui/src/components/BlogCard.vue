<template>
  <div class="card mb-3">
    <div class="row g-0">
      <div class="col-md-4">
        <img :src="blog.img_path" class="img-fluid rounded-start" alt="No image" />
      </div>
      <div class="col-md-8">
        <div class="card-body">
          <h5 class="card-title">
            Title :
            <span :contenteditable="this.edit" ref="title" :class="{ 'bg-gray': this.edit }">{{ blog.title }}</span>
          </h5>
          <router-link :to="{ name: 'about', params: { user_name: blog.user_name } }">
            User : {{ blog.user_name }}
          </router-link>
          <p
            :contenteditable="this.edit"
            class="card-text"
            ref="description"
            :class="{ 'bg-gray': this.edit }"
            style="height: 150px; overflow: auto"
          >
            {{ blog.description }}
          </p>
          <p class="card-text">
            <small class="text-muted">{{ blog.timestamp }}</small>
          </p>
          <div v-if="blog.user_name === $store.state.user.user_name" class="card-footer">
            <button v-if="showEdit" @click="editBlog()" class="btn btn-primary">Edit</button>
            <button v-if="!showEdit" @click="submitEdit(blog.blog_id)" class="btn btn-primary">Submit Edit</button>
            <button class="btn btn-primary" @click="deleteBlog(blog.blog_id)">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    name: "BlogCard",
    props: {
      blog: Object,
    },
    data() {
      return { edit: false, showEdit: true };
    },
    methods: {
      async submitEdit(blog_id) {
        const formData = new FormData();
        formData.append("title", this.$refs.title.textContent);
        formData.append("description", this.$refs.description.textContent);
        const resp = await fetch(this.$store.state.base_url + `/api/blog/${blog_id}`, {
          method: "put",
          body: formData,
          headers: { "Authentication-Token": this.$store.state.authentication_token },
        });
        const data = await resp.json();
        const index = this.$store.state.user.blogs.findIndex((blog) => blog.blog_id === blog_id);

        // const index = this.$store.state.user.blogs.findIndex((blog) => blog.blog_id === blog_id);
        this.$store.dispatch("editBlog", { index: index, data: data });

        this.edit = false;
        this.showEdit = true;
      },
      editBlog() {
        this.edit = true;
        this.showEdit = false;
      },
      async deleteBlog(blog_id) {
        const resp = await fetch(this.$store.state.base_url + `/api/blog/${blog_id}`, {
          method: "delete",
          headers: { "Authentication-Token": this.$store.state.authentication_token },
        });
        const data = await resp.json();
        console.log(data);
        const index = this.$store.state.user.blogs.findIndex((blog) => blog.blog_id === blog_id);
        this.$store.dispatch("deleteBlog", index);
      },
    },
  };
</script>
<style>
  .bg-gray {
    background-color: #ccc;
  }
</style>

<!-- <template>
  <div class="card mb-3">
    <div class="row g-0">
      <div class="col-md-4">
        <img :src="blog.img_path" class="img-fluid rounded-start" alt="No image" />
      </div>
      <div class="col-md-8">
        <div class="card-body">
          <h5 class="card-title">
            Title : <span :contenteditable="this.edit" ref="title">{{ blog.title }}</span>
          </h5>
          <router-link :to="{ name: 'about', params: { user_name: blog.user_name } }">
            User : {{ blog.user_name }}
          </router-link>
          <p :contenteditable="this.edit" class="card-text" ref="description">{{ blog.description }}</p>
          <p class="card-text">
            <small class="text-muted">{{ blog.timestamp }}</small>
          </p>
          <div v-if="blog.user_name === this.$store.state.user.user_name" class="card-footer">
            <button v-if="showEdit" @click="editBlog()" class="btn btn-primary">Edit</button>
            <button v-if="!showEdit" @click="submitEdit(blog.blog_id)" class="btn btn-primary">Submit Edit</button>
            <button class="btn btn-primary" @click="deleteBlog(blog.blog_id)">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    name: "BlogCard",
    props: {
      blog: Object,
    },
    data() {
      return { edit: false, showEdit: true };
    },
    methods: {
      async submitEdit(blog_id) {
        const formData = new FormData();
        formData.append("title", this.$refs.title.textContent);
        formData.append("description", this.$refs.description.textContent);
        const resp = await fetch(this.$store.state.base_url + `/api/blog/${blog_id}`, {
          method: "put",
          body: formData,
        });
        const data = await resp.json();
        const index = this.$store.state.user.blogs.findIndex((blog) => blog.blog_id === blog_id);
        this.$store.state.user.blogs[index] = data;
        console.log(data);
        this.edit = false;
        this.showEdit = true;
      },
      editBlog() {
        this.edit = true;
        this.showEdit = false;
      },
      async deleteBlog(blog_id) {
        const resp = await fetch(this.$store.state.base_url + `/api/blog/${blog_id}`, { method: "delete" });
        const data = await resp.json();
        console.log(data);
        this.$store.state.user.blogs = this.$store.state.user.blogs.filter((blog) => blog.blog_id !== blog_id);
      },
    },
  };
</script> -->
