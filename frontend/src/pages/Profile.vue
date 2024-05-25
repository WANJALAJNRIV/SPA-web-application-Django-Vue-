<template>
  <div class="profile-container">
    <div class="profile-header">
      <div class="h3">{{ title }}</div>
      <router-link class="edit-profile-link" :to="{ name: 'EditProfile' }">Edit Profile</router-link>
    </div>

    

    <!-- Display user details -->
    <div class="profile-section" v-if="userDetails">
      <h3>User Details:</h3>
      <ul>
        <li>
          <strong>
            <img :src="'http://localhost:8000' + userDetails.profile_image" alt="Profile photo" />
            <p>Profile photo</p>
          </strong>
        </li>
        <li><strong>Username:</strong> {{ userDetails.username }}</li>
        <li><strong>Email:</strong> {{ userDetails.email }}</li>
        <li><strong>Date of Birth:</strong> {{ userDetails.date_of_birth }}</li>
      </ul>
    </div>

      <!-- Display favorite categories with delete buttons -->
  <div class="profile-section" v-if="userDetails && favoriteCategories.length > 0">
    <h3>Favorite Categories:</h3>
    <ul>
      <li v-for="categoryItem in favoriteCategories" :key="categoryItem.id">
        {{ categoryItem.category.name }}
        <button @click="deleteCategory(categoryItem.category.id)">Delete</button>
      </li>
    </ul>
  </div>


    <!-- Choose from existing categories section -->
    <div class="profile-section">
      <h3>Choose from Existing Categories:</h3>
      <select v-model="selectedCategory">
        <option v-for="category in allCategories" :key="category.id" :value="category.id">
          {{ category.name }}
        </option>
      </select>
      <button @click="addCategory">Add</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useProfileStore } from '../store/store';

interface UserDetails {
  profile_image: string;
  username: string;
  email: string;
  date_of_birth: string;
}

interface Category {
  id: number;
  name: string;
}

interface CategoryItem {
  id: number;
  category: {
    id: number;
    name: string;
  };
  added_at: string;
}

const profileStore = useProfileStore();
const userDetails = ref<UserDetails | null>(null);
const favoriteCategories = ref<CategoryItem[]>([]);
const allCategories = ref<Category[]>([]);
const selectedCategory = ref<number | null>(null);
const title = 'Profile';

const fetchData = async () => {
  try {
    let accessToken = profileStore.userAccessToken;

    const response = await fetch('http://localhost:8000/user-info/', {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (response.ok) {
      const data = await response.json();
      userDetails.value = data;
    } else {
      console.error('Failed to fetch user details:', response.statusText);
    }
  } catch (error) {
    console.error('Fetch error:', error);
  }

  try {
    let accessToken = profileStore.userAccessToken;

    // Fetch favorite categories
    const categoriesResponse = await fetch('http://localhost:8000/user_favorite_categories/', {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (categoriesResponse.ok) {
      const categoriesData = await categoriesResponse.json();
      favoriteCategories.value = categoriesData;
    } else {
      console.error('Failed to fetch favorite categories:', categoriesResponse.statusText);
    }

    // Fetch all available categories
    const allCategoriesResponse = await fetch('http://localhost:8000/categories/', {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (allCategoriesResponse.ok) {
      const allCategoriesData = await allCategoriesResponse.json();
      allCategories.value = allCategoriesData;
    } else {
      console.error('Failed to fetch all categories:', allCategoriesResponse.statusText);
    }
  } catch (error) {
    console.error('Fetch error:', error);
  }
};

const addCategory = async () => {
  try {
    if (selectedCategory.value !== null) {
      let accessToken = profileStore.userAccessToken;

      const response = await fetch('http://localhost:8000/user_favorite_categories/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ category_id: selectedCategory.value }),
      });

      if (response.ok) {
        // Fetch updated favorite categories
        await fetchData();
        selectedCategory.value = null; // Clear selected category after successful addition
      } else {
        console.error('Failed to add category:', response.statusText);
      }
    }
  } catch (error) {
    console.error('Fetch error:', error);
  }
};

const deleteCategory = async (categoryId: number) => {
  try {
    let accessToken = profileStore.userAccessToken;

    const response = await fetch(`http://localhost:8000/user_favorite_categories/${categoryId}/`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (response.ok) {
      // Fetch updated favorite categories
      await fetchData();
    } else {
      console.error('Failed to delete category:', response.statusText);
    }
  } catch (error) {
    console.error('Fetch error:', error);
  }
};

fetchData(); // Directly fetch data without onMounted
</script>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.h3 {
  color: #3498db;
}

.edit-profile-link {
  text-decoration: none;
  color: #27ae60;
  font-weight: bold;
}

.profile-section {
  margin-bottom: 20px;
  background-color: #fff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
  color: #333;
}

strong {
  display: flex;
  align-items: center;
  color: #333;
}

img {
  width: 50px;
  height: 50px;
  margin-right: 10px;
  border-radius: 50%;
}

pre {
  white-space: pre-wrap;
  background-color: #ecf0f1;
  padding: 10px;
  border-radius: 5px;
}
</style>
