<template>
  <div class="edit-profile-container">
    <h3>Edit Profile:</h3>
    <form @submit.prevent="saveChanges">
      <div class="form-group">
        <label for="username">Username:</label>
        <input v-model="editedUser.username" type="text" id="username" required>
      </div>

      <div class="form-group">
        <label for="email">Email:</label>
        <input v-model="editedUser.email" type="email" id="email" required>
      </div>

      <div class="form-group">
        <label for="dateOfBirth">Date of Birth:</label>
        <input v-model="editedUser.date_of_birth" type="date" id="dateOfBirth" required>
      </div>

      <div class="form-group">
        <label for="profilePhoto">Profile Photo:</label>
        <input type="file" @change="handleFileChange" accept="image/*" id="profilePhoto">
      </div>

      <button type="submit" class="save-button">Save Changes</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useProfileStore } from '../store/store';

interface EditedUser {
  username: string;
  email: string;
  date_of_birth: string;
  profile_image: File | null;
}

export default defineComponent({
  setup() {
    const editedUser = ref<EditedUser>({
      username: '',
      email: '',
      date_of_birth: '',
      profile_image: null,
    });

    const saveChanges = async () => {
      try {
        const formData = new FormData();
        formData.append('username', editedUser.value.username);
        formData.append('email', editedUser.value.email);
        formData.append('date_of_birth', editedUser.value.date_of_birth);
        formData.append('profile_image', editedUser.value.profile_image || '');

        const profileStore = useProfileStore();

        // Make a POST request to save changes
        const response = await fetch('http://localhost:8000/update-profile/', {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${profileStore.userAccessToken}`,
          },
          body: formData,
        });

        if (response.ok) {
          // Handle success, e.g., show a success message
          console.log('Profile updated successfully');
        } else {
          console.error('Failed to update profile:', response.statusText);
        }
      } catch (error) {
        console.error('Update profile error:', error);
      }
    };

    const handleFileChange = (event: Event) => {
      const target = event.target as HTMLInputElement;
      // Set the selected file in the editedUser object
      editedUser.value.profile_image = target.files?.[0] || null;
    };

    return {
      editedUser,
      saveChanges,
      handleFileChange,
    };
  },
});
</script>

<style scoped>
.edit-profile-container {
  max-width: 400px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  margin-bottom: 10px;
}

.save-button {
  background-color: #3498db;
  color: #fff;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.save-button:hover {
  background-color: #2980b9;
}
</style>
