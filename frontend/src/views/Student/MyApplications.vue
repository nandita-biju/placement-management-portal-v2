<template>

<div>

    <h2 class="mb-4">
        My Applications
    </h2>

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

            <h4>
                {{ application.job_title }}
            </h4>

            <h6 class="text-muted">
                {{ application.company_name }}
            </h6>

            <p>

                <strong>Applied On:</strong>

                {{ formatDate(application.applied_at) }}

            </p>

            <span
                class="badge"
                :class="badgeColor(application.status)"
            >
                {{ application.status }}
            </span>

        </div>

    </div>

</div>

</template>

<script setup>

import { ref, onMounted } from "vue";

import { getMyApplications } from "../../services/applicationService";

const applications = ref([]);

onMounted(async ()=>{

    applications.value = await getMyApplications();

});

const badgeColor = (status)=>{

    switch(status){

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

const formatDate = (date)=>{

    return new Date(date).toLocaleDateString();

};

</script>