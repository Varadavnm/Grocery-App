<template>
  <div class="container">
    <h2 class="mt-4">Add Item</h2>
    <form @submit.prevent="addItem" class="mt-4">
      <div class="mb-3">
        <label for="name" class="form-label">Name:</label>
        <input
          type="text"
          id="name"
          v-model="name"
          required
          class="form-control"
        />
      </div>
      <div class="mb-3">
        <label for="category" class="form-label">Category:</label>
        <select id="category" v-model="category" required class="form-select">
          <option value="" disabled>Select a category</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">
            {{ cat.category_name }}
          </option>
          <option value="request_new_category">Request New Category</option>
        </select>

        <div v-if="category === 'request_new_category'" class="mt-3">
          <label for="new_category" class="form-label">New Category:</label>
          <input
            type="text"
            id="new_category"
            v-model="newCategory"
            required
            class="form-control"
          />
          <button @click="requestNewCategory" class="btn btn-primary mt-2">
            Request New Category
          </button>
        </div>
      </div>

      <div class="mb-3">
        <label for="stock" class="form-label">Stock:</label>
        <input
          type="number"
          id="stock"
          v-model="stock"
          required
          class="form-control"
        />
      </div>
      <div class="mb-3">
        <label for="manufacture_date" class="form-label"
          >Manufacture Date:</label
        >
        <input
          type="date"
          id="manufacture_date"
          v-model="manufacture_date"
          required
          class="form-control"
        />
      </div>
      <div class="mb-3">
        <label for="expiry_date" class="form-label">Expiry Date:</label>
        <input
          type="date"
          id="expiry_date"
          v-model="expiry_date"
          required
          class="form-control"
        />
      </div>
      <div class="mb-3">
        <label for="rate_per_unit" class="form-label">Rate per Unit:</label>
        <input
          type="number"
          id="rate_per_unit"
          v-model="rate_per_unit"
          required
          class="form-control"
        />
      </div>
      <div class="mb-3">
        <input type="file" @change="handleFileChange" class="form-control" />
        <button @click="uploadFile" class="btn btn-primary mt-2">Upload</button>
        <p v-if="fileUploadError" class="error mt-2">{{ fileUploadError }}</p>
      </div>
      <button type="submit" class="btn btn-primary">Add Item</button>
    </form>
    <p v-if="message" class="success mt-3">{{ message }}</p>
    <p v-if="error" class="error mt-3">{{ error }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: "",
      category: "",
      categories: [],
      stock: 0,
      manufacture_date: "",
      expiry_date: "",
      rate_per_unit: 0.0,
      newCategory: "",
      selectedFile: null,
      fileUploadError: null,
      error: null,
      message: null,
    };
  },
  created() {
    this.getCategories();
  },
  methods: {
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    async getCategories() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await fetch("http://localhost:5000/get_categories", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.categories = data.categories;
          // console.log("Categories fetched successfully:", this.categories);
        } else {
          console.log("Failed to fetch categories. Response:", response);
        }
      } catch (error) {
        console.error("Error fetching categories:", error);
      }
    },

    async addItem() {
      try {
        const jsonData = {
          name: this.name,
          category_id: this.category,
          stock: this.stock,
          manufacture_date: this.manufacture_date,
          expiry_date: this.expiry_date,
          rate_per_unit: this.rate_per_unit,
        };
        console.log(jsonData);
        const formData = new FormData();
        formData.append("file", this.selectedFile);
        formData.append("data", JSON.stringify(jsonData));
        const token = localStorage.getItem("access_token");
        const response = await fetch("http://localhost:5000/add_item", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        });

        if (response.ok) {
          const responseData = await response.json();
          this.message = responseData.message;
          this.name = "";
          this.category = "";
          this.stock = 0;
          this.manufacture_date = "";
          this.expiry_date = "";
          this.rate_per_unit = 0.0;
        } else {
          const errorData = await response.json();
          this.error = `Error: ${response.status} - ${errorData.message}`;
        }
      } catch (error) {
        this.error = "An error occurred while adding the item.";
        console.error("Error:", error);
      }
    },

    async uploadFile() {
      try {
        const formData = new FormData();
        formData.append("file", this.selectedFile);

        // Append the JSON data with the key "data"
        formData.append(
          "data",
          JSON.stringify({
            name: this.name,
            stock: this.stock,
            category_id: this.category,
            rate_per_unit: this.rate_per_unit,
            manufacture_date: this.manufacture_date,
            expiry_date: this.expiry_date,
          })
        );

        const token = localStorage.getItem("access_token");
        const response = await fetch("http://localhost:5000/add_item", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        });
        if (response.ok) {
          const responseData = await response.json();
          this.message = responseData.message;
          this.selectedFile = null;
        } else {
          const errorData = await response.json();
          this.fileUploadError = `Error: ${response.status} - ${errorData.message}`;
        }
      } catch (error) {
        this.fileUploadError = "Error uploading file.";
        console.error("Error uploading file:", error);
      }
    },

    async requestNewCategory() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await fetch("http://localhost:5000/request_category", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            category_name: this.newCategory,
          }),
        });

        if (response.ok) {
          const responseData = await response.json();
          this.message = responseData.message;
          this.newCategory = ""; // Clear the new category input field after a successful request
          window.location.reload();
        } else {
          const errorData = await response.json();
          this.error = `Error: ${response.status} - ${errorData.message}`;
        }
      } catch (error) {
        this.error = "An error occurred while requesting a new category.";
        console.error("Error:", error);
      }
    },
  },
};
</script>

<style scoped>
.error {
  color: red;
}
.success {
  color: green;
}
</style>
