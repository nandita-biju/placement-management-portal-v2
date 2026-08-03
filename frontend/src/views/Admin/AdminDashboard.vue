<template>
  <div class="container py-4">

    <h2 class="fw-bold mb-5">
      Dashboard
    </h2>

    <div class="row g-4">

      <!-- Students -->
      <div class="col-md-6 col-lg-3">
        <div class="card dashboard-card border-0 shadow">

          <div class="top-line bg-primary"></div>

          <div class="card-body text-center">

            <h1 class="count text-primary">
              {{ stats.students }}
            </h1>

            <h5 class="fw-semibold">
              Students
            </h5>

          </div>

        </div>
      </div>

      <!-- Companies -->
      <div class="col-md-6 col-lg-3">
        <div class="card dashboard-card border-0 shadow">

          <div class="top-line bg-success"></div>

          <div class="card-body text-center">

            <h1 class="count text-success">
              {{ stats.companies }}
            </h1>

            <h5 class="fw-semibold">
              Companies
            </h5>

          </div>

        </div>
      </div>

      <!-- Drives -->
      <div class="col-md-6 col-lg-3">
        <div class="card dashboard-card border-0 shadow">

          <div class="top-line bg-warning"></div>

          <div class="card-body text-center">

            <h1 class="count text-warning">
              {{ stats.jobs }}
            </h1>

            <h5 class="fw-semibold">
              Placement Drives
            </h5>

          </div>

        </div>
      </div>

      <!-- Applications -->
      <div class="col-md-6 col-lg-3">
        <div class="card dashboard-card border-0 shadow">

          <div class="top-line bg-info"></div>

          <div class="card-body text-center">

            <h1 class="count text-info">
              {{ stats.applications }}
            </h1>

            <h5 class="fw-semibold">
              Applications
            </h5>

          </div>

        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getDashboard } from "../../services/adminService";

const stats = ref({
    students: 0,
    companies: 0,
    jobs: 0,
    applications: 0
});

onMounted(async () => {

    try {

        stats.value = await getDashboard();

    }

    catch (error) {

        console.log(error);

    }

});
</script>

<style scoped>

.dashboard-card{
    border-radius:18px;
    overflow:hidden;
    transition:0.3s;
    background:white;
}

.dashboard-card:hover{
    transform:translateY(-8px);
    box-shadow:0 15px 35px rgba(0,0,0,0.15)!important;
}

.top-line{
    height:8px;
    width:100%;
}

.card-body{
    padding:35px 20px;
}

.count{
    font-size:64px;
    font-weight:700;
    margin-bottom:10px;
}

h5{
    color:#555;
    margin-bottom:0;
}

</style>