<template>
  <div>
    <h2>Your Favorite Articles</h2>
    <ul class="favorite-categories-list">
      <li v-for="category in userFavoriteCategories" :key="category.categoryId">
        <div class="category-ribbon">
          <span class="category-name">{{ category.categoryName }}</span>
        </div>
        <ul class="article-list">
          <router-link
            v-for="article in category.articles"
            :key="article.id"
            :to="{ name: 'article-detail', params: { id: article.id } }"
            class="article-link"
          >
            <li class="article-item">{{ article.title }}</li>
          </router-link>
        </ul>
      </li>
    </ul>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useProfileStore } from '../store/store';

interface Category {
  categoryId: number;
  categoryName: string;
  articles: Article[];
}

interface Article {
  id: number;
  title: string;
}

const userFavoriteCategories = ref<Category[]>([]);

const fetchUserFavoriteCategories = async () => {
  try {
    const profileStore = useProfileStore();
    const accessToken = profileStore.userAccessToken;

    const response = await fetch('http://localhost:8000/user_favorite_categories_with_articles', {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch user favorite categories: ${response.statusText}`);
    }

    const data = await response.json();
    userFavoriteCategories.value = data.groupedArticles;
  } catch (error) {
    console.error('Fetch user favorite categories error:', error);
  }
};

onMounted(() => {
  fetchUserFavoriteCategories();
});
</script>




<style scoped>
.favorite-categories-list {
  list-style-type: none;
  padding: 0;
}

.category-ribbon {
    background-color: #ecf0f1; /* Light gray background for articles */
  padding: 8px;
  margin-bottom: 5px;
  border-radius: 5px;
}

.category-name {
  font-weight: bold;
}

.article-list {
  list-style-type: none;
  padding: 0;
}

.article-item {
  
  background-color: #3498db; /* Blue color */
  color: #fff; /* White text */
  padding: 8px 15px;
  margin-bottom: 5px;
  display: inline-block;
  border-radius: 5px;
  margin: 10px;

}
</style>
