<script setup>
import { ref , watch } from 'vue';

const emits = defineEmits(['selectionChange']);

const props = defineProps({
    options: Array,
    label: String,
    initialValue: Array
})

const selected = ref(props.initialValue || [])

const addToSelected = (event) => {
    const value = parseInt(event.target.value.trim());
    if (!selected.value.includes(value)) {
        selected.value.push(value);
    }

    emits('selectionChange', selected.value);
    
}

const removeFromSelected = (index) => {
    selected.value.splice(index, 1);
    emits('selectionChange', selected.value);
}

watch(() => props.initialValue, (newValue) => {
    selected.value = newValue;
});

</script>

<template>
    <div class="selectC">
        <div class="label">{{ label }}</div>
        <select @change="addToSelected" @click="addToSelected">
            <option v-for="(option, index) in options" :value="index">{{ option }}</option>
        </select>
        <div class="selected">
            <div @click="removeFromSelected(index)" class="tags" v-for="(option, index) in selected" :key="index">
                <span class="tagLabel">{{ options[option ] }}</span>
            </div>
        </div>
    </div>
</template>

<style scoped>
.selectC {
    display: flex;
    flex-direction: column;
}
.label {
    margin: 10px 0px;
}
select {
    min-width: 300px;
    margin-right: 1rem;
    font-size: large;
    padding: 0.5rem;
    background-color: var(--back-1);
    border: none;
    color: var(--fore-0);
    margin-bottom: 10px;
}
select:focus {
    outline: none;
}
.selected {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    padding: 4px 0px;
}
.tags{
    display: flex;
    margin: 4px 0px;
    margin-right: 8px;
    padding: 8px 16px;
    background-color: var(--back-1);
    border-radius: 20px;
}

</style>
