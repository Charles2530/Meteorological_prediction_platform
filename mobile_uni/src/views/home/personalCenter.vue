<template>
  <div>
    <div class="card-warp">
      <el-card class="box-card">
        <el-row>
          <el-col :span="24">
            <Avatar ref="uploadRef" />
            <el-descriptions :column="1" border>
              <el-descriptions-item>
                <template #label>
                  <el-text type="primary">
                    <el-icon><User /></el-icon>
                    用户名
                  </el-text>
                </template>
                <el-text>
                  {{ userInfo.username }}
                </el-text>
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label>
                  <el-text type="primary">
                    <el-icon><Message /></el-icon>
                    邮箱
                  </el-text>
                </template>
                <el-text class="w-150px" truncated>
                  {{ userInfo.email }}
                </el-text>
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label>
                  <el-text type="primary">
                    <el-icon><Key /></el-icon>
                    身份
                  </el-text>
                </template>
                <el-text>
                  <el-text v-if="userInfo.role == UserRole.User"
                    >普通用户</el-text
                  >
                  <el-text v-else-if="userInfo.role == UserRole.Administrator">
                    管理员
                  </el-text>
                  <el-text v-else>游客</el-text>
                </el-text>
              </el-descriptions-item>
              <!-- 订阅城市 -->
              <el-descriptions-item>
                <template #label>
                  <el-text type="primary">
                    <el-icon><Location /></el-icon>
                    订阅城市
                  </el-text>
                </template>
                <div>
                  <el-text>
                    <el-tag
                      v-for="city in bookingCities"
                      :key="city.city"
                      type="success"
                      class="mr-1"
                    >
                      {{ city.city }}
                    </el-tag>
                  </el-text>
                </div>
              </el-descriptions-item>
            </el-descriptions>
          </el-col>
        </el-row>
        <el-divider />
        <div class="button-container">
          <el-button
            type="primary"
            text
            sm
            class="button-item"
            @click="operateEmail = true"
          >
            <el-icon class="ml-1 mr-3"><Message /></el-icon>更新邮箱
          </el-button>
          <el-button
            type="primary"
            text
            sm
            class="button-item"
            @click="operateAvatar"
          >
            <el-icon class="ml-1 mr-3"><User /></el-icon>更新头像
          </el-button>
          <el-button
            type="danger"
            text
            sm
            class="button-item"
            @click="operatePassword = true"
          >
            <el-icon class="ml-1 mr-3"><Key /></el-icon>更新密码
          </el-button>
          <el-button
            type="danger"
            text
            sm
            class="button-item"
            @click="userInfo.logout"
          >
            <el-icon class="ml-1 mr-3"><House /></el-icon>退出登录
          </el-button>
        </div>
      </el-card>
    </div>
    <el-dialog v-model="operateEmail" title="更新邮箱">
      <el-form
        :model="emailForm"
        ref="emailFormRef"
        :rules="emailRules"
        status-icon
        @submit.prevent
      >
        <el-form-item label="新邮箱" :error="emailError" prop="email">
          <el-input
            v-model="emailForm.email"
            autocomplete="off"
            @keyup.enter="confirmEmail(emailFormRef)"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="operateEmail = false" text>
            取消
          </el-button>
          <el-button type="primary" @click="confirmEmail(emailFormRef)" text bg>
            确定
          </el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
    <el-dialog v-model="operatePassword" title="更新密码">
      <el-form
        :model="passwordForm"
        ref="passwordFormRef"
        :rules="passwordRules"
        status-icon
        hide-required-asterisk
        @submit.prevent
      >
        <el-form-item
          label="旧密码"
          :error="passwordError.oldPassword"
          prop="oldPassword"
        >
          <el-input
            v-model="passwordForm.oldPassword"
            autocomplete="off"
            clearable
            show-password
          />
        </el-form-item>
        <el-form-item
          label="新密码"
          :error="passwordError.newPassword"
          prop="newPassword"
        >
          <el-input
            v-model="passwordForm.newPassword"
            autocomplete="off"
            clearable
            show-password
            @keyup.enter="confirmPassword(passwordFormRef)"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="operatePassword = false" text>
            取消
          </el-button>
          <el-button
            type="primary"
            @click="confirmPassword(passwordFormRef)"
            text
            bg
          >
            确定
          </el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { useUserInfo } from "@/stores/userInfo";
import { useLoginConfig } from "@/stores/loginConfig";
import { UserRole } from "@/types/user.ts";
import { User, Message, Key } from "@element-plus/icons-vue";
import type { FormInstance, FormRules } from "element-plus";
import { post, get } from "@/api/index";
import Avatar from "@c/content/avatar.vue";
import { md5 } from "js-md5";
import { GetSubscribeResponse } from "@/types/weather";

interface EmailForm {
  email: string;
}
interface EmailResponse {
  success: boolean;
  reason?: string;
}
interface PasswordForm {
  oldPassword: string;
  newPassword: string;
}
interface PasswordResponse {
  success: boolean;
  reason?: string;
}

const permission = [UserRole.User, UserRole.Administrator];
const userInfo = useUserInfo();
const loginConfig = useLoginConfig();
const bookingCities = ref([]);
onMounted(() => {
  if (!permission.includes(userInfo.role)) loginConfig.showLoginPanel = true;
  getSubscribeStatus();
});
const getSubscribeStatus = () => {
  get<GetSubscribeResponse>("/api/subscribe/").then((res) => {
    bookingCities.value.splice(
      0,
      bookingCities.value.length,
      ...res.data.tableData
    );
  });
};
const operateEmail = ref(false);
const emailFormRef = ref<FormInstance>();
const emailForm = reactive<EmailForm>({
  email: "",
});
const emailRules = reactive<FormRules<EmailForm>>({
  email: [
    {
      type: "email",
      message: () => "邮箱格式错误",
      trigger: "blur",
    },
  ],
});
const emailError = ref("");
const confirmEmail = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate((valid) => {
    if (valid) {
      post<EmailResponse>("/api/operate/email/", emailForm).then((res) => {
        const response = res.data;
        if (response.success) {
          userInfo.email = emailForm.email;
          operateEmail.value = false;
        }
      });
    } else return false;
  });
};
watch(emailForm, (_newValue, _oldValue) => {
  emailError.value = "";
});

const operatePassword = ref(false);
const passwordFormRef = ref<FormInstance>();
const passwordForm = reactive<PasswordForm>({
  oldPassword: "",
  newPassword: "",
});
const passwordRules = reactive<FormRules<PasswordForm>>({
  oldPassword: [
    {
      required: true,
      message: () => "请输入密码",
      trigger: "blur",
    },
  ],
  newPassword: [
    {
      required: true,
      message: () => "请输入密码",
      trigger: "blur",
    },
    {
      min: 6,
      message: () => "密码至少需要 6 个字符",
      trigger: "blur",
    },
    {
      max: 20,
      message: () => "密码不能超过 20 个字符",
      trigger: "blur",
    },
  ],
});
const passwordError = reactive({
  oldPassword: "",
  newPassword: "",
});
const confirmPassword = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate((valid) => {
    if (valid) {
      const encodePasswordForm = {
        oldPassword: md5(passwordForm.oldPassword),
        newPassword: md5(passwordForm.newPassword),
      };
      post<PasswordResponse>("/api/operate/password/", encodePasswordForm).then(
        (res) => {
          const response = res.data;
          if (response.success) {
            operatePassword.value = false;
            //userInfo.logout();
          }
        }
      );
    } else return false;
  });
};
watch(passwordForm, (_newValue, _oldValue) => {
  passwordError.oldPassword = "";
  passwordError.newPassword = "";
});

const uploadRef = ref();
const operateAvatar = () => {
  uploadRef.value!.upload();
};
</script>

<style scoped>
.card-warp {
  display: flex;
  align-items: center;
  justify-content: center;
}

.box-card {
  width: 600px;
  text-align: center;
}

.button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.button-item {
  margin: 5px 0;
  width: 100%;
}

@media (max-width: 768px) {
  .button-item {
    width: 90%;
  }
}
</style>
