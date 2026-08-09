<template>

<div class="container">

    <router-link
        :to="`/company/applicants/${route.params.jobId}`"
        class="btn btn-secondary mb-4"
    >
        ← Back
    </router-link>

    <div class="card shadow">

        <div class="card-header">
            <h3>Student Profile</h3>
        </div>

        <div class="card-body">

            <div class="row mb-3">

                <div class="col-md-3">
                    <strong>Name</strong>
                </div>

                <div class="col-md-9">
                    {{ student.full_name }}
                </div>

            </div>

            <div class="row mb-3">

                <div class="col-md-3">
                    <strong>Education</strong>
                </div>

                <div class="col-md-9">
                    {{ student.education }}
                </div>

            </div>

            <div class="row mb-3">

                <div class="col-md-3">
                    <strong>Branch</strong>
                </div>

                <div class="col-md-9">
                    {{ student.branch || 'N/A' }}
                </div>

            </div>

            <div class="row mb-3">

                <div class="col-md-3">
                    <strong>CGPA</strong>
                </div>

                <div class="col-md-9">
                    {{ student.cgpa !== null && student.cgpa !== undefined ? student.cgpa : 'N/A' }}
                </div>

            </div>

            <div class="row mb-3">

                <div class="col-md-3">
                    <strong>Graduation Year</strong>
                </div>

                <div class="col-md-9">
                    {{ student.graduation_year || 'N/A' }}
                </div>

            </div>


            <div class="row mb-3">

                <div class="col-md-3">
                    <strong>Skills</strong>
                </div>

                <div class="col-md-9">
                    {{ student.skills }}
                </div>

            </div>

            <div class="row mb-3">

                <div class="col-md-3">
                    <strong>Experience</strong>
                </div>

                <div class="col-md-9">
                    {{ student.experience }}
                </div>

            </div>

            <div class="row">

                <div class="col-md-3">
                    <strong>Resume</strong>
                </div>

                <div class="col-md-9">

                    <button
                        v-if="student.resume_link"
                        class="btn btn-primary btn-sm"
                        @click="handleViewResume"
                    >
                        View Resume
                    </button>

                    <span
                        v-else
                        class="text-muted"
                    >
                        No resume uploaded
                    </span>

                </div>

            </div>

        </div>

    </div>

</div>

</template>

<script setup>

import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { getStudentById } from "../../services/studentService";
import api from "../../api/axios";

const route = useRoute();

const student = ref({});

onMounted(async () => {

    try {

        student.value = await getStudentById(
            route.params.studentId
        );

    }

    catch(error){

        console.log(error);

    }

});

const handleViewResume = async () => {

    try {

        const response = await api.get(
            `/student/student/${route.params.studentId}/resume`,
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

    }

    catch (error) {

        alert(
            error.response?.data?.message ||
            "Unable to open resume"
        );

    }

};

</script>