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
              @click="navigateToRequestUpdateCategory(category.id)"
              class="btn btn-warning"
            >
              Request Update
            </button>
            <button
              @click="requestDeleteCategory(category.id)"
              class="btn btn-danger"
            >
              Request Deletion
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
      selectedDate: null,
      today: new Date().toISOString().split("T")[0],
      dailyPurchaseReport: null,
      dailyBarChartImageUrl: null,
      monthlyPurchaseReport: null,
      monthlyBarChartImageUrl: null,
      categories: [],
    };
  },
  methods: {
    navigateToRequestUpdateCategory(categoryId) {
      this.$router.push({
        name: "updateCategoryRequest",
        params: { categoryId: categoryId },
      });
      console.log(categoryId);
    },

    requestDeleteCategory(categoryId) {
      this.$router.push(`/delete_category_request/${categoryId}`);
    },
    navigateToCategory(categoryId) {
      this.$router.push({ name: "category", params: { categoryId } });
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
    showCategory(categoryId) {
      this.$router.push({
        name: "category",
        params: { categoryId: categoryId },
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

<style scoped>
.purchase-item {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
}

.download-link {
  color: #007bff;
  text-decoration: underline;
  cursor: pointer;
}

.download-link:hover {
  color: #0056b3;
}
</style>
