<template>
  <div>
    <h2>Login Page</h2>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useProfileStore } from '../store/store';
import { useRouter } from 'vue-router';


const profileStore = useProfileStore();
const data = ref(null);
const router = useRouter();


onMounted(async () => {
  try {
    // Extract user details from the current URL fragment
    const hashFragment = window.location.hash.substr(1);
    const userObject = JSON.parse(decodeURIComponent(hashFragment));

    // Save all user details to Pinia store
    profileStore.setAllUserDetails(userObject);

    // Fetch data using the access_token
    const accessToken = userObject.access_token;

    const response = await fetch('http://localhost:8000/user-info/', {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
    });

    if (response.ok) {
      const responseData = await response.json();
      data.value = responseData;

      profileStore.setFetchedData(responseData);
      profileStore.allUserDetails;
      localStorage.setItem('fetchedData', JSON.stringify(responseData));

      router.push('/');

    } else {
      // Handle request failure
      console.error('Failed to fetch data');
    }
  } catch (error) {
    console.error('Login error:', error);
  }
});
</script>
