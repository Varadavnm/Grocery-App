<template>
  <div>
    <div>
      <b-container class="mt-4">
        <b-row>
          <b-col>
            <input
              type="date"
              id="selectedDate"
              v-model="selectedDate"
              required
            />
          </b-col>
          <b-col>
            <b-button @click="generateDailyPurchaseReport" variant="primary">
              Generate Daily Purchase Report
            </b-button>
            <b-button @click="generateMonthlyPurchaseReport" variant="primary">
              Generate Monthly Purchase Report
            </b-button>
          </b-col>
        </b-row>
      </b-container>
      <div v-if="dailyPurchaseReport" class="mt-4">
        <h2 class="mb-3">Daily Purchase Report</h2>
        <div
          v-for="(purchase, index) in dailyPurchaseReport.daily_purchases"
          :key="index"
          class="purchase-item"
        >
          <p>
            <strong>Item Name:</strong> {{ purchase.item_name }}<br />
            <strong>Item Quantity:</strong> {{ purchase.item_quantity }}<br />
            <strong>Total Amount:</strong> {{ purchase.total_amount }}
          </p>
        </div>
        <p class="mt-3">
          <strong>CSV File:</strong>
          <a
            @click="downloadCSV('daily_purchase_report.csv')"
            class="download-link"
            >Download CSV</a
          >
        </p>
        <img
          :src="'data:image/png;base64,' + dailyBarChartImageUrl"
          alt="Bar Chart"
        />
      </div>

      <div v-if="monthlyPurchaseReport" class="mt-4">
        <h2 class="mb-3">Monthly Purchase Report</h2>
        <div
          v-for="(purchase, index) in monthlyPurchaseReport.monthly_purchases"
          :key="index"
          class="purchase-item"
        >
          <p>
            <strong>Item Name:</strong> {{ purchase.item_name }}<br />
            <strong>Item Quantity:</strong> {{ purchase.item_quantity }}<br />
            <strong>Total Amount:</strong> {{ purchase.total_amount }}
          </p>
        </div>
        <p class="mt-3">
          <strong>CSV File:</strong>
          <a
            @click="downloadCSV('monthly_purchase_report.csv')"
            class="download-link"
            >Download CSV</a
          >
        </p>
        <img
          :src="'data:image/png;base64,' + monthlyBarChartImageUrl"
          alt="Monthly Bar Chart"
        />
      </div>
    </div>
    <div class="container mt-4">
      <div v-if="categoryRequests && categoryRequests.length > 0">
        <h3>Category Requests</h3>
        <ul class="list-group">
          <li
            v-for="categoryRequest in categoryRequests"
            :key="categoryRequest.category_name"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            {{ categoryRequest.category_name }}
            <div>
              <button
                @click="
                  approveCategory(categoryRequest.category_name, 'approve')
                "
                class="btn btn-success"
              >
                Approve
              </button>
              <button
                @click="
                  approveCategory(categoryRequest.category_name, 'disapprove')
                "
                class="btn btn-danger"
              >
                Not Approve
              </button>
            </div>
          </li>
        </ul>
      </div>

      <div v-if="managers && managers.length > 0" class="mt-4">
        <h3>Manager Requests</h3>
        <ul class="list-group">
          <li
            v-for="manager in managers"
            :key="manager.id"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            {{ manager.username }} - {{ manager.email }}
            <div>
              <button
                @click="approveManager(manager.id, 'approve')"
                class="btn btn-success"
              >
                Approve
              </button>
              <button
                @click="approveManager(manager.id, 'disapprove')"
                class="btn btn-danger"
              >
                Not Approve
              </button>
            </div>
          </li>
        </ul>
      </div>

      <div
        v-if="categoryUpdateRequests && categoryUpdateRequests.length > 0"
        class="mt-4"
      >
        <h3>Category Update Requests</h3>
        <ul class="list-group">
          <li
            v-for="updateRequest in categoryUpdateRequests"
            :key="updateRequest.id"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            {{ updateRequest.name }}
            <div>
              <button
                @click="
                  approveCategoryUpdate(
                    updateRequest.id,
                    'approve',
                    updateRequest.name
                  )
                "
                class="btn btn-success"
              >
                Approve
              </button>
              <button
                @click="
                  approveCategoryUpdate(
                    updateRequest.id,
                    'disapprove',
                    updateRequest.name
                  )
                "
                class="btn btn-danger"
              >
                Not Approve
              </button>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <div class="d-flex flex-column justify-content-left">
      <div v-for="category in categories" :key="category.id">
        <div class="card m-4 justify-content-center" style="width: 8rem">
          <img
            v-if="category.name === 'Fresh Milk'"
            class="card-img-top"
            :src="require('@/assets/Milk.png')"
            alt="Fresh Milk Image"
          />
          <img
            v-else-if="category.name === 'Pulses'"
            class="card-img-top align-items-centre display-flex"
            :src="require('@/assets/Staples.png')"
            alt="Pulses Image"
          />
          <div class="card-body">
            <h5 class="card-title">{{ category.name }}</h5>
          </div>
          <div>
            <button
              @click="navigateToUpdateCategory(category.id)"
              class="btn btn-warning"
            >
              Update
            </button>
            <button @click="DeleteCategory(category.id)" class="btn btn-danger">
              Delete Category
            </button>
            <!-- Button to Navigate -->
            <button
              @click="navigateToCategory(category.id)"
              class="btn btn-primary"
            >
              Go to {{ category.name }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: "",
      categoryRequests: [],
      managers: [],
      categories: [],
    };
  },
  created() {
    this.fetchCategoryRequests();
    this.fetchManagers();
    this.fetchCategoryUpdateRequests();
  },
  methods: {
    navigateToUpdateCategory(categoryId) {
      this.$router.push({
        name: "updateCategoryAdmin",
        params: { categoryId: categoryId },
      });
      console.log(categoryId);
    },
    DeleteCategory(categoryId) {
      this.$router.push({
        name: "deleteCategoryAdmin",
        params: { id: categoryId },
      });
      console.log(categoryId);
    },
    async fetchCategoryRequests() {
      try {
        const token = localStorage.getItem("access_token");

        const response = await fetch("http://127.0.0.1:5000/request_category", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.categoryRequests = data.category_requests;
          if (this.categoryRequests.length === 0) {
            this.message = "No category requests at present";
          } else {
            this.message = "";
          }
        } else {
          this.message = "An error occurred while fetching category requests";
        }
      } catch (error) {
        this.message = "An error occurred while fetching category requests";
        console.error("Error:", error);
      }
    },
    async fetchCategoryUpdateRequests() {
      try {
        const token = localStorage.getItem("access_token");

        const response = await fetch(
          "http://127.0.0.1:5000/update_category_request",
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (response.ok) {
          const data = await response.json();
          this.categoryUpdateRequests = data.update_requests;
          if (this.categoryUpdateRequests.length === 0) {
            this.message = "No category update requests at present";
          } else {
            this.message = "";
          }
        } else {
          this.message =
            "An error occurred while fetching category update requests";
        }
      } catch (error) {
        this.message =
          "An error occurred while fetching category update requests";
        console.error("Error:", error);
      }
    },
    async approveCategoryUpdate(updateRequestId, action, categoryName) {
      try {
        const token = localStorage.getItem("access_token");

        const postResponse = await fetch(
          `http://127.0.0.1:5000/update_category/${updateRequestId}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              action: action,
              name: categoryName,
            }),
          }
        );

        if (postResponse.ok) {
          this.categoryUpdateRequests = this.categoryUpdateRequests.filter(
            (request) => request.id !== updateRequestId
          );

          const postData = await postResponse.json();
          this.message = postData.message;
        } else {
          this.message = "Sorry, category update request not approved!";
        }
      } catch (error) {
        console.error("Error approving category update:", error);
      }
    },

    async fetchManagers() {
      try {
        const token = localStorage.getItem("access_token");

        const response = await fetch("http://127.0.0.1:5000/add_manager", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.managers = data.managers;
          if (this.managers.length === 0) {
            this.message = "No manager requests at present";
          } else {
            this.message = "";
          }
        } else {
          this.message = "An error occurred while fetching manager requests";
        }
      } catch (error) {
        this.message = "An error occurred while fetching manager requests";
        console.error("Error:", error);
      }
    },
    async approveCategory(categoryName, action) {
      if (action === "approve") {
        try {
          const token = localStorage.getItem("access_token");

          const postResponse = await fetch(
            "http://127.0.0.1:5000/add_category",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
              body: JSON.stringify({
                category_name: categoryName,
                action: action,
              }),
            }
          );

          if (postResponse.ok) {
            this.categoryRequests = this.categoryRequests.filter(
              (request) => request.name !== categoryName
            );

            const postData = await postResponse.json();
            this.message = postData.message;
          } else {
            this.message = "Sorry, category request not approved!";
          }
        } catch (error) {
          console.error("Error approving category:", error);
        }
      } else {
        this.message = "Sorry, category request not approved!";
      }
    },

    async approveManager(managerId, action) {
      if (action === "approve") {
        try {
          const token = localStorage.getItem("access_token");
          const manager = this.managers.find((m) => m.id === managerId);

          const postResponse = await fetch(
            "http://127.0.0.1:5000/add_manager",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
              body: JSON.stringify({
                id: managerId,
                username: manager.username,
                email: manager.email,
                password: manager.password,
                address: manager.address,
                phone_number: manager.phone_number,
                fs_uniquifier: manager.fs_uniquifier,
                department: manager.department,
                filename: manager.filename,
                action: action,
              }),
            }
          );

          if (postResponse.ok) {
            const postData = await postResponse.json();
            this.message = postData.message;
            this.fetchManagers();
          } else {
            this.message = "Sorry, manager not approved!";
          }
        } catch (error) {
          console.error("Error approving manager:", error);
        }
      }
    },
    async generateDailyPurchaseReport() {
      try {
        const token = localStorage.getItem("access_token");
        const apiUrl = "http://127.0.0.1:5000/dashboard";

        const response = await fetch(apiUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            selected_date: this.selectedDate,
          }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        // Daily report data and chart
        const dailyCsvData = data.csv_data;
        this.dailyBarChartImageUrl = data.bar_chart_image_daily;

        // Display daily report data
        const dailyBlob = new Blob([dailyCsvData], { type: "text/csv" });
        const dailyLink = document.createElement("a");
        dailyLink.href = window.URL.createObjectURL(dailyBlob);
        dailyLink.download = "daily_purchase_report.csv";
        document.body.appendChild(dailyLink);
        dailyLink.click();
        document.body.removeChild(dailyLink);

        this.dailyPurchaseReport = data;
      } catch (error) {
        console.error("Error generating daily purchase report:", error);
      }
    },

    async generateMonthlyPurchaseReport() {
      try {
        const token = localStorage.getItem("access_token");
        const apiUrl = "http://127.0.0.1:5000/dashboard";

        const response = await fetch(apiUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            selected_date: this.selectedDate,
          }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        // Monthly report data and chart
        const monthlyCsvData = data.csv_data_monthly;
        this.monthlyBarChartImageUrl = data.bar_chart_image_monthly;

        // Display monthly report data
        const monthlyBlob = new Blob([monthlyCsvData], { type: "text/csv" });
        const monthlyLink = document.createElement("a");
        monthlyLink.href = window.URL.createObjectURL(monthlyBlob);
        monthlyLink.download = "monthly_purchase_report.csv";
        document.body.appendChild(monthlyLink);
        monthlyLink.click();
        document.body.removeChild(monthlyLink);

        this.monthlyPurchaseReport = data;
      } catch (error) {
        console.error("Error generating monthly purchase report:", error);
      }
    },

    downloadCSV(fileName) {
      fetch(`http://localhost:5000/download_csv/${fileName}`)
        .then((response) => response.blob())
        .then((blob) => {
          const link = document.createElement("a");
          link.href = window.URL.createObjectURL(blob);
          link.download = fileName;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        })
        .catch((error) => {
          console.error("Error downloading CSV:", error);
        });
    },
  },
  mounted() {
    // Fetch categories and products using the fetch API
    fetch("http://localhost:5000/categories")
      .then((response) => response.json())
      .then((data) => {
        this.categories = data.categories;
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  },
};
</script>
