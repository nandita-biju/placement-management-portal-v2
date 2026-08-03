<template>

<div class="d-flex">

    <AdminSidebar />

    <div class="flex-grow-1">

        <AdminNavbar />

        <div class="p-4">

            <router-view />

        </div>

    </div>

</div>

</template>

<script setup>
import AdminNavbar from "../components/Admin/AdminNavbar.vue";
import AdminSidebar from "../components/Admin/AdminSidebar.vue";
</script>