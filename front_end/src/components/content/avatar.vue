<template>
  <el-upload
    ref="uploadRef"
    :action="url"
    :headers="header"
    method="post"
    :show-file-list="false"
    :before-upload="beforeAvatarUpload"
    accept="image/jpeg, image/jpg, image/png, image/gif"
    :on-success="handleAvatarSuccess"
  >
    <div style="margin: 0 auto">
      <el-avatar :size="150" :src="userInfo.avatar" />
    </div>
  </el-upload>
</template>

<script setup lang="ts">
import { useUserInfo } from "@/stores/userInfo";
import { Local } from "@/utils/storage";
import type { UploadProps } from "element-plus";
import { UploadInstance } from "element-plus";

const userInfo = useUserInfo();
const url = import.meta.env.VITE_APP_BASE_API + "/api/operate/upload/";
const header = reactive({
  Authorization: `${Local.get("Bearer")?.Bearer ?? ""}`,
});
const allowTypes = ["image/jpeg", "image/jpg", "image/png", "image/gif"];

const beforeAvatarUpload: UploadProps["beforeUpload"] = (rawFile) => {
  if (!allowTypes.includes(rawFile.type)) {
    ElMessage({
      message: "头像格式限制: jpeg, jpg, png, gif",
      type: "error",
    });
    // ElMessage.error("头像格式限制: jpeg, jpg, png, gif");
    return false;
  } else if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage({
      message: "头像大小限制: 2M",
      type: "error",
    });
    // ElMessage.error("头像大小限制: 2M");
    return false;
  }
  return true;
};

const uploadRef = ref<UploadInstance>();
const upload = () => {
  uploadRef.value?.$el.querySelector("input").click();
};

const handleAvatarSuccess: UploadProps["onSuccess"] = (response) => {
  if (response.success == true) {
    userInfo.setAvatar(response.avatar);
  } else {
    ElMessage.error(response.reason);
  }
};

defineExpose({
  upload,
});
</script>
