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

                    <a
                        :href="student.resume_link"
                        target="_blank"
                    >
                        View Resume
                    </a>

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

</script>