<script setup>
import { onUnmounted, onMounted } from 'vue';

const emits = defineEmits(['clickedOut']);

function out(e) {
    if (!e.target.closest('.floatingMenu')) {
        emits('clickedOut')
    }
}
// after completely loaded 
onMounted(() => {
    // after completely loaded
    setTimeout(() => {
        document.addEventListener('click', (e) => out(e))
    }, 200)
})


// remove event listener
onUnmounted(() => {
    console.log("unmounted")
    document.removeEventListener('click', (e) => out(e))
})

</script>
<template>
    <div class="floatingMenu">
        <slot></slot>
    </div>
</template>

<style scoped>
.floatingMenu {
    position: fixed;
    display: inline-flex;
    flex-direction: column;
    z-index: 100;
}
</style>
