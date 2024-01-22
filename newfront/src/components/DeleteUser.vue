<template>
  <div>
    <h2>Delete User</h2>
    <button @click="deleteCurrentUser">Delete My Account</button>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import jwt_decode from "jwt-decode";

export default {
  data() {
    return {
      error: null,
    };
  },
  methods: {
    async deleteCurrentUser() {
      const confirmed = window.confirm(
        "Are you sure you want to delete your account?"
      );

      if (!confirmed) {
        // If the user cancels, do nothing
        return;
      }

      try {
        // Fetch user information from localStorage
        const token = localStorage.getItem("access_token");

        // Decode the access token
        const decodedToken = jwt_decode(token);

        // Check if the decoded token has the expected structure
        if (!decodedToken || typeof decodedToken.sub === "undefined") {
          console.error("Invalid decoded token structure.");
          this.error = "Invalid user information in the token.";
          return;
        }

        // Extract user ID from the decoded token
        const userId = decodedToken.sub;

        const response = await fetch(
          `http://127.0.0.1:5000/delete_user/${userId}`,
          {
            method: "DELETE",
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          this.error = `Error: ${response.status} - ${errorData.message}`;
          console.error("User Deletion Error:", errorData);
        } else {
          localStorage.removeItem("user");

          const responseData = await response.json();
          this.error = null;
          console.log("User Deletion Successful:", responseData);
          window.location.reload();
          this.$router.push("/register_user");
        }
      } catch (error) {
        this.error = "Error deleting user.";
        console.error("Error deleting user:", error);
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
