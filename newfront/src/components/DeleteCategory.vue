<template>
  <div>
    <h2>Delete Category</h2>
    <p>Are you sure you want to delete this category?</p>
    <button @click="showConfirmationDialog" class="btn btn-danger">
      Delete Category
    </button>
    <div v-if="showDialog" class="modal" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Deletion</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="hideConfirmationDialog"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete this category?</p>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-dismiss="modal"
              @click="hideConfirmationDialog"
            >
              Cancel
            </button>
            <button
              type="button"
              class="btn btn-danger"
              @click="deleteCategory"
            >
              Delete
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
      showDialog: false,
    };
  },
  methods: {
    showConfirmationDialog() {
      this.showDialog = true;
    },
    hideConfirmationDialog() {
      this.showDialog = false;
    },
    async deleteCategory() {
      const categoryId = this.$route.params.categoryID;

      try {
        const response = await fetch(
          `http://localhost:5000/delete_category_request/${categoryId}`,
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log(data.message);
        this.$route.push("/");
      } catch (error) {
        console.error("Error deleting category:", error);
      } finally {
        this.hideConfirmationDialog();
      }
    },
  },
};
</script>
