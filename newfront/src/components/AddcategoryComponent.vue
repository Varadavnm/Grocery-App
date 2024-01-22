<template>
  <div>
    <h2>Add Category</h2>
    <p v-if="isAdmin">Is Admin: {{ isAdmin }}</p>
    <form @submit.prevent="addCategory" v-if="isAdmin" class="form-container">
      <label for="category_name">Category Name:</label>
      <input type="text" id="category_name" v-model="categoryName" required />
      <button type="submit">Add Category</button>
    </form>
    <p v-if="isAdmin && errorMessage" class="error">{{ errorMessage }}</p>
    <p v-if="isAdmin && successMessage" class="success">{{ successMessage }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      categoryName: "",
      errorMessage: "",
      successMessage: "",
    };
  },
  computed: {
    isAdmin() {
      // Check the user's role from local storage
      const userRole = localStorage.getItem("role");
      return userRole === "admin";
    },
  },
  methods: {
    async addCategory() {
      if (!this.isAdmin) {
        this.errorMessage = "You are not authorized to perform this action.";
        return;
      }
      try {
        const token = localStorage.getItem("access_token");
        console.log(token);
        const response = await fetch("http://127.0.0.1:5000/add_category", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ category_name: this.categoryName }),
        });

        if (response.ok) {
          this.successMessage = "Category added successfully";
          window.location.reload();
          this.errorMessage = "";
        } else {
          const data = await response.json();
          this.errorMessage = data.message;
          this.successMessage = "";
        }
      } catch (error) {
        console.error("Error adding category:", error);
        this.errorMessage = "An error occurred while adding the category";
        this.successMessage = "";
      }
    },
  },
};
</script>
<style>
@media only screen and (max-width: 600px) {
  .form-container {
    max-width: 100%;
    align-items: flex-start;
  }
}
</style>
