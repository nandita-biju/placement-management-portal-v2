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
        <span class="visually-hidden">
          Loading dashboard...
        </span>
      </div>

      <p class="text-muted mt-3">
        Loading dashboard...
      </p>
    </div>

    <div v-else>
      <!-- Header -->
      <div class="dashboard-header mb-4">
        <div>
          <h2 class="fw-bold mb-2">
            Admin Dashboard
          </h2>

          <p class="mb-0">
            Manage students, companies, placement drives, and applications.
          </p>
        </div>

        <router-link
          to="/admin/reports"
          class="btn btn-light"
        >
          Reports & Statistics
        </router-link>
      </div>

      <!-- Statistics -->
      <div class="row g-4 mb-4">
        <div class="col-md-6 col-lg-3">
          <router-link
            to="/admin/students"
            class="text-decoration-none"
          >
            <div class="card dashboard-card border-0 shadow h-100">
              <div class="top-line bg-primary"></div>

              <div class="card-body text-center">
                <h1 class="count text-primary">
                  {{ stats.students }}
                </h1>

                <h5 class="fw-semibold text-dark">
                  Students
                </h5>

                <p class="text-muted small mb-0">
                  Manage student accounts
                </p>
              </div>
            </div>
          </router-link>
        </div>

        <div class="col-md-6 col-lg-3">
          <router-link
            to="/admin/companies"
            class="text-decoration-none"
          >
            <div class="card dashboard-card border-0 shadow h-100">
              <div class="top-line bg-success"></div>

              <div class="card-body text-center">
                <h1 class="count text-success">
                  {{ stats.companies }}
                </h1>

                <h5 class="fw-semibold text-dark">
                  Companies
                </h5>

                <p class="text-muted small mb-0">
                  Approve and manage companies
                </p>
              </div>
            </div>
          </router-link>
        </div>

        <div class="col-md-6 col-lg-3">
          <router-link
            to="/admin/drives"
            class="text-decoration-none"
          >
            <div class="card dashboard-card border-0 shadow h-100">
              <div class="top-line bg-warning"></div>

              <div class="card-body text-center">
                <h1 class="count text-warning">
                  {{ stats.jobs }}
                </h1>

                <h5 class="fw-semibold text-dark">
                  Placement Drives
                </h5>

                <p class="text-muted small mb-0">
                  Review and approve drives
                </p>
              </div>
            </div>
          </router-link>
        </div>

        <div class="col-md-6 col-lg-3">
          <router-link
            to="/admin/applications"
            class="text-decoration-none"
          >
            <div class="card dashboard-card border-0 shadow h-100">
              <div class="top-line bg-info"></div>

              <div class="card-body text-center">
                <h1 class="count text-info">
                  {{ stats.applications }}
                </h1>

                <h5 class="fw-semibold text-dark">
                  Applications
                </h5>

                <p class="text-muted small mb-0">
                  View placement activity
                </p>
              </div>
            </div>
          </router-link>
        </div>
      </div>

      <!-- Administration Tools -->
      <div class="card shadow-sm border-0">
        <div class="card-body p-4">
          <h4 class="mb-3">
            Administration Tools
          </h4>

          <div class="d-flex flex-wrap gap-2">
            <router-link
              to="/admin/companies"
              class="btn btn-outline-success"
            >
              Manage Companies
            </router-link>

            <router-link
              to="/admin/students"
              class="btn btn-outline-primary"
            >
              Manage Students
            </router-link>

            <router-link
              to="/admin/drives"
              class="btn btn-outline-warning"
            >
              Manage Drives
            </router-link>

            <router-link
              to="/admin/applications"
              class="btn btn-outline-info"
            >
              View Applications
            </router-link>

            <router-link
              to="/admin/reports"
              class="btn btn-outline-secondary"
            >
              Reports
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getDashboard } from "../../services/adminService";

const loading = ref(true);

const stats = ref({
  students: 0,
  companies: 0,
  jobs: 0,
  applications: 0
});

onMounted(async () => {
  try {
    stats.value = await getDashboard();
  } catch (error) {
    console.log(error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.dashboard-header {
  background: linear-gradient(135deg, #0d6efd, #084298);
  border-radius: 18px;
  color: white;
  padding: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.dashboard-card {
  border-radius: 18px;
  overflow: hidden;
  background: white;
  transition: 0.25s ease;
  cursor: pointer;
}

.dashboard-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15) !important;
}

.top-line {
  height: 8px;
  width: 100%;
}

.card-body {
  padding: 30px 20px;
}

.count {
  font-size: 54px;
  font-weight: 700;
  margin-bottom: 10px;
}

@media (max-width: 576px) {
  .dashboard-header {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>