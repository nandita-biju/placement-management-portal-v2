<template>
  <div class="container">
    <h2 class="mb-4">
      Companies
    </h2>

    <!-- Search -->
    <div class="row mb-4">
      <div class="col-md-4">
        <input
          v-model="query"
          @input="search"
          class="form-control"
          placeholder="Search Companies..."
        >
      </div>

      <div class="col-auto">
        <button
          class="btn btn-primary"
          @click="search"
        >
          Search
        </button>
      </div>

      <div class="col-auto">
        <button
          class="btn btn-secondary"
          @click="loadCompanies"
        >
          Reset
        </button>
      </div>
    </div>

    <div
      v-if="companies.length === 0"
      class="alert alert-info"
    >
      No companies found.
    </div>

    <!-- Companies Table -->
    <div
      v-else
      class="table-responsive"
    >
      <table class="table table-bordered table-hover align-middle">
        <thead class="table-dark">
          <tr>
            <th>Company</th>
            <th>Industry</th>
            <th>Location</th>
            <th>Approval</th>
            <th>Status</th>
            <th style="min-width: 470px;">
              Actions
            </th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="company in companies"
            :key="company.id"
          >
            <td>{{ company.company_name }}</td>

            <td>{{ company.industry || "Not provided" }}</td>

            <td>{{ company.location || "Not provided" }}</td>

            <td>
              <span
                class="badge"
                :class="approvalBadge(company.approval_status)"
              >
                {{ company.approval_status }}
              </span>
            </td>

            <td>
              <span
                class="badge"
                :class="statusBadge(company.status)"
              >
                {{ company.status }}
              </span>
            </td>

            <td>
              <button
                type="button"
                class="btn btn-info btn-sm me-2"
                @click="viewProfile(company.id)"
              >
                View Profile
              </button>

              <button
                type="button"
                class="btn btn-primary btn-sm me-2"
                @click="viewDriveHistory(company.id)"
              >
                Drive History
              </button>

              <!-- Pending -->
              <template v-if="company.approval_status === 'pending'">
                <button
                  class="btn btn-success btn-sm me-2"
                  @click="approve(company.id)"
                >
                  Approve
                </button>

                <button
                  class="btn btn-danger btn-sm"
                  @click="reject(company.id)"
                >
                  Reject
                </button>
              </template>

              <!-- Approved -->
              <template v-else-if="company.approval_status === 'approved'">
                <template v-if="company.status === 'active'">
                  <button
                    class="btn btn-warning btn-sm me-2"
                    @click="blacklist(company.id)"
                  >
                    Blacklist
                  </button>

                  <button
                    class="btn btn-secondary btn-sm"
                    @click="deactivate(company.id)"
                  >
                    Deactivate
                  </button>
                </template>

                <template v-else-if="company.status === 'deactivated'">
                  <button
                    class="btn btn-primary btn-sm"
                    @click="activate(company.id)"
                  >
                    Activate
                  </button>
                </template>

                <template v-else-if="company.status === 'blacklisted'">
                  <button
                    class="btn btn-success btn-sm"
                    @click="unblacklist(company.id)"
                  >
                    Unblacklist
                  </button>
                </template>
              </template>

              <!-- Rejected -->
              <template v-else>
                <button
                  class="btn btn-success btn-sm"
                  @click="approve(company.id)"
                >
                  Approve
                </button>
              </template>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Company Profile Modal -->
    <div
      id="companyProfileModal"
      class="modal fade"
      tabindex="-1"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              Company Profile
            </h5>

            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
            ></button>
          </div>

          <div class="modal-body">
            <div
              v-if="profileLoading"
              class="text-center py-4"
            >
              <div class="spinner-border"></div>
            </div>

            <div
              v-else-if="profileError"
              class="alert alert-danger"
            >
              {{ profileError }}
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
                  <strong>Approval Status</strong>

                  <p>
                    <span
                      class="badge"
                      :class="approvalBadge(selectedCompany.approval_status)"
                    >
                      {{ selectedCompany.approval_status }}
                    </span>
                  </p>
                </div>

                <div class="col-md-6 mb-3">
                  <strong>Account Status</strong>

                  <p>
                    <span
                      class="badge"
                      :class="statusBadge(selectedCompany.status)"
                    >
                      {{ selectedCompany.status }}
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

    <!-- Company Drive History Modal -->
    <div
      id="companyDriveHistoryModal"
      class="modal fade"
      tabindex="-1"
    >
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              Drive History
              <span v-if="historyCompanyName">
                — {{ historyCompanyName }}
              </span>
            </h5>

            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
            ></button>
          </div>

          <div class="modal-body">
            <div
              v-if="historyLoading"
              class="text-center py-4"
            >
              <div class="spinner-border"></div>
            </div>

            <div
              v-else-if="historyError"
              class="alert alert-danger"
            >
              {{ historyError }}
            </div>

            <div
              v-else-if="companyDrives.length === 0"
              class="alert alert-info mb-0"
            >
              This company has not created any placement drives yet.
            </div>

            <div
              v-else
              class="table-responsive"
            >
              <table class="table table-bordered table-hover align-middle">
                <thead class="table-dark">
                  <tr>
                    <th>Drive Title</th>
                    <th>Salary</th>
                    <th>Eligible Branch</th>
                    <th>Deadline</th>
                    <th>Applicants</th>
                    <th>Status</th>
                  </tr>
                </thead>

                <tbody>
                  <tr
                    v-for="drive in companyDrives"
                    :key="drive.drive_id"
                  >
                    <td>{{ drive.title }}</td>

                    <td>{{ drive.salary || "Not specified" }}</td>

                    <td>{{ drive.eligible_branch || "All" }}</td>

                    <td>
                      {{ drive.application_deadline || "N/A" }}
                    </td>

                    <td>
                      <span class="badge bg-primary">
                        {{ drive.applicant_count }}
                      </span>
                    </td>

                    <td>
                      <span
                        class="badge"
                        :class="driveStatusBadge(drive.status)"
                      >
                        {{ drive.status }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
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
import { ref, onMounted } from "vue";
import * as bootstrap from "bootstrap";

import {
  getCompanies,
  approveCompany,
  rejectCompany,
  activateCompany,
  deactivateCompany,
  blacklistCompany,
  unblacklistCompany,
  searchCompanies,
  getCompanyDriveHistory
} from "../../services/adminService";

import { getCompanyById } from "../../services/companyService";

const companies = ref([]);
const query = ref("");

const selectedCompany = ref(null);
const profileLoading = ref(false);
const profileError = ref("");

const companyDrives = ref([]);
const historyCompanyName = ref("");
const historyLoading = ref(false);
const historyError = ref("");

const loadCompanies = async () => {
  try {
    companies.value = await getCompanies();
  } catch (error) {
    console.log(error);
  }
};

const viewProfile = async (companyId) => {
  selectedCompany.value = null;
  profileLoading.value = true;
  profileError.value = "";

  const modalElement =
    document.getElementById("companyProfileModal");

  const modal = new bootstrap.Modal(modalElement);

  modal.show();

  try {
    selectedCompany.value = await getCompanyById(companyId);
  } catch (error) {
    profileError.value =
      error.response?.data?.message ||
      "Unable to load profile.";
  } finally {
    profileLoading.value = false;
  }
};

const viewDriveHistory = async (companyId) => {
  companyDrives.value = [];
  historyCompanyName.value = "";
  historyLoading.value = true;
  historyError.value = "";

  const modalElement = document.getElementById(
    "companyDriveHistoryModal"
  );

  const modal = new bootstrap.Modal(modalElement);

  modal.show();

  try {
    const response =
      await getCompanyDriveHistory(companyId);

    historyCompanyName.value = response.company_name;
    companyDrives.value = response.drives || [];
  } catch (error) {
    historyError.value =
      error.response?.data?.message ||
      "Unable to load company drive history.";
  } finally {
    historyLoading.value = false;
  }
};

const approve = async (id) => {
  await approveCompany(id);
  await loadCompanies();
};

const reject = async (id) => {
  await rejectCompany(id);
  await loadCompanies();
};

const activate = async (id) => {
  await activateCompany(id);
  await loadCompanies();
};

const deactivate = async (id) => {
  await deactivateCompany(id);
  await loadCompanies();
};

const blacklist = async (id) => {
  await blacklistCompany(id);
  await loadCompanies();
};

const unblacklist = async (id) => {
  await unblacklistCompany(id);
  await loadCompanies();
};

const approvalBadge = (status) => {
  if (status === "approved") {
    return "bg-success";
  }

  if (status === "rejected") {
    return "bg-danger";
  }

  return "bg-warning text-dark";
};

const statusBadge = (status) => {
  if (status === "active") {
    return "bg-success";
  }

  if (status === "blacklisted") {
    return "bg-dark";
  }

  if (status === "deactivated") {
    return "bg-secondary";
  }

  return "bg-warning text-dark";
};

const driveStatusBadge = (status) => {
  if (status === "approved") {
    return "bg-success";
  }

  if (status === "rejected") {
    return "bg-danger";
  }

  return "bg-warning text-dark";
};

const search = async () => {
  if (!query.value.trim()) {
    await loadCompanies();
    return;
  }

  try {
    companies.value = await searchCompanies(query.value);
  } catch (error) {
    console.log(error);
  }
};

onMounted(loadCompanies);
</script>