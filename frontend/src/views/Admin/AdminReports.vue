<template>
  <div class="container">

    <h2 class="mb-4">
      Reports & Statistics
    </h2>

    <!-- Loading -->
    <div
      v-if="loading"
      class="text-center py-5"
    >
      <div
        class="spinner-border"
        role="status"
      >
        <span class="visually-hidden">
          Loading...
        </span>
      </div>
    </div>


    <!-- Error -->
    <div
      v-else-if="error"
      class="alert alert-danger"
    >
      {{ error }}
    </div>


    <!-- Reports -->
    <div v-else>

      <!-- ========================= -->
      <!-- OVERVIEW CARDS -->
      <!-- ========================= -->

      <h4 class="mb-3">
        Overview
      </h4>

      <div class="row g-3 mb-5">

        <!-- Students -->
        <div class="col-md-4">

          <div class="card shadow-sm h-100">

            <div class="card-body">

              <h6 class="text-muted">
                Total Students
              </h6>

              <h2>
                {{ reports.students.total }}
              </h2>

            </div>

          </div>

        </div>


        <!-- Companies -->
        <div class="col-md-4">

          <div class="card shadow-sm h-100">

            <div class="card-body">

              <h6 class="text-muted">
                Total Companies
              </h6>

              <h2>
                {{ reports.companies.total }}
              </h2>

            </div>

          </div>

        </div>


        <!-- Drives -->
        <div class="col-md-4">

          <div class="card shadow-sm h-100">

            <div class="card-body">

              <h6 class="text-muted">
                Total Placement Drives
              </h6>

              <h2>
                {{ reports.drives.total }}
              </h2>

            </div>

          </div>

        </div>


        <!-- Applications -->
        <div class="col-md-4">

          <div class="card shadow-sm h-100">

            <div class="card-body">

              <h6 class="text-muted">
                Total Applications
              </h6>

              <h2>
                {{ reports.applications.total }}
              </h2>

            </div>

          </div>

        </div>


        <!-- Selected -->
        <div class="col-md-4">

          <div class="card shadow-sm h-100">

            <div class="card-body">

              <h6 class="text-muted">
                Students Selected
              </h6>

              <h2>
                {{ reports.applications.selected }}
              </h2>

            </div>

          </div>

        </div>


        <!-- Placement Rate -->
        <div class="col-md-4">

          <div class="card shadow-sm h-100">

            <div class="card-body">

              <h6 class="text-muted">
                Placement Rate
              </h6>

              <h2>
                {{ reports.placement_rate }}%
              </h2>

            </div>

          </div>

        </div>

      </div>


      <!-- ========================= -->
      <!-- STUDENT STATISTICS -->
      <!-- ========================= -->

      <h4 class="mb-3">
        Student Statistics
      </h4>

      <div class="card shadow-sm mb-5">

        <div class="card-body">

          <div class="row text-center">

            <div class="col-md-4">

              <h5>
                {{ reports.students.active }}
              </h5>

              <span class="badge bg-success">
                Active
              </span>

            </div>


            <div class="col-md-4">

              <h5>
                {{ reports.students.blacklisted }}
              </h5>

              <span class="badge bg-dark">
                Blacklisted
              </span>

            </div>


            <div class="col-md-4">

              <h5>
                {{ reports.students.deactivated }}
              </h5>

              <span class="badge bg-secondary">
                Deactivated
              </span>

            </div>

          </div>

        </div>

      </div>


      <!-- ========================= -->
      <!-- COMPANY STATISTICS -->
      <!-- ========================= -->

      <h4 class="mb-3">
        Company Statistics
      </h4>

      <div class="card shadow-sm mb-5">

        <div class="card-body">

          <div class="row text-center">

            <div class="col-md-4 mb-3">

              <h5>
                {{ reports.companies.active }}
              </h5>

              <span class="badge bg-success">
                Active
              </span>

            </div>


            <div class="col-md-4 mb-3">

              <h5>
                {{ reports.companies.blacklisted }}
              </h5>

              <span class="badge bg-dark">
                Blacklisted
              </span>

            </div>


            <div class="col-md-4 mb-3">

              <h5>
                {{ reports.companies.deactivated }}
              </h5>

              <span class="badge bg-secondary">
                Deactivated
              </span>

            </div>


            <div class="col-md-4">

              <h5>
                {{ reports.companies.pending }}
              </h5>

              <span class="badge bg-warning text-dark">
                Pending
              </span>

            </div>


            <div class="col-md-4">

              <h5>
                {{ reports.companies.approved }}
              </h5>

              <span class="badge bg-success">
                Approved
              </span>

            </div>


            <div class="col-md-4">

              <h5>
                {{ reports.companies.rejected }}
              </h5>

              <span class="badge bg-danger">
                Rejected
              </span>

            </div>

          </div>

        </div>

      </div>


      <!-- ========================= -->
      <!-- APPLICATION STATISTICS -->
      <!-- ========================= -->

      <h4 class="mb-3">
        Application Statistics
      </h4>

      <div class="card shadow-sm mb-5">

        <div class="card-body">

          <div class="row text-center">

            <div class="col-md-3">

              <h5>
                {{ reports.applications.applied }}
              </h5>

              <span class="badge bg-warning text-dark">
                Applied
              </span>

            </div>


            <div class="col-md-3">

              <h5>
                {{ reports.applications.shortlisted }}
              </h5>

              <span class="badge bg-primary">
                Shortlisted
              </span>

            </div>


            <div class="col-md-3">

              <h5>
                {{ reports.applications.selected }}
              </h5>

              <span class="badge bg-success">
                Selected
              </span>

            </div>


            <div class="col-md-3">

              <h5>
                {{ reports.applications.rejected }}
              </h5>

              <span class="badge bg-danger">
                Rejected
              </span>

            </div>

          </div>

        </div>

      </div>


      <!-- ========================= -->
      <!-- DRIVE STATISTICS -->
      <!-- ========================= -->

      <h4 class="mb-3">
        Placement Drive Statistics
      </h4>

      <div
        v-if="reports.drive_statistics.length === 0"
        class="alert alert-info"
      >
        No placement drives found.
      </div>


      <div
        v-else
        class="table-responsive"
      >

        <table
          class="table table-bordered table-hover align-middle"
        >

          <thead class="table-dark">

            <tr>

              <th>Drive</th>

              <th>Company</th>

              <th>Applicants</th>

              <th>Shortlisted</th>

              <th>Selected</th>

              <th>Rejected</th>

            </tr>

          </thead>


          <tbody>

            <tr
              v-for="drive in reports.drive_statistics"
              :key="drive.drive_id"
            >

              <td>
                {{ drive.title }}
              </td>

              <td>
                {{ drive.company_name }}
              </td>

              <td>
                {{ drive.applicants }}
              </td>

              <td>
                {{ drive.shortlisted }}
              </td>

              <td>

                <span class="badge bg-success">
                  {{ drive.selected }}
                </span>

              </td>

              <td>

                <span class="badge bg-danger">
                  {{ drive.rejected }}
                </span>

              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

  </div>
</template>


<script setup>

import { ref, onMounted } from "vue";

import {
  getReports
} from "../../services/adminService";


const loading = ref(true);

const error = ref("");

const reports = ref({

  students: {

    total: 0,

    active: 0,

    blacklisted: 0,

    deactivated: 0

  },

  companies: {

    total: 0,

    active: 0,

    blacklisted: 0,

    deactivated: 0,

    pending: 0,

    approved: 0,

    rejected: 0

  },

  drives: {

    total: 0

  },

  applications: {

    total: 0,

    applied: 0,

    shortlisted: 0,

    selected: 0,

    rejected: 0

  },

  placement_rate: 0,

  drive_statistics: []

});


const loadReports = async () => {

  try {

    loading.value = true;

    error.value = "";

    reports.value = await getReports();

  }

  catch (err) {

    console.log(err);

    error.value =
      err.response?.data?.message ||
      "Unable to load reports.";

  }

  finally {

    loading.value = false;

  }

};


onMounted(() => {

  loadReports();

});

</script>