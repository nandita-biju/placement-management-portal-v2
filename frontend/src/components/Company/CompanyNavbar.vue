<template>
  <nav class="navbar navbar-light bg-white shadow-sm">

    <div class="container-fluid">

      <h3 class="mb-0">
        Student Portal
      </h3>

      <button
        class="btn btn-outline-danger"
        @click="logout"
      >
        Logout
      </button>

    </div>

  </nav>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const logout = () => {
  localStorage.clear();
  router.push("/");
};
</script>