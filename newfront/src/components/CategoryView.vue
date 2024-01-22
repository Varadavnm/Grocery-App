<template>
  <div class="container mt-4">
    <h1 class="mb-4">{{ category.name }}</h1>

    <div class="card-columns">
      <div
        v-for="product in products"
        :key="product.id"
        class="card"
        style="width: 18rem"
      >
        <img
          v-if="product.photo_filename"
          :src="`/static/product_photos/${product.photo_filename}`"
          class="card-img-top"
          alt="Product Image"
        />
        <div class="card-body">
          <router-link
            :to="{ name: 'productDetails', params: { id: product.id } }"
          >
            <h5 class="card-title">{{ product.name }}</h5>
          </router-link>
          <p class="card-text">Stock: {{ product.stock }}</p>
          <router-link
            :to="{ name: 'productDetails', params: { id: product.id } }"
            class="btn btn-primary"
          >
            View Details
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      category: {},
      products: [],
      loading: false,
      error: null,
    };
  },
  mounted() {
    this.fetchCategoryData();
  },
  methods: {
    async fetchCategoryData() {
      try {
        this.loading = true;
        const response = await fetch(
          `http://127.0.0.1:5000/view_category/${this.$route.params.categoryId}`
        );

        if (!response.ok) {
          throw new Error("Failed to fetch data");
        }

        const data = await response.json();
        this.category = data.category;
        this.products = data.products;
        this.loading = false;
      } catch (error) {
        console.error("Error fetching category data:", error);
        this.loading = false;
        this.error = "Failed to fetch category data. Please try again later.";
      }
    },
  },
};
</script>
