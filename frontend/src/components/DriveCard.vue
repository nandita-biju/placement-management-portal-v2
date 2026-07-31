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