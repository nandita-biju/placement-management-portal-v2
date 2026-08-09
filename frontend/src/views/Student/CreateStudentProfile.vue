<template>
  <div class="container">

    <div class="card shadow">

      <div class="card-header">
        <h3>Complete Your Profile</h3>
      </div>

      <div class="card-body">

        <form @submit.prevent="createProfileHandler">

          <!-- Full Name -->
          <div class="mb-3">
            <label class="form-label">Full Name</label>

            <input
              v-model="profile.full_name"
              class="form-control"
              required
            >
          </div>

          <!-- Education -->
          <div class="mb-3">
            <label class="form-label">Education</label>

            <input
              v-model="profile.education"
              class="form-control"
            >
          </div>

          <!-- Skills -->
          <div class="mb-3">
            <label class="form-label">Skills</label>

            <textarea
              v-model="profile.skills"
              rows="3"
              class="form-control"
            ></textarea>
          </div>

          <!-- Branch -->
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

          <!-- CGPA -->
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

          <!-- Graduation Year -->
          <div class="mb-3">
            <label class="form-label">Graduation Year</label>

            <select
              v-model.number="profile.graduation_year"
              class="form-select"
              required
            >
              <option value="" disabled>
                Select Graduation Year
              </option>

              <option :value="2024">2024</option>
              <option :value="2025">2025</option>
              <option :value="2026">2026</option>
              <option :value="2027">2027</option>
              <option :value="2028">2028</option>
            </select>
          </div>

          <!-- Experience -->
          <div class="mb-3">
            <label class="form-label">Experience</label>

            <input
              v-model="profile.experience"
              class="form-control"
            >
          </div>


          <!-- Resume -->
          <div class="mb-3">

            <label class="form-label">
              Resume
            </label>

            <input
              type="file"
              class="form-control"
              accept=".pdf,application/pdf"
              @change="handleResumeUpload"
            >

            <small class="text-muted">
              Only PDF files are allowed.
            </small>

          </div>


          <!-- Submit -->
          <button
            class="btn btn-primary"
            type="submit"
            :disabled="loading"
          >
            {{ loading ? "Creating Profile..." : "Create Profile" }}
          </button>

        </form>

      </div>

    </div>

  </div>
</template>


<script setup>

import { ref } from "vue";
import { useRouter } from "vue-router";

import {
    createProfile,
    uploadResume
} from "../../services/studentService";


const router = useRouter();


// Student profile
const profile = ref({

    full_name: "",
    education: "",
    skills: "",
    branch: "",
    cgpa: null,
    graduation_year: null,
    experience: "",
    resume_link: ""

});


// Selected resume file
const selectedResume = ref(null);


// Loading state
const loading = ref(false);


// Resume file selection
const handleResumeUpload = (event) => {

    const file = event.target.files[0];

    if (!file) {
        selectedResume.value = null;
        return;
    }

    // Make sure it is a PDF
    if (file.type !== "application/pdf") {

        alert("Please select a PDF file.");

        event.target.value = "";

        selectedResume.value = null;

        return;
    }

    selectedResume.value = file;
};


// Create profile
const createProfileHandler = async () => {

    loading.value = true;

    try {

        // --------------------------------
        // STEP 1: Create student profile
        // --------------------------------

        await createProfile({

            full_name: profile.value.full_name,
            education: profile.value.education,
            skills: profile.value.skills,
            branch: profile.value.branch,
            cgpa: profile.value.cgpa,
            graduation_year: profile.value.graduation_year,
            experience: profile.value.experience

        });


        // --------------------------------
        // STEP 2: Upload resume if selected
        // --------------------------------

        if (selectedResume.value) {

            const formData = new FormData();

            formData.append(
                "resume",
                selectedResume.value
            );

            await uploadResume(formData);

        }


        // --------------------------------
        // STEP 3: Success
        // --------------------------------

        alert("Profile created successfully!");

        router.push("/student/profile");

    }

    catch (error) {

        console.error(
            "Create student profile error:",
            error
        );

        alert(
            error.response?.data?.message ||
            error.message ||
            "Failed to create profile."
        );

    }

    finally {

        loading.value = false;

    }

};

</script>