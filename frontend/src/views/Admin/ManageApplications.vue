<template>

<div class="container">

    <h2 class="mb-4">
        Applications
    </h2>

    <div
        v-if="applications.length===0"
        class="alert alert-info"
    >
        No applications found.
    </div>

    <table
        v-if="applications.length>0"
        class="table table-bordered table-hover align-middle"
    >

        <thead class="table-dark">

            <tr>

                <th>Student</th>
                <th>Company</th>
                <th>Drive</th>
                <th>Status</th>
                <th>Applied On</th>

            </tr>

        </thead>

        <tbody>

            <tr
                v-for="application in applications"
                :key="application.id"
            >

                <td>{{ application.student_name }}</td>

                <td>{{ application.company_name }}</td>

                <td>{{ application.drive_title }}</td>

                <td>

                    <span
                        class="badge"
                        :class="statusBadge(application.status)"
                    >
                        {{ application.status }}
                    </span>

                </td>

                <td>{{ application.applied_at }}</td>

            </tr>

        </tbody>

    </table>

</div>

</template>

<script setup>

import { ref,onMounted } from "vue";

import {
    getApplications
} from "../../services/adminService";

const applications = ref([]);

const loadApplications = async()=>{

    applications.value = await getApplications();

};

onMounted(loadApplications);

const statusBadge=(status)=>{

    if(status==="Applied")
        return "bg-warning text-dark";

    if(status==="Shortlisted")
        return "bg-primary";

    if(status==="Selected")
        return "bg-success";

    if(status==="Rejected")
        return "bg-danger";

    return "bg-secondary";

};

</script>