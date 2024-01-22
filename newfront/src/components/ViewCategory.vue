<template>
  <div>
    <div v-for="category in categories" :key="category.id">
      <h2>{{ category.name }} Products</h2>
      <div v-if="category.products && category.products.length > 0">
        <div
          class="small-card"
          v-for="product in category.products"
          :key="product.id"
        >
          <h4>{{ product.name }}</h4>
          <p>Stock: {{ product.stock }}</p>
          <button @click="redirectToRating(product.id)">Rate</button>
          <button @click="redirectToPurchase(product.id)">Purchase</button>
          <button @click="redirectToDelete(product.id)">Delete</button>
        </div>
      </div>
      <div v-else>
        <p>No products available in this category.</p>
      </div>
    </div>
    <div v-if="categories.length === 0">
      <p>No products available in any category.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      categories: [],
    };
  },
  methods: {
    redirectToRating(productId) {
      this.$router.push({ name: "ratings", params: { id: productId } });
      console.log(`Rate product with ID ${productId}`);
    },
    redirectToPurchase(productId) {
      this.$router.push("/add_to_cart");
      console.log(`Purchase product with ID ${productId}`);
    },
    redirectToDelete(productId) {
      this.$router.push(`/delete_product/${productId}`);
      console.log(`Delete product with ID ${productId}`);
    },
  },
  mounted() {
    const categoryId = this.$route.params.categoryId;
    fetch(`http://localhost:5000/category/${categoryId}`)
      .then((response) => response.json())
      .then((data) => {
        this.categories = data.category ? [data.category] : [];
      })
      .catch((error) => {
        console.error("Error fetching category data:", error);
      });
  },
};
</script>

<style scoped>
.small-card {
  padding: 10px;
  cursor: pointer;
  transition: 0.3s all ease-in-out;
  height: 200px;
  width: 150px;
  border: 1px solid #ddd;
  margin: 10px;
}

.small-card:hover {
  box-shadow: 2px 2px 15px #fd9a6ce5;
  transform: scale(1.02);
}

.small-card h4 {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 5px;
}

.small-card p {
  font-size: 12px;
}
</style>
