<template>
  <div class="container">

    <h2 class="mb-4">
      Students
    </h2>

    <!-- Search Bar -->
    <div class="row mb-4">

      <div class="col-md-4">

        <input
          v-model="query"
          @input="search"
          class="form-control"
          placeholder="Search Students..."
        />

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
          @click="loadStudents"
        >
          Reset
        </button>

      </div>

    </div>


    <!-- No Students -->
    <div
      v-if="students.length === 0"
      class="alert alert-info"
    >
      No students found.
    </div>


    <!-- Students Table -->
    <table
      v-else
      class="table table-bordered table-hover align-middle"
    >

      <thead class="table-dark">

        <tr>

          <th>Student Name</th>

          <th>Education</th>

          <th>Skills</th>

          <th>Status</th>

          <th>Resume</th>

          <th style="min-width: 300px;">
            Actions
          </th>

        </tr>

      </thead>


      <tbody>

        <tr
          v-for="student in students"
          :key="student.id"
        >

          <!-- Name -->
          <td>
            {{ student.full_name }}
          </td>


          <!-- Education -->
          <td>
            {{ student.education || "Not provided" }}
          </td>


          <!-- Skills -->
          <td>
            {{ student.skills || "Not provided" }}
          </td>


          <!-- Status -->
          <td>

            <span
              class="badge px-3 py-2"
              :class="statusBadge(student)"
            >
              {{ statusText(student) }}
            </span>

          </td>


          <!-- Resume -->
          <td class="text-center">

            <button
              v-if="student.resume_link"
              type="button"
              class="btn btn-outline-primary btn-sm"
              @click="viewResume(student.id)"
            >
              View Resume
            </button>

            <span
              v-else
              class="text-muted"
            >
              No Resume
            </span>

          </td>


          <!-- Actions -->
          <td>

            <button
              type="button"
              class="btn btn-info btn-sm me-2"
              @click="viewProfile(student.id)"
            >
              View Profile
            </button>

            <button
              type="button"
              class="btn btn-primary btn-sm me-2"
              @click="viewPlacementHistory(student.id)"
            >
              Placement History
            </button>

            <!-- ACTIVE STUDENT -->
            <template
              v-if="
                student.is_active &&
                student.status === 'active'
              "
            >

              <button
                type="button"
                class="btn btn-danger btn-sm me-2"
                @click="blacklist(student.id)"
              >
                Blacklist
              </button>


              <button
                type="button"
                class="btn btn-outline-danger btn-sm"
                @click="deactivate(student.id)"
              >
                Deactivate
              </button>

            </template>


            <!-- BLACKLISTED STUDENT -->
            <template
              v-else-if="
                student.is_active &&
                student.status === 'blacklisted'
              "
            >

              <button
                type="button"
                class="btn btn-warning btn-sm me-2"
                @click="unblacklist(student.id)"
              >
                Unblacklist
              </button>


              <button
                type="button"
                class="btn btn-outline-danger btn-sm"
                @click="deactivate(student.id)"
              >
                Deactivate
              </button>

            </template>


            <!-- DEACTIVATED STUDENT -->
            <template v-else>

              <button
                type="button"
                class="btn btn-success btn-sm"
                @click="activate(student.id)"
              >
                Activate
              </button>

            </template>

          </td>

        </tr>

      </tbody>

    </table>


    <!-- Student Profile Modal -->
    <div
      class="modal fade"
      id="studentProfileModal"
      tabindex="-1"
      aria-labelledby="studentProfileModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">

          <div class="modal-header">
            <h5
              class="modal-title"
              id="studentProfileModalLabel"
            >
              Student Profile
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>

          <div class="modal-body">

            <!-- Loading -->
            <div
              v-if="profileLoading"
              class="text-center py-4"
            >
              <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>

            <!-- Error -->
            <div
              v-else-if="profileError"
              class="alert alert-danger"
            >
              {{ profileError }}
            </div>

            <!-- Profile Data -->
            <div v-else-if="selectedStudent">

              <div class="row">

                <div class="col-md-6 mb-3">
                  <strong>Full Name</strong>
                  <p>{{ selectedStudent.full_name }}</p>
                </div>

                <div class="col-md-6 mb-3">
                  <strong>Education</strong>
                  <p>{{ selectedStudent.education || 'Not specified' }}</p>
                </div>

                <div class="col-md-6 mb-3">
                  <strong>Branch</strong>
                  <p>{{ selectedStudent.branch || 'Not specified' }}</p>
                </div>

                <div class="col-md-6 mb-3">
                  <strong>CGPA</strong>
                  <p>{{ selectedStudent.cgpa !== null && selectedStudent.cgpa !== undefined ? selectedStudent.cgpa : 'Not specified' }}</p>
                </div>

                <div class="col-md-6 mb-3">
                  <strong>Graduation Year</strong>
                  <p>{{ selectedStudent.graduation_year || 'Not specified' }}</p>
                </div>

                <div class="col-md-6 mb-3">
                  <strong>Skills</strong>
                  <p>{{ selectedStudent.skills || 'Not specified' }}</p>
                </div>

                <div class="col-md-6 mb-3">
                  <strong>Experience</strong>
                  <p>{{ selectedStudent.experience || 'Not specified' }}</p>
                </div>

                <div class="col-md-6 mb-3">
                  <strong>Resume</strong>
                  <p>
                    <span
                      v-if="selectedStudent.resume_link"
                      class="badge bg-success"
                    >
                      Uploaded
                    </span>
                    <span
                      v-else
                      class="badge bg-secondary"
                    >
                      Not Uploaded
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

    <!-- Placement History Modal -->
    <div
      id="placementHistoryModal"
      class="modal fade"
      tabindex="-1"
    >
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              Placement History
              <span v-if="historyStudentName">
                — {{ historyStudentName }}
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
              v-else-if="placementHistory.length === 0"
              class="alert alert-info mb-0"
            >
              This student has not applied to any placement drives yet.
            </div>

            <div
              v-else
              class="table-responsive"
            >
              <table class="table table-bordered table-hover align-middle">
                <thead class="table-dark">
                  <tr>
                    <th>Company</th>
                    <th>Drive</th>
                    <th>Applied On</th>
                    <th>Status</th>
                    <th>Interview</th>
                  </tr>
                </thead>

                <tbody>
                  <tr
                    v-for="item in placementHistory"
                    :key="item.application_id"
                  >
                    <td>{{ item.company_name }}</td>

                    <td>{{ item.job_title }}</td>

                    <td>
                      {{
                        item.applied_at
                          ? new Date(item.applied_at).toLocaleDateString()
                          : "Not specified"
                      }}
                    </td>

                    <td>
                      <span class="badge bg-secondary">
                        {{ item.status }}
                      </span>
                    </td>

                    <td>
                      <span
                        v-if="item.interview_status === 'Scheduled'"
                        class="badge bg-info text-dark"
                      >
                        {{ item.interview_date }} ·
                        {{ item.interview_time }} ·
                        {{ item.interview_mode }}
                      </span>

                      <span
                        v-else
                        class="text-muted"
                      >
                        Not scheduled
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
import api from "../../api/axios";
import { getStudentById } from "../../services/studentService";
import * as bootstrap from "bootstrap";

import {
  getStudents,
  deactivateStudent,
  activateStudent,
  blacklistStudent,
  unblacklistStudent,
  searchStudents,
  getStudentPlacementHistory
} from "../../services/adminService";


const students = ref([]);

const query = ref("");

const selectedStudent = ref(null);
const profileLoading = ref(false);
const profileError = ref("");
const placementHistory = ref([]);
const historyStudentName = ref("");
const historyLoading = ref(false);
const historyError = ref("");


// ===============================
// LOAD STUDENTS
// ===============================

const loadStudents = async () => {

  try {

    students.value = await getStudents();

  } catch (error) {

    console.error(
      "Failed to load students:",
      error
    );

  }

};


// ===============================
// VIEW PROFILE
// ===============================

const viewProfile = async (studentId) => {

  selectedStudent.value = null;
  profileLoading.value = true;
  profileError.value = "";

  // Open the modal
  const modalEl = document.getElementById("studentProfileModal");
  const modal = new bootstrap.Modal(modalEl);
  modal.show();

  try {

    selectedStudent.value = await getStudentById(studentId);

  } catch (error) {

    profileError.value =
      error.response?.data?.message ||
      "Unable to load profile.";

  } finally {

    profileLoading.value = false;

  }

};


// ===============================
// DEACTIVATE
// ===============================

const deactivate = async (studentId) => {

  try {

    await deactivateStudent(studentId);

    await loadStudents();

  } catch (error) {

    console.error(
      "Failed to deactivate student:",
      error
    );

  }

};


// ===============================
// ACTIVATE
// ===============================

const activate = async (studentId) => {

  try {

    await activateStudent(studentId);

    await loadStudents();

  } catch (error) {

    console.error(
      "Failed to activate student:",
      error
    );

  }

};


// ===============================
// BLACKLIST
// ===============================

const blacklist = async (studentId) => {

  try {

    await blacklistStudent(studentId);

    await loadStudents();

  } catch (error) {

    console.error(
      "Failed to blacklist student:",
      error
    );

  }

};


// ===============================
// UNBLACKLIST
// ===============================

const unblacklist = async (studentId) => {

  try {

    await unblacklistStudent(studentId);

    await loadStudents();

  } catch (error) {

    console.error(
      "Failed to unblacklist student:",
      error
    );

  }

};


// ===============================
// STATUS BADGE
// ===============================

const statusBadge = (student) => {

  if (!student.is_active) {

    return "bg-secondary text-white";

  }

  if (student.status === "blacklisted") {

    return "bg-dark text-white";

  }

  return "bg-success text-white";

};


// ===============================
// STATUS TEXT
// ===============================

const statusText = (student) => {

  if (!student.is_active) {

    return "Deactivated";

  }

  if (student.status === "blacklisted") {

    return "Blacklisted";

  }

  return "Active";

};


// ===============================
// VIEW RESUME
// ===============================

const viewResume = async (studentId) => {

  try {

    const response = await api.get(
      `/student/student/${studentId}/resume`,
      {
        responseType: "blob"
      }
    );

    const blob = new Blob(
      [response.data],
      { type: "application/pdf" }
    );

    const fileURL = URL.createObjectURL(blob);

    window.open(fileURL, "_blank");

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Unable to open resume"
    );

  }

};


// ===============================
// SEARCH
// ===============================

const search = async () => {

  try {

    if (!query.value.trim()) {

      await loadStudents();

      return;

    }

    students.value =
      await searchStudents(query.value);

  } catch (error) {

    console.error(
      "Failed to search students:",
      error
    );

  }

};


// ===============================
// INITIAL LOAD
// ===============================

onMounted(() => {

  loadStudents();

});

const viewPlacementHistory = async (studentId) => {
  placementHistory.value = [];
  historyStudentName.value = "";
  historyLoading.value = true;
  historyError.value = "";

  const modalElement = document.getElementById(
    "placementHistoryModal"
  );

  const modal = new bootstrap.Modal(modalElement);

  modal.show();

  try {
    const response =
      await getStudentPlacementHistory(studentId);

    historyStudentName.value = response.student_name;
    placementHistory.value = response.history;
  } catch (error) {
    historyError.value =
      error.response?.data?.message ||
      "Unable to load placement history.";
  } finally {
    historyLoading.value = false;
  }
};
</script>