import { writable } from 'svelte/store'

const persist_storage = (key, initValue) => {
    const storedValueStr = sessionStorage.getItem(key)
    const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue)
    store.subscribe((val) => {
        sessionStorage.setItem(key, JSON.stringify(val))
    })
    return store
}

export const page = persist_storage("page", 0)
export const keyword = persist_storage("keyword", "")
export const access_token = persist_storage("access_token", "")
export const username = persist_storage("username", "")
export const nickname = persist_storage("nickname", "")
export const is_login = persist_storage("is_login", false)

export function resetUserStore() {
    access_token.set('');
    username.set('');
    is_login.set(false);
    nickname.set('');
    page.set(0);
    keyword.set('');
}