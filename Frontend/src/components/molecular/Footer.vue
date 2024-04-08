<template>
    <div id="footer">
            <a>Term Of Service</a>
            <a href="">Handicrafted With ❤️ in India</a>
            <a href="">Privacy Policy</a>
    </div>
</template>

<script>
</script>

<style scoped>
    #footer{
        display: flex;
        align-items: center;
        justify-content: space-evenly;
        padding: 10px;
        text-align: center;
        flex-direction: row;
        flex-wrap: wrap;
    }
    a{
        display: block;
        margin: 4px;
        color: var(--text2);
        opacity: 0.5;
        font-size: small;
    }
    a:hover{
        opacity: 0.8;
        color: var(--shade);
    }

    @media only screen and (min-width: 750px) {
        a{
            font-size: medium;
        }
    }
</style>