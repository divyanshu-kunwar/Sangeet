<script setup>
import logoIcon from '@/assets/logo.svg'
import Button_ from '../atomic/Button_.vue';

import { useRoute } from 'vue-router';

const curr_route = useRoute().name;

</script>
<template>
    <div class="topHead">
        <router-link :to="'/'">
            <img :src="logoIcon" />
        </router-link>
        
        <div id="actionBtn">
            <router-link v-if="curr_route!='Login'" :to="'/login'">
                <Button_ label="Login" type="bordered" size="small" shape="rectangle" />
            </router-link>
            <router-link v-if="curr_route!='Register'" :to="'/register'">
                <Button_ label="Register" type="bordered" size="small" shape="rectangle" />
            </router-link>
        </div>

    </div>
</template>
<style scoped>

.topHead {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    max-width: 1920px;
    padding: 4rem 8rem 0rem;
    padding: max(4rem, 3%) 8% 0%;
    margin-left: auto;
    margin-right: auto;
}

.topHead div {
    display: flex;
}

.topHead> a >img {
    width: clamp(80px, 10vw, 120px);
}

.topHead div>* {
    margin-left: 20px;
}
</style>