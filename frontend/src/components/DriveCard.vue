<template>
  <div class="card shadow-sm mb-4">

    <div class="card-body">

      <h4>{{ drive.title }}</h4>

      <p>{{ drive.description }}</p>

      <p>
        <strong>Salary:</strong>
        {{ drive.salary }}
      </p>

      <p>
        <strong>Skills Required:</strong>
        {{ drive.skills_required }}
      </p>

      <div class="row text-muted small mb-3">
        <div class="col-md-6" v-if="drive.eligible_branch">
          <strong>Eligible Branch:</strong> {{ drive.eligible_branch }}
        </div>
        <div class="col-md-6" v-if="drive.min_cgpa !== null && drive.min_cgpa !== undefined">
          <strong>Min CGPA:</strong> {{ drive.min_cgpa }}
        </div>
        <div class="col-md-6" v-if="drive.eligible_graduation_year">
          <strong>Graduation Year:</strong> {{ drive.eligible_graduation_year }}
        </div>
        <div class="col-md-6" v-if="drive.application_deadline">
          <strong>Deadline:</strong> {{ drive.application_deadline }}
        </div>
      </div>


      <p>
        <strong>Status:</strong>

        <span
          class="badge"
          :class="badgeClass"
        >
          {{ drive.status }}
        </span>

      </p>

      <router-link
        :to="`/company/applicants/${drive.id}`"
        class="btn btn-primary"
      >
        View Applicants
      </router-link>

    </div>

  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
    drive: Object
});

const badgeClass = computed(() => {

    if (props.drive.status === "approved")
        return "bg-success";

    if (props.drive.status === "rejected")
        return "bg-danger";

    return "bg-warning text-dark";

});
</script>