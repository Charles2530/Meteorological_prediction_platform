<template>
  <el-dropdown style="height: inherit; margin-left: 5px">
    <div class="avatar">
      <el-avatar :size="40" fit="fill" :src="userInfo.avatar" />
    </div>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item
          v-if="userInfo.role == UserRole.Visitor"
          @click="loginConfig.setShowLoginPanel(true)"
        >
          用户登录
        </el-dropdown-item>
        <el-dropdown-item
          v-if="userInfo.role != UserRole.Visitor"
          @click="router.push({ name: 'user' })"
        >
          个人中心
        </el-dropdown-item>
        <el-dropdown-item
          v-if="userInfo.role != UserRole.Visitor"
          @click="userInfo.logout"
        >
          退出登录
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup lang="ts">
import { useUserInfo } from "@/stores/userInfo";
import { useLoginConfig } from "@/stores/loginConfig";
import { UserRole } from "@/types/user.ts";
import router from "@/router";

const userInfo = useUserInfo();
const loginConfig = useLoginConfig();
</script>

<style scoped>
.avatar {
  height: inherit;
  width: inherit;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}
</style>
