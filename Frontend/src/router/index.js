import HomeView from '@/views/Home.vue'
import ComponentsView from '@/views/Components.vue'

// =========================== auth =========================
import LoginView from '@/views/auth/Login.vue'
import RegisterView from '@/views/auth/Register.vue'
import ForgotPassView from '@/views/auth/ForgotPass.vue'

// =========================== user =========================
import MusicDashboard from '@/views/user/MusicDashboard.vue'
import HomeSection from '@/views/user/HomeSection.vue'
import BrowseSection from '@/views/user/BrowseSection.vue'
import NotificationSection from '@/views/user/NotificationSection.vue'
import ProfileSection from '@/views/user/ProfileSection.vue'
import SupportSection from '@/views/user/SupportSection.vue'
import AccountSection from '@/views/user/AccountSection.vue'

import SongDetail from '@/views/user/Songs.vue'
import AlbumDetail from '@/views/user/Albums.vue'
import ArtistsDetail from '@/views/user/Artists.vue'
import TagsDetail from '@/views/user/Tags.vue'
import playlistDetail from '@/views/user/playlist.vue'

// =========================== admin =========================
import AdminView from '@/views/admin/Admin.vue'
import adminDashboard from '@/views/admin/dashboard.vue'
import adminSongs from '@/views/admin/songs.vue'
import adminUsers from '@/views/admin/users.vue'
import adminCategories from '@/views/admin/categories.vue'
import adminFlaggedItems from '@/views/admin/flagged.vue'

import AddCategory from '@/views/admin/AddCategory.vue'
import EditCategory from '@/views/admin/EditCategory.vue'

// =========================== studio =========================
import StudioView from '@/views/studio/Studio.vue'
import studioDashboard from '@/views/studio/dashboard.vue'
import studioSongs from '@/views/studio/songs.vue'
import studioAlbums from '@/views/studio/albums.vue'

import AddSong from '@/views/studio/AddSong.vue'
import EditSong from '@/views/studio/EditSong.vue'
import AddAlbum from '@/views/studio/AddAlbum.vue'
import EditAlbum from '@/views/studio/EditAlbum.vue'


import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    name: 'Home',
    path: '/',
    component: HomeView
  },
  {
    name: 'Login',
    path: '/login',
    component: LoginView
  },
  {
    name: 'Register',
    path: '/register',
    component: RegisterView
  },
  {
    name: 'ForgetPassword',
    path: '/forgot-password',
    component: ForgotPassView
  },
  {
    name:'components',
    path:'/components',
    component: ComponentsView,
  },
  {
    path:'/app',
    component: MusicDashboard,
    children:[
      {
        name:'app',
        path:'',
        component: HomeSection
      },
      {
        name:'browse',
        path:'browse',
        component: BrowseSection,
      },
      {
        name:'account',
        path:'account',
        component: AccountSection,
      },
      {
        name:'notification',
        path:'notification',
        component: NotificationSection,
      },
      {
        name:'profile',
        path:'profile',
        component: ProfileSection,
      },
      {
        name:'support',
        path:'support',
        component: SupportSection,
      },
      {
        name:'songDetail',
        path:'song/:id',
        component: SongDetail
      },
      {
        name:'albumDetail',
        path:'album/:id',
        component: AlbumDetail
      },{
        name:'artistDetail',
        path:'artist/:id',
        component: ArtistsDetail
      },
      {
        name:'tagDetail',
        path:'tags/:id',
        component: TagsDetail
      },
      {
        name:'playlistDetail',
        path:'playlist/:id',
        component: playlistDetail
      }
    ]
  },
  {
    path:'/studio',
    component: StudioView,
    children:[
      {
        name:'studio',
        path:'',
        component: studioDashboard
      },
      {
        name:'studio_songs',
        path:'songs',
        component: studioSongs
      },
      {
        name:'studio_albums',
        path:'albums',
        component: studioAlbums
      },
      {
        name:'AddSong',
        path:'addSong',
        component: AddSong
      },
      {
        name:'EditSong',
        path:'editSong/:id',
        component: EditSong
      },
      {
        name:'AddAlbum',
        path:'addAlbum',
        component: AddAlbum
      },
      {
        name:'EditAlbum',
        path:'editAlbum/:id',
        component: EditAlbum
      }
    ]
  },
  {
    path:'/admin',
    component: AdminView,
    children:[
      {
        name:'admin',
        path:'',
        component: adminDashboard
      },
      {
        name:'admin_songs',
        path:'songs',
        component: adminSongs
      },
      {
        name:'admin_users',
        path:'users',
        component: adminUsers
      },
      {
        name:'admin_categories',
        path:'categories',
        component: adminCategories
      },
      {
        name:'admin_flagged',
        path:'flagged',
        component: adminFlaggedItems
      },
      {
        name: 'AddCategory',
        path: 'addCategory',
        component: AddCategory
      },
      {
        name: 'EditCategory',
        path: 'editCategory/:id',
        component: EditCategory
      }
    ]
  },
]


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes
})

export default router
