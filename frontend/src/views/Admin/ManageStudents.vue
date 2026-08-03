<template>
  <div class="container">

    <h2 class="mb-4">
      Students
    </h2>

    <!-- Search Bar -->
    <div class="row mb-4">

      <div class="col-md-4">

        <input
          v-model="query"
          @input="search"
          class="form-control"
          placeholder="Search Students..."
        />

      </div>

      <div class="col-auto">

        <button
          class="btn btn-primary"
          @click="search"
        >
          Search
        </button>

      </div>

      <div class="col-auto">

        <button
          class="btn btn-secondary"
          @click="loadStudents"
        >
          Reset
        </button>

      </div>

    </div>

    <!-- No Students -->
    <div
      v-if="students.length === 0"
      class="alert alert-info"
    >
      No students found.
    </div>

    <!-- Students Table -->
    <table
      v-if="students.length > 0"
      class="table table-bordered table-hover align-middle"
    >

      <thead class="table-dark">

        <tr>
          <th>Name</th>
          <th>Education</th>
          <th>Skills</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>

      </thead>

      <tbody>

        <tr
          v-for="student in students"
          :key="student.id"
        >

          <td>{{ student.full_name }}</td>

          <td>{{ student.education }}</td>

          <td>{{ student.skills }}</td>

          <td>

            <span
              class="badge"
              :class="student.is_active ? 'bg-success' : 'bg-secondary'"
            >
              {{ student.is_active ? "Active" : "Inactive" }}
            </span>

          </td>

          <td>

            <button
              v-if="student.is_active"
              class="btn btn-danger"
              @click="deactivate(student.id)"
            >
              Deactivate
            </button>

            <button
              v-else
              class="btn btn-success"
              @click="activate(student.id)"
            >
              Activate
            </button>

          </td>

        </tr>

      </tbody>

    </table>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

import {
  getStudents,
  deactivateStudent,
  activateStudent,
  searchStudents
} from "../../services/adminService";

const students = ref([]);
const query = ref("");

const loadStudents = async () => {

  students.value = await getStudents();

};

onMounted(loadStudents);

const deactivate = async (id) => {

  if (!confirm("Deactivate this student?"))
    return;

  await deactivateStudent(id);

  loadStudents();

};

const activate = async (id) => {

  if (!confirm("Activate this student?"))
    return;

  await activateStudent(id);

  loadStudents();

};

const search = async () => {

  if (!query.value.trim()) {

    loadStudents();
    return;

  }

  students.value = await searchStudents(query.value);

};
</script>