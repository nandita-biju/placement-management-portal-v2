<template>
  <div class="container vh-100 d-flex justify-content-center align-items-center">
    <div class="card shadow p-4" style="width: 400px;">
      <h2 class="text-center mb-4">Placement Portal</h2>

      <form @submit.prevent="login">

        <div class="mb-3">
          <label class="form-label">Email</label>
          <input
            v-model="email"
            type="email"
            class="form-control"
            placeholder="Enter email"
            required
          >
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>
          <input
            v-model="password"
            type="password"
            class="form-control"
            placeholder="Enter password"
            required
          >
        </div>

        <button class="btn btn-primary w-100">
          Login
        </button>

      </form>

      <hr>

      <div class="text-center">
        <router-link to="/register/student">
          Register as Student
        </router-link>

        <br>

        <router-link to="/register/company">
          Register as Company
        </router-link>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { login as loginUser } from "../../services/authServices";

const router = useRouter();

const email = ref("");
const password = ref("");

const login = async () => {

    try {

        const response = await loginUser(
            email.value,
            password.value
        );

        localStorage.setItem(
            "token",
            response.token
        );

        localStorage.setItem(
            "role",
            response.role
        );

        if(response.role === "student"){
            router.push("/student/dashboard");
        }

        else if(response.role === "company"){
            router.push("/company/dashboard");
        }

        else{
            router.push("/admin/dashboard");
        }

    }

    catch(error){

        alert(
            error.response.data.message
        );

    }

};
</script>