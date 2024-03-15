import {defineStore} from 'pinia'
export const userStore = defineStore({
    id: 'user',
    state: () => {
        return {
            token: localStorage.getItem('token') || '',
            right: localStorage.getItem('right') || '',
        }
    },
    getters: {
        isLogin: (state) => !!state.token,
    },
})