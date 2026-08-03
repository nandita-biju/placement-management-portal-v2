<template>

<div>

    <h2 class="mb-4">
        Browse Placement Drives
    </h2>

    <input
        v-model="search"
        class="form-control mb-4"
        placeholder="Search company or job title..."
    >

    <div
        v-for="drive in filteredDrives"
        :key="drive.id"
        class="card shadow mb-4"
    >

        <div class="card-body">

            <h4>
                {{ drive.title }}
            </h4>

            <h6 class="text-muted">
                {{ drive.company_name }}
            </h6>

            <p>
                {{ drive.description }}
            </p>

            <p>

                <strong>Salary:</strong>

                {{ drive.salary }}

            </p>

            <p>

                <strong>Skills Required:</strong>

                {{ drive.skills_required }}

            </p>

            <div class="row mb-3 p-3 bg-light rounded border">
                <div class="col-md-6 mb-2">
                    <strong>Eligible Branch:</strong>
                    <span class="ms-1 badge bg-info text-dark">{{ drive.eligible_branch || 'All Branches' }}</span>
                </div>
                <div class="col-md-6 mb-2">
                    <strong>Minimum CGPA:</strong>
                    <span class="ms-1 badge bg-info text-dark">{{ drive.min_cgpa !== null && drive.min_cgpa !== undefined ? drive.min_cgpa : 'None' }}</span>
                </div>
                <div class="col-md-6 mb-2">
                    <strong>Graduation Year:</strong>
                    <span class="ms-1 badge bg-info text-dark">{{ drive.eligible_graduation_year || 'All' }}</span>
                </div>
                <div class="col-md-6 mb-2">
                    <strong>Application Deadline:</strong>
                    <span class="ms-1 badge bg-secondary">{{ drive.application_deadline || 'No deadline' }}</span>
                </div>
            </div>

            <div class="d-flex align-items-center gap-2">
                <button
                    class="btn"
                    :class="getEligibilityStatus(drive).isEligible ? 'btn-success' : 'btn-secondary'"
                    @click="apply(drive.id)"
                >
                    {{ getEligibilityStatus(drive).isEligible ? 'Apply' : 'Not Eligible' }}
                </button>
                <span v-if="!getEligibilityStatus(drive).isEligible" class="text-danger small fw-bold">
                    ({{ getEligibilityStatus(drive).reason }})
                </span>
            </div>

        </div>

    </div>

</div>

</template>

<script setup>

import { ref, computed, onMounted } from "vue";

import {
    getAllDrives,
    applyDrive
}
from "../../services/driveService";

import { getProfile } from "../../services/studentService";

const drives = ref([]);

const studentProfile = ref(null);

const search = ref("");

onMounted(async ()=>{

    try {
        drives.value = await getAllDrives();
    } catch(err) {
        console.error("Failed to fetch drives", err);
    }

    try {
        studentProfile.value = await getProfile();
    } catch(err) {
        console.log("No student profile found yet");
    }

});

const getEligibilityStatus = (drive) => {
    if (!studentProfile.value) {
        return { isEligible: true, reason: "" };
    }
    const s = studentProfile.value;

    // 1. Branch check
    if (drive.eligible_branch && drive.eligible_branch.toLowerCase() !== "all branches" && drive.eligible_branch.toLowerCase() !== "all") {
        if (!s.branch || s.branch.trim().toLowerCase() !== drive.eligible_branch.trim().toLowerCase()) {
            return { isEligible: false, reason: `Required Branch: ${drive.eligible_branch}` };
        }
    }

    // 2. CGPA check
    if (drive.min_cgpa !== null && drive.min_cgpa !== undefined) {
        if (s.cgpa === null || s.cgpa === undefined || s.cgpa < drive.min_cgpa) {
            return { isEligible: false, reason: `Min CGPA: ${drive.min_cgpa}` };
        }
    }

    // 3. Graduation year check
    if (drive.eligible_graduation_year) {
        if (!s.graduation_year || s.graduation_year !== drive.eligible_graduation_year) {
            return { isEligible: false, reason: `Only for ${drive.eligible_graduation_year} batch` };
        }
    }

    // 4. Deadline check
    if (drive.application_deadline) {
        const todayStr = new Date().toISOString().split("T")[0];
        if (todayStr > drive.application_deadline) {
            return { isEligible: false, reason: "Deadline passed" };
        }
    }

    return { isEligible: true, reason: "" };
};

const filteredDrives = computed(()=>{

    return drives.value.filter(drive=>{

        return (

            drive.title
            .toLowerCase()
            .includes(search.value.toLowerCase())

            ||

            drive.company_name
            .toLowerCase()
            .includes(search.value.toLowerCase())

        );

    });

});

const apply = async(jobId)=>{

    try{

        const response = await applyDrive(jobId);

        alert(response.message);

    }

    catch(error){

        alert(
            error.response?.data?.message || error.message
        );

    }

};

</script>