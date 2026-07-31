<template>

<div class="container">

    <h2 class="mb-4">
        My Placement Drives
    </h2>

    <DriveCard
        v-for="drive in drives"
        :key="drive.id"
        :drive="drive"
    />

</div>

</template>

<script setup>
import { ref, onMounted } from "vue";

import { getMyDrives } from "../../services/companyService";

import DriveCard from "../../components/DriveCard.vue";

const drives = ref([]);

onMounted(async () => {

    try {

        drives.value = await getMyDrives();

    }

    catch (error) {

        console.log(error);

    }

});
</script>