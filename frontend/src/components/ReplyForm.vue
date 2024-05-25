<template>
  <div class="reply-area">
    <textarea v-model="replyText" placeholder="Type your reply..."></textarea>
    <button @click="saveReply" :disabled="replyText.trim() === ''">Save Reply</button>
  </div>
</template>

<script lang="ts" >
import { useProfileStore } from '../store/store';


export default {
  props: ['commentId'],
  data() {
    return {
      replyText: '',
    };
  },
  methods: {
    saveReply() {
      const profileStore = useProfileStore();
      const accessToken = profileStore.userAccessToken;

      const requestData = {
        text: this.replyText,
        user: profileStore.getFetchedData.id,
        comment: this.commentId,
      };

      fetch(`http://localhost:8000/api/reply/create/${this.commentId}/`, {
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
          this.$emit('reply-added');
        })
        .catch(error => {
          console.error('Error:', error);
        });
    },
  },
};
</script>

<style scoped>
.reply-area {
  margin-top: 10px;
}

.reply-area textarea {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
}

.reply-area button {
  padding: 8px 16px;
  background-color: #4caf50; /* Green */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.reply-area button:disabled {
  background-color: #b0b0b0; /* Gray */
  cursor: not-allowed;
}

.reply-area button:hover:disabled {
  background-color: #b0b0b0; /* Gray */
}
</style>
