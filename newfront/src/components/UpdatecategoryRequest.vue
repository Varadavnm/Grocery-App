<template>
  <div>
    <h2>Update Category</h2>
    <form @submit.prevent="updateCategory">
      <div class="form-group">
        <label for="categoryName">Category Name</label>
        <input
          type="text"
          id="categoryName"
          v-model="updatedCategoryName"
          class="form-control"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">Update Category</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      updatedCategoryName: "",
    };
  },
  methods: {
    async updateCategory() {
      const categoryId = this.$route.params.categoryId;

      try {
        const response = await fetch(
          `http://127.0.0.1:5000/update_category_request/${categoryId}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
            body: JSON.stringify({
              name: this.updatedCategoryName,
            }),
          }
        );

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log(data.message);
        this.$router.push("/");
      } catch (error) {
        console.error("Error updating category:", error);
      }
    },
  },
};
</script>
