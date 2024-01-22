<template>
  <div>
    <button @click="logout">Logout</button>
  </div>
</template>
<script>
export default {
  methods: {
    async logout() {
      try {
        const token = localStorage.getItem("access_token");

        const response = await fetch("http://127.0.0.1:5000/logout", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          window.location.reload();
          localStorage.removeItem("access_token");
          localStorage.removeItem("email");
          localStorage.removeItem("role");
          console.log("Successfully logged out");

          this.$router.push("/");
          await this.$store.dispatch("fetchUserData");
        } else {
          console.error("Error logging out. Status:", response.status);
        }
      } catch (error) {
        console.error("Error logging out:", error);
      }
    },
  },
};
</script>
