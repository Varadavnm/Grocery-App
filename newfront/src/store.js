import { createStore } from "vuex";

export default createStore({
  state: {
    productData: [],
    cart: [],
    loading: false, // Added loading state
    user: {}, // Added user state
  },
  mutations: {
    setProductData(state, products) {
      state.productData = products;
    },
    updateStock(state, { productId, quantity }) {
      const productIndex = state.productData.findIndex(
        (p) => p.id === productId
      );

      if (productIndex !== -1) {
        state.productData[productIndex] = {
          ...state.productData[productIndex],
          stock: state.productData[productIndex].stock - quantity,
        };
      }
    },
    addToCart(state, product) {
      const existingProduct = state.cart.find((item) => item.id === product.id);

      if (existingProduct) {
        existingProduct.quantity += 1;
      } else {
        state.cart.push({ ...product, quantity: 1 });
      }
    },
    setLoading(state, value) {
      state.loading = value;
    },
    setUser(state, user) {
      state.user = user;
    },
  },
  actions: {
    async fetchProductData({ commit }) {
      commit("setLoading", true);

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
          commit("setProductData", data.products);
        }
      } catch (error) {
        console.error("Error fetching product data:", error);
        // Optionally, you might want to commit an error state or message here
      } finally {
        commit("setLoading", false);
      }
    },
    async sendPurchaseEmail({ commit }, selectedProduct) {
      commit("setLoading", true);

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
            body: JSON.stringify({ item_name: selectedProduct }),
          }
        );

        if (response.ok) {
          commit("updateStock", { productId: selectedProduct, quantity: 1 });
          commit("addToCart", selectedProduct);
        } else {
          // Handle failure if needed
        }
      } catch (error) {
        console.error("Error sending purchase email:", error);
        // Optionally, you might want to commit an error state or message here
      } finally {
        commit("setLoading", false);
      }
    },
    async fetchUserData({ commit }) {
      commit("setLoading", true);

      try {
        const token = localStorage.getItem("access_token");
        const response = await fetch("http://127.0.0.1:5000/user_profile", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const userData = await response.json();
          commit("setUser", userData);
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
        // Optionally, you might want to commit an error state or message here
      } finally {
        commit("setLoading", false);
      }
    },
  },
  getters: {
    getProductData: (state) => state.productData,
    cartTotalQuantity(state) {
      return state.cart.reduce((total, product) => total + product.quantity, 0);
    },
    isLoading(state) {
      return state.loading;
    },
    getUserData: (state) => state.user,
  },
});
