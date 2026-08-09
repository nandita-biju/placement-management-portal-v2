<template>
  <div class="container py-4">
    <!-- Loading -->
    <div
      v-if="loading"
      class="text-center py-5"
    >
      <div
        class="spinner-border text-primary"
        role="status"
      >
        <span class="visually-hidden">Loading dashboard...</span>
      </div>

      <p class="text-muted mt-3">
        Loading student dashboard...
      </p>
    </div>

    <div v-else>
      <!-- Welcome -->
      <div class="bg-primary text-white rounded p-4 mb-4">
        <h2 class="mb-2">
          Student Dashboard
        </h2>

        <p class="mb-0">
          Welcome{{ profile?.full_name ? `, ${profile.full_name}` : "" }}
          to the Placement Portal.
        </p>
      </div>

      <!-- First-time Profile Creation -->
      <div
        v-if="!hasProfile"
        class="alert alert-warning d-flex justify-content-between align-items-center flex-wrap gap-3 mb-4"
      >
        <div>
          <strong>Complete your profile to apply for placement drives.</strong>

          <div class="small">
            Add your academic details and upload your latest resume.
          </div>
        </div>

        <router-link
          to="/student/profile/create"
          class="btn btn-primary"
        >
          Create Profile
        </router-link>
      </div>

      <!-- Summary Cards -->
      <div class="row g-4 mb-4">
        <div class="col-lg-4 col-md-6">
          <div class="card shadow-sm h-100">
            <div class="card-body d-flex flex-column p-4">
              <h4 class="mb-3">
                Placement Drives
              </h4>

              <p class="mb-4">
                {{ drives.length }} approved placement drive(s) available.
              </p>

              <router-link
                to="/student/drives"
                class="btn btn-success mt-auto align-self-start"
              >
                Browse Drives
              </router-link>
            </div>
          </div>
        </div>

        <div class="col-lg-4 col-md-6">
          <div class="card shadow-sm h-100">
            <div class="card-body d-flex flex-column p-4">
              <h4 class="mb-3">
                My Applications
              </h4>

              <p class="mb-4">
                {{ applications.length }} application(s) submitted.
              </p>

              <router-link
                to="/student/applications"
                class="btn btn-warning mt-auto align-self-start"
              >
                View Applications
              </router-link>
            </div>
          </div>
        </div>

        <!-- Only visible after profile is created -->
        <div
          v-if="hasProfile"
          class="col-lg-4 col-md-6"
        >
          <div class="card shadow-sm h-100">
            <div class="card-body d-flex flex-column p-4">
              <h4 class="mb-3">
                My Profile
              </h4>

              <p class="mb-4">
                Keep your profile and resume up to date.
              </p>

              <router-link
                to="/student/profile/edit"
                class="btn btn-outline-primary mt-auto align-self-start"
              >
                Edit Profile
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Approved Placement Drives -->
      <div class="card shadow-sm mb-4">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
            <h4 class="mb-0">
              Placement Drives
            </h4>

            <router-link
              to="/student/drives"
              class="btn btn-sm btn-outline-success"
            >
              Browse All Drives
            </router-link>
          </div>

          <div
            v-if="drives.length === 0"
            class="alert alert-info mb-0"
          >
            No placement drives are available at the moment.
          </div>

          <div
            v-else
            class="row g-3"
          >
            <div
              v-for="drive in drives"
              :key="drive.id"
              class="col-lg-6"
            >
              <div class="card border h-100">
                <div class="card-body d-flex flex-column">
                  <h5>
                    {{ drive.title }}
                  </h5>

                  <p class="text-muted mb-2">
                    {{ drive.company_name }}
                  </p>

                  <p class="small mb-3">
                    {{ drive.description || "No description provided." }}
                  </p>

                  <div class="mb-3 small">
                    <div>
                      <strong>Salary:</strong>
                      {{ drive.salary || "Not specified" }}
                    </div>

                    <div>
                      <strong>Deadline:</strong>
                      {{ drive.application_deadline || "No deadline" }}
                    </div>
                  </div>

                  <router-link
                    to="/student/drives"
                    class="btn btn-outline-success mt-auto align-self-start"
                  >
                    View & Apply
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

import {
  getProfile,
  getMyApplications
} from "../../services/studentService";

import { getAllDrives } from "../../services/driveService";

const router = useRouter();

const loading = ref(true);
const hasProfile = ref(false);

const profile = ref(null);
const drives = ref([]);
const applications = ref([]);

const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("role");

  router.push("/");
};

onMounted(async () => {
  try {
    drives.value = await getAllDrives();
  } catch (error) {
    console.log("Unable to load placement drives", error);
  }

  try {
    applications.value = await getMyApplications();
  } catch (error) {
    console.log("Unable to load applications", error);
  }

  try {
    profile.value = await getProfile();
    hasProfile.value = true;
  } catch (error) {
    // A 404 means a newly registered student has not created a profile yet.
    if (error.response?.status === 404) {
      hasProfile.value = false;
    } else {
      console.log("Unable to load student profile", error);
    }
  } finally {
    loading.value = false;
  }
});
</script>