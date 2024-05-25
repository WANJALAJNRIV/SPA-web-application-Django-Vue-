<template>
  <div class="article-detail-container">
    <h2 v-if="article" class="article-title">{{ article.title }}</h2>
    <p v-if="article" class="article-content">{{ article.content }}</p>
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
}

export default defineComponent({
  data() {
    return {
      article: null as Article | null,
    };
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
  },

  components: {
    CommentSection,
  },
});
</script>

<style scoped>
.article-detail-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.article-title {
  font-size: 28px;
  color: #3498db;
  margin-bottom: 15px;
}

.article-content {
  font-size: 16px;
  line-height: 1.6;
  color: #333;
  margin-bottom: 20px;
}

.comment-section {
  margin-top: 30px;
}
</style>
