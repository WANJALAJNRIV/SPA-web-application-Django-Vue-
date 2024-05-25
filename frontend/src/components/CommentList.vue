<template>
  <div class="comments">
    <div v-for="comment in comments" :key="comment.id" class="comment-container">
      <hr class="divider" />
      <div v-if="editingCommentId === comment.id" class="edit-comment">
        <input v-model="commentEditText" class="edit-input" />
        <div class="edit-buttons">
          <button @click="saveEditedComment(comment.id)" class="action-button primary">Save Comment</button>
          <button @click="cancelEdit(comment.id)" class="action-button secondary">Cancel</button>
        </div>
      </div>
      <div v-else class="comment-details">
        <p>{{ comment.text }}</p>
        <div class="comment-meta">
          <div v-if="isCurrentUserComment(comment.user)" class="comment-actions">
            <button @click="startEdit(comment.id)" class="action-button primary">Edit Comment</button>
            <button @click="deleteComment(comment.id)" class="action-button danger">Delete Comment</button>
          </div>
        </div>
      </div>
      <reply-form :commentId="comment.id" @reply-added="handleReplyAdded" />
      <div v-for="reply in comment.replies" :key="reply.id" class="reply-container">
        <div v-for="nestedReply in reply.replies" :key="nestedReply.id" class="nested-reply">
          {{ nestedReply.text }}
          <div v-if="isCurrentUserReply(nestedReply.user)" class="comment-actions">
            <button @click="startEditReply(comment.id, nestedReply.id)" class="action-button primary">Edit Reply</button>
            <button @click="deleteReply(nestedReply.id)" class="action-button danger">Delete Reply</button>

            <!-- Ensure there is an input field and edit buttons for editing the reply text -->
            <input v-if="editingReplyId === nestedReply.id" v-model="replyEditText" class="edit-input" />
            <div class="edit-buttons" v-if="editingReplyId === nestedReply.id">
              <button @click="saveEditedReply(nestedReply.id, comment.id)" class="action-button primary">Save Reply</button>
              <button @click="cancelReplyEdit(nestedReply.id)" class="action-button secondary">Cancel</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import ReplyForm from './ReplyForm.vue';
import { useProfileStore } from '../store/store';

interface Comment {
  id: number;
  text: string;
  user: number;
}

interface Reply {
  id: number;
  text: string;
  user: number; // Add the 'user' property to the Reply interface
  replies?: Reply[];
  // other properties
}

export default {
  props: ['comments'],
  components: {
    ReplyForm,
  },
  data() {
    return {
      commentEditText: '',
      replyEditText: '',
      editingReplyId: null as number | null,
      editingCommentId: null as number | null,
    };
  },
  methods: {
    isCurrentUserComment(commentUserId: number) {
      const profileStore = useProfileStore();
      return commentUserId === profileStore.getFetchedData.id;
    },

    isCurrentUserReply(replyUserId: number) {
      const profileStore = useProfileStore();
      return replyUserId === profileStore.getFetchedData.id;
    },

    handleReplyAdded() {
      this.$emit('comment-added');
    },

    deleteComment(commentId: number) {
      const profileStore = useProfileStore();
      const accessToken = profileStore.userAccessToken;

      fetch(`http://localhost:8000/api/comments/${commentId}/`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
          .then(response => {
            if (response.ok) {
              console.log(`Comment with ID ${commentId} deleted successfully`);
              this.$emit('comment-deleted');
            } else {
              console.error('Failed to delete comment:', response.statusText);
            }
          })
          .catch(error => {
            console.error('Error deleting comment:', error);
          });
    },

    deleteReply(replyId: string) {
      const profileStore = useProfileStore();
      const accessToken = profileStore.userAccessToken;

      fetch(`http://localhost:8000/api/replies/${replyId}/`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
          .then(response => {
            if (response.ok) {
              console.log(`Reply with ID ${replyId} deleted successfully`);
              this.$emit('comment-deleted');
            } else {
              console.error('Failed to delete reply:', response.statusText);
            }
          })
          .catch(error => {
            console.error('Error deleting reply:', error);
          });
    },

    async editComment(commentId: number, newText: string) {
      try {
        const profileStore = useProfileStore();
        const accessToken = profileStore.userAccessToken;
        const articleId = this.$route.params.id;

        const updatedPayload = {
          text: newText,
          article: articleId,
          user: profileStore.getFetchedData.id,
        };

        const updateResponse = await fetch(`http://localhost:8000/api/comments/${commentId}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${accessToken}`,
          },
          body: JSON.stringify(updatedPayload),
        });

        if (!updateResponse.ok) {
          throw new Error(`Failed to update comment: ${updateResponse.statusText}`);
        }

        console.log(`Comment with ID ${commentId} updated successfully`);
        this.$emit('comment-updated');
      } catch (error) {
        console.error('Error updating comment:', error);
      }
    },

    async editReply(commentId: number, replyId: number, newText: string) {
      try {
        const profileStore = useProfileStore();
        const accessToken = profileStore.userAccessToken;

        const updatedPayloadReply = {
          text: newText,
          user: profileStore.getFetchedData.id,
          comment: commentId, // Include the comment ID in the payload
        };

        const updateResponse = await fetch(`http://localhost:8000/api/replies/${replyId}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${accessToken}`,
          },
          body: JSON.stringify(updatedPayloadReply),
        });

        if (!updateResponse.ok) {
          throw new Error(`Failed to update reply: ${updateResponse.statusText}`);
        }

        console.log(`Reply with ID ${replyId} updated successfully`);
        this.$emit('comment-updated');
      } catch (error) {
        console.error('Error updating reply:', error);
      }
    },

    startEdit(commentId: number | null) {
      this.editingCommentId = commentId;
      const commentToEdit = this.comments.find((comment: Comment) => comment.id === commentId);
      this.commentEditText = commentToEdit ? commentToEdit.text : '';
    },

    startEditReply(commentId: number, replyId: number) {
      const comment = this.comments.find((comment: Comment) => comment.id === commentId);

      if (comment) {
        const findReply = (replies: Reply[], id: number): Reply | null => {
          for (const reply of replies) {
            if (reply.id === id) {
              return reply;
            }
            const nestedReply = findReply(reply.replies || [], id);
            if (nestedReply) {
              return nestedReply;
            }
          }
          return null;
        };

        const replyToEdit = findReply(comment.replies, replyId);
        if (replyToEdit) {
          this.editingReplyId = replyId;
          this.replyEditText = replyToEdit.text || '';
        } else {
          console.error(`Reply with ID ${replyId} not found.`);
        }
      } else {
        console.error(`Comment with ID ${commentId} not found.`);
      }
    },

    saveEditedComment(commentId: number) {
      const newText = this.commentEditText;
      this.editComment(commentId, newText);
      this.editingCommentId = null;
      this.commentEditText = '';
    },

    saveEditedReply(replyId: number, commentId: number) {
      const newText = this.replyEditText;
      this.editReply(commentId, replyId, newText);
      this.editingReplyId = null;
      this.replyEditText = '';
    },

    cancelEdit(commentId: number) {
      this.editingCommentId = null;
      this.commentEditText = '';
      console.log(commentId);
    },

    cancelReplyEdit(replyId: number) {
      this.editingReplyId = null;
      this.replyEditText = '';
      console.log(replyId);
    },
  },
};
</script>


<style scoped>
.comments {
  /* Overall styling for the comments section */
  font-family: 'Arial', sans-serif;
}

.comment-container {
  /* Styling for each comment container */
  margin-bottom: 20px;
}

.divider {
  /* Styling for the horizontal divider */
  border: 1px solid #ccc;
}

.edit-comment {
  /* Styling for the editing comment section */
  margin-top: 10px;
}

.edit-input {
  /* Styling for the input field in the editing comment section */
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  box-sizing: border-box;
}

.edit-buttons {
  /* Styling for the buttons in the editing comment section */
  display: flex;
  justify-content: space-between;
}

.comment-details {
  /* Styling for the comment details section */
  margin-top: 10px;
}

.comment-meta {
  /* Styling for the comment meta information */
  color: #777;
}

.comment-actions {
  /* Styling for the comment actions (edit and delete buttons) */
  margin-top: 10px;
}

.action-button {
  /* Styling for action buttons (primary and secondary) */
  padding: 8px 12px;
  cursor: pointer;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  margin-right: 10px;
}

.primary {
  /* Styling for primary action button */
  background-color: #4CAF50;
  color: white;
}

.secondary {
  /* Styling for secondary action button */
  background-color: #ddd;
  color: #333;
}

.danger {
  /* Styling for danger action button */
  background-color: #f44336;
  color: white;
}

.reply-container {
  /* Styling for the container of replies */
  margin-left: 20px;
}

.nested-reply {
  /* Styling for each nested reply */
  margin-top: 10px;
  border-left: 2px solid #4CAF50;
  padding-left: 10px;
}

</style>