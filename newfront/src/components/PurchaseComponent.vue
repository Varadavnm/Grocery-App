<template>
  <div>
    <div>
      <h2>Add Item to Cart</h2>
      <form @submit.prevent="addToCart">
        <div class="form-group">
          <label for="selectedProduct">Select a product:</label>
          <select
            v-model="selectedProduct"
            id="selectedProduct"
            class="form-control"
          >
            <option
              v-for="(product, index) in productData"
              :key="index"
              :value="product.item_name"
            >
              {{ product.item_name }} - :{{
                product.stock > 0 ? product.stock : "Out of Stock"
              }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="item_quantity">Quantity</label>
          <input
            v-model.number="item_quantity"
            type="number"
            id="item_quantity"
            class="form-control"
          />
        </div>
        <button type="submit" class="btn btn-primary">Add to Cart</button>
        <p class="text-danger" v-if="error">{{ error }}</p>
        <p class="text-success" v-if="message">{{ message }}</p>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedProduct: "",
      item_quantity: 1,
      productData: [],
      error: "",
      message: "",
    };
  },
  methods: {
    async addToCart() {
      if (this.selectedProduct) {
        try {
          const token = localStorage.getItem("access_token");

          const response = await fetch("http://127.0.0.1:5000/add_to_cart", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              item_name: this.selectedProduct,
              item_quantity: this.item_quantity,
            }),
          });

          if (response.ok) {
            this.message = "Item added to the Cart";
            this.error = "";
            this.selectedProduct = "";
            this.updateStock({
              itemName: this.selectedProduct,
              quantity: this.item_quantity,
            });
          } else {
            this.error = "Failed to add item. Please try again.";
            this.message = "";
          }
        } catch (error) {
          this.error = "An error occurred while adding the item.";
          this.message = "";
          console.error("Error:", error);
        }
      } else {
        this.error = "Please select a product to add to the cart.";
        this.message = "";
      }
    },
    updateStock({ itemName, quantity }) {
      this.$store.commit("updateStock", { itemName, quantity });
    },
    async fetchProductData() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await fetch("http://127.0.0.1:5000/get_products", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.productData = data.products;
        }
      } catch (error) {
        console.error("Error:", error);
      }
    },
    async sendPurchaseEmail() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await fetch(
          "http://127.0.0.1:5000/send_purchase_email",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ item_name: this.selectedProduct }),
          }
        );

        if (response.ok) {
          this.message = "Purchase email sent to admin.";
        } else {
          this.error = "Failed to send the purchase email. Please try again.";
        }
      } catch (error) {
        this.error = "An error occurred while sending the purchase email.";
        console.error("Error:", error);
      }
    },
  },
  created() {
    this.fetchProductData();
  },
};
</script>
