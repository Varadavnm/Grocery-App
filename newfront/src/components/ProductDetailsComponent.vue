<template>
  <div>
    <h2>Product Details</h2>
    <div>
      <h3>{{ product.name }}</h3>
      <p>{{ product.description }}</p>
      <h4 v-if="product.id">Rate the product</h4>
      <!-- Include the RatingComponent here -->
      <RatingComponent :productId="product.id" v-if="product.id" />
      <!-- Add more product details as needed -->
      <button @click="addToCart" class="add-to-cart-button">Add to Cart</button>
      <!-- Display the Delete Product button based on the user's role -->
      <button @click="deleteProduct" class="delete-product-button">
        Delete Product
      </button>
    </div>
  </div>
</template>

<script>
import RatingComponent from "@/components/RatingComponent.vue";

export default {
  components: {
    RatingComponent,
  },
  data() {
    return {
      product: {},
    };
  },
  mounted() {
    this.fetchProductDetails();
  },
  methods: {
    async fetchProductDetails() {
      try {
        console.log("This is the product page");
        const productId = this.$route.params.id;
        const response = await fetch(
          `http://127.0.0.1:5000/view_product/${productId}`
        );

        if (!response.ok) {
          console.error("Failed to fetch product details");
          return;
        }

        const productData = await response.json();
        this.product = productData;
      } catch (error) {
        console.error("Error during product details fetch:", error);
      }
    },
    addToCart() {
      this.$store.dispatch("addToCart", this.product);
      this.$router.push("/view_cart");
    },
    async deleteProduct() {
      try {
        const productId = this.product.id;
        const accessToken = localStorage.getItem("access_token");

        const response = await fetch(
          `http://127.0.0.1:5000/delete_product/${productId}`,
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
        this.$router.push("/products");
      } catch (error) {
        console.error("Error during product deletion:", error);
      }
    },
  },
};
</script>
