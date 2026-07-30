<template>
  <div class="container mt-5">

    <div class="card shadow">

      <div class="card-header">
        <h3>Complete Your Profile</h3>
      </div>

      <div class="card-body">

        <form @submit.prevent="createProfileHandler">

          <div class="mb-3">
            <label class="form-label">Full Name</label>
            <input
              v-model="profile.full_name"
              class="form-control"
              required
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Education</label>
            <input
              v-model="profile.education"
              class="form-control"
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Skills</label>
            <textarea
              v-model="profile.skills"
              rows="3"
              class="form-control"
            ></textarea>
          </div>

          <div class="mb-3">
            <label class="form-label">Experience</label>
            <input
              v-model="profile.experience"
              class="form-control"
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Resume Link</label>
            <input
              v-model="profile.resume_link"
              class="form-control"
            >
          </div>

          <button
            class="btn btn-primary"
            type="submit"
          >
            Create Profile
          </button>

        </form>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { createProfile } from "../../services/studentService";

const router = useRouter();

const profile = ref({
    full_name: "",
    education: "",
    skills: "",
    experience: "",
    resume_link: ""
});

const createProfileHandler = async () => {

    try{

        await createProfile(profile.value);

        alert("Profile created successfully!");

        router.push("/student/profile");

    }

    catch(error){

        alert(
            error.response?.data?.message || error.message
        );

    }

};
</script>