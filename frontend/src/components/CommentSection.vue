<template>
  <div class="comment-section">
    <h2 class="section-title">Comments</h2>
    <div class="comments-container">
      <comment-list :comments="commentsData" @comment-added="handleCommentAdded" @comment-deleted="handleCommentDeleted" @comment-updated="handleCommentUpdated" />
      <comment-form @comment-added="handleCommentAdded" />
    </div>
  </div>
</template>

<script lang="ts">
import CommentList from './CommentList.vue';
import CommentForm from './CommentForm.vue';
import { useProfileStore } from '../store/store';

export default {
  components: {
    CommentList,
    CommentForm,
  },
  data() {
    return {
      commentsData: [],
    };
  },
  methods: {
    async fetchComments() {
      try {
        const profileStore = useProfileStore();
        const accessToken = profileStore.userAccessToken;
        const articleId = this.$route.params.id;

        const response = await fetch(`http://localhost:8000/api/comment_list/${articleId}/`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch comments. Status: ${response.status}`);
        }

        const data = await response.json();
        this.commentsData = data;
          console.log(data);
      } catch (error) {
        console.error('Error fetching comments:', error);
      }
    },

    handleCommentAdded() {
      // Call fetchComments when a new comment is added
      this.fetchComments();
    },
    handleCommentDeleted() {
      // Call fetchComments when a comment is deleted
      this.fetchComments();
    },
    handleCommentUpdated() {
      // Call fetchComments when a comment is updated
      this.fetchComments();
    },
  },
  mounted() {
    // Call fetchComments when the component is mounted
    this.fetchComments();
  },
};
</script>

<style scoped>
.comment-section {
  margin-top: 20px;
}

.section-title {
  font-size: 24px;
  margin-bottom: 15px;
  color: #333;
}

.comments-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
