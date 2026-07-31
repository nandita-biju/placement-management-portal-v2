<template>
  <div class="container">

    <div class="card shadow">

      <div class="card-header d-flex justify-content-between align-items-center">

        <h3>Company Profile</h3>

        <router-link
          to="/company/profile/edit"
          class="btn btn-primary"
        >
          Edit Profile
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

        <div class="row">

          <div class="col-md-3">
            <strong>Approval Status</strong>
          </div>

          <div class="col-md-9">

            <span
              class="badge"
              :class="badgeClass"
            >
              {{ profile.approval_status }}
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

onMounted(async () => {

    try{
        profile.value = await getCompanyProfile();
    }

    catch(error){
        console.log(error);
    }

});

const badgeClass = computed(() => {

    if(profile.value.approval_status === "approved")
        return "bg-success";

    if(profile.value.approval_status === "rejected")
        return "bg-danger";

    return "bg-warning text-dark";

});
</script>