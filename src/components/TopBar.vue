<script setup lang="ts">

import UserIcon from '@src/components/icons/UserIcon.vue';
// import MenuDotsVerticalIcon from '@src/components/icons/MenuDotsVerticalIcon.vue';

</script>

<template>
    <div id="top_bar_cont">
        <div id="avatar_icon_cont">
            <UserIcon fill_color="#FFFFFF" style="width: 24px; height: 24px;" />
        </div>
        <div id="user_info">
            <div id="full_username">Test User</div>
            <div id="user_email">test-user@pertech.com</div>
        </div>
        <div style="flex-grow: 1;"></div>
        <img src="/images/pertech_logo.png" alt="PerTech Logo" style="height: 40px;">
        <!-- <div v-ripple id="menu_ripple">
            <MenuDotsVerticalIcon fill_color="var(--p-primary-color)" style="width: 16px; height: 16px;" />
        </div> -->
    </div>
</template>

<style lang="css" scoped>
#full_username {
    font-size: 16px;
    font-weight: bold;
}

#user_email {
    font-size: 14px;
    color: #757575;
    font-weight: normal;
}

#user_info {
    height: 100%;
    width: fit-content;
    color: var(--p-primary-color);
    margin-left: 8px;
}

#menu_ripple {
    position: relative;
    overflow: hidden;
    --p-ripple-background: #BDBDBD;
    width: 40px;
    height: 40px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
}

#avatar_icon_cont {
    width: 40px;
    height: 40px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    background-color: var(--p-primary-color);
}

#top_bar_cont {
    position: absolute;
    top: 8px;
    left: 2vw;
    width: 96vw;
    padding: 8px 16px;
    box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
    border-radius: 4px;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    background-color: #FFFFFF;
}
</style>