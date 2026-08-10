<template>
  <div>
    <div class="bg-primary text-white p-5 rounded mb-4">
      <h1>Company Dashboard</h1>

      <p class="mb-0">
        Welcome back, {{ profile.company_name || "Company" }}
      </p>
    </div>

    <!-- Company Details -->
    <div class="card shadow mb-4">
      <div class="card-body">
        <h4 class="mb-3">
          Company Details
        </h4>

        <div class="row">
          <div class="col-md-6 mb-3">
            <strong>Company Name:</strong>

            <p class="mb-0">
              {{ profile.company_name || "Not provided" }}
            </p>
          </div>

          <div class="col-md-6 mb-3">
            <strong>Industry:</strong>

            <p class="mb-0">
              {{ profile.industry || "Not provided" }}
            </p>
          </div>

          <div class="col-md-6 mb-3">
            <strong>Location:</strong>

            <p class="mb-0">
              {{ profile.location || "Not provided" }}
            </p>
          </div>

          <div class="col-md-6 mb-3">
            <strong>HR Contact:</strong>

            <p class="mb-0">
              {{ profile.hr_contact || "Not provided" }}
            </p>
          </div>

          <div class="col-md-6">
            <strong>Website:</strong>

            <p class="mb-0">
              <a
                v-if="profile.website"
                :href="profile.website"
                target="_blank"
                rel="noopener"
              >
                {{ profile.website }}
              </a>

              <span v-else>
                Not provided
              </span>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Actions and Summary -->
    <div class="row g-4 mb-4 align-items-stretch">
      <div class="col-lg-4 col-md-6">
        <div class="card shadow h-100">
          <div class="card-body d-flex flex-column p-4">
            <h3 class="mb-3">
              Create Drive
            </h3>

            <p class="mb-4">
              Create a new placement drive.
            </p>

            <router-link
              to="/company/create-drive"
              class="btn btn-primary mt-auto align-self-start"
            >
              Create
            </router-link>
          </div>
        </div>
      </div>

      <div class="col-lg-4 col-md-6">
        <div class="card shadow h-100">
          <div class="card-body d-flex flex-column p-4">
            <h3 class="mb-3">
              My Drives
            </h3>

            <p class="mb-4">
              {{ drives.length }} placement drive(s) created.
            </p>

            <router-link
              to="/company/drives"
              class="btn btn-success mt-auto align-self-start"
            >
              View Drives
            </router-link>
          </div>
        </div>
      </div>

      <div class="col-lg-4 col-md-6">
        <div class="card shadow h-100">
          <div class="card-body d-flex flex-column p-4">
            <h3 class="mb-3">
              Applicants
            </h3>

            <p class="mb-2">
              {{ totalApplicants }} application(s) received.
            </p>

            <p class="text-muted mb-4">
              Review all applicants or choose a drive below.
            </p>

            <a
              href="#all-applicants"
              class="btn btn-warning mt-auto align-self-start"
            >
              View All Applicants
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Created Drives -->
    <div
      id="placement-drives"
      class="card shadow"
    >
      <div class="card-body">
        <h4 class="mb-3">
          Created Placement Drives
        </h4>

        <div
          v-if="loadingDrives"
          class="text-muted"
        >
          Loading placement drives...
        </div>

        <div
          v-else-if="drives.length === 0"
          class="alert alert-info mb-0"
        >
          No placement drives created yet.
        </div>

        <div
          v-else
          class="table-responsive"
        >
          <table class="table table-bordered table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>Drive Title</th>
                <th>Location</th>
                <th>Applicants</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="drive in drives"
                :key="drive.id"
              >
                <td>
                  {{ drive.title }}
                </td>

                <td>
                  {{ drive.location || "Not specified" }}
                </td>

                <td>
                  <span class="badge bg-success">
                    {{ drive.applicant_count ?? 0 }}
                  </span>
                </td>

                <td>
                  <router-link
                    :to="`/company/applicants/${drive.id ?? drive.job_id}`"
                    class="btn btn-sm btn-warning"
                  >
                    View Applicants
                  </router-link>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- All Applicants -->
    <div
      id="all-applicants"
      class="card shadow mt-4"
    >
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
          <h4 class="mb-0">
            All Applicants
          </h4>

          <div>
            <span class="badge bg-primary me-2">
              Total: {{ allApplicants.length }}
            </span>

            <span class="badge bg-warning text-dark me-2">
              Shortlisted: {{ shortlistedApplicants }}
            </span>

            <span class="badge bg-success">
              Selected: {{ selectedApplicants }}
            </span>
          </div>
        </div>

        <div
          v-if="loadingApplicants"
          class="text-muted"
        >
          Loading applicants...
        </div>

        <div
          v-else-if="allApplicants.length === 0"
          class="alert alert-info mb-0"
        >
          No students have applied to your placement drives yet.
        </div>

        <div
          v-else
          class="table-responsive"
        >
          <table class="table table-bordered table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>Student</th>
                <th>Email</th>
                <th>Applied Drive</th>
                <th>Status</th>
                <th>Applied On</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="application in allApplicants"
                :key="application.application_id || application.id"
              >
                <td>
                  {{
                    application.student_name ||
                    application.name ||
                    "Student"
                  }}
                </td>

                <td>
                  {{
                    application.student_email ||
                    application.email ||
                    "Not provided"
                  }}
                </td>

                <td>
                  {{ application.drive_title }}
                </td>

                <td>
                  <span
                    class="badge"
                    :class="statusClass(application.status)"
                  >
                    {{ application.status || "Applied" }}
                  </span>
                </td>

                <td>
                  {{ formatDate(application.applied_at) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import {
  getCompanyProfile,
  getMyDrives,
  getApplicants
} from "../../services/companyService";

const profile = ref({});
const drives = ref([]);
const allApplicants = ref([]);

const loadingDrives = ref(true);
const loadingApplicants = ref(true);

const totalApplicants = computed(() => {
  return drives.value.reduce((total, drive) => {
    return total + Number(drive.applicant_count ?? 0);
  }, 0);
});

const shortlistedApplicants = computed(() => {
  return allApplicants.value.filter(
    (application) => application.status === "Shortlisted"
  ).length;
});

const selectedApplicants = computed(() => {
  return allApplicants.value.filter(
    (application) => application.status === "Selected"
  ).length;
});

const formatDate = (date) => {
  if (!date) {
    return "Not specified";
  }

  const d = new Date(date);

  return d.toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric"
  });
};

const statusClass = (status) => {
  if (status === "Selected") {
    return "bg-success";
  }

  if (status === "Rejected") {
    return "bg-danger";
  }

  if (status === "Shortlisted") {
    return "bg-warning text-dark";
  }

  return "bg-secondary";
};

onMounted(async () => {
  try {
    profile.value = await getCompanyProfile();

    const response = await getMyDrives();

    drives.value = Array.isArray(response)
      ? response
      : response.jobs || [];

    const applicantResults = await Promise.allSettled(
      drives.value.map(async (drive) => {
        const applicantResponse = await getApplicants(drive.id);

        const applications = Array.isArray(applicantResponse)
          ? applicantResponse
          : applicantResponse.applications || [];

        return applications.map((application) => ({
          ...application,
          drive_title: drive.title
        }));
      })
    );

    allApplicants.value = applicantResults
      .filter((result) => result.status === "fulfilled")
      .flatMap((result) => result.value);
  } catch (err) {
    console.log(err);
  } finally {
    loadingDrives.value = false;
    loadingApplicants.value = false;
  }
});
</script>