<template>
  <template>
    <div class="common-layout">
      <el-container>
        <el-header>Header</el-header>
        <el-container>
          <el-aside width="200px">Aside</el-aside>
          <el-container>
            <el-main>
              <div id="app">
                <router-view v-slot="{ Component }">
                  <transition :name="transition">
                    <component :is="Component" />
                  </transition>
                </router-view></div
            ></el-main>
            <el-footer>Footer</el-footer>
          </el-container>
        </el-container>
      </el-container>
    </div>
  </template>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";
const route = useRoute();
const transition = computed(() => {
  return (route.meta?.transition as string) || "fade";
});
</script>
