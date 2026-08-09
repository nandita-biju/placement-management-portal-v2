<template>
  <div class="container mt-4">

    <div class="card shadow">

      <div class="card-header">
        <h3>Create Company Profile</h3>
      </div>

      <div class="card-body">

        <form @submit.prevent="createProfile">

          <!-- Company Name -->
          <div class="mb-3">
            <label class="form-label">Company Name</label>

            <input
              v-model="profile.company_name"
              type="text"
              class="form-control"
              placeholder="e.g. Microsoft"
              required
            >
          </div>

          <!-- Industry -->
          <div class="mb-3">
            <label class="form-label">Industry</label>

            <input
              v-model="profile.industry"
              type="text"
              class="form-control"
              placeholder="e.g. Information Technology"
            >
          </div>

          <!-- Location -->
          <div class="mb-3">
            <label class="form-label">Location</label>

            <input
              v-model="profile.location"
              type="text"
              class="form-control"
              placeholder="e.g. Chennai"
            >
          </div>

          <!-- HR Contact -->
          <div class="mb-3">
            <label class="form-label">HR Contact</label>

            <input
              v-model="profile.hr_contact"
              type="text"
              class="form-control"
              placeholder="e.g. John Doe / +91 9876543210"
            >
          </div>

          <!-- Website -->
          <div class="mb-3">
            <label class="form-label">Website</label>

            <input
              v-model="profile.website"
              type="url"
              class="form-control"
              placeholder="https://example.com"
            >
          </div>

          <!-- Buttons -->
          <div class="d-flex gap-2">

            <button
              type="submit"
              class="btn btn-success"
              :disabled="loading"
            >
              {{ loading ? "Creating..." : "Create Profile" }}
            </button>

            <button
              type="button"
              class="btn btn-secondary"
              @click="goBack"
            >
              Cancel
            </button>

          </div>

          <!-- Error -->
          <div
            v-if="errorMessage"
            class="alert alert-danger mt-3"
          >
            {{ errorMessage }}
          </div>

        </form>

      </div>

    </div>

  </div>
</template>


<script setup>

import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../../api/axios";


const router = useRouter();


const profile = ref({

  company_name: "",
  industry: "",
  location: "",
  hr_contact: "",
  website: ""

});


const loading = ref(false);
const errorMessage = ref("");


const createProfile = async () => {

  loading.value = true;
  errorMessage.value = "";

  try {

    await api.post(
      "/company/profile",
      {
        company_name: profile.value.company_name,
        industry: profile.value.industry,
        location: profile.value.location,
        hr_contact: profile.value.hr_contact,
        website: profile.value.website
      }
    );

    alert("Company profile created successfully");

    router.push("/company/dashboard");

  } catch (error) {

    console.error("Create company profile error:", error);

    if (error.response) {

      errorMessage.value =
        error.response.data?.message ||
        "Failed to create company profile.";

    } else {

      errorMessage.value =
        "Unable to connect to the backend.";

    }

  } finally {

    loading.value = false;

  }

};


const goBack = () => {

  router.back();

};

</script>