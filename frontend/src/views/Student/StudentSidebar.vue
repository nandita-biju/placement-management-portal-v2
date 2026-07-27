<template>
  <div class="sidebar bg-dark text-white">

    <h3 class="text-center py-4">
      Placement Portal
    </h3>

    <router-link to="/student/dashboard" class="menu">
      🏠 Dashboard
    </router-link>

    <router-link to="/student/profile" class="menu">
      👤 My Profile
    </router-link>

    <router-link to="/student/edit-profile" class="menu">
      ✏ Edit Profile
    </router-link>

    <router-link to="/student/drives" class="menu">
      💼 Placement Drives
    </router-link>

    <router-link to="/student/applications" class="menu">
      📄 My Applications
    </router-link>

    <router-link to="/student/notifications" class="menu">
      🔔 Notifications
    </router-link>

    <button
      class="btn btn-danger mx-3 mt-auto mb-4"
      @click="logout"
    >
      Logout
    </button>

  </div>
</template>

<script setup>

import { useRouter } from "vue-router";

const router = useRouter();

const logout = () => {

    localStorage.clear();

    router.push("/");

};

</script>

<style scoped>

.sidebar{

    width:250px;
    height:100vh;

    position:fixed;

    display:flex;
    flex-direction:column;

}

.menu{

    padding:16px 24px;

    color:white;

    text-decoration:none;

}

.menu:hover{

    background:#495057;

}

.router-link-active{

    background:#0d6efd;

}

</style>