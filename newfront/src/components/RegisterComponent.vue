<template>
  <div class="container mt-4">
    <div class="card">
      <div class="card-body">
        <h2 class="card-title text-center mb-4">
          Register {{ role_name === "manager" ? "Manager" : "Customer" }}
        </h2>
        <form @submit.prevent="registerUser">
          <div class="mb-3">
            <label for="name" class="form-label">Name:</label>
            <input
              type="text"
              id="name"
              v-model="name"
              class="form-control"
              required
            />
          </div>
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
          <div class="mb-3">
            <label for="role" class="form-label">Role:</label>
            <select id="role" v-model="role_name" class="form-select" required>
              <option value="customer">Customer</option>
              <option value="manager">Manager</option>
            </select>
          </div>
          <div class="mb-3">
            <label for="address" class="form-label">Address:</label>
            <input
              type="text"
              id="address"
              v-model="address"
              class="form-control"
              required
            />
          </div>
          <div class="mb-3">
            <label for="phone_number" class="form-label">Phone Number:</label>
            <input
              type="text"
              id="phone_number"
              v-model="phone_number"
              class="form-control"
              required
            />
          </div>
          <div v-if="role_name === 'manager'" class="mb-3">
            <label for="department" class="form-label">Department:</label>
            <input
              type="text"
              id="department"
              v-model="department"
              class="form-control"
              required
            />
          </div>
          <div class="d-grid">
            <button type="submit" class="btn btn-primary">Register</button>
          </div>
        </form>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>
        <p v-if="error" class="error mt-3">{{ error }}</p>
      </div>
    </div>
    <div class="mt-4">
      <input type="file" @change="handleFileChange" class="form-control" />
      <div class="mt-2">
        <button @click="uploadFile" class="btn btn-secondary">Upload</button>
      </div>
      <p v-if="fileUploadError" class="error mt-2">{{ fileUploadError }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: "",
      email: "",
      password: "",
      role_name: "customer",
      address: "",
      phone_number: "",
      department: "",
      error: null,
      selectedFile: null,
      fileUploadError: null,
      successMessage: null,
    };
  },
  methods: {
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    async registerUser() {
      try {
        // Prepare the JSON data
        const jsonData = {
          name: this.name,
          email: this.email,
          password: this.password,
          role_name: this.role_name,
          address: this.address,
          phone_number: this.phone_number,
          department: this.department,
        };

        const formData = new FormData();
        formData.append("file", this.selectedFile);
        formData.append("data", JSON.stringify(jsonData));

        const response = await fetch("http://127.0.0.1:5000/register_user", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          const errorData = await response.json();
          this.error = `Error: ${response.status} - ${errorData.message}`;
          console.error("Registration Error:", errorData);
        } else {
          const responseData = await response.json();
          this.error = null;
          this.successMessage = "Registration successful!";
          console.log("Registration Successful:", responseData);
          window.location.reload();
        }
      } catch (error) {
        this.error = "An error occurred while registering.";
        console.error("Error:", error);
      }
    },
    async uploadFile() {
      try {
        const formData = new FormData();
        formData.append("file", this.selectedFile);

        const response = await fetch("http://127.0.0.1:5000/upload_file", {
          method: "POST",
          body: formData,
        });
        if (!response.ok) {
          const errorData = await response.json();
          this.fileUploadError = `Error: ${response.status} - ${errorData.message}`;
          console.error("File Upload Error:", errorData);
        } else {
          const responseData = await response.json();
          this.fileUploadError = null;
          console.log("File Upload Successful:", responseData);
        }
      } catch (error) {
        this.fileUploadError = "Error uploading file.";
        console.error("Error uploading file:", error);
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
