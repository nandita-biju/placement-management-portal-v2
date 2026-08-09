<template>
  <div class="container">

    <div class="card shadow">

      <div class="card-header d-flex justify-content-between align-items-center">

        <h3>Company Profile</h3>

        <router-link
            v-if="profileExists"
            to="/company/profile/edit"
            class="btn btn-primary"
        >
            Edit Profile
        </router-link>

        <router-link
            v-else
            to="/company/profile/create"
            class="btn btn-success"
        >
            Create Profile
        </router-link>

      </div>

      <div class="card-body">

        <div class="row mb-3">

          <div class="col-md-3">
            <strong>Company Name</strong>
          </div>

          <div class="col-md-9">
            {{ profile.company_name }}
          </div>

        </div>

        <div class="row mb-3">

          <div class="col-md-3">
            <strong>Industry</strong>
          </div>

          <div class="col-md-9">
            {{ profile.industry }}
          </div>

        </div>

        <div class="row mb-3">

          <div class="col-md-3">
            <strong>Location</strong>
          </div>

          <div class="col-md-9">
            {{ profile.location }}
          </div>

        </div>

        <div class="row mb-3">

          <div class="col-md-3">
            <strong>HR Contact</strong>
          </div>

          <div class="col-md-9">
            {{ profile.hr_contact }}
          </div>

        </div>

        <div class="row mb-3">

          <div class="col-md-3">
            <strong>Website</strong>
          </div>

          <div class="col-md-9">
            <a
              :href="profile.website"
              target="_blank"
            >
              {{ profile.website }}
            </a>
          </div>

        </div>

        <!-- Approval Status -->
        <div class="row mb-3">

          <div class="col-md-3">
            <strong>Approval Status</strong>
          </div>

          <div class="col-md-9">

            <span
              class="badge"
              :class="approvalBadgeClass"
            >
              {{ profile.approval_status }}
            </span>

          </div>

        </div>


        <!-- Account Status -->
        <div class="row">

          <div class="col-md-3">
            <strong>Account Status</strong>
          </div>

          <div class="col-md-9">

            <span
              class="badge"
              :class="accountStatusBadgeClass"
            >
              {{ accountStatusText }}
            </span>

          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { getCompanyProfile } from "../../services/companyService";

const profile = ref({});
const profileExists = ref(false);

onMounted(async () => {

    try {

        profile.value = await getCompanyProfile();
        profileExists.value = true;

    }

    catch (error) {

        if (error.response?.status === 404) {
            profileExists.value = false;
        }

        else {
            console.log(error);
        }

    }

});

const badgeClass = computed(() => {

    if (profile.value.approval_status === "approved")
        return "bg-success";

    if (profile.value.approval_status === "rejected")
        return "bg-danger";

    return "bg-warning text-dark";

});

const approvalBadgeClass = computed(() => {

  if (profile.value.approval_status === "approved") {
    return "bg-success";
  }

  if (profile.value.approval_status === "rejected") {
    return "bg-danger";
  }

  return "bg-warning text-dark";
});


const accountStatusText = computed(() => {

  if (profile.value.status === "deactivated") {
    return "Deactivated";
  }

  if (profile.value.status === "blacklisted") {
    return "Blacklisted";
  }

  return "Active";
});


const accountStatusBadgeClass = computed(() => {

  if (profile.value.status === "deactivated") {
    return "bg-secondary";
  }

  if (profile.value.status === "blacklisted") {
    return "bg-danger";
  }

  return "bg-success";
});
</script>