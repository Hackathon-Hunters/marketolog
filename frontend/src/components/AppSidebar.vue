<script setup lang="ts">
import type { SidebarProps } from '@/ui/sidebar'

import NavMain from '@/components/NavMain.vue'
import NavProjects from '@/components/NavProjects.vue'
import NavUser from '@/components/NavUser.vue'
import TeamSwitcher from '@/components/TeamSwitcher.vue'
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from '@/components/ui/sidebar'

import {
  AudioWaveform,
  BookOpen,
  Bot,
  Command,
  Frame,
  GalleryVerticalEnd,
  Map,
  PieChart,
  Settings,
  SquareTerminal,
} from 'lucide-vue-next'
import { userStore } from '../store'
import { computed, watch, ref, onMounted } from 'vue'

// Состояние имени компании с возможностью обновления
const companyName = ref('Acme Inc')

// Отслеживаем изменения данных пользователя
watch(() => userStore.currentUser.company, (newCompany) => {
  if (newCompany?.name) {
    companyName.value = newCompany.name
  }
}, { immediate: true, deep: true })

// Получаем список команд с актуальным названием компании
const teams = computed(() => [
  {
    name: companyName,
    logo: GalleryVerticalEnd,
    plan: 'Enterprise',
  },
])

// This is sample data.
const data = {
  user: {
    name: 'shadcn',
    email: 'm@example.com',
    avatar: '/avatars/shadcn.jpg',
  },
  navMain: [
    {
      title: 'Main menu',
      url: '/main/dashboard',
      icon: SquareTerminal,
      isActive: true,
      items: [
        {
          title: 'Dashboard',
          url: '/main/dashboard',
        },
        {
          title: 'Info',
          url: '/main/info',
        },
      ],
    },
  ],
  // projects: [
  //   {
  //     name: 'Design Engineering',
  //     url: '#',
  //     icon: Frame,
  //   },
  //   {
  //     name: 'Sales & Marketing',
  //     url: '#',
  //     icon: PieChart,
  //   },
  //   {
  //     name: 'Travel',
  //     url: '#',
  //     icon: Map,
  //   },
  // ],
}
</script>

<template>
  <Sidebar v-bind="$props">
    <SidebarHeader>
      <TeamSwitcher :teams="teams" />
    </SidebarHeader>
    <SidebarContent>
      <NavMain :items="data.navMain" />
      <!-- <NavProjects :projects="data.projects" /> -->
    </SidebarContent>
    <SidebarFooter>
      <NavUser :user="userStore.currentUser" />
    </SidebarFooter>
    <SidebarRail />
  </Sidebar>
</template>
