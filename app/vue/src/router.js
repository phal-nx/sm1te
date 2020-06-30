import Vue from 'vue';
import Router from 'vue-router';

import PersonalBlog from './views/Overview.vue';
import UserProfileLite from './views/UserProfileLite.vue';
import AddNewPost from './views/AddNewPost.vue';
import Errors from './views/Errors.vue';
import ComponentsOverview from './views/ComponentsOverview.vue';
import Tables from './views/Tables.vue';
import BlogPosts from './views/BlogPosts.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  linkActiveClass: 'active',
  linkExactActiveClass: 'exact-active',
  scrollBehavior() {
    return { x: 0, y: 0 };
  },
  routes: [
    {
      path: '/',
      redirect: '/overview',
    },
    {
      path: '/overview',
      name: 'overview',
      component: PersonalBlog,
    },
    {
      path: '/hosts',
      name: 'hosts',
      component: UserProfileLite,
    },
    {
      path: '/add-pack',
      name: 'add-pack',
      component: AddNewPost,
    },

    {
      path: '/most-vulnerable',
      name: 'most-vulnerable',
      component: ComponentsOverview,
    },
    {
      path: '/servers',
      name: 'servers',
      component: Tables,
    },
    {
      path: '/admin',
      name: 'admin',
      component: BlogPosts,
    }, {
      path: '*',
      redirect: '/errors',
    },
  ],
});
