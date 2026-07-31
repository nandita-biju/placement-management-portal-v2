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

            <button
                class="btn btn-success"
                @click="apply(drive.id)"
            >
                Apply
            </button>

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

const drives = ref([]);

const search = ref("");

onMounted(async ()=>{

    drives.value = await getAllDrives();

});

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
            error.response.data.message
        );

    }

};

</script>