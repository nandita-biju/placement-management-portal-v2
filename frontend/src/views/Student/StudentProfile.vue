<template>
<div class="row">

    <div class="col-md-6 mb-3">
        <strong>Full Name</strong>
        <p>{{ profile.full_name }}</p>
    </div>

    <div class="col-md-6 mb-3">
        <strong>Education</strong>
        <p>{{ profile.education }}</p>
    </div>

    <div class="col-md-6 mb-3">
        <strong>Branch</strong>
        <p>{{ profile.branch || 'Not specified' }}</p>
    </div>

    <div class="col-md-6 mb-3">
        <strong>Current CGPA</strong>
        <p>{{ profile.cgpa !== null && profile.cgpa !== undefined ? profile.cgpa : 'Not specified' }}</p>
    </div>

    <div class="col-md-6 mb-3">
        <strong>Graduation Year</strong>
        <p>{{ profile.graduation_year || 'Not specified' }}</p>
    </div>

    <div class="col-md-6 mb-3">
        <strong>Skills</strong>
        <p>{{ profile.skills }}</p>
    </div>


    <div class="col-md-6 mb-3">
        <strong>Experience</strong>
        <p>{{ profile.experience }}</p>
    </div>

    <div class="row mb-3">

        <div class="col-md-3">
            <strong>Resume</strong>
        </div>

        <div class="col-md-9">

            <button
            v-if="profile.resume_link"
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
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getProfile, viewResume } from "../../services/studentService";

const router = useRouter();

const profile = ref({});

onMounted(async () => {

    try{

        profile.value = await getProfile();

    }

    catch(error){

        if(error.response && error.response.status === 404){

            router.push("/student/profile/create");

        }

    }

});

const handleViewResume = async () => {

    try {

        const response = await viewResume();

        const blob = new Blob(
            [response.data],
            { type: "application/pdf" }
        );

        const fileURL = URL.createObjectURL(blob);

        const newTab = window.open(fileURL, "_blank");

        if (newTab) {
            newTab.addEventListener("beforeunload", () => {
                URL.revokeObjectURL(fileURL);
            });
        }

    }

    catch (error) {

        alert(
            error.response?.data?.message ||
            "Unable to open resume"
        );

    }

};
</script>