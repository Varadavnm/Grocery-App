<template>
  <div>
    <h2>Update Category</h2>
    <form @submit.prevent="updateCategory">
      <div class="form-group">
        <label for="categoryName">New Category Name</label>
        <input
          type="text"
          id="categoryName"
          v-model="newCategoryName"
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
      newCategoryName: "",
    };
  },
  methods: {
    async updateCategory() {
      const categoryId = this.$route.params.categoryId;

      try {
        const response = await fetch(
          `http://localhost:5000/update_category/${categoryId}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
            body: JSON.stringify({
              name: this.newCategoryName,
            }),
          }
        );

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log(data.message);
      } catch (error) {
        console.error("Error updating category:", error);
      }
    },
  },
};
</script>
