<template>
  <div>
    <h2>Search</h2>
    <form class="d-flex" @submit.prevent="searchProducts">
      <input
        class="form-control me-2"
        type="search"
        placeholder="Search"
        v-model="searchQuery"
      />
      <button class="btn btn-outline-success" type="submit">Search</button>
    </form>
    <div>
      <h2>Product and Category Results</h2>
      <div v-if="products.length > 0">
        <h3>Product Results</h3>
        <div v-for="product in products" :key="product.id">
          <h4>{{ product.name }}</h4>
          <p>{{ product.description }}</p>
        </div>
      </div>
      <div v-if="categories.length > 0">
        <h3>Category Results</h3>
        <div
          v-for="category in categories"
          :key="category.id"
          @click="showCategory(category.id)"
          class="col-lg-3 col-md-4 col-sm-6 col-12 mb-4"
        >
          <div class="card d-flex flex-column align-items-center">
            <h5>{{ category.name }}</h5>
            <ul>
              <li v-for="product in category.products" :key="product.id">
                <router-link
                  :to="{
                    name: 'productDetails',
                    params: { id: product.id },
                  }"
                  class="btn btn-primary"
                >
                  View Details
                </router-link>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div v-if="products.length === 0 && categories.length === 0">
        <p>No results found.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: "",
      products: [],
      categories: [],
    };
  },
  methods: {
    async searchProducts() {
      try {
        console.log("Searching for products");
        const token = localStorage.getItem("access_token");
        const response = await fetch(
          `http://127.0.0.1:5000/search?q=${encodeURIComponent(
            this.searchQuery
          )}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Search Error:", errorData);
          return;
        }

        const searchData = await response.json();
        this.products = searchData.products || [];
        this.categories = searchData.categories || [];
        console.log(searchData);
      } catch (error) {
        console.error("Error during search:", error);
      }
    },
    showCategory(categoryId) {
      console.log(categoryId);
      this.$router.push({
        name: "category",
        params: { categoryId: categoryId },
      });
    },
  },
};
</script>

<style>
.navbar-form .form-control {
  width: 150px;
}
</style>
