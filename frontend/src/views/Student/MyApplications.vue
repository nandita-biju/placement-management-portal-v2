<template>

  <div>

    <h2 class="mb-4">
      My Applications
    </h2>


    <!-- ========================= -->
    <!-- EXPORT CSV -->
    <!-- ========================= -->

    <div class="d-flex justify-content-end mb-3">

      <button
        class="btn btn-success"
        @click="exportCSV"
        :disabled="exporting"
      >
        {{ exporting ? "Generating..." : "Export CSV" }}
      </button>

    </div>


    <!-- ========================= -->
    <!-- APPLICATIONS -->
    <!-- ========================= -->

    <div
      v-if="applications.length === 0"
      class="alert alert-info"
    >
      You haven't applied to any placement drives yet.
    </div>


    <div
      v-for="application in applications"
      :key="application.application_id"
      class="card shadow mb-3"
    >

      <div class="card-body">

        <!-- Job -->
        <h4>
          {{ application.job_title }}
        </h4>

        <!-- Company -->
        <h6 class="text-muted mb-3">
          {{ application.company_name }}
        </h6>


        <!-- Applied Date -->
        <p>

          <strong>
            Applied On:
          </strong>

          {{ formatDate(application.applied_at) }}

        </p>


        <!-- ========================= -->
        <!-- APPLICATION STATUS -->
        <!-- ========================= -->

        <p class="mb-2">

          <strong>
            Application Status:
          </strong>

          <span
            class="badge ms-2"
            :class="badgeColor(application.status)"
          >
            {{ application.status }}
          </span>

        </p>


        <!-- ========================= -->
        <!-- INTERVIEW STATUS -->
        <!-- ========================= -->

        <div
          v-if="hasInterview(application)"
          class="mt-3"
        >

          <hr>

          <h5 class="mb-3">
            Interview Scheduled
          </h5>


          <!-- Interview Date -->

          <p>

            <strong>
              Date:
            </strong>

            {{ formatInterviewDate(application.interview_date) }}

          </p>


          <!-- Interview Time -->

          <p>

            <strong>
              Time:
            </strong>

            {{ formatInterviewTime(application.interview_time) }}

          </p>


          <!-- Interview Mode -->

          <p>

            <strong>
              Mode:
            </strong>

            <span
              class="badge ms-2"
              :class="
                application.interview_mode === 'Online'
                  ? 'bg-primary'
                  : 'bg-secondary'
              "
            >
              {{ application.interview_mode }}
            </span>

          </p>


          <!-- ========================= -->
          <!-- ONLINE INTERVIEW -->
          <!-- ========================= -->

          <div
            v-if="
              application.interview_mode === 'Online' &&
              application.interview_location
            "
            class="mt-3"
          >

            <strong>
              Meeting Link:
            </strong>

            <a
              :href="application.interview_location"
              target="_blank"
              rel="noopener noreferrer"
              class="btn btn-primary btn-sm ms-2"
            >
              Join Interview
            </a>

          </div>


          <!-- ========================= -->
          <!-- OFFLINE INTERVIEW -->
          <!-- ========================= -->

          <div
            v-else-if="
              application.interview_mode === 'Offline' &&
              application.interview_location
            "
            class="mt-3"
          >

            <strong>
              Location:
            </strong>

            <span class="ms-2">
              {{ application.interview_location }}
            </span>

          </div>

        </div>


        <!-- ========================= -->
        <!-- SELECTION RESULT -->
        <!-- ========================= -->

        <div
          v-if="application.status === 'Selected'"
          class="alert alert-success mt-3 mb-0"
        >

          <strong>
            🎉 Congratulations!
          </strong>

          <br>

          You have been selected for this placement drive.

        </div>


        <!-- ========================= -->
        <!-- REJECTION RESULT -->
        <!-- ========================= -->

        <div
          v-else-if="application.status === 'Rejected'"
          class="alert alert-danger mt-3 mb-0"
        >

          <strong>
            Application Result
          </strong>

          <br>

          Unfortunately, you were not selected for this placement drive.

        </div>


        <!-- ========================= -->
        <!-- SHORTLISTED -->
        <!-- ========================= -->

        <div
          v-else-if="
            application.status === 'Shortlisted' &&
            !hasInterview(application)
          "
          class="alert alert-warning mt-3 mb-0"
        >

          <strong>
            You have been shortlisted!
          </strong>

          <br>

          The company has not scheduled your interview yet.

        </div>


      </div>

    </div>


    <!-- ========================= -->
    <!-- SCHEDULED INTERVIEWS -->
    <!-- ========================= -->

    <!--

      This section is kept as a separate summary
      so students can quickly see all upcoming interviews.

    -->

    <div
      v-if="interviews.length > 0"
      class="mt-5"
    >

      <h2 class="mb-4">
        Upcoming Interviews
      </h2>


      <div
        v-for="interview in interviews"
        :key="interview.id || interview.application_id"
        class="card shadow mb-3"
      >

        <div class="card-body">


          <!-- ========================= -->
          <!-- COMPANY / JOB -->
          <!-- ========================= -->

          <h4>

            {{ interview.job_title || "Placement Interview" }}

          </h4>

          <h6 class="text-muted mb-3">

            {{ interview.company_name || "Company" }}

          </h6>


          <!-- ========================= -->
          <!-- DATE -->
          <!-- ========================= -->

          <p>

            <strong>
              Date:
            </strong>

            {{ formatInterviewDate(interview.interview_date) }}

          </p>


          <!-- ========================= -->
          <!-- TIME -->
          <!-- ========================= -->

          <p>

            <strong>
              Time:
            </strong>

            {{ formatInterviewTime(interview.interview_time) }}

          </p>


          <!-- ========================= -->
          <!-- MODE -->
          <!-- ========================= -->

          <p>

            <strong>
              Mode:
            </strong>

            <span
              class="badge ms-2"
              :class="
                interview.interview_mode === 'Online'
                  ? 'bg-primary'
                  : 'bg-secondary'
              "
            >
              {{ interview.interview_mode }}
            </span>

          </p>


          <!-- ========================= -->
          <!-- ONLINE LINK -->
          <!-- ========================= -->

          <div
            v-if="
              interview.interview_mode === 'Online' &&
              interview.interview_location
            "
            class="mt-3"
          >

            <a
              :href="interview.interview_location"
              target="_blank"
              rel="noopener noreferrer"
              class="btn btn-primary"
            >
              Join Interview
            </a>

          </div>


          <!-- ========================= -->
          <!-- OFFLINE LOCATION -->
          <!-- ========================= -->

          <div
            v-else-if="
              interview.interview_mode === 'Offline' &&
              interview.interview_location
            "
            class="mt-3"
          >

            <strong>
              Location:
            </strong>

            <span class="ms-2">
              {{ interview.interview_location }}
            </span>

          </div>


        </div>

      </div>

    </div>


    <!-- ========================= -->
    <!-- NO INTERVIEWS -->
    <!-- ========================= -->

    <div
      v-else
      class="mt-5"
    >

      <h2 class="mb-4">
        Upcoming Interviews
      </h2>

      <div class="alert alert-info">

        No interviews scheduled yet.

      </div>

    </div>


  </div>

</template>


<script setup>

import { ref, onMounted } from "vue";


import {
  getMyApplications,
  exportApplications,
  checkExportStatus
} from "../../services/applicationService";


import {
  getMyInterviews
} from "../../services/studentService";



/* ========================= */
/* STATE */
/* ========================= */

const applications = ref([]);

const interviews = ref([]);

const exporting = ref(false);



/* ========================= */
/* LOAD DATA */
/* ========================= */

onMounted(async () => {

  try {

    applications.value =
      await getMyApplications();


    await loadInterviews();

  }

  catch (error) {

    console.log(
      "Unable to load applications:",
      error
    );

  }

});



/* ========================= */
/* APPLICATION STATUS BADGE */
/* ========================= */

const badgeColor = (status) => {

  switch (status) {

    case "Applied":
      return "bg-primary";

    case "Shortlisted":
      return "bg-warning text-dark";

    case "Interview Scheduled":
      return "bg-info";

    case "Selected":
      return "bg-success";

    case "Rejected":
      return "bg-danger";

    default:
      return "bg-secondary";

  }

};



/* ========================= */
/* CHECK INTERVIEW */
/* ========================= */

const hasInterview = (application) => {

  return (
    application.interview_status === "Scheduled" ||
    application.interview_date ||
    application.interview_time
  );

};



/* ========================= */
/* APPLICATION DATE */
/* ========================= */

const formatDate = (date) => {

  if (!date) {
    return "Not specified";
  }

  return new Date(date).toLocaleDateString();

};



/* ========================= */
/* INTERVIEW DATE */
/* ========================= */

const formatInterviewDate = (date) => {

  if (!date) {
    return "Not specified";
  }

  return new Date(date).toLocaleDateString();

};



/* ========================= */
/* INTERVIEW TIME */
/* ========================= */

const formatInterviewTime = (time) => {

  if (!time) {
    return "Not specified";
  }

  /*
    Backend may return:

    14:30:00

    or

    14:30
  */

  const parts = time.split(":");

  if (parts.length < 2) {
    return time;
  }

  const hours = parseInt(parts[0]);

  const minutes = parts[1];

  const date = new Date();

  date.setHours(hours);
  date.setMinutes(parseInt(minutes));

  return date.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit"
  });

};



/* ========================= */
/* LOAD INTERVIEWS */
/* ========================= */

const loadInterviews = async () => {

  try {

    interviews.value =
      await getMyInterviews();

  }

  catch (error) {

    console.log(
      "Unable to load interviews:",
      error
    );

  }

};



/* ========================= */
/* EXPORT APPLICATIONS */
/* ========================= */

const exportCSV = async () => {

  exporting.value = true;

  try {

    const response = await exportApplications();

    const taskId = response.task_id;

    const interval = setInterval(async () => {

      try {

        const status = await checkExportStatus(taskId);

        // =========================
        // COMPLETED
        // =========================

        if (status.status === "Completed") {

          clearInterval(interval);

          exporting.value = false;

          const link = document.createElement("a");

          link.href =
            `http://127.0.0.1:5000/exports/${status.filename}`;

          link.download = status.filename;

          document.body.appendChild(link);

          link.click();

          link.remove();

          // Notification
          alert(
            "✅ Your applications CSV has been downloaded successfully!"
          );
        }

        // =========================
        // FAILED
        // =========================

        else if (status.status === "Failed") {

          clearInterval(interval);

          exporting.value = false;

          alert("❌ Export failed.");

        }

      }

      catch (error) {

        clearInterval(interval);

        exporting.value = false;

        console.log(error);

        alert(
          "Unable to check export status."
        );

      }

    }, 2000);

  }

  catch (error) {

    exporting.value = false;

    console.log(error);

    alert(
      "Export failed."
    );

  }

};

</script>