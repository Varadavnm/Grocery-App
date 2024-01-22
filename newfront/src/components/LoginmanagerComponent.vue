<template>
  <div class="container mt-4">
    <div class="card">
      <div class="card-body">
        <h2 class="card-title text-center mb-4">Manager Login</h2>
        <form @submit.prevent="loginmanager">
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
        <p v-if="error" class="error mt-3">{{ error }}</p>
        <p v-if="message" class="mt-3">
          {{ message }}
          <button @click="navigateToManagerDashboard" class="btn btn-secondary">
            Go to Dashboard
          </button>
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
      error: null,
      message: "",
      accessToken: "",
    };
  },
  methods: {
    navigateToManagerDashboard() {
      this.$router.push("/manager_dashboard");
    },
    async loginmanager() {
      try {
        const response = await fetch("http://127.0.0.1:5000/login_manager", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
          }),
        });

        if (response.ok) {
          // Login successful
          const data = await response.json();
          console.log("Manager Login successful:", data);
          // Update message and access token
          this.message = data.message;
          this.accessToken = data.access_token;
          localStorage.setItem("access_token", data.access_token);
          localStorage.setItem("email", this.email); // Store the email in 'email'
          localStorage.setItem("role", "manager"); // Store the role in 'role'
          window.location.reload();
        } else {
          // Login failed
          this.error = "Invalid manager credentials. Please try again.";
          console.error(
            "Manager Login failed:",
            response.status,
            response.statusText
          );
        }
      } catch (error) {
        this.error = "An error occurred while manager logging in.";
        console.error("Manager Login Error:", error);
      }
    },
  },
};
</script>

<style scoped>
.error {
  color: red;
}
</style>
