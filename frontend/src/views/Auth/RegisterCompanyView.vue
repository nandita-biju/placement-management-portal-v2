<template>
  <div class="container vh-100 d-flex justify-content-center align-items-center">

    <div class="card shadow p-4" style="width:450px;">

      <h2 class="text-center mb-4">
        Company Registration
      </h2>

      <form @submit.prevent="registerCompany">

        <div class="mb-3">
          <label class="form-label">Email</label>

          <input
            v-model="email"
            type="email"
            class="form-control"
            placeholder="Enter Email"
            required
          >
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>

          <input
            v-model="password"
            type="password"
            class="form-control"
            placeholder="Enter Password"
            required
          >
        </div>

        <button
          class="btn btn-primary w-100"
        >
          Register
        </button>

      </form>

      <hr>

      <div class="text-center">

        Already have an account?

        <router-link to="/">
          Login
        </router-link>

      </div>

    </div>

  </div>
</template>

<script setup>

import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../../api/axios";

const router = useRouter();

const email = ref("");
const password = ref("");

const registerCompany = async () => {

    try{

        await api.post(
            "/auth/register/company",
            {
                email: email.value,
                password: password.value
            }
        );

        alert("Company registered successfully!");

        router.push("/");

    }

    catch(error){

        if(error.response){
            alert(error.response.data.message);
        }

        else{
            alert("Unable to connect to server.");
        }

    }

};

</script>