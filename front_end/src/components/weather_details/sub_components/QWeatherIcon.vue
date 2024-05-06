<template>
    <SvgIcon :name="`${ icon }${ fill ? '-fill' : '' }`" :size="size"/>
</template>

<script setup>
import SvgIcon from 'svg-icon';
defineProps({
    icon: { type: Number },
    size: { type: Number },
    fill: { type: Boolean, default: false }
})
</script>

<style scoped>
</style>
