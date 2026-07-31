<template>
<div
class="bg-dark text-white d-flex flex-column p-4"
style="width:280px; min-height:100vh;"
>

<div>

<h2 class="mb-5">
Placement Portal
</h2>

<ul class="nav flex-column">

<li class="nav-item mb-3">
<router-link to="/company/dashboard" class="nav-link text-white">
Dashboard
</router-link>
</li>

<li class="nav-item mb-3">
<router-link to="/company/profile" class="nav-link text-white">
Company Profile
</router-link>
</li>

<li class="nav-item mb-3">
<router-link to="/company/create-drive" class="nav-link text-white">
Create Drive
</router-link>
</li>

<li class="nav-item mb-3">
<router-link to="/company/drives" class="nav-link text-white">
My Drives
</router-link>
</li>

<li class="nav-item mb-3">
<router-link to="/company/applicants" class="nav-link text-white">
Applicants
</router-link>
</li>

</ul>

</div>

<div class="mt-auto">

<button
class="btn btn-outline-danger w-100"
@click="logout"
>
Logout
</button>

</div>

</div>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const logout = () => {
    localStorage.clear();
    router.push("/");
};
</script>