<template>
  <div class="container">
    
    <router-link
        to="/company/drives"
        class="btn btn-secondary mb-4"
    >
        ← Back to My Drives
    </router-link>

    <h2 class="mb-4">Applicants</h2>

    

    <div
      v-if="applicants.length === 0"
      class="alert alert-info"
    >
      No applications received yet.
    </div>

    <table
      v-else
      class="table table-bordered table-hover"
    >

      <thead class="table-dark text-center">
        <tr>
            <th>Name</th>
            <th>Resume</th>
            <th>Profile</th>
            <th>Status</th>
            <th>Actions</th>
        </tr>
    </thead>

      <tbody>

        <tr
            v-for="applicant in applicants"
            :key="applicant.application_id"
            class="align-middle"
        >

            <td>
                {{ applicant.student_name }}
            </td>

            <td class="text-center">

                <a
                    :href="applicant.resume_link"
                    target="_blank"
                >
                    View Resume
                </a>

            </td>

            <td class="text-center">

                <router-link
                    :to="`/company/student/${applicant.student_id}/${route.params.jobId}`"
                    class="btn btn-info btn-sm"
                >
                    View Profile
                </router-link>

            </td>

            <td class="text-center">

                <span
                    class="badge"
                    :class="getStatusBadge(applicant.status)"
                >
                    {{ applicant.status }}
                </span>

            </td>

            <td class="text-center">

                <!-- Applied -->
                <template v-if="applicant.status === 'Applied'">

                    <button
                        class="btn btn-primary btn-sm me-2"
                        @click="changeStatus(applicant.application_id, 'Shortlisted')"
                    >
                        Shortlist
                    </button>

                    <button
                        class="btn btn-danger btn-sm"
                        @click="changeStatus(applicant.application_id, 'Rejected')"
                    >
                        Reject
                    </button>

                </template>

                <!-- Shortlisted -->
                <template v-else-if="applicant.status === 'Shortlisted'">

                    <button
                        class="btn btn-success btn-sm me-2"
                        @click="changeStatus(applicant.application_id, 'Selected')"
                    >
                        Select
                    </button>

                    <button
                        class="btn btn-danger btn-sm"
                        @click="changeStatus(applicant.application_id, 'Rejected')"
                    >
                        Reject
                    </button>

                </template>

                <!-- Selected -->
                <template v-else-if="applicant.status === 'Selected'">

                    <button
                        class="btn btn-success btn-sm"
                        disabled
                    >
                        ✓ Selected
                    </button>

                </template>

                <!-- Rejected -->
                <template v-else-if="applicant.status === 'Rejected'">

                    <button
                        class="btn btn-danger btn-sm"
                        disabled
                    >
                        ✕ Rejected
                    </button>

                </template>

            </td>

        </tr>

      </tbody>

    </table>

  </div>
</template>

<script setup>
    import { ref, onMounted } from "vue";
    import { useRoute } from "vue-router";
    import {
        getApplicants,
        updateApplicationStatus
    } from "../../services/companyService";

    const route = useRoute();

    const applicants = ref([]);

    const loadApplicants = async () => {

        try {

            applicants.value = await getApplicants(
                route.params.jobId
            );

        }

        catch (error) {

            console.log(error);

        }

    };

    onMounted(() => {

        loadApplicants();

    });

    const changeStatus = async (applicationId, status) => {

        try {

            await updateApplicationStatus(
                applicationId,
                status
            );

            alert("Application status updated successfully!");

            await loadApplicants();

        }

        catch (error) {

            alert(
                error.response?.data?.message ||
                error.message
            );

        }

    };

    const getStatusBadge = (status) => {

        if (status === "Applied")
            return "bg-warning text-dark";

        if (status === "Shortlisted")
            return "bg-primary";

        if (status === "Selected")
            return "bg-success";

        if (status === "Rejected")
            return "bg-danger";

        return "bg-secondary";

    };
</script>