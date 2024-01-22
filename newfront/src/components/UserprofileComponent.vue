<template>
  <div>
    <h2>User Profile</h2>
    <div class="user-profile">
      <div class="profile-image">
        <img
          v-if="user.photo_base64"
          :src="'data:image/png;base64,' + user.photo_base64"
          alt="User Photo"
        />
      </div>
      <div class="user-details">
        <h3>{{ user.username }}</h3>
        <p>Email: {{ user.email }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: {},
    };
  },
  methods: {
    async fetchUser() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await fetch("http://127.0.0.1:5000/user_profile", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          console.error("Failed to fetch user profile");
          return;
        }

        const userData = await response.json();
        this.user = userData;
      } catch (error) {
        console.error("Error during user profile fetch:", error);
      }
    },
  },
  mounted() {
    this.fetchUser();
  },
};
</script>

<style>
.user-profile {
  display: flex;
  align-items: center;
}

.profile-image {
  width: 80px;
  height: 80px;
  overflow: hidden;
  border-radius: 100%;
  margin-right: 10px;
}

.profile-image img {
  width: 100%;
  height: auto;
  border-radius: 50%;
}
</style>
