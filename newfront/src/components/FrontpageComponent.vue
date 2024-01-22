<template>
  <div class="d-flex flex-wrap justify-content-center">
    <div
      v-for="category in categories"
      :key="category.id"
      @click="showCategory(category.id)"
      class="col-lg-3 col-md-4 col-sm-6 col-12 mb-4"
    >
      <div class="card d-flex flex-column align-items-center">
        <img
          v-if="category.name === 'Fresh Milk'"
          class="card-img-top"
          :src="require('@/assets/Milk.png')"
          alt="Fresh Milk Image"
          style="width: 100%; max-width: 150px; height: auto"
        />
        <img
          v-else-if="category.name === 'Pulses'"
          class="card-img-top"
          :src="require('@/assets/Staples.png')"
          alt="Pulses Image"
          style="width: 100%; max-width: 150px; height: auto"
        />
        <img
          v-else
          class="card-img-top"
          :src="require('@/assets/Staples.png')"
          alt="Default Image"
          style="width: 100%; max-width: 150px; height: auto"
        />
        <div class="card-body flex-fill">
          <h5 class="card-title">{{ category.name }}</h5>
          <router-link
            :to="{ name: 'category', params: { categoryId: category.id } }"
            class="btn btn-primary w-100"
          >
            {{ category.name }}
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
      categories: [],
    };
  },
  mounted() {
    fetch("http://localhost:5000/categories")
      .then((response) => response.json())
      .then((data) => {
        this.categories = data.categories;
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  },
  methods: {
    showCategory(categoryId) {
      this.$router.push({
        name: "category",
        params: { categoryId: categoryId },
      });
    },
  },
};
</script>
<style>
div {
  background-color: aqua;
}
</style>
