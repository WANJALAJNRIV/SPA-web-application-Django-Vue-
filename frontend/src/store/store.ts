// store.ts
import { createPinia, defineStore } from 'pinia';

interface AuthState {
  accessToken: string | null;
}

interface ProfileState {
  profileDetails: any | null; // Adjust the type as needed
  fetchedData: any | null; // Adjust the type as needed
  allUserDetails: { access_token: string } | null;
}

// Auth Store
export const useAuthStore = defineStore('auth', {
  // State
  state: (): AuthState => ({
    accessToken: null,
  }),

  // Getters
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },

  // Actions
  actions: {
    setAccessToken(token: string) {
      this.accessToken = token;
    },
    clearAccessToken() {
      this.accessToken = null;
    },
  },
});

// Profile Store
export const useProfileStore = defineStore('profile', {
  // State
  state: (): ProfileState => ({
    profileDetails: null,
    fetchedData: null,
    allUserDetails: null,
  }),

  // Getters
  getters: {
    userAccessToken(): string | null {
      return this.allUserDetails ? this.allUserDetails.access_token : null;
    },
    getAllUserDetails(): any {
      return this.allUserDetails ? this.allUserDetails : null;
    },
    getFetchedData(): any {
      return this.fetchedData ? this.fetchedData : null;
    },
  },

  // Actions
  actions: {
    setProfileDetails(details: any) {
      this.profileDetails = details;
    },
    setFetchedData(data: any) {
      this.fetchedData = data;
    },
    clearProfileDetails() {
      this.profileDetails = null;
    },
    setAllUserDetails(userObject: { access_token: string }) {
      this.allUserDetails = userObject;
    },
    logUserDetails() {
      console.log('User Details:', this.allUserDetails);
    },
  },
});

export const pinia = createPinia();
