<template>
  <div class="container mt-4">
    <div class="card">
      <div class="card-body">
        <h2 class="card-title text-center mb-4">Login as Customer</h2>
        <form @submit.prevent="loginCustomer">
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
        <div v-if="message" class="mt-3">
          <p>{{ message }}</p>
          <p>{{ message2 }}</p>
        </div>
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
      message2: "", // Added message2
      accessToken: "",
    };
  },
  methods: {
    async loginCustomer() {
      try {
        const response = await fetch("http://127.0.0.1:5000/login_customer", {
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
          console.log("Login successful:", data);
          // After successful login
          this.$store.dispatch("fetchUserData");
          this.$router.push("/");
          window.location.reload();

          // Update message and access token
          this.message = data.message;
          this.accessToken = data.access_token;
          localStorage.setItem("access_token", data.access_token);
          localStorage.setItem("email", this.email); // Store the email in 'email'
          localStorage.setItem("role", "customer"); // Store the role in 'role'
        } else {
          // Login failed
          this.error = "Invalid credentials. Please try again.";
          console.error("Login failed:", response.status, response.statusText);
        }
      } catch (error) {
        this.error = "An error occurred while logging in.";
        console.error("Error:", error);
      }
    },
  },
};
</script>
