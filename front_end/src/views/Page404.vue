<template>
  <div
    class="flex items-center justify-center w-screen h-screen bg-gradient-to-r from-blue-400/80 to-red-500/80"
  >
    <div class="text-center">
      <h1 class="font-extrabold text-white text-9xl">404</h1>
      <p class="text-white text-3xl mt-4">
        Sorry, the page you're looking for cannot be found
      </p>
      <router-link to="/">
        <el-button
          class="mt-8 font-bold py-2 px-4 rounded shadow-lg hover:shadow-xl transition duration-200"
          type="primary"
          round
          >Go Home</el-button
        >
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "NotFoundPage",
};
</script>
