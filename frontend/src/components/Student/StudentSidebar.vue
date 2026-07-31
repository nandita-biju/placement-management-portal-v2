<template>

<div
class="bg-dark text-white p-3"
style="width:280px; min-height:100vh;"
>

<h2 class="mb-5">
Placement Portal
</h2>

<ul class="nav flex-column">

<li class="nav-item mb-3">
<router-link
to="/student/dashboard"
class="nav-link text-white"
>
Dashboard
</router-link>
</li>

<li class="nav-item mb-3">
<router-link
to="/student/profile"
class="nav-link text-white"
>
My Profile
</router-link>
</li>

<li class="nav-item mb-3">
<router-link
to="/student/profile/edit"
class="nav-link text-white"
>
Edit Profile
</router-link>
</li>

<li class="nav-item mb-3">
<router-link
to="/student/drives"
class="nav-link text-white"
>
Browse Drives
</router-link>
</li>

<li class="nav-item mb-3">
<router-link
to="/student/applications"
class="nav-link text-white"
>
My Applications
</router-link>
</li>

</ul>

</div>

</template>