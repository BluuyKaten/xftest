import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Users from '../views/Users.vue'
import Posts from '../views/Posts.vue'
import Speech from '../views/Speech.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/users',
    name: 'Users',
    component: Users
  },
  {
    path: '/posts',
    name: 'Posts',
    component: Posts
  },
  {
    path: '/speech',
    name: 'Speech',
    component: Speech
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 