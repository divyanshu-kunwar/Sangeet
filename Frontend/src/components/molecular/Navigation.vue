<script setup>
import { computed } from 'vue'

import { useRouter } from 'vue-router';
const router = useRouter();
const curr_route = computed(() => router.currentRoute.value.name);

defineProps({
    navigations: Array
})
</script>

<template>
    <div class="navigation">
        <RouterLink v-for="navItem in navigations" :key="navItem.route"
            :class="curr_route == navItem.route ? 'navItem navSelected cursor' : 'navItem cursor'"
            :to="{ name: navItem.route }">
            <img :src="curr_route == navItem.route ? navItem.Icon_selected : navItem.Icon" />
            <span>{{ navItem.name }}</span>
        </RouterLink>
    </div>
</template>

<style scoped>
.navigation {
    display: flex;
    flex-direction: column;
    align-items: start;
    justify-content: center;
    padding: 1rem;
}

.navItem {
    display: flex;
    align-items: center;
    width: 100%;
    padding: 0.5rem 8%;
    color: var(--fore-0);
    transition: all 0.2s linear;
    margin: 8px 0px;
}

.navSelected {
    color: var(--fore-2);
}

.navItem img {
    height: 26px;
    margin-right: 8%;
    filter: brightness(80%);
}

.navSelected img {
    filter: brightness(100%);
}
</style>