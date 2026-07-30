<template>
  <div class="container py-4">

    <!-- Welcome -->
    <div class="bg-primary text-white rounded p-4 mb-4">
      <h2>Student Dashboard</h2>
      <p class="mb-0">
        Welcome to the Placement Portal.
      </p>
    </div>

    <!-- Quick Stats -->
    <div class="row mb-4">

      <div class="col-md-4 mb-3">
        <div class="card shadow-sm text-center p-3">
          <h5>Profile</h5>
          <p>Complete your profile.</p>
          <router-link
              to="/student/profile/create"
              class="btn btn-primary"
          >
              Complete Profile
          </router-link>
        </div>
      </div>

      <div class="col-md-4 mb-3">
        <div class="card shadow-sm text-center p-3">
          <h5>Placement Drives</h5>
          <p>Browse all approved drives.</p>
          <router-link
            to="/student/drives"
            class="btn btn-success"
          >
            Browse Drives
          </router-link>
        </div>
      </div>

      <div class="col-md-4 mb-3">
        <div class="card shadow-sm text-center p-3">
          <h5>Applications</h5>
          <p>Track your applications.</p>
          <router-link
            to="/student/applications"
            class="btn btn-warning"
          >
            My Applications
          </router-link>
        </div>
      </div>

    </div>

    <!-- Notifications -->
    <div class="card shadow-sm mb-4">
      <div class="card-header">
        <h5 class="mb-0">Notifications</h5>
      </div>

      <div class="card-body">

        <ul class="list-group">

          <li class="list-group-item">
            📢 Welcome to the Placement Portal.
          </li>

          <li class="list-group-item">
            📌 Complete your student profile before applying.
          </li>

          <li class="list-group-item">
            📄 Upload your latest resume.
          </li>

          <li class="list-group-item">
            🔔 Check your application status regularly.
          </li>

        </ul>

      </div>
    </div>

    <!-- Shortcuts -->
    <div class="card shadow-sm">
      <div class="card-header">
        <h5 class="mb-0">Quick Actions</h5>
      </div>

      <div class="card-body d-flex flex-wrap gap-2">

        <router-link
          to="/student/edit-profile"
          class="btn btn-outline-primary"
        >
          Edit Profile
        </router-link>

        <router-link
          to="/student/drives"
          class="btn btn-outline-success"
        >
          Browse Drives
        </router-link>

        <router-link
          to="/student/applications"
          class="btn btn-outline-warning"
        >
          My Applications
        </router-link>

        <button
          class="btn btn-outline-danger"
          @click="logout"
        >
          Logout
        </button>

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