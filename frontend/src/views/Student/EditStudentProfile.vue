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


          <!-- Resume Section -->
          <div class="mb-3">

            <label class="form-label">
              Resume
            </label>

            <!-- Resume already uploaded -->
            <div v-if="profile.resume_link" class="mb-2">

              <span class="badge bg-success me-2">
                ✅ Resume uploaded
              </span>

              <button
                type="button"
                class="btn btn-outline-primary btn-sm me-2"
                @click="handleViewResume"
              >
                View Resume
              </button>

              <button
                type="button"
                class="btn btn-outline-danger btn-sm"
                @click="handleDeleteResume"
              >
                Delete Resume
              </button>

            </div>

            <!-- No resume -->
            <div v-else class="mb-2">
              <span class="text-muted">
                No resume uploaded
              </span>
            </div>

            <!-- Upload / Re-upload -->
            <input
              type="file"
              class="form-control"
              accept=".pdf,application/pdf"
              @change="handleResumeUpload"
            >

            <small class="text-muted">
              Only PDF files are allowed. {{ profile.resume_link ? 'Uploading a new file will replace the existing resume.' : '' }}
            </small>

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
    updateProfile,
    uploadResume,
    viewResume,
    deleteResume
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

const handleResumeUpload = async (event) => {

    const file = event.target.files[0];

    if (!file) {
        return;
    }

    try {

        const formData = new FormData();

        formData.append("resume", file);

        await uploadResume(formData);

        alert("Resume uploaded successfully!");

        profile.value = await getProfile();

    }

    catch (error) {

        alert(
            error.response?.data?.message ||
            error.message
        );

    }
};

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

const handleDeleteResume = async () => {

    if (!confirm("Are you sure you want to delete your resume?")) {
        return;
    }

    try {

        await deleteResume();

        alert("Resume deleted successfully!");

        profile.value = await getProfile();

    }

    catch (error) {

        alert(
            error.response?.data?.message ||
            error.message
        );

    }

};

const goBack = () => {
    router.push("/student/profile");
};
</script>