<template>
  <div class="container">

    <!-- Back -->
    <router-link
      to="/company/drives"
      class="btn btn-secondary mb-4"
    >
      ← Back to My Drives
    </router-link>

    <h2 class="mb-4">
      Applicants
    </h2>


    <!-- No Applicants -->
    <div
      v-if="applicants.length === 0"
      class="alert alert-info"
    >
      No applications received yet.
    </div>


    <!-- Applicants Table -->
    <table
      v-else
      class="table table-bordered table-hover"
    >

      <thead class="table-dark text-center">

        <tr>
          <th>Name</th>
          <th>Resume</th>
          <th>Profile</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>

      </thead>


      <tbody>

        <tr
          v-for="applicant in applicants"
          :key="applicant.application_id"
          class="align-middle"
        >

          <!-- Student Name -->
          <td>
            {{ applicant.student_name }}
          </td>


          <!-- Resume -->
          <td class="text-center">

            <button
              v-if="applicant.resume_link"
              class="btn btn-primary btn-sm"
              @click="viewResume(applicant.student_id)"
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


          <!-- Profile -->
          <td class="text-center">

            <router-link
              :to="`/company/student/${applicant.student_id}/${route.params.jobId}`"
              class="btn btn-info btn-sm"
            >
              View Profile
            </router-link>

          </td>


          <!-- Status -->
          <td class="text-center">

            <span
              class="badge"
              :class="getStatusBadge(applicant.status)"
            >
              {{ applicant.status }}
            </span>

            <!-- Interview Scheduled Indicator -->
            <div
              v-if="
                applicant.status === 'Shortlisted' &&
                applicant.interview_status === 'Scheduled'
              "
              class="mt-2"
            >

              <span class="badge bg-info">
                Interview Scheduled
              </span>

            </div>

          </td>


          <!-- Actions -->
          <td class="text-center">


            <!-- ================================= -->
            <!-- APPLIED -->
            <!-- ================================= -->

            <template
              v-if="applicant.status === 'Applied'"
            >

              <button
                class="btn btn-primary btn-sm me-2"
                @click="changeStatus(
                  applicant.application_id,
                  'Shortlisted'
                )"
              >
                Shortlist
              </button>


              <button
                class="btn btn-danger btn-sm"
                @click="changeStatus(
                  applicant.application_id,
                  'Rejected'
                )"
              >
                Reject
              </button>

            </template>


            <!-- ================================= -->
            <!-- SHORTLISTED - INTERVIEW NOT SCHEDULED -->
            <!-- ================================= -->

            <template
              v-else-if="
                applicant.status === 'Shortlisted' &&
                applicant.interview_status !== 'Scheduled'
              "
            >

              <button
                class="btn btn-warning btn-sm me-2"
                @click="openInterviewModal(applicant)"
              >
                Schedule Interview
              </button>


              <button
                class="btn btn-danger btn-sm"
                @click="changeStatus(
                  applicant.application_id,
                  'Rejected'
                )"
              >
                Reject
              </button>

            </template>


            <!-- ================================= -->
            <!-- SHORTLISTED - INTERVIEW SCHEDULED -->
            <!-- ================================= -->

            <template
              v-else-if="
                applicant.status === 'Shortlisted' &&
                applicant.interview_status === 'Scheduled'
              "
            >

              <button
                class="btn btn-success btn-sm me-2"
                @click="changeStatus(
                  applicant.application_id,
                  'Selected'
                )"
              >
                ✓ Select
              </button>


              <button
                class="btn btn-danger btn-sm"
                @click="changeStatus(
                  applicant.application_id,
                  'Rejected'
                )"
              >
                ✕ Reject
              </button>

            </template>


            <!-- ================================= -->
            <!-- SELECTED -->
            <!-- ================================= -->

            <template
              v-else-if="applicant.status === 'Selected'"
            >

              <button
                class="btn btn-success btn-sm"
                disabled
              >
                ✓ Selected
              </button>

            </template>


            <!-- ================================= -->
            <!-- REJECTED -->
            <!-- ================================= -->

            <template
              v-else-if="applicant.status === 'Rejected'"
            >

              <button
                class="btn btn-danger btn-sm"
                disabled
              >
                ✕ Rejected
              </button>

            </template>


          </td>

        </tr>

      </tbody>

    </table>



    <!-- ========================================= -->
    <!-- SCHEDULE INTERVIEW MODAL -->
    <!-- ========================================= -->

    <div
      v-if="showInterviewModal"
      class="modal fade show d-block"
      tabindex="-1"
      style="background-color: rgba(0, 0, 0, 0.5);"
    >

      <div class="modal-dialog">

        <div class="modal-content">


          <!-- Modal Header -->

          <div class="modal-header">

            <h5 class="modal-title">
              Schedule Interview
            </h5>


            <button
              type="button"
              class="btn-close"
              @click="closeInterviewModal"
            ></button>

          </div>



          <!-- Modal Body -->

          <div class="modal-body">


            <!-- Student -->

            <div
              v-if="selectedApplication"
              class="mb-3"
            >

              <strong>
                Student:
              </strong>

              {{ selectedApplication.student_name }}

            </div>



            <!-- Interview Date -->

            <div class="mb-3">

              <label class="form-label">
                Interview Date
              </label>

              <input
                v-model="interviewForm.interview_date"
                type="date"
                class="form-control"
                required
              >

            </div>



            <!-- Interview Time -->

            <div class="mb-3">

              <label class="form-label">
                Interview Time
              </label>

              <input
                v-model="interviewForm.interview_time"
                type="time"
                class="form-control"
                required
              >

            </div>



            <!-- Interview Mode -->

            <div class="mb-3">

              <label class="form-label">
                Interview Mode
              </label>

              <select
                v-model="interviewForm.interview_mode"
                class="form-select"
              >

                <option value="Online">
                  Online
                </option>

                <option value="Offline">
                  Offline
                </option>

              </select>

            </div>



            <!-- Location / Meeting Link -->

            <div class="mb-3">

              <label class="form-label">
                Meeting Link / Location
              </label>

              <input
                v-model="interviewForm.interview_location"
                type="text"
                class="form-control"
                placeholder="Enter meeting link or interview location"
                required
              >

            </div>


          </div>



          <!-- Modal Footer -->

          <div class="modal-footer">

            <button
              type="button"
              class="btn btn-secondary"
              @click="closeInterviewModal"
            >
              Cancel
            </button>


            <button
              type="button"
              class="btn btn-primary"
              @click="submitInterview"
            >
              Schedule Interview
            </button>

          </div>


        </div>

      </div>

    </div>

  </div>
</template>



<script setup>

import { ref, onMounted } from "vue";

import { useRoute } from "vue-router";

import api from "../../api/axios";

import {
  getApplicants,
  updateApplicationStatus,
  scheduleInterview
} from "../../services/companyService";



/* =========================================
   ROUTE
========================================= */

const route = useRoute();



/* =========================================
   APPLICANTS
========================================= */

const applicants = ref([]);



/* =========================================
   INTERVIEW MODAL
========================================= */

const showInterviewModal = ref(false);

const selectedApplication = ref(null);



/* =========================================
   INTERVIEW FORM
========================================= */

const interviewForm = ref({

  interview_date: "",

  interview_time: "",

  interview_mode: "Online",

  interview_location: ""

});



/* =========================================
   LOAD APPLICANTS
========================================= */

const loadApplicants = async () => {

  try {

    applicants.value = await getApplicants(
      route.params.jobId
    );

  }

  catch (error) {

    console.log(error);

  }

};



/* =========================================
   INITIAL LOAD
========================================= */

onMounted(() => {

  loadApplicants();

});



/* =========================================
   UPDATE APPLICATION STATUS
========================================= */

const changeStatus = async (
  applicationId,
  status
) => {

  try {

    await updateApplicationStatus(
      applicationId,
      status
    );


    alert(
      "Application status updated successfully!"
    );


    await loadApplicants();

  }

  catch (error) {

    alert(
      error.response?.data?.message ||
      error.message
    );

  }

};



/* =========================================
   STATUS BADGE
========================================= */

const getStatusBadge = (status) => {

  if (status === "Applied")
    return "bg-warning text-dark";


  if (status === "Shortlisted")
    return "bg-primary";


  if (status === "Selected")
    return "bg-success";


  if (status === "Rejected")
    return "bg-danger";


  return "bg-secondary";

};



/* =========================================
   VIEW RESUME
========================================= */

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
      {
        type: "application/pdf"
      }
    );


    const fileURL =
      URL.createObjectURL(blob);


    window.open(
      fileURL,
      "_blank"
    );


  }

  catch (error) {

    alert(
      error.response?.data?.message ||
      "Unable to open resume"
    );

  }

};



/* =========================================
   OPEN INTERVIEW MODAL
========================================= */

const openInterviewModal = (applicant) => {

  selectedApplication.value = applicant;


  interviewForm.value = {

    interview_date: "",

    interview_time: "",

    interview_mode: "Online",

    interview_location: ""

  };


  showInterviewModal.value = true;

};



/* =========================================
   CLOSE INTERVIEW MODAL
========================================= */

const closeInterviewModal = () => {

  showInterviewModal.value = false;

  selectedApplication.value = null;

};



/* =========================================
   SUBMIT INTERVIEW
========================================= */

const submitInterview = async () => {

  if (!selectedApplication.value) {

    return;

  }


  try {

    await scheduleInterview(

      selectedApplication.value.application_id,

      interviewForm.value

    );


    alert(
      "Interview scheduled successfully!"
    );


    closeInterviewModal();


    await loadApplicants();

  }

  catch (error) {

    alert(
      error.response?.data?.message ||
      error.message
    );

  }

};

</script>