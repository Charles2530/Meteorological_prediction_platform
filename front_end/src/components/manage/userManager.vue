<template>
  <el-container class="panel bg-white">
    <el-main class="no-padding">
      <el-table
        :data="userlist"
        v-loading="loading"
        class="table"
        size="small"
        table-layout="auto"
      >
        <el-table-column :label="manage.user.uid">
          <el-table-column prop="uid">
            <template #header>
              <el-input
                v-model="request.uid"
                size="small"
                :suffix-icon="Search"
                @keyup.enter="getUserList"
              />
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column :label="manage.user.username">
          <el-table-column prop="username">
            <template #header>
              <el-input
                v-model="request.username"
                size="small"
                :suffix-icon="Search"
                @keyup.enter="getUserList"
              />
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column :label="manage.user.email">
          <el-table-column prop="email">
            <template #header>
              <el-input
                v-model="request.email"
                size="small"
                :suffix-icon="Search"
                @keyup.enter="getUserList"
              />
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column :label="manage.user.role.label" width="120">
          <el-table-column prop="role" width="120">
            <template #header>
              <el-select
                v-model="request.role"
                size="small"
                @change="getUserList"
                clearable
              >
                <el-option
                  size="small"
                  :label="manage.user.role.User"
                  value="1"
                >
                  <el-tag type="info">{{ manage.user.role.User }}</el-tag>
                </el-option>
                <el-option
                  size="small"
                  :label="manage.user.role.Administrator"
                  value="2"
                >
                  <el-tag type="warning">{{
                    manage.user.role.Administrator
                  }}</el-tag>
                </el-option>
              </el-select>
            </template>
            <template #default="scope">
              <el-tag v-if="scope.row.role == 1" type="info">
                {{ manage.user.role.User }}
              </el-tag>
              <el-tag v-else type="warning">
                {{ manage.user.role.Administrator }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column prop="last_login" :label="manage.user.last_login" />
        <el-table-column
          prop="operate"
          width="400px"
          :label="manage.user.operate.title"
          fixed="right"
        >
          <template #default="scope">
            <el-button-group>
              <el-popconfirm
                :width="200"
                :title="manage.user.operate.delete.confirm"
                :cancel-button-text="manage.cancel"
                :confirm-button-text="manage.confirm"
                @confirm="handleDelete(scope.row.uid)"
              >
                <template #reference>
                  <el-button type="danger" size="small">
                    <el-icon class="mr-2"><CircleClose /></el-icon
                    >{{ manage.user.operate.delete.label }}
                  </el-button>
                </template>
              </el-popconfirm>
              <el-popconfirm
                :width="200"
                :title="manage.user.operate.set.confirm"
                v-if="scope.row.role == UserRole.User"
                :cancel-button-text="manage.cancel"
                :confirm-button-text="manage.confirm"
                @confirm="handleSet(scope.row.uid, UserRole.Administrator)"
              >
                <template #reference>
                  <el-button type="warning" size="small">
                    <el-icon class="mr-2"><Setting /></el-icon>
                    {{ manage.user.operate.set.label }}
                  </el-button>
                </template>
              </el-popconfirm>
              <el-popconfirm
                :width="200"
                :title="manage.user.operate.unset.confirm"
                v-if="scope.row.role == UserRole.Administrator"
                :cancel-button-text="manage.cancel"
                :confirm-button-text="manage.confirm"
                @confirm="handleSet(scope.row.uid, UserRole.User)"
              >
                <template #reference>
                  <el-button type="warning" size="small">
                    <el-icon class="mr-2"><Setting /></el-icon>
                    {{ manage.user.operate.unset.label }}
                  </el-button>
                </template>
              </el-popconfirm>
              <el-button
                type="success"
                size="small"
                @click="
                  emailForm.uid = scope.row.uid;
                  operateEmail = true;
                "
              >
                <el-icon class="mr-2"><EditPen /></el-icon>
                {{ manage.user.operate.email.label }}
              </el-button>
              <el-button
                type="success"
                size="small"
                @click="
                  passwordForm.uid = scope.row.uid;
                  operatePassword = true;
                "
              >
                <el-icon class="mr-2"><Finished /></el-icon>
                {{ manage.user.operate.password.label }}
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
      <div class="no-padding" style="margin-top: 10px">
        <div style="display: flex">
          <el-button type="primary" @click="getUserList" class="ml-2" plain>
            <el-icon class="mr-3"><Loading /></el-icon>
            {{ manage.reload }}
          </el-button>
          <div style="flex: 1"></div>
          <div class="pagination">
            <el-select
              v-model="pagination.page_size"
              style="width: 100px; margin-right: 5px"
              @change="getUserList"
            >
              <el-option :value="10" label="10" />
              <el-option :value="15" label="15" />
              <el-option :value="20" label="20" />
            </el-select>
            <el-text>
              {{
                (manage.pagination.total,
                [pagination.page, pagination.page_total])
              }}
            </el-text>
            <el-pagination
              style="margin-left: 5px; margin-right: 5px"
              :current-page="pagination.page"
              :page-size="pagination.page_size"
              :page-count="pagination.page_total"
              :total="pagination.total"
              background
              layout="prev, pager, next"
              @current-change="handleCurrentChange"
            />
            <el-text>{{ manage.pagination.jump }}</el-text>
            <el-input-number
              style="width: 60px; margin-left: 5px; margin-right: 5px"
              :controls="false"
              :min="1"
              :max="pagination.page_total"
              v-model="jump"
              :value-on-clear="pagination.page"
              size="small"
              @blur="handleJump(false)"
              @keyup.enter="handleJump(true)"
            />
            <el-text>{{ manage.pagination.page }}</el-text>
          </div>
        </div>
        <el-dialog
          v-model="operateEmail"
          :title="manage.user.operate.email.label"
        >
          <el-form
            :model="emailForm"
            ref="emailFormRef"
            :rules="emailRules"
            status-icon
            @submit.prevent
          >
            <el-form-item :error="emailError" prop="email">
              <el-input
                v-model="emailForm.email"
                autocomplete="off"
                @keyup.enter.prevent="confirmEmail(emailFormRef)"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="operateEmail = false" text>
                {{ manage.cancel }}
              </el-button>
              <el-button
                type="primary"
                @click="confirmEmail(emailFormRef)"
                text
                bg
              >
                {{ manage.confirm }}
              </el-button>
            </el-form-item>
          </el-form>
        </el-dialog>
        <el-dialog
          v-model="operatePassword"
          :title="manage.user.operate.password.label"
        >
          <el-form
            :model="passwordForm"
            ref="passwordFormRef"
            :rules="passwordRules"
            status-icon
            hide-required-asterisk
            @submit.prevent
          >
            <el-form-item :error="passwordError" prop="password">
              <el-input
                v-model="passwordForm.password"
                autocomplete="off"
                clearable
                show-password
                @keyup.enter="confirmPassword(passwordFormRef)"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="operatePassword = false" text>
                {{ manage.cancel }}
              </el-button>
              <el-button
                type="primary"
                @click="confirmPassword(passwordFormRef)"
                text
                bg
              >
                {{ manage.confirm }}
              </el-button>
            </el-form-item>
          </el-form>
        </el-dialog>
      </div>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { UserDetail, UserRole } from "@/types/user";
import { post } from "@/api/index";
import throttle from "lodash/throttle";
import { Search } from "@element-plus/icons-vue";
import type { FormInstance, FormRules } from "element-plus";
import { md5 } from "js-md5";
interface QueryForm {
  page: number;
  page_size: number;
  uid?: number;
  username?: string;
  email?: string;
  role?: UserRole;
}
interface QueryResponse {
  all: number;
  now: number;
  page_total: number;
  page: number;
  userlist: UserDetail[];
}

const userlist = reactive<UserDetail[]>([]);
const loading = ref(false);
const jump = ref(1);
const pagination = reactive({
  all: 0,
  total: 0,
  page_total: 1,
  page: 1,
  page_size: 10,
});

const request = reactive<QueryForm>({
  page: pagination.page,
  page_size: pagination.page_total,
  uid: undefined,
  username: undefined,
  email: undefined,
  role: undefined,
});

const getUserList = throttle(() => {
  loading.value = true;
  request.page = pagination.page;
  request.page_size = pagination.page_size;
  post<QueryResponse>("/api/manage/user/list/", request).then((res) => {
    const data = res.data;
    userlist.splice(0, userlist.length, ...data.userlist);
    pagination.all = data.all;
    pagination.total = data.now;
    pagination.page_total = data.page_total;
    pagination.page = data.page;
    loading.value = false;
    jump.value = pagination.page;
  });
});

const handleCurrentChange = (page: number) => {
  pagination.page = page;
  getUserList();
};

const handleJump = (force: boolean) => {
  if (pagination.page != jump.value || force) {
    pagination.page = jump.value;
    getUserList();
  }
};

interface DeleteForm {
  uid: number;
}
interface Response {
  success: boolean;
  reason?: string;
}
const handleDelete = throttle((id: number) => {
  const request: DeleteForm = {
    uid: id,
  };
  post<Response>("/api/manage/user/delete/", request).then((res) => {
    const response = res.data;
    getUserList();
    if (response.success) {
      ElMessage.success(manage.user.operate.delete.success);
    } else {
      ElMessage({
        message: response.reason,
        type: "error",
      });
    }
  });
}, 500);

interface SetForm {
  uid: number;
  role: UserRole;
}
const handleSet = throttle((id: number, role: UserRole) => {
  const request: SetForm = {
    uid: id,
    role: role,
  };
  post<Response>("/api/manage/user/set/", request).then((res) => {
    const response = res.data;
    getUserList();
    if (response.success) {
      if (role == UserRole.Administrator)
        ElMessage.success(manage.user.operate.set.success);
      else if (role == UserRole.User)
        ElMessage.success(manage.user.operate.unset.success);
    } else ElMessage.error(manage.invaild);
  });
}, 500);

interface EmailForm {
  uid: number;
  email: string;
}
const operateEmail = ref(false);
const emailFormRef = ref<FormInstance>();
const emailForm = reactive<EmailForm>({
  uid: 0,
  email: "",
});
const emailRules = reactive<FormRules<EmailForm>>({
  email: [
    {
      type: "email",
      message: () => manage.user.operate.email.format,
      trigger: "blur",
    },
  ],
});
const emailError = ref("");
const confirmEmail = throttle((formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate((valid) => {
    if (valid) {
      post<Response>("/api/manage/user/email/", emailForm).then((res) => {
        const response = res.data;
        if (response.success) {
          getUserList();
          operateEmail.value = false;
          ElMessage.success(manage.user.operate.email.success);
        } else {
          emailError.value = `${response.reason!}`;
        }
      });
    } else return false;
  });
}, 500);
watch(emailForm, (_newValue, _oldValue) => {
  emailError.value = "";
});

interface PasswordForm {
  uid: number;
  password: string;
}
const operatePassword = ref(false);
const passwordFormRef = ref<FormInstance>();
const passwordForm = reactive<PasswordForm>({
  uid: 0,
  password: "",
});
const passwordRules = reactive<FormRules<PasswordForm>>({
  password: [
    {
      required: true,
      message: () => manage.user.operate.password.required,
      trigger: "blur",
    },
    {
      min: 6,
      message: () => manage.user.operate.password.minLength,
      trigger: "blur",
    },
    {
      max: 20,
      message: () => manage.user.operate.password.maxLength,
      trigger: "blur",
    },
  ],
});
const passwordError = ref("");
const confirmPassword = throttle((formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate((valid) => {
    if (valid) {
      const encodePasswordForm = {
        uid: passwordForm.uid,
        password: md5(passwordForm.password),
      };
      post<Response>("/api/manage/user/password/", encodePasswordForm).then(
        (res) => {
          const response = res.data;
          if (response.success) {
            getUserList();
            operatePassword.value = false;
            ElMessage.success(manage.user.operate.password.success);
          } else {
            passwordError.value = `${response.reason!}`;
          }
        }
      );
    } else return false;
  });
}, 500);
watch(passwordForm, (_newValue, _oldValue) => {
  passwordError.value = "";
});

onMounted(() => {
  getUserList();
});
onUnmounted(() => {
  userlist.splice(0, userlist.length);
});

const manage = {
  pagination: {
    total: "共 {0} 条, 已筛选 {1} 条",
    jump: "跳转至",
    page: "页",
  },
  taglist: {
    new: "+ 添加",
  },
  user: {
    title: "用户管理",
    uid: "用户 ID",
    username: "用户名",
    email: "邮箱",
    role: {
      label: "身份",
      0: "游客",
      User: "用户",
      Administrator: "管理员",
    },
    last_login: "上次登录时间",
    operate: {
      title: "操作",
      delete: {
        label: "删除",
        confirm: "确定删除该用户?",
        success: "删除成功",
      },
      set: {
        label: "设为管理",
        confirm: "确认将该用户设为管理?",
        success: "设置成功",
      },
      unset: {
        label: "移除管理",
        confirm: "确认将该用户移除管理?",
        success: "移除成功",
      },
      email: {
        label: "修改邮箱",
        format: "邮箱格式错误",
        success: "邮箱修改成功",
      },
      password: {
        label: "修改密码",
        required: "请输入密码",
        minLength: "密码至少需要 6 个字符",
        maxLength: "密码不能超过 20 个字符",
        format: "密码格式错误",
        success: "密码修改成功",
      },
    },
  },
  cancel: "取消",
  confirm: "确定",
  reload: "刷新",
  invaild: "无效操作",
};
</script>

<style scoped>
.panel {
  height: 100%;
}
.pagination {
  display: flex;
  flex-direction: row;
  margin-right: 10px;
}

.no-padding {
  padding: 0px;
}
</style>
