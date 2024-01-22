<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
<template>
  <div>
    <h2> Cart </h2>
    <h3>{{ message }}</h3>
    <ul>
      <li v-for="(item, index) in userCart" :key="index">
        <div>{{ item.item_name }}</div>
        <div>Quantity: {{ item.item_quantity }}</div>
        <div>Total Amount: {{ item.total_amount }}</div>
      </li>
    </ul>
    <button @click="proceedToCheckout">Proceed to Checkout</button>
  </div>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  data() {
    return {
      isCartModalOpen: true,
      userCart: [],
      message: '', // Add this line to initialize message
    };
  },
  methods: {
    showCartModal() {
      this.isCartModalOpen = true;
    },
    closeCartModal() {
      this.isCartModalOpen = false;
    },
    async proceedToCheckout() {
      // Make a POST request to the server to initiate the checkout process
      const token = localStorage.getItem("access_token"); // Get the user's access token from local storage

      try {
        const response = await fetch("http://127.0.0.1:5000/purchase_cart", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          this.message = "Purchase successful";
          this.userCart = [];
        } else {
          console.error("Error during checkout:", response.statusText);
        }
      } catch (error) {
        console.error("Error during checkout:", error);
      }
    },
  },
  async created() {
    // Fetch the user's cart items when the component is created
    const token = localStorage.getItem("access_token"); // Get the user's access token from local storage

    try {
      const response = await fetch("http://127.0.0.1:5000/view_cart", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        this.userCart = data; // Update the userCart with the fetched cart data
      } else {
        console.error("Error fetching cart data:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching cart data:", error);
    }
  },
});
// eslint-disable-next-line prettier/prettier
</script>