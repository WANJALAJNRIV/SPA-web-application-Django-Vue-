<template>
    <main class="container pt-4">
      <div class="navbar">
        <router-link class="nav-link" :to="{ name: 'Home' }">Home</router-link>
        <router-link class="nav-link" :to="{ name: 'Profile' }">Profile</router-link>
        <router-link class="nav-link" :to="{ name: 'logout' }">Log out</router-link>
      </div>
      <RouterView class="flex-shrink-0" />
    </main>
  </template>
  
  <style scoped>
  .navbar {
    background-color: #2c3e50; /* Dark background color */
    padding: 10px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    width: 100%;
    height: 10vh;
  }
  
  .nav-link {
    color: #ecf0f1; /* Light text color */
    text-decoration: none;
    transition: color 0.3s ease; /* Smooth color transition on hover */
  }
  
  .nav-link:hover {
    color: #3498db; /* Blue color on hover */
  }
  </style>
  