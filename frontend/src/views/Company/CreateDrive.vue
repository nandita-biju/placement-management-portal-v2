<template>

<div class="container">

<div class="card shadow">

<div class="card-header">
<h3>Create Placement Drive</h3>
</div>

<div class="card-body">

<form @submit.prevent="createDrive">

<div class="mb-3">
<label class="form-label">Job Title</label>
<input
v-model="job.title"
class="form-control"
required
>
</div>

<div class="mb-3">
<label class="form-label">Description</label>
<textarea
v-model="job.description"
rows="4"
class="form-control"
></textarea>
</div>

<div class="mb-3">
<label class="form-label">Salary</label>
<input
v-model="job.salary"
class="form-control"
>
</div>

<div class="mb-3">
<label class="form-label">Skills Required</label>
<textarea
v-model="job.skills_required"
rows="3"
class="form-control"
></textarea>
</div>

<button
class="btn btn-primary"
type="submit"
>
Create Drive
</button>

</form>

</div>

</div>

</div>

</template>

<script setup>

import { ref } from "vue";
import { useRouter } from "vue-router";
import { createJob } from "../../services/jobService";

const router = useRouter();

const job = ref({

title: "",
description: "",
salary: "",
skills_required: ""

});

const createDrive = async ()=>{

try{

const response = await createJob(job.value);

alert(response.message);

router.push("/company/drives");

}

catch(error){

alert(
error.response?.data?.message || error.message
);

}

};

</script>