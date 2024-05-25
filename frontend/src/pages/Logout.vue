<template>
    <div>
      <h1>Logging out...</h1>
    </div>
  </template>
  
  <script setup lang="ts">
  import { onMounted } from 'vue';
  import { useAuthStore } from '../store/store';
  import { useProfileStore } from '../store/store';
  
  const authStore = useAuthStore();
  const profileStore = useProfileStore();
  
  onMounted(() => {
    // Clear Pinia stores and local storage
    authStore.clearAccessToken();
    profileStore.clearProfileDetails();
    localStorage.clear();
    window.location.href = 'http://localhost:8000/logout/';
  });
  </script>
  