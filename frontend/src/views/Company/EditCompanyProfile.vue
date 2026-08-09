<template>
  <div class="card shadow">

    <div class="card-header">
      <h3>Edit Company Profile</h3>
    </div>

    <div class="card-body">

      <form @submit.prevent="saveProfile">

        <!-- Company Name -->
        <div class="mb-3">
          <label class="form-label">
            Company Name
          </label>

          <input
            v-model="profile.company_name"
            type="text"
            class="form-control"
            required
          >
        </div>


        <!-- Industry -->
        <div class="mb-3">
          <label class="form-label">
            Industry
          </label>

          <input
            v-model="profile.industry"
            type="text"
            class="form-control"
          >
        </div>


        <!-- Location -->
        <div class="mb-3">
          <label class="form-label">
            Location
          </label>

          <input
            v-model="profile.location"
            type="text"
            class="form-control"
          >
        </div>


        <!-- HR Contact -->
        <div class="mb-3">
          <label class="form-label">
            HR Contact
          </label>

          <input
            v-model="profile.hr_contact"
            type="text"
            class="form-control"
            placeholder="Enter HR contact"
          >
        </div>


        <!-- Website -->
        <div class="mb-3">
          <label class="form-label">
            Website
          </label>

          <input
            v-model="profile.website"
            type="url"
            class="form-control"
            placeholder="https://company.com"
          >
        </div>


        <!-- Buttons -->
        <div class="d-flex gap-2">

          <button
            type="submit"
            class="btn btn-success"
          >
            Save Changes
          </button>

          <button
            type="button"
            class="btn btn-secondary"
            @click="goBack"
          >
            Cancel
          </button>

        </div>

      </form>

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