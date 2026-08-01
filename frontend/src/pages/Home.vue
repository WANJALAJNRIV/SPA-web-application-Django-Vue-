<template>
  <div>
    <div class="masthead">
      <p class="dateline">{{ today }} &middot; Your daily briefing</p>
    </div>

    <section v-if="userFavoriteCategories.length > 0" class="favorites-section">
      <h2>For You</h2>
      <p class="section-subtitle">Based on the categories you follow.</p>
      <div class="category-block" v-for="category in userFavoriteCategories" :key="category.categoryId">
        <span class="category-badge">{{ category.categoryName }}</span>
        <div class="article-cards">
          <router-link
            v-for="article in category.articles"
            :key="article.id"
            :to="{ name: 'article-detail', params: { id: article.id } }"
            class="article-card"
          >
            <h3>{{ article.title }}</h3>
            <p>{{ excerpt(article.content) }}</p>
          </router-link>
        </div>
      </div>
    </section>

    <section>
      <h2>Latest Articles</h2>
      <p v-if="!allCategories.length && !allArticles.length" class="empty-state">Loading articles…</p>
      <div v-for="category in allCategories" :key="category.id">
        <div class="category-block" v-if="articlesForCategory(category.id).length">
          <span class="category-badge">{{ category.name }}</span>
          <div class="article-cards">
            <router-link
              v-for="article in articlesForCategory(category.id)"
              :key="article.id"
              :to="{ name: 'article-detail', params: { id: article.id } }"
              class="article-card"
            >
              <h3>{{ article.title }}</h3>
              <p>{{ excerpt(article.content) }}</p>
            </router-link>
          </div>
        </div>
      </div>
    </section>
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
  content: string;
  category: number;
}

interface AllCategory {
  id: number;
  name: string;
}

const userFavoriteCategories = ref<Category[]>([]);
const allArticles = ref<Article[]>([]);
const allCategories = ref<AllCategory[]>([]);

const today = new Date().toLocaleDateString(undefined, {
  weekday: 'long',
  year: 'numeric',
  month: 'long',
  day: 'numeric',
});

const excerpt = (content: string) => {
  if (!content) return '';
  return content.length > 140 ? content.slice(0, 140).trim() + '…' : content;
};

const articlesForCategory = (categoryId: number) =>
  allArticles.value.filter((article) => article.category === categoryId);

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

const fetchAllArticles = async () => {
  try {
    const profileStore = useProfileStore();
    const accessToken = profileStore.userAccessToken;

    const [articlesResponse, categoriesResponse] = await Promise.all([
      fetch('http://localhost:8000/api/articles/', {
        headers: { Authorization: `Bearer ${accessToken}` },
      }),
      fetch('http://localhost:8000/categories/', {
        headers: { Authorization: `Bearer ${accessToken}` },
      }),
    ]);

    if (articlesResponse.ok) {
      allArticles.value = await articlesResponse.json();
    }
    if (categoriesResponse.ok) {
      allCategories.value = await categoriesResponse.json();
    }
  } catch (error) {
    console.error('Fetch all articles error:', error);
  }
};

onMounted(() => {
  fetchUserFavoriteCategories();
  fetchAllArticles();
});
</script>


<style scoped>
.masthead {
  border-bottom: 1px solid var(--color-border, #e5e2dc);
  padding-bottom: 12px;
  margin-bottom: 24px;
}

.dateline {
  margin: 0;
  color: var(--color-muted, #6c757d);
  font-size: 0.85rem;
  letter-spacing: 0.02em;
}

.section-subtitle {
  margin-top: -8px;
  margin-bottom: 16px;
  color: var(--color-muted, #6c757d);
  font-size: 0.9rem;
}

.favorites-section {
  margin-bottom: 32px;
}

.empty-state {
  color: var(--color-muted, #6c757d);
}

.category-block {
  margin-bottom: 28px;
}

.article-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
  margin-top: 12px;
}

.article-card {
  display: block;
  background: var(--color-surface, #fff);
  border: 1px solid var(--color-border, #e0e4e8);
  border-radius: 8px;
  padding: 16px 18px;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.article-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

.article-card h3 {
  margin: 0 0 8px;
  font-size: 1.05rem;
  line-height: 1.35;
  color: var(--color-ink, #1a1a1a);
}

.article-card p {
  margin: 0;
  font-size: 0.85rem;
  color: var(--color-muted, #6c757d);
  line-height: 1.5;
}
</style>
