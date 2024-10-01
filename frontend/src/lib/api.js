import qs from "qs";     // frontend % npm install qs
import { access_token, username, nickname, is_login } from "./store";
import { get } from "svelte/store";
import { push } from "svelte-spa-router";

async function fastapi(operation, url, params, success_callback, failure_callback) {
    let method = operation;
    let content_type = 'application/json';
    let body = JSON.stringify(params);

    if(operation === 'login') {
        method = 'post';
        content_type = 'application/x-www-form-urlencoded';
        body = qs.stringify(params);
    }

    let _url = import.meta.env.VITE_SERVER_URL+url;
    if(method === 'get') {
        _url += "?" + new URLSearchParams(params);
    }

    let options = {
        method: method,
        headers: {
            "Content-Type": content_type
        }
    };

    const _access_token = get(access_token)
    if (_access_token) {
        options.headers["Authorization"] = "Bearer " + _access_token;
    }

    if (method !== 'get') {
        options['body'] = body;
    }

    try {
        const response = await fetch(_url, options);
        
        // 204 No Content 처리
        if (response.status === 204) {
            if(success_callback) {
                success_callback();
            }
            return null;
        }

        // 성공 응답 처리
        if (response.ok) {
            const data = await response.json();
            if (success_callback) {
                success_callback(data);
            } 
            return data;
        }
        
        // token time out
        if (operation !== 'login' && response.status == 401) { 
            access_token.set('');
            username.set('');
            nickname.set('');
            is_login.set(false);
            alert("로그인이 필요합니다.");
            push('/user-login');
            return;
        }

        // 실패 응답 처리
        const errorData = await response.json();
        throw errorData;

    } catch (error) {
        // 실패 콜백 호출
        if (failure_callback) {
            failure_callback(error);
        } else {
            alert(JSON.stringify(error));
        }
    }

};

export default fastapi;