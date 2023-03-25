<template>
  <!-- Button trigger modal -->
  <div>
    <button type="button" class="btn btn-primary ms-5 nav-item" data-bs-toggle="modal" data-bs-target="#staticBackdrop">
      Add new blog
    </button>
    <!-- Modal -->
    <div
      class="modal fade"
      id="staticBackdrop"
      data-bs-backdrop="static"
      data-bs-keyboard="false"
      tabindex="-1"
      aria-labelledby="staticBackdropLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="staticBackdropLabel" style="color: black">Add tracker</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body" style="color: black">
            <form @submit.prevent="submitBlog()">
              <div class="row mb-3">
                <label for="title" class="form-label col-auto">Title</label>
                <div class="col">
                  <input
                    v-model="title"
                    type="text"
                    class="form-control"
                    id="title"
                    aria-describedby="title"
                    required
                  />
                </div>
              </div>
              <div class="col mb-3">
                <label for="caption" class="form-label">Caption / description</label>
                <textarea v-model="description" class="form-control" id="caption" rows="3" required></textarea>
              </div>
              <div class="mb-3">
                <label for="image" @click="triggerChangeOnImagesInput" class="form-label">Upload Image</label>
                <input
                  class="form-control"
                  ref="image"
                  @change="handleImageUpload()"
                  type="file"
                  id="image"
                  accept="image/*"
                />
              </div>
              <div class="col mb-3">
                <button class="btn btn-primary" data-bs-dismiss="modal">Submit</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    title: "Addblog",

    data() {
      return { title: "", description: "", image: null, feed: [] };
    },
    computed: {
      imagesSelected() {
        return this.image.length > 0;
      },
      imagetitles() {
        return this.imagesSelected
          ? Array.from(this.image)
              .map((image) => image.title)
              .join("; ")
          : "";
      },
    },
    methods: {
      triggerChangeOnImagesInput() {
        this.$refs.image.click();
      },
      handleImageUpload() {
        this.image = this.$refs.image.files[0];
      },
      async submitBlog() {
        const formData = new FormData();
        formData.append("user_name", this.$store.state.user.user_name);
        formData.append("id", this.$store.state.user.id);
        formData.append("title", this.title);
        formData.append("description", this.description);
        formData.append("image", this.image);
        let resp = await fetch(this.$store.state.base_url + `/api/blog`, { method: "post", body: formData });
        let data = await resp.json();
        // console.log(data);
        this.$store.dispatch("addBlog", data);
      },
      submitImage() {
        console.log("Hello");
        let formData = new FormData();
        // this.image.forEach((image, i) => formData.append("images[" + i + "]", image));
        formData.append("images", this.image[0]);
        console.log("last");
        fetch("http://127.0.0.1:5000/api/image", {
          method: "post",
          body: formData,
          headers: { "Authentication-Token": this.$store.state.authentication_token },
        })
          .then((response) => {
            console.log(`SUCCESS!! Response: ${response.data}`);
            // this.resetImages();
            // this.heading = "Thank you for your images!";
          })
          .catch((error) => {
            console.error(`FAILURE!! ${error}`);
            // this.resetImages();
            // this.heading = "Something went wrong...";
          });
      },
    },
  };
</script>
