<template>
  <div class="profile-container">
    <div class="profile-header">
      <h1>{{ title }}</h1>
      <router-link class="edit-profile-link" :to="{ name: 'EditProfile' }">Edit Profile</router-link>
    </div>

    <!-- Display user details -->
    <div class="profile-section" v-if="userDetails">
      <div class="identity-row">
        <img
          v-if="!imageFailed"
          :src="'http://localhost:8000' + userDetails.profile_image"
          alt="Profile photo"
          class="avatar"
          @error="imageFailed = true"
        />
        <div v-else class="avatar avatar-fallback">{{ initials }}</div>
        <div>
          <p class="username">{{ userDetails.username }}</p>
          <p class="email">{{ userDetails.email }}</p>
        </div>
      </div>
      <dl class="details-list">
        <dt>Date of Birth</dt>
        <dd>{{ userDetails.date_of_birth || 'Not set' }}</dd>
      </dl>
    </div>

    <!-- Display favorite categories with delete buttons -->
    <div class="profile-section" v-if="userDetails && favoriteCategories.length > 0">
      <h2>Favorite Categories</h2>
      <ul class="category-list">
        <li v-for="categoryItem in favoriteCategories" :key="categoryItem.id">
          <span class="category-badge">{{ categoryItem.category.name }}</span>
          <button class="delete-button" @click="deleteCategory(categoryItem.category.id)">Remove</button>
        </li>
      </ul>
    </div>

    <!-- Choose from existing categories section -->
    <div class="profile-section">
      <h2>Add a Favorite Category</h2>
      <div class="add-category-row">
        <select v-model="selectedCategory">
          <option v-for="category in allCategories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>
        <button class="add-button" @click="addCategory">Add</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
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
const imageFailed = ref(false);
const title = 'Profile';

const initials = computed(() => {
  const username = userDetails.value?.username || '';
  return username.slice(0, 2).toUpperCase();
});

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
      imageFailed.value = false;
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
  max-width: 640px;
  margin: 0 auto;
  padding: 8px 20px 40px;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.profile-header h1 {
  margin: 0;
  font-size: 1.6rem;
  color: var(--color-ink, #1a1a1a);
}

.edit-profile-link {
  text-decoration: none;
  color: var(--color-accent, #a3241d);
  font-weight: 600;
  font-size: 0.9rem;
}

.edit-profile-link:hover {
  text-decoration: underline;
}

.profile-section {
  margin-bottom: 20px;
  background-color: var(--color-surface, #fff);
  padding: 20px;
  border-radius: 10px;
  border: 1px solid var(--color-border, #e5e2dc);
}

.profile-section h2 {
  margin: 0 0 14px;
  font-size: 1.1rem;
  color: var(--color-ink, #1a1a1a);
}

.identity-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
  border: 1px solid var(--color-border, #e5e2dc);
}

.avatar-fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-accent, #a3241d);
  color: #fff;
  font-family: var(--font-headline, Georgia, serif);
  font-weight: 700;
  font-size: 1.3rem;
}

.username {
  margin: 0 0 2px;
  font-weight: 600;
  font-size: 1.05rem;
  color: var(--color-ink, #1a1a1a);
}

.email {
  margin: 0;
  color: var(--color-muted, #6c757d);
  font-size: 0.9rem;
}

.details-list {
  margin: 0;
  padding-top: 12px;
  border-top: 1px solid var(--color-border, #e5e2dc);
}

.details-list dt {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--color-muted, #6c757d);
  margin-bottom: 2px;
}

.details-list dd {
  margin: 0;
  color: var(--color-ink, #1a1a1a);
}

.category-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.category-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.delete-button {
  background: none;
  border: 1px solid var(--color-border, #e5e2dc);
  color: var(--color-muted, #6c757d);
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8rem;
}

.delete-button:hover {
  border-color: var(--color-accent, #a3241d);
  color: var(--color-accent, #a3241d);
}

.add-category-row {
  display: flex;
  gap: 10px;
}

.add-category-row select {
  flex: 1;
  padding: 8px 10px;
  border: 1px solid var(--color-border, #e5e2dc);
  border-radius: 6px;
  background: var(--color-surface, #fff);
}

.add-button {
  background: var(--color-accent, #a3241d);
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.add-button:hover {
  background: var(--color-accent-dark, #7c1b16);
}
</style>
