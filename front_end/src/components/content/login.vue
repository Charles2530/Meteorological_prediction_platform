<template>
  <el-dialog
    v-model="loginConfig.showLoginPanel"
    :title="isLogin ? '登录' : '注册'"
    center
    @closed="checkLogin()"
  >
    <div class="login-panel">
      <el-form
        ref="loginFormRef"
        v-if="isLogin"
        :rules="loginRules"
        status-icon
        hide-required-asterisk
        :model="loginForm"
        label-width="80px"
        label-position="right"
      >
        <el-form-item
          :label="'用户名'"
          prop="username"
          :error="loginError['username']"
        >
          <el-input v-model="loginForm.username" clearable />
        </el-form-item>
        <el-form-item
          :label="'密码'"
          prop="password"
          :error="loginError['password']"
        >
          <el-input
            v-model="loginForm.password"
            clearable
            show-password
            @keyup.enter="submitLoginForm(loginFormRef)"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" link @click="isLogin = false">
            还没有账号, 注册一个?
          </el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitLoginForm(loginFormRef)">
            登录
          </el-button>
        </el-form-item>
      </el-form>
      <el-form
        ref="registerFormRef"
        v-else
        :rules="registerRules"
        status-icon
        hide-required-asterisk
        :model="registerForm"
        label-width="80px"
        label-position="right"
      >
        <el-form-item
          :label="'用户名'"
          prop="username"
          :error="registerError.username"
        >
          <el-input v-model="registerForm.username" clearable />
        </el-form-item>
        <el-form-item
          :label="'密码'"
          prop="password"
          :error="registerError.password"
        >
          <el-input
            v-model="registerForm.password"
            clearable
            show-password
            @keyup.enter="submitRegisterForm(registerFormRef)"
          />
        </el-form-item>
        <el-form-item :label="'邮箱'" prop="email" :error="registerError.email">
          <el-input
            v-model="registerForm.email"
            clearable
            @keyup.enter="submitRegisterForm(registerFormRef)"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" link @click="isLogin = true">
            {{ "已有账号?" }}
          </el-button>
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            @click="submitRegisterForm(registerFormRef)"
          >
            {{ "注册" }}
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { useUserInfo } from "@/stores/userInfo";
import { useLoginConfig } from "@/stores/loginConfig";
import router from "@/router";
import { ElMessage, type FormInstance, type FormRules } from "element-plus";
import { UserInfo } from "@/types/user.ts";
import { post } from "@/api/index";

interface LoginForm {
  username: string;
  password: string;
}
interface LoginResponse {
  success: boolean;
  info?: {
    token: string;
    userInfo: UserInfo;
  };
  reason?: string;
}
interface RegisterForm {
  username: string;
  password: string;
  email: string;
}
interface RegisterResponse {
  success: boolean;
  info?: {
    token: string;
    userInfo: UserInfo;
  };
  reason?: string;
}

const userInfo = useUserInfo();
const loginConfig = useLoginConfig();
const isLogin = ref(true);
const checkLogin = () => {
  if (!router.currentRoute.value.meta.permission.includes(userInfo.role)) {
    console.log(
      "checkLogin: ",
      router.currentRoute.value.meta.permission,
      userInfo.role
    );
    router.push({ name: "Home" });
  }
};

const loginFormRef = ref<FormInstance>();
const loginForm = reactive<LoginForm>({
  username: "",
  password: "",
});
const loginError = reactive({
  username: "",
  password: "",
});
const loginRules = reactive<FormRules<LoginForm>>({
  username: [
    {
      required: true,
      message: () => "用户名不能为空",
      trigger: "blur",
    },
    {
      min: 3,
      message: () => "用户名至少需要 3 个字符",
      trigger: "blur",
    },
    {
      max: 20,
      message: () => "用户名不能超过 20 个字符",
      trigger: "blur",
    },
  ],
  password: [
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
const submitLoginForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  if (loginError.username == " ") return; // 提示账号密码错误后未更改再次提交
  formEl.validate((valid) => {
    if (valid) {
      post<LoginResponse>("/api/login", loginForm).then(
        (res) => {
          const response = res.data;
          if (response.success == true) {
            const info = response.info!;
            userInfo.login(info.userInfo, info.token);
            loginConfig.$patch({ showLoginPanel: false });
            ElMessage({
              message: "登录成功",
              type: "success",
            });
          } else {
            console.log("error:", res);
          }
        },
        (error) => {
          console.log("error: ", error);
        }
      );
    } else {
      return false;
    }
  });
};
watch(loginForm, (_newVal, _oldVal) => {
  loginError.username = "";
  loginError.password = "";
});

const registerFormRef = ref<FormInstance>();
const registerForm = reactive<RegisterForm>({
  username: "",
  password: "",
  email: "",
});
const registerError = reactive({
  username: "",
  password: "",
  email: "",
});
const registerRules = reactive<FormRules<RegisterForm>>({
  username: [
    {
      required: true,
      message: () => "用户名不能为空",
      trigger: "blur",
    },
    {
      min: 3,
      message: () => "用户名至少需要 3 个字符",
      trigger: "blur",
    },
    {
      max: 15,
      message: () => "用户名不能超过 20 个字符",
      trigger: "blur",
    },
  ],
  password: [
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
  email: [
    {
      type: "email",
      message: () => "邮箱格式错误",
      trigger: "blur",
    },
  ],
});
const submitRegisterForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  // if (registerError.username == ' ') return; // 提示账号密码错误后未更改再次提交
  formEl.validate((valid) => {
    if (valid) {
      post<RegisterResponse>("/api/register", registerForm).then(
        (res) => {
          const response = res.data;
          if (response.success == true) {
            const info = response.info!;
            userInfo.login(info.userInfo, info.token);
            loginConfig.$patch({ showLoginPanel: false });
            ElMessage({
              message: "注册成功",
              type: "success",
            });
          }
        },
        (error) => {
          console.log("error: ", error);
        }
      );
    } else {
      return false;
    }
  });
};
watch(registerForm, (_oldVal, _newVal) => {
  registerError.username = " ";
  registerError.password = " ";
  registerError.email = " ";
});
</script>

<style scoped>
.login-panel {
  margin: 20px;
  max-width: 350px;
}
</style>
