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
        <strong>Skills</strong>
        <p>{{ profile.skills }}</p>
    </div>

    <div class="col-md-6 mb-3">
        <strong>Experience</strong>
        <p>{{ profile.experience }}</p>
    </div>

    <div class="col-md-12 mb-3">
        <strong>Resume</strong>
        <br>

        <a
            :href="profile.resume_link"
            target="_blank"
            class="btn btn-primary mt-2"
        >
            View Resume
        </a>
    </div>

</div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getProfile } from "../../services/studentService";

const profile = ref({});

onMounted(async () => {

    try{

        profile.value = await getProfile();

    }

    catch(error){

        if(error.response.status === 404){

            router.push("/student/profile/create");

        }

    }

});
</script>