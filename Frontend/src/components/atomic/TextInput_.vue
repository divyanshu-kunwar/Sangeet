<script setup>
import { ref , watch} from 'vue';
import Button_ from './Button_.vue';

const props = defineProps({
    label: String,
    type: String,
    placeholder: String,
    shape:String,
    icon:String,
    initialValue: String,
    size: {
        type: String,
        default: "small"
    }
})

let inputValue = ref(props.initialValue || "")

watch(() => props.initialValue, (newValue) => {
    inputValue.value = newValue;
});


</script>
<template>

    <div class="textinput">

        <span class="label" v-if="shape != 'search'">
            {{label}}
        </span>
    
        <div>
            <Button_ v-if="type=='number'" />
            <div class="stacked">
                <img v-if="icon" :src="icon" />
                <input :class="size+ ' ' +type + ' ' + shape " :type="type" :placeholder="placeholder"
                v-model="inputValue" @input="$emit('inp' , inputValue)" />
                <Button_ v-if="type=='number'" />
            </div>
        </div>

    </div>

</template>

<style scoped>

.textinput{
    display: flex;
    flex-direction: column;
}

.label{
    margin-bottom: 1rem;
}

input {
    width: 100%;
    height: fit-content;
    background-color: var(--back-1);
    border: none;
    outline: none;
    font-size: large;
    color: var(--fore-0);
    border: 1px solid var(--back-2);
    transition: all 0.8s ease-in-out;
}

input:focus {
    color: var(--fore-2);
    border: 1px solid var(--primary);
}

.large {
    font-size: large;
    padding: 10px 15px;
    border-radius: 6px;
}

.small {
    font-size: medium;
    padding: 6px 15px;
    border-radius: 4px;
}

input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
    -webkit-appearance: none;
}

.search{
    border-radius: 28px;
    padding: 1rem 4rem;
}
.search::placeholder{
    text-align: center;
}
.stacked{
    display: flex;
}

.stacked img{
    margin-right: -3rem;
    z-index: 1;
    opacity: 0.6;
}

.stacked:hover img{
    opacity: 1;
}

</style>