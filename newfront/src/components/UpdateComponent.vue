<template>
  <div class="container mt-5">
    <h2 class="mb-4">Update User Information</h2>
    <form @submit.prevent="updateUser" class="needs-validation">
      <div class="mb-3">
        <label for="username" class="form-label">Username:</label>
        <input
          type="text"
          id="username"
          v-model="username"
          class="form-control"
        />
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">Email:</label>
        <input type="email" id="email" v-model="email" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="address" class="form-label">Address:</label>
        <input
          type="text"
          id="address"
          v-model="address"
          class="form-control"
        />
      </div>
      <div class="mb-3">
        <label for="phone_number" class="form-label">Phone Number:</label>
        <input
          type="text"
          id="phone_number"
          v-model="phone_number"
          class="form-control"
        />
      </div>
      <div class="mb-3">
        <label for="department" class="form-label">Department:</label>
        <input
          type="text"
          id="department"
          v-model="department"
          class="form-control"
        />
      </div>
      <div class="mb-3">
        <label for="new_password" class="form-label">New Password:</label>
        <input
          type="password"
          id="new_password"
          v-model="new_password"
          class="form-control"
        />
      </div>

      <button type="submit" class="btn btn-primary">Update Information</button>
    </form>
    <p v-if="error" class="text-danger mt-3">{{ error }}</p>
    <div v-if="message" class="text-success mt-3">
      <p>{{ message }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      email: "",
      address: "",
      phone_number: "",
      department: "",
      new_password: "",
      error: null,
      message: "",
    };
  },
  methods: {
    async updateUser() {
      try {
        const token = localStorage.getItem("access_token");

        const response = await fetch("http://localhost:5000/update_profile", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            address: this.address,
            phone_number: this.phone_number,
            department: this.department,
            new_password: this.new_password,
          }),
        });

        if (response.ok) {
          this.message = "User information updated successfully";
        } else {
          this.error = "Failed to update user information. Please try again.";
        }
      } catch (error) {
        this.error = "An error occurred while updating user information.";
        console.error("Error:", error);
      }
    },
  },
};
</script>

<style scoped>
@media only screen and (max-width: 767px) {
  .container {
    width: 100%;
    padding: 0 15px;
  }
}

@media only screen and (min-width: 768px) {
  .needs-validation {
    max-width: 500px;
    margin: auto;
  }
}

.form-label {
  font-weight: bold;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
}

.btn-primary:hover {
  background-color: #0056b3;
}
</style>
