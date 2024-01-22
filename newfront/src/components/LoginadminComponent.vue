<template>
  <div class="container mt-4">
    <div class="card">
      <div class="card-body">
        <h2 class="card-title text-center mb-4">Admin Login</h2>
        <form @submit.prevent="loginAdmin">
          <div class="mb-3">
            <label for="email" class="form-label">Email:</label>
            <input
              type="email"
              id="email"
              v-model="email"
              class="form-control"
              required
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password:</label>
            <input
              type="password"
              id="password"
              v-model="password"
              class="form-control"
              required
            />
          </div>
          <div class="d-grid">
            <button type="submit" class="btn btn-primary">Login</button>
          </div>
        </form>
        <p v-if="message" class="mt-3">
          {{ message }}
          <router-link to="/admin_dashboard" class="btn btn-success"
            >Go to Dashboard</router-link
          >
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
      message: "",
      access_token: "",
    };
  },
  methods: {
    navigateToAdminDashboard() {
      this.$router.push({ name: "adminDashboard" });
    },
    async loginAdmin(event) {
      event.preventDefault();
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/login_admin?include_auth_token",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email: this.email,
              password: this.password,
            }),
          }
        );

        if (response.status === 200) {
          const data = await response.json();
          localStorage.setItem("access_token", data.access_token);
          localStorage.setItem("email", this.email); // Store the email in 'email'
          localStorage.setItem("role", "admin"); // Store the role in 'role'
          this.message = "Login successful";
          this.access_token = data.access_token;
          console.log(this.access_token);
          this.router.push("/");
          window.location.reload();
        } else {
          const errorData = await response.json();
          this.message = errorData.message || "Login failed";
        }
      } catch (error) {
        console.error(error);
        this.message = "An error occurred during login";
      }
    },
  },
};
</script>
