<template>
  <div class="container">
    <h2 class="mb-4">
      Placement Drives
    </h2>

    <!-- Search -->
    <div class="row mb-4">
      <div class="col-md-5">
        <input
          v-model="query"
          class="form-control"
          placeholder="Search company, job title, or skills..."
        >
      </div>

      <div class="col-auto">
        <button
          class="btn btn-secondary"
          @click="query = ''"
        >
          Reset
        </button>
      </div>
    </div>

    <p class="text-muted">
      {{ filteredDrives.length }}
      {{ filteredDrives.length === 1 ? "drive" : "drives" }}
      found.
    </p>

    <!-- No Drives -->
    <div
      v-if="filteredDrives.length === 0"
      class="alert alert-info"
    >
      No drives found.
    </div>

    <!-- Drives Table -->
    <div
      v-else
      class="table-responsive"
    >
      <table class="table table-bordered table-hover align-middle">
        <thead class="table-dark">
          <tr>
            <th>Company</th>
            <th>Job Title</th>
            <th>Salary</th>
            <th>Eligible Branch</th>
            <th>Min CGPA</th>
            <th>Batch</th>
            <th>Deadline</th>
            <th>Status</th>
            <th width="180">
              Actions
            </th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="drive in filteredDrives"
            :key="drive.id"
          >
            <td>{{ drive.company_name }}</td>

            <td>{{ drive.title }}</td>

            <td>{{ drive.salary || "Not specified" }}</td>

            <td>{{ drive.eligible_branch || "All" }}</td>

            <td>
              {{
                drive.min_cgpa !== null &&
                drive.min_cgpa !== undefined
                  ? drive.min_cgpa
                  : "None"
              }}
            </td>

            <td>
              {{ drive.eligible_graduation_year || "All" }}
            </td>

            <td>
              {{ drive.application_deadline || "N/A" }}
            </td>

            <td>
              <span
                class="badge"
                :class="statusBadge(drive.status)"
              >
                {{ drive.status }}
              </span>
            </td>

            <td>
              <template v-if="drive.status === 'pending'">
                <button
                  class="btn btn-success btn-sm me-2"
                  @click="approve(drive.id)"
                >
                  Approve
                </button>

                <button
                  class="btn btn-danger btn-sm"
                  @click="reject(drive.id)"
                >
                  Reject
                </button>
              </template>

              <template v-else-if="drive.status === 'approved'">
                <button
                  class="btn btn-danger btn-sm"
                  @click="reject(drive.id)"
                >
                  Reject
                </button>
              </template>

              <template v-else>
                <button
                  class="btn btn-success btn-sm"
                  @click="approve(drive.id)"
                >
                  Approve
                </button>
              </template>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

import {
  getDrives,
  approveDrive,
  rejectDrive
} from "../../services/adminService";

const drives = ref([]);
const query = ref("");

const loadDrives = async () => {
  try {
    drives.value = await getDrives();
  } catch (error) {
    console.log(error);
  }
};

const filteredDrives = computed(() => {
  const searchText = query.value.trim().toLowerCase();

  return drives.value.filter((drive) => {
    return (
      (drive.company_name || "")
        .toLowerCase()
        .includes(searchText) ||

      (drive.title || "")
        .toLowerCase()
        .includes(searchText) ||

      (drive.skills_required || "")
        .toLowerCase()
        .includes(searchText)
    );
  });
});

const approve = async (id) => {
  await approveDrive(id);
  await loadDrives();
};

const reject = async (id) => {
  await rejectDrive(id);
  await loadDrives();
};

const statusBadge = (status) => {
  if (status === "approved") {
    return "bg-success";
  }

  if (status === "rejected") {
    return "bg-danger";
  }

  return "bg-warning text-dark";
};

onMounted(loadDrives);
</script>