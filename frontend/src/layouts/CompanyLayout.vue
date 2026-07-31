<template>
  <div class="d-flex">

    <!-- Sidebar -->
    <div
      class="bg-dark text-white d-flex flex-column p-3"
      style="width:280px; min-height:100vh;"
    >
      <div>

        <h4 class="mb-5">
          Placement Portal
        </h4>

        <ul class="nav flex-column">

          <li class="nav-item mb-3">
            <router-link
              to="/company/dashboard"
              class="nav-link text-white"
            >
              Dashboard
            </router-link>
          </li>

          <li class="nav-item mb-3">
            <router-link
              to="/company/profile"
              class="nav-link text-white"
            >
              Company Profile
            </router-link>
          </li>

          <li class="nav-item mb-3">
            <router-link
              to="/company/create-drive"
              class="nav-link text-white"
            >
              Create Drive
            </router-link>
          </li>

          <li class="nav-item mb-3">
            <router-link
              to="/company/drives"
              class="nav-link text-white"
            >
              My Drives
            </router-link>
          </li>

          <li class="nav-item mb-3">
            <router-link
              to="/company/applicants"
              class="nav-link text-white"
            >
              Applicants
            </router-link>
          </li>

        </ul>

      </div>

      <!-- Logout button at bottom -->
      <div class="mt-auto">
        <button
          class="btn btn-danger w-100"
          @click="logout"
        >
          Logout
        </button>
      </div>

    </div>

    <!-- Main Content -->
    <div class="flex-grow-1 bg-light">

      <nav class="navbar navbar-light bg-white shadow-sm px-4">
        <h4 class="mb-0">
          Company Portal
        </h4>
      </nav>

      <div class="p-4">
        <router-view />
      </div>

    </div>

  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const logout = () => {

    localStorage.removeItem("token");
    localStorage.removeItem("role");

    router.push("/");

};
</script>