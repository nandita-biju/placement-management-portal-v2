<template>
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
          to="/admin/dashboard"
          class="nav-link text-white"
        >
          Dashboard
        </router-link>
      </li>

      <li class="nav-item mb-2">
        <router-link
          to="/admin/companies"
          class="nav-link text-white"
        >
          Companies
        </router-link>
      </li>

      <li class="nav-item mb-2">
        <router-link
          to="/admin/students"
          class="nav-link text-white"
        >
          Students
        </router-link>
      </li>

      <li class="nav-item mb-2">
        <router-link
          to="/admin/drives"
          class="nav-link text-white"
        >
          Placement Drives
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