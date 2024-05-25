<template>
  <div>
    <hr class="divider" />
    <h3>Add a New Comment</h3>
    <hr class="divider" />
    <textarea v-model="commentText" class="comment-textarea" placeholder="Type your comment here..."></textarea>
    <button @click="saveComment" :disabled="commentText.trim() === ''" class="save-button">Save Comment</button>
    <br />
  </div>
</template>

<script  lang="ts">
import { useProfileStore } from '../store/store';

export default {
  data() {
    return {
      commentText: '',
      comments: [] as Comment[],

    };
  },
  methods: {
    saveComment() {
      const profileStore = useProfileStore();
      const accessToken = profileStore.userAccessToken;
      const articleId = this.$route.params.id;

      const requestData = {
        text: this.commentText,
        article: articleId,
        user: profileStore.getFetchedData.id,
      };

      fetch(`http://localhost:8000/api/comments/create/${articleId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify(requestData),
      })
        .then(response => response.json())
        .then(data => {
          console.log('Success:', data);
          this.comments.push(data);

          // Optionally, you can clear the commentText after successful submission
          this.commentText = '';
          this.$emit('comment-added');
        })
        .catch(error => {
          // Handle error, e.g., show an error message
          console.error('Error:', error);
        });
    },
  },
};
</script>

<style scoped>
.divider {
  border: 1px solid #ccc;
  margin: 10px 0;
}

.comment-textarea {
  width: 100%;
  height: 100px;
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.save-button {
  background-color: #4caf50;
  color: white;
  padding: 10px 15px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.save-button:disabled {
  background-color: #a0a0a0;
  cursor: not-allowed;
}
</style>
