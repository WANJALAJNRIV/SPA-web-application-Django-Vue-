<template>
  <div class="article-detail-container">
    <router-link :to="{ name: 'Home' }" class="back-link">&larr; Back to Home</router-link>
    <div v-if="article">
      <span v-if="categoryName" class="category-badge">{{ categoryName }}</span>
      <h1 class="article-title">{{ article.title }}</h1>
      <p class="article-meta">Published {{ formattedDate }}</p>
      <p class="article-content">{{ article.content }}</p>
    </div>
    <p v-else>Loading...</p>
    <div class="comment-section">
      <CommentSection />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import CommentSection from '../components/CommentSection.vue';
import { useProfileStore } from '../store/store';

interface Article {
  title: string;
  content: string;
  category: number;
  created_at: string;
}

interface Category {
  id: number;
  name: string;
}

export default defineComponent({
  data() {
    return {
      article: null as Article | null,
      categories: [] as Category[],
    };
  },

  computed: {
    categoryName(): string {
      if (!this.article) return '';
      const match = this.categories.find((c) => c.id === this.article!.category);
      return match ? match.name : '';
    },
    formattedDate(): string {
      if (!this.article?.created_at) return '';
      return new Date(this.article.created_at).toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    },
  },

  mounted() {
    const profileStore = useProfileStore();
    const accessToken = profileStore.userAccessToken;
    const specificKey = this.$route.params.id;

    fetch(`http://localhost:8000/api/articles/${specificKey}`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data: Article) => {
        this.article = data;
      })
      .catch((error) => {
        console.error('Error fetching article details:', error);
      });

    fetch('http://localhost:8000/categories/', {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then((response) => (response.ok ? response.json() : []))
      .then((data: Category[]) => {
        this.categories = data;
      })
      .catch((error) => {
        console.error('Error fetching categories:', error);
      });
  },

  components: {
    CommentSection,
  },
});
</script>

<style scoped>
.article-detail-container {
  max-width: 720px;
  margin: 0 auto;
  padding: 20px;
}

.back-link {
  display: inline-block;
  margin-bottom: 16px;
  color: var(--color-accent, #a3241d);
  text-decoration: none;
  font-size: 0.9rem;
}

.back-link:hover {
  text-decoration: underline;
}

.article-title {
  font-size: 2rem;
  line-height: 1.25;
  color: var(--color-ink, #1a1a1a);
  margin: 10px 0 6px;
}

.article-meta {
  color: var(--color-muted, #6c757d);
  font-size: 0.85rem;
  margin-bottom: 24px;
}

.article-content {
  font-size: 1.05rem;
  line-height: 1.75;
  color: #2c2c2c;
  white-space: pre-line;
  margin-bottom: 20px;
}

.comment-section {
  margin-top: 40px;
  border-top: 1px solid var(--color-border, #e5e2dc);
  padding-top: 24px;
}
</style>
