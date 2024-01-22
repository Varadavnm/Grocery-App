<template>
  <div>
    <p>Rate this product:</p>
    <div class="rating-stars">
      <button v-for="star in 5" :key="star" @click="rateProduct(star)">
        {{ star }}
      </button>
    </div>
    <p v-if="rated !== null">You have rated this product</p>
    <p>Current Rating: {{ currentRating }}/5 stars</p>
  </div>
</template>

<script>
export default {
  props: ["id"],
  data() {
    return {
      rated: null,
      currentRating: 0,
    };
  },
  mounted() {
    this.fetchUserRating();
  },
  methods: {
    async fetchUserRating() {
      try {
        const accessToken = localStorage.getItem("access_token");

        const response = await fetch(
          `http://127.0.0.1:5000/rate_product/${this.productId}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${accessToken}`,
              "Content-Type": "application/json",
            },
          }
        );

        if (!response.ok) {
          console.error("Failed to fetch user rating");
          return;
        }

        const ratingData = await response.json();
        this.rated = ratingData.current_rating;
        this.currentRating = ratingData.current_rating;
      } catch (error) {
        console.error("Error during user rating fetch:", error);
      }
    },
    async rateProduct(stars) {
      try {
        const accessToken = localStorage.getItem("access_token");

        if (!accessToken) {
          console.error("Access token is missing");
          return;
        }

        const response = await fetch(
          `http://127.0.0.1:5000/rate_product/${this.productId}`,
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${accessToken}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              productId: this.productId,
              stars: stars,
            }),
          }
        );

        if (!response.ok) {
          console.error("Failed to submit rating");
          const errorData = await response.json();
          console.error("Error details:", errorData);
          return;
        }

        const responseData = await response.json();
        console.log(
          "Rating submitted successfully. New rating:",
          responseData.current_rating
        );
        this.rated = stars;
        this.currentRating = responseData.current_rating;
      } catch (error) {
        console.error("Error during rating submission:", error);
      }
    },
  },
};
</script>

<style scoped>
.rating-stars {
  display: flex;
}

.rating-stars button {
  background: none;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
  margin-right: 5px;
}

.rating-stars button:hover {
  color: #f39c12; /* Highlight color on hover */
}

.rating-stars button.active {
  color: #f39c12; /* Rated star color */
}

body {
  background-color: lightgreen;
}
</style>
