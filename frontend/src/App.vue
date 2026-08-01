<template>
    <div class="page">
      <header class="site-header">
        <div class="site-header-inner">
          <router-link class="brand" :to="{ name: 'Home' }">Horizon News</router-link>
          <nav class="site-nav">
            <router-link class="site-nav-link" :to="{ name: 'Home' }">Home</router-link>
            <router-link class="site-nav-link" :to="{ name: 'Profile' }">Profile</router-link>
            <router-link class="site-nav-link" :to="{ name: 'logout' }">Log out</router-link>
          </nav>
        </div>
      </header>
      <main class="container pt-4">
        <RouterView class="flex-shrink-0" />
      </main>
      <footer class="site-footer">
        <span>&copy; {{ year }} Horizon News. Demo content only, for evaluation purposes.</span>
      </footer>
    </div>
  </template>

  <script setup lang="ts">
  const year = new Date().getFullYear();
  </script>

  <style scoped>
  .page {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  /* Note: this header intentionally avoids the class name "navbar" - Bootstrap's
     global .navbar rule (display:flex, flex-wrap:wrap) collides with it and makes
     child elements shrink to fit-content instead of filling the width. */
  .site-header {
    display: block;
    background-color: #1a1a1a;
    border-bottom: 3px solid var(--color-accent, #a3241d);
    padding: 0 24px;
  }

  .site-header-inner {
    width: 100%;
    max-width: 1100px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 64px;
  }

  .brand {
    color: #fff;
    font-family: var(--font-headline, Georgia, serif);
    font-weight: 900;
    font-size: 1.5rem;
    letter-spacing: 0.3px;
    text-decoration: none;
    white-space: nowrap;
  }

  .site-nav {
    display: flex;
    gap: 24px;
    align-items: center;
  }

  .site-nav-link {
    color: #ecf0f1;
    text-decoration: none;
    font-size: 0.9rem;
    transition: color 0.2s ease;
  }

  .site-nav-link:hover {
    color: #e0a29e;
  }

  .site-footer {
    margin-top: auto;
    text-align: center;
    padding: 20px;
    color: var(--color-muted, #6c757d);
    font-size: 0.8rem;
    border-top: 1px solid var(--color-border, #e5e2dc);
  }
  </style>
