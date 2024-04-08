<script setup>
import {useRouter} from 'vue-router'
const router = useRouter()
defineProps({
    label:String,
    image:String,
    artist:String,
    href:String,
})

function navigate(href){
    if(href)
        router.push({path:href})
}

</script>
<template>
    <div class="listItem cursor" >
        <img :src="image"  />
        <div class="vertical" @click="navigate(href)">
            <span class="label">{{label}}</span>
            <span class="artist">{{artist}}</span>
        </div>
    </div>
</template>

<style scoped>
    .listItem{
        display: flex;
        padding: 0px 10px;
        align-items: center;
    }
    .listItem:hover{
        color: var(--fore-2);
    }
    .listItem > img{
        width: 50px;
        height: 50px;
        border-radius: 4px;
    }
    .vertical{
        display: flex;
        flex-direction: column;
        margin-left: 1rem;
    }
    .label{
        max-width: 180px;
        font-size: medium;
        text-wrap: nowrap;
        overflow-x: hidden;
        text-overflow: ellipsis;
    }

    .artist{
        max-width: 180px;
        font-size: small;
        text-wrap: nowrap;
        overflow-x: hidden;
        text-overflow: ellipsis;
    }

</style>