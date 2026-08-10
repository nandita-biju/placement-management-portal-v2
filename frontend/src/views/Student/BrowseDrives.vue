<template>
  <div>
    <h2 class="mb-4">
      Explore Placement Drives & Companies
    </h2>

    <!-- Search and Filter -->
    <div class="row g-3 align-items-center mb-4">
      <div class="col-md-7">
        <input
          v-model="search"
          class="form-control"
          placeholder="Search company, job title, or skills..."
        >
      </div>

      <div class="col-md-5">
        <div class="form-check form-switch">
          <input
            id="eligibleOnly"
            v-model="onlyEligible"
            class="form-check-input"
            type="checkbox"
          >

          <label
            class="form-check-label"
            for="eligibleOnly"
          >
            Show only drives I am eligible for
          </label>
        </div>
      </div>
    </div>

    <div class="d-flex justify-content-between align-items-center mb-4">
      <span class="text-muted">
        {{ filteredDrives.length }} drive(s) found
      </span>
    </div>

    <div
      v-if="!studentProfile"
      class="alert alert-warning"
    >
      Complete your student profile to check eligibility and apply for drives.
    </div>

    <!-- No Matching Drives -->
    <div
      v-if="filteredDrives.length === 0"
      class="alert alert-info"
    >
      No placement drives match your search or eligibility filter.
    </div>

    <!-- Drive Cards -->
    <div
      v-for="drive in filteredDrives"
      :key="drive.id"
      class="card shadow mb-4"
    >
      <div class="card-body">
        <h4>
          {{ drive.title }}
        </h4>

        <h6 class="text-muted">
          {{ drive.company_name }}
        </h6>

        <p>
          {{ drive.description }}
        </p>

        <p>
          <strong>Salary:</strong>
          {{ drive.salary || "Not specified" }}
        </p>

        <p>
          <strong>Skills Required:</strong>
          {{ drive.skills_required || "Not specified" }}
        </p>

        <!-- Eligibility Requirements -->
        <div class="row mb-3 p-3 bg-light rounded border">
          <div class="col-md-6 mb-2">
            <strong>Eligible Branch:</strong>

            <span class="ms-1 badge bg-info text-dark">
              {{ drive.eligible_branch || "All Branches" }}
            </span>
          </div>

          <div class="col-md-6 mb-2">
            <strong>Minimum CGPA:</strong>

            <span class="ms-1 badge bg-info text-dark">
              {{
                drive.min_cgpa !== null &&
                drive.min_cgpa !== undefined
                  ? drive.min_cgpa
                  : "None"
              }}
            </span>
          </div>

          <div class="col-md-6 mb-2">
            <strong>Graduation Year:</strong>

            <span class="ms-1 badge bg-info text-dark">
              {{ drive.eligible_graduation_year || "All" }}
            </span>
          </div>

          <div class="col-md-6 mb-2">
            <strong>Application Deadline:</strong>

            <span class="ms-1 badge bg-secondary">
              {{ drive.application_deadline || "No deadline" }}
            </span>
          </div>
        </div>

        <!-- Actions -->
        <div class="d-flex align-items-center flex-wrap gap-2">
          <button
            class="btn"
            :class="
              appliedJobIds.has(drive.id)
                ? 'btn-secondary'
                : getEligibilityStatus(drive).isEligible
                  ? 'btn-success'
                  : 'btn-secondary'
            "
            :disabled="
              appliedJobIds.has(drive.id) ||
              !getEligibilityStatus(drive).isEligible
            "
            @click="apply(drive.id)"
          >
            {{
              appliedJobIds.has(drive.id)
                ? "Applied"
                : getEligibilityStatus(drive).isEligible
                  ? "Apply"
                  : "Not Eligible"
            }}
          </button>

          <span
            v-if="!getEligibilityStatus(drive).isEligible"
            class="text-danger small fw-bold"
          >
            ({{ getEligibilityStatus(drive).reason }})
          </span>

          <button
            class="btn btn-outline-info btn-sm"
            @click="viewCompany(drive.company_id)"
          >
            View Company
          </button>
        </div>
      </div>
    </div>

    <!-- Company Profile Modal -->
    <div
      id="companyModal"
      class="modal fade"
      tabindex="-1"
      aria-labelledby="companyModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5
              id="companyModalLabel"
              class="modal-title"
            >
              Company Profile
            </h5>

            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>

          <div class="modal-body">
            <div
              v-if="companyLoading"
              class="text-center py-4"
            >
              <div
                class="spinner-border"
                role="status"
              >
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>

            <div
              v-else-if="companyError"
              class="alert alert-danger"
            >
              {{ companyError }}
            </div>

            <div v-else-if="selectedCompany">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <strong>Company Name</strong>
                  <p>{{ selectedCompany.company_name }}</p>
                </div>

                <div class="col-md-6 mb-3">
                  <strong>Industry</strong>
                  <p>{{ selectedCompany.industry || "Not specified" }}</p>
                </div>

                <div class="col-md-6 mb-3">
                  <strong>Location</strong>
                  <p>{{ selectedCompany.location || "Not specified" }}</p>
                </div>

                <div class="col-md-6 mb-3">
                  <strong>Website</strong>

                  <p>
                    <a
                      v-if="selectedCompany.website"
                      :href="selectedCompany.website"
                      target="_blank"
                      rel="noopener"
                    >
                      {{ selectedCompany.website }}
                    </a>

                    <span v-else>
                      Not specified
                    </span>
                  </p>
                </div>

                <div class="col-md-6 mb-3">
                  <strong>HR Contact</strong>
                  <p>{{ selectedCompany.hr_contact || "Not specified" }}</p>
                </div>

                <div class="col-md-6 mb-3">
                  <strong>Status</strong>

                  <p>
                    <span class="badge bg-success">
                      {{ selectedCompany.approval_status }}
                    </span>
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import * as bootstrap from "bootstrap";

import {
  getAllDrives,
  applyDrive
} from "../../services/driveService";

import { getMyApplications } from "../../services/studentService";

import { getProfile } from "../../services/studentService";
import { getCompanyById } from "../../services/companyService";

const drives = ref([]);
const studentProfile = ref(null);
const appliedJobIds = ref(new Set());

const search = ref("");
const onlyEligible = ref(false);

const selectedCompany = ref(null);
const companyLoading = ref(false);
const companyError = ref("");

onMounted(async () => {
  try {
    drives.value = await getAllDrives();
  } catch (error) {
    console.error("Failed to fetch drives", error);
  }

  try {
    studentProfile.value = await getProfile();
  } catch (error) {
    console.log("No student profile found yet");
  }

  try {
    const applications = await getMyApplications();
    appliedJobIds.value = new Set(
      applications.map((app) => app.job_id)
    );
  } catch (error) {
    console.log("Could not fetch existing applications");
  }
});

const getEligibilityStatus = (drive) => {
  if (!studentProfile.value) {
    return {
      isEligible: false,
      reason: "Complete your profile first"
    };
  }

  const student = studentProfile.value;

  if (
    drive.eligible_branch &&
    drive.eligible_branch.toLowerCase() !== "all branches" &&
    drive.eligible_branch.toLowerCase() !== "all"
  ) {
    if (
      !student.branch ||
      student.branch.trim().toLowerCase() !==
        drive.eligible_branch.trim().toLowerCase()
    ) {
      return {
        isEligible: false,
        reason: `Required Branch: ${drive.eligible_branch}`
      };
    }
  }

  if (
    drive.min_cgpa !== null &&
    drive.min_cgpa !== undefined
  ) {
    if (
      student.cgpa === null ||
      student.cgpa === undefined ||
      student.cgpa < drive.min_cgpa
    ) {
      return {
        isEligible: false,
        reason: `Min CGPA: ${drive.min_cgpa}`
      };
    }
  }

  if (drive.eligible_graduation_year) {
    if (
      !student.graduation_year ||
      student.graduation_year !== drive.eligible_graduation_year
    ) {
      return {
        isEligible: false,
        reason: `Only for ${drive.eligible_graduation_year} batch`
      };
    }
  }

  if (drive.application_deadline) {
    const today = new Date().toISOString().split("T")[0];

    if (today > drive.application_deadline) {
      return {
        isEligible: false,
        reason: "Deadline passed"
      };
    }
  }

  return {
    isEligible: true,
    reason: ""
  };
};

const filteredDrives = computed(() => {
  const searchText = search.value.trim().toLowerCase();

  return drives.value.filter((drive) => {
    const matchesSearch =
      (drive.title || "")
        .toLowerCase()
        .includes(searchText) ||

      (drive.company_name || "")
        .toLowerCase()
        .includes(searchText) ||

      (drive.skills_required || "")
        .toLowerCase()
        .includes(searchText);

    const isEligible =
      getEligibilityStatus(drive).isEligible;

    return matchesSearch &&
      (!onlyEligible.value || isEligible);
  });
});

const apply = async (jobId) => {
  try {
    const response = await applyDrive(jobId);

    appliedJobIds.value = new Set([
      ...appliedJobIds.value,
      jobId
    ]);

    alert(response.message);
  } catch (error) {
    alert(
      error.response?.data?.message ||
      error.message
    );
  }
};

const viewCompany = async (companyId) => {
  selectedCompany.value = null;
  companyLoading.value = true;
  companyError.value = "";

  const modalElement =
    document.getElementById("companyModal");

  const modal = new bootstrap.Modal(modalElement);

  modal.show();

  try {
    selectedCompany.value =
      await getCompanyById(companyId);
  } catch (error) {
    companyError.value =
      error.response?.data?.message ||
      "Unable to load company profile.";
  } finally {
    companyLoading.value = false;
  }
};
</script>