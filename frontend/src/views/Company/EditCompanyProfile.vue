<template>
  <div class="container">

    <div class="card shadow">

      <div class="card-header">
        <h3>Edit Company Profile</h3>
      </div>

      <div class="card-body">

        <form @submit.prevent="saveProfile">

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
              placeholder="https://company.com"
            >
          </div>

          <div class="d-flex gap-2">

            <button
              class="btn btn-success"
              type="submit"
            >
              Save Changes
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
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import {
    getCompanyProfile,
    updateCompanyProfile
} from "../../services/companyService";

const router = useRouter();

const profile = ref({});

onMounted(async () => {

    try {

        profile.value = await getCompanyProfile();

    }

    catch (error) {

        console.log(error);

    }

});

const saveProfile = async () => {

    try {

        // Automatically add https:// if missing
        if (
            profile.value.website &&
            !profile.value.website.startsWith("http")
        ) {
            profile.value.website =
                "https://" + profile.value.website;
        }

        await updateCompanyProfile(profile.value);

        alert("Company profile updated successfully!");

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