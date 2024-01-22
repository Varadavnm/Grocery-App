<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <router-link class="navbar-brand" to="/">Home</router-link>

      <!-- Navbar Toggler for Small Screens -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navbar Items -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <user-profile />
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/login_admin"
              >Admin Login</router-link
            >
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/login_customer"
              >Login Customer</router-link
            >
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/login_manager"
              >Manager Login</router-link
            >
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/register_user"
              >Register</router-link
            >
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/add_to_cart"
              >Purchase</router-link
            >
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/add_item"
              >Add Products</router-link
            >
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/add_category"
              >Add Category</router-link
            >
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/search">Search</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/delete_user"
              >Delete User</router-link
            >
          </li>
          <li v-if="isManager()" class="nav-item">
            <router-link class="nav-link" to="/manager_dashboard"
              >Manager Dashboard</router-link
            >
          </li>
          <li v-if="isAdmin()" class="nav-item">
            <router-link class="nav-link" to="/admin_dashboard"
              >Admin Dashboard</router-link
            >
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/logout">Logout</router-link>
          </li>
        </ul>
      </div>
    </nav>
    <router-link class="cart-link" to="/view_cart">
      <i class="bi bi-cart-fill"></i> Cart
    </router-link>
    <router-view />
  </div>
</template>

<script>
import UserProfile from "./components/UserprofileComponent.vue";
import "bootstrap/dist/css/bootstrap.css";

export default {
  components: {
    UserProfile,
  },
  computed: {},
  methods: {
    isManager() {
      // Check the user's role here
      const role = localStorage.getItem("role");
      if (role === "manager") {
        return true;
      }
    },
    isAdmin() {
      // Check the user's role here
      const role = localStorage.getItem("role");
      if (role === "admin") {
        return true;
      }
    },
  },
};
</script>

<style>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css");

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: skyblue;
}
.navbar-form .form-control {
  width: 150px;
}
</style>
