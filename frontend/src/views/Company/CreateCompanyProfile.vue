<template>
  <div class="container">

    <div class="card shadow">

      <div class="card-header">
        <h3>Create Company Profile</h3>
      </div>

      <div class="card-body">

        <form @submit.prevent="createProfile">

          <div class="mb-3">
            <label class="form-label">Company Name</label>
            <input
              v-model="profile.company_name"
              class="form-control"
              required
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Industry</label>
            <input
              v-model="profile.industry"
              class="form-control"
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Location</label>
            <input
              v-model="profile.location"
              class="form-control"
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Website</label>
            <input
              v-model="profile.website"
              class="form-control"
              placeholder="https://example.com"
            >
          </div>

          <div class="d-flex gap-2">

            <button
              class="btn btn-success"
              type="submit"
            >
              Create Profile
            </button>

            <button
              class="btn btn-secondary"
              type="button"
              @click="goBack"
            >
              Cancel
            </button>

          </div>

        </form>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { createCompanyProfile } from "../../services/companyService";

const router = useRouter();

const profile = ref({
    company_name: "",
    industry: "",
    location: "",
    website: ""
});

const createProfile = async () => {

    try {

        if (
            profile.value.website &&
            !profile.value.website.startsWith("http")
        ) {
            profile.value.website =
                "https://" + profile.value.website;
        }

        await createCompanyProfile(profile.value);

        alert("Company profile created successfully!");

        router.push("/company/profile");

    }

    catch (error) {

        alert(
            error.response?.data?.message || error.message
        );

    }

};

const goBack = () => {

    router.push("/company/profile");

};
</script>