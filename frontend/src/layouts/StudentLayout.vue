<template>
  <div class="d-flex">

    <!-- Sidebar -->
    <div
      class="bg-dark text-white p-3"
      style="width:260px; min-height:100vh;"
    >
      <h4 class="mb-4">
        Placement Portal
      </h4>

      <ul class="nav flex-column">

        <li class="nav-item mb-2">
          <router-link
            to="/student/dashboard"
            class="nav-link text-white"
          >
            Dashboard
          </router-link>
        </li>

        <li class="nav-item mb-2">
          <router-link
            to="/student/profile"
            class="nav-link text-white"
          >
            My Profile
          </router-link>
        </li>

        <li class="nav-item mb-2">
          <router-link
            to="/student/profile/edit"
            class="nav-link text-white"
          >
            Edit Profile
          </router-link>
        </li>

        <li class="nav-item mb-2">
          <router-link
            to="/student/drives"
            class="nav-link text-white"
          >
            Explore
          </router-link>
        </li>

        <li class="nav-item mb-2">
          <router-link
            to="/student/applications"
            class="nav-link text-white"
          >
            My Applications
          </router-link>
        </li>

        <li class="nav-item mt-4">
          <button
            class="btn btn-danger w-100"
            @click="logout"
          >
            Logout
          </button>
        </li>

      </ul>

    </div>

    <!-- Main Content -->
    <div class="flex-grow-1">

      <nav class="navbar navbar-light bg-light shadow-sm px-4">
        <h4 class="mb-0">
          Student Portal
        </h4>
      </nav>

      <div class="p-4">
        <router-view />
      </div>

    </div>

  </div>
</template>


<script setup>
import StudentNavbar from "../components/Student/StudentNavbar.vue";
import StudentSidebar from "../components/Student/StudentSidebar.vue";
import { useRouter } from "vue-router";

const router = useRouter();

const logout = () => {

    localStorage.removeItem("token");
    localStorage.removeItem("role");

    router.push("/");

};
</script>