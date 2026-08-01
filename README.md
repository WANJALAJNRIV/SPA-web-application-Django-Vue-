# Horizon News

A full-stack news publishing platform built with **Django** (REST API + server-rendered auth) and **Vue 3 + TypeScript** (single-page app frontend). It demonstrates a complete content workflow: accounts, personalized category feeds, and threaded discussion on articles.

## Features

- Account registration and login/logout (Django templates + forms, server-side rendered)
- User profiles with profile photo, email, and date of birth, editable via Ajax
- Articles organized into categories, with a personalized "favorite categories" feed
- Comments and threaded replies on articles, editable and deletable by their author
- JWT-authenticated REST API powering the Vue frontend
- Typed throughout: TypeScript on the frontend, Python type hints on the backend

## Tech stack

| Layer      | Technology                                            |
|------------|--------------------------------------------------------|
| Backend    | Django 5, Django REST Framework, SimpleJWT             |
| Frontend   | Vue 3, TypeScript, Vite, Pinia, Vue Router             |
| Database   | SQLite by default (swappable via env vars, see `project/database.py`) |

## How it works

Horizon News is two applications that talk to each other over HTTP: a **Django backend** that owns
the data and handles authentication, and a **Vue single-page app** that renders the reading
experience once you're logged in.

```
 Browser
   │
   │  1. Visit the site → Django serves a plain HTML login page
   ▼
 Django (port 8000)
   │  - Server-rendered login / signup forms (no JavaScript needed to log in)
   │  - Verifies your password, creates a session
   │  - Issues a JWT (JSON Web Token) that proves who you are
   │
   │  2. On success, redirects to the Vue app with that token attached
   ▼
 Vue SPA (served by Django in production, or Vite in development)
   │  - Stores the token (in the browser's local storage, so refreshing the page
   │    doesn't log you out)
   │  - Every time it needs data — articles, comments, your profile — it calls
   │    the Django REST API and attaches the token as proof of identity
   ▼
 Django REST API  (e.g. /api/articles/, /categories/, /api/comments/...)
   │  - Checks the token, looks up the data in the database, returns JSON
   ▼
 SQLite database (articles, categories, comments, replies, users)
```

**Why this shape?** It mirrors how most real production news/media sites are built: a classic,
crawlable, no-JS login flow (good for security and SEO) combined with a fast, app-like reading
experience once inside (good for engagement). The two halves are decoupled — you could swap the
Vue frontend for a mobile app and it would talk to the exact same API.

### What happens on each page

- **Login / Signup** (`/login/`, `/register/`) — plain Django pages, no Vue involved yet.
- **Home** (`/`) — once logged in, the Vue app asks the API for (1) articles in your favorite
  categories and (2) all articles grouped by category, and renders both as a news homepage.
- **Article page** (`/article/:id`) — fetches one article plus its category name, and loads/creates
  comments and threaded replies via the API as you interact with them (no full page reloads).
- **Profile page** (`/profile/`) — shows your account details and lets you add/remove favorite
  categories; changes save immediately via the API.

### Project structure

```
project/            Django settings, URL routing, database config
users/               Custom user model, signup/login/logout views & templates
api/                 Articles, categories, comments, replies — models, API views, serializers
  management/commands/seed_demo_data.py   Fills the database with demo content
frontend/            The Vue 3 + TypeScript single-page app (source code)
  src/pages/          One component per screen (Home, Article, Profile, ...)
  src/components/      Reusable pieces (comment list, comment form, reply form)
  src/store/store.ts    Shared state: who's logged in, their token, their profile data
templates/           Server-rendered Django pages (login, signup, base layout)
```

## Running it locally

1. Install Python dependencies (from the project root):

    ```console
    pip install -r requirements.txt
    ```

2. Create the database:

    ```console
    python manage.py migrate
    ```

3. (Optional but recommended) Populate the database with demo content:

    ```console
    python manage.py seed_demo_data
    ```

4. Install JavaScript dependencies (from the `frontend` folder):

    ```console
    cd frontend
    npm install
    ```

5. Start the Django server (from the project root):

    ```console
    python manage.py runserver
    ```

6. Start the Vue dev server (from the `frontend` folder):

    ```console
    npm run dev
    ```

7. Open http://localhost:5173, log in with one of the demo accounts below, and browse.

### Two ways to run the frontend

- **`npm run dev`** (used above) — starts Vite's dev server on port 5173 with hot-reload. Best while
  actively changing the frontend.
- **`npm run build`** — type-checks the TypeScript, bundles the Vue app, and copies the result into
  `api/static/api/spa/` and `api/templates/api/spa/`. After this, Django alone (just
  `python manage.py runserver`, no separate frontend server) serves the whole site on port 8000 —
  this is the shape a real deployment would take.

## Demo data

Running `python manage.py seed_demo_data` populates the database with entirely fictional
content, safe to show to clients or reviewers. Nothing here refers to a real person, company,
or event. The command is idempotent — running it again won't create duplicates.

It creates:

- **7 categories**: World, Business, Technology, Sports, Entertainment, Health, Science
- **28 articles** (4 per category), written by 6 fictional newsroom bylines
- **3 reader accounts**, each with 3 favorite categories pre-selected
- **~12 comments** and several threaded replies across a sample of articles
- **1 admin account** for browsing Django's admin panel

### Demo login credentials

All demo accounts share the same password: **`HorizonDemo2026!`**

| Username        | Role              |
|-----------------|-------------------|
| `demo_reader1`  | Reader (has favorite categories set) |
| `demo_reader2`  | Reader (has favorite categories set) |
| `demo_reader3`  | Reader (has favorite categories set) |
| `demo_admin`    | Site admin (`/admin/`) |

The newsroom byline accounts (`a.rowntree`, `m.solberg`, `l.nakamura`, `d.okafor`, `t.vance`, `s.kowalski`) also use the same password and can be used to demonstrate authorship.

> These are local demo accounts only, generated by the seed script — not real users. Re-run the seed command any time to reset back to this known state (it won't touch other accounts you create).
