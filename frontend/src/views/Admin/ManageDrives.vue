<template>
  <div class="container">

    <h2 class="mb-4">
      Placement Drives
    </h2>

    <div
      v-if="drives.length === 0"
      class="alert alert-info"
    >
      No drives found.
    </div>

    <table
      v-else
      class="table table-bordered table-hover align-middle"
    >

      <thead class="table-dark">

        <tr>
          <th>Company</th>
          <th>Job Title</th>
          <th>Salary</th>
          <th>Skills Required</th>
          <th>Status</th>
          <th width="220">
            Actions
          </th>
        </tr>

      </thead>

      <tbody>

        <tr
          v-for="drive in drives"
          :key="drive.id"
        >

          <td>{{ drive.company_name }}</td>

          <td>{{ drive.title }}</td>

          <td>{{ drive.salary }}</td>

          <td>{{ drive.skills_required }}</td>

          <td>

            <span
              class="badge"
              :class="statusBadge(drive.status)"
            >
              {{ drive.status }}
            </span>

          </td>

          <td>

            <!-- Pending -->
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

            <!-- Approved -->
            <template v-else-if="drive.status === 'approved'">

              <button
                class="btn btn-danger btn-sm"
                @click="reject(drive.id)"
              >
                Reject
              </button>

            </template>

            <!-- Rejected -->
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
</template>

<script setup>
import { ref, onMounted } from "vue";

import {
    getDrives,
    approveDrive,
    rejectDrive
} from "../../services/adminService";

const drives = ref([]);

const loadDrives = async () => {

    try {

        drives.value = await getDrives();

    }

    catch (error) {

        console.log(error);

    }

};

onMounted(loadDrives);

const approve = async (id) => {

    await approveDrive(id);

    loadDrives();

};

const reject = async (id) => {

    await rejectDrive(id);

    loadDrives();

};

const statusBadge = (status) => {

    if (status === "approved")
        return "bg-success";

    if (status === "rejected")
        return "bg-danger";

    return "bg-warning text-dark";

};
</script>