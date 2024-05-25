// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files
import Home from '../pages/Home.vue';
import Profile from '../pages/Profile.vue';
import Article from '../pages/Article.vue';
import Logout from '../pages/Logout.vue';
import  Login_successful from '../pages/Login_successful.vue';
import  ProfileForm from '../pages/ProfileForm.vue';




let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Home', component: Home },
        { path: '/profile/', name: 'Profile', component: Profile },
        { path: '/profile/edit/', name: 'EditProfile', component: ProfileForm },
        { path: '/article/:id', name: 'article-detail', component: Article },
        {path: '/logout', name: 'logout', component: Logout },
        {path: '/login/successful/', name: 'login-successful', component: Login_successful},
         
    ]
})

export default router
