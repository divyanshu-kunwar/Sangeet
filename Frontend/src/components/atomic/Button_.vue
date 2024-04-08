<script setup>
defineProps({
    label: String,
    icon: String,
    type: String,
    shape:{
        type:String,
        default:'rect'
    },
    size:{
        type:String,
        default:"large"
    },
})
</script>

<template>
    <div :class="'btn '+ type + ' ' + size + ' ' + shape">
        <img v-if="icon" :src="icon"/>
        <span v-if="label">{{ label }}</span>
    </div>
</template>

<style scoped>
    .btn{
        display: flex;
        width: fit-content;
        height: fit-content;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 10px;
        transition: all 0.5s ease-in-out;
        color: var(--fore-1);
    }
    .btn:hover{
        scale: 1.01;
        color: var(--fore-2);
    }
    .small{
        font-size: medium;
        border-radius: 4px;
    }
    .small img{
        width: 24px;
        height: 24px;
    }
    .large{
        font-size: larger;
        border-radius:6px;
    }
    .large img{
        width: 30px;
        height: 30px;
    }

    img , span{
        margin-left: 4px;
        margin-right: 4px;
    }
    .filled{
        background-color: var(--shade);
    }

    .bordered{
        color: var(--fore-0);
        border: 1px solid var(--fore-0);
    }
    .none{
        border: none;
        background-color: transparent;
    }
    .gradient{
        background: var(--gradient);
    }
    .circle{
       border-radius: 100%;
       aspect-ratio: 1;
    }

    .filled:hover{
        background-color: var(--primary);
    }

    .none:hover , .grayscale:hover{
        background-color: var(--back-2);
    }
    .bordered:hover{
        background-color: var(--primary);
        border: 1px solid var(--primary);
    }

    .grayscale{
        background-color: var(--back-1);
    }

</style>