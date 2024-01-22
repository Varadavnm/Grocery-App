<template>
  <div>
    <h2>Delete Category</h2>
    <button @click="deleteCategoryAdmin">Delete Category</button>
    <p v-if="successMessage" class="success">{{ successMessage }}</p>
    <p v-if="loading">Deleting...</p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      error: null,
      successMessage: null,
      loading: false,
    };
  },
  methods: {
    async deleteCategoryAdmin() {
      const confirmed = window.confirm(
        "Are you sure you want to delete category?"
      );

      if (!confirmed) {
        return;
      }

      try {
        this.loading = true;

        const categoryId = this.$route.params.id;
        const response = await fetch(
          `http://127.0.0.1:5000/delete_category_admin/${categoryId}`,
          {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          this.error = `Error: ${response.status} - ${errorData.message}`;
          console.error("Category Deletion Error:", errorData);
        } else {
          const responseData = await response.json();
          this.error = null;
          this.successMessage = responseData.message;
          console.log("Category Deletion Successful:", responseData);
          this.$router.go(0);
        }
      } catch (error) {
        this.error = "Error deleting category.";
        console.error("Delete Category Error:", error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.error {
  color: red;
}
</style>
