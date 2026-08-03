<template>
  <div class="container">

    <div class="card shadow">

      <div class="card-header">
        <h3>Edit Profile</h3>
      </div>

      <div class="card-body">

        <form @submit.prevent="saveProfile">

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
            <label class="form-label">Branch</label>
            <select
              v-model="profile.branch"
              class="form-select"
              required
            >
              <option value="" disabled>Select Branch</option>
              <option value="CSE">CSE</option>
              <option value="ECE">ECE</option>
              <option value="EEE">EEE</option>
              <option value="MECH">MECH</option>
              <option value="CIVIL">CIVIL</option>
              <option value="IT">IT</option>
              <option value="Chemical">Chemical</option>
              <option value="Aerospace">Aerospace</option>
              <option value="Data Science">Data Science</option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">Current CGPA</label>
            <input
              v-model.number="profile.cgpa"
              type="number"
              step="0.01"
              min="0"
              max="10"
              class="form-control"
              placeholder="e.g. 8.5"
              required
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Graduation Year</label>
            <select
              v-model.number="profile.graduation_year"
              class="form-select"
              required
            >
              <option value="" disabled>Select Graduation Year</option>
              <option :value="2024">2024</option>
              <option :value="2025">2025</option>
              <option :value="2026">2026</option>
              <option :value="2027">2027</option>
              <option :value="2028">2028</option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">Skills</label>
            <textarea
              v-model="profile.skills"
              class="form-control"
              rows="3"
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

          <div class="d-flex gap-2">

            <button
              class="btn btn-success"
              type="submit"
            >
              Save Changes
            </button>

            <button
              class="btn btn-secondary"
              type="button"
              @click="goBack"
            >
              Cancel
            </button>

          </div>

        </form>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import {
    getProfile,
    updateProfile
} from "../../services/studentService";

const router = useRouter();

const profile = ref({});

onMounted(async () => {
    profile.value = await getProfile();
});

const saveProfile = async () => {

    try {

        await updateProfile(profile.value);

        alert("Profile updated successfully!");

        router.push("/student/profile");

    }

    catch (error) {

        console.log(error);

        alert(
            error.response?.data?.message || error.message
        );

    }

};

const goBack = () => {
    router.push("/student/profile");
};
</script>