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

<div class="mb-3">
<label class="form-label">Eligible Branch <span class="text-danger">*</span></label>
<select
v-model="job.eligible_branch"
class="form-select"
required
>
<option value="" disabled>Select Eligible Branch</option>
<option value="All Branches">All Branches</option>
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
<label class="form-label">Minimum CGPA <span class="text-danger">*</span></label>
<input
v-model.number="job.min_cgpa"
type="number"
step="0.1"
min="0"
max="10"
class="form-control"
placeholder="e.g. 7.5"
required
>
</div>

<div class="mb-3">
<label class="form-label">Eligible Graduation Year <span class="text-danger">*</span></label>
<select
v-model.number="job.eligible_graduation_year"
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
<label class="form-label">Application Deadline <span class="text-danger">*</span></label>
<input
v-model="job.application_deadline"
type="date"
class="form-control"
required
>
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
skills_required: "",
eligible_branch: "",
min_cgpa: "",
eligible_graduation_year: "",
application_deadline: ""

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