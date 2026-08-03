<template>
  <div class="container">

    <h2 class="mb-4">
      Companies
    </h2>

    <div
      v-if="companies.length === 0"
      class="alert alert-info"
    >
      No companies found.
    </div>

    <table
      v-else
      class="table table-bordered table-hover align-middle"
    >

      <thead class="table-dark">

        <tr>
          <th>Company</th>
          <th>Industry</th>
          <th>Location</th>
          <th>Approval</th>
          <th>Status</th>
          <th width="320">
            Actions
          </th>
        </tr>

      </thead>

      <tbody>

        <tr
          v-for="company in companies"
          :key="company.id"
        >

          <td>{{ company.company_name }}</td>

          <td>{{ company.industry }}</td>

          <td>{{ company.location }}</td>

          <td>

            <span
              class="badge"
              :class="approvalBadge(company.approval_status)"
            >
              {{ company.approval_status }}
            </span>

          </td>

          <td>

            <span
              class="badge"
              :class="statusBadge(company.status)"
            >
              {{ company.status }}
            </span>

          </td>

          <td>

            <!-- Pending Companies -->
            <template v-if="company.approval_status === 'pending'">

                <button
                    class="btn btn-success btn-sm me-2"
                    @click="approve(company.id)"
                >
                    Approve
                </button>

                <button
                    class="btn btn-danger btn-sm"
                    @click="reject(company.id)"
                >
                    Reject
                </button>

            </template>


            <!-- Approved Companies -->
            <template v-else-if="company.approval_status === 'approved'">

                <!-- Active -->
                <template v-if="company.status === 'active'">

                    <button
                        class="btn btn-warning btn-sm me-2"
                        @click="blacklist(company.id)"
                    >
                        Blacklist
                    </button>

                    <button
                        class="btn btn-secondary btn-sm"
                        @click="deactivate(company.id)"
                    >
                        Deactivate
                    </button>

                </template>


                <!-- Deactivated -->
                <template v-else-if="company.status === 'deactivated'">

                    <button
                        class="btn btn-primary btn-sm"
                        @click="activate(company.id)"
                    >
                        Activate
                    </button>

                </template>


                <!-- Blacklisted -->
                <template v-else-if="company.status === 'blacklisted'">

                    <button
                        class="btn btn-success btn-sm"
                        @click="unblacklist(company.id)"
                    >
                        Unblacklist
                    </button>

                </template>

            </template>


            <!-- Rejected -->
            <template v-else>

                <button
                    class="btn btn-success btn-sm"
                    @click="approve(company.id)"
                >
                    Approve
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

import {
    getCompanies,
    approveCompany,
    rejectCompany,
    activateCompany,
    deactivateCompany,
    blacklistCompany,
    unblacklistCompany
} from "../../services/adminService";

const companies = ref([]);

const loadCompanies = async () => {

    companies.value = await getCompanies();

};

onMounted(loadCompanies);

const approve = async (id) => {

    await approveCompany(id);

    loadCompanies();

};

const reject = async (id) => {

    await rejectCompany(id);

    loadCompanies();

};

const activate = async (id) => {

    await activateCompany(id);

    loadCompanies();

};

const deactivate = async (id) => {

    await deactivateCompany(id);

    loadCompanies();

};

const blacklist = async (id) => {

    await blacklistCompany(id);

    loadCompanies();

};

const unblacklist = async (id) => {

    await unblacklistCompany(id);

    loadCompanies();

};

const approvalBadge = (status) => {

    if(status==="approved")
        return "bg-success";

    if(status==="rejected")
        return "bg-danger";

    return "bg-warning text-dark";

};

const statusBadge = (status) => {

    if(status==="active")
        return "bg-success";

    if(status==="blacklisted")
        return "bg-dark";

    if(status==="deactivated")
        return "bg-secondary";

    return "bg-warning text-dark";

};
</script>