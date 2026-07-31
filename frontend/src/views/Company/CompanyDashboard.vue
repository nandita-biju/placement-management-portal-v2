<template>
  <div>

    <div class="bg-primary text-white p-5 rounded mb-4">

      <h1>Company Dashboard</h1>

      <p class="mb-0">
        Welcome back, {{ profile.company_name || "Company" }}
      </p>

    </div>

    <div class="row">

      <div class="col-md-4 mb-3">

        <div class="card shadow h-100">

          <div class="card-body">

            <h3>Create Drive</h3>

            <p>Create a new placement drive.</p>

            <router-link
              to="/company/create-drive"
              class="btn btn-primary"
            >
              Create
            </router-link>

          </div>

        </div>

      </div>

      <div class="col-md-4 mb-3">

        <div class="card shadow h-100">

          <div class="card-body">

            <h3>My Drives</h3>

            <p>Manage all posted drives.</p>

            <router-link
              to="/company/drives"
              class="btn btn-success"
            >
              View
            </router-link>

          </div>

        </div>

      </div>

      <div class="col-md-4 mb-3">

        <div class="card shadow h-100">

          <div class="card-body">

            <h3>Applicants</h3>

            <p>Review student applications.</p>

            <router-link
              to="/company/applicants"
              class="btn btn-warning"
            >
              View
            </router-link>

          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getCompanyProfile } from "../../services/companyService";

const profile = ref({});

onMounted(async () => {
  try {
    profile.value = await getCompanyProfile();
  } catch (err) {
    console.log(err);
  }
});
</script>