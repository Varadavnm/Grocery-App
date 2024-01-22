<template>
  <div class="delete-product-container">
    <h2>Delete Product</h2>
    <p class="confirmation-message">
      Are you sure you want to delete the product?
    </p>
    <div class="button-container">
      <button @click="confirmDelete" class="btn btn-danger">
        Confirm Delete
      </button>
      <router-link to="/view_products" class="btn btn-secondary"
        >Cancel</router-link
      >
    </div>
  </div>
</template>

<script>
export default {
  props: ["id"],
  mounted() {
    console.log("Product ID in DeleteProduct:", this.id);
  },
  methods: {
    async confirmDelete() {
      try {
        const accessToken = localStorage.getItem("access_token");

        const response = await fetch(
          `http://127.0.0.1:5000/delete_product/${this.id}`,
          {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );

        if (!response.ok) {
          console.error("Failed to delete product");
          return;
        }

        console.log("Product deleted successfully");
        this.$router.push("/");
      } catch (error) {
        console.error("Error during product deletion:", error);
      }
    },
  },
};
</script>

<style scoped>
.delete-product-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.confirmation-message {
  font-size: 16px;
  margin-bottom: 20px;
}

.button-container {
  display: flex;
  justify-content: space-between;
}
</style>
