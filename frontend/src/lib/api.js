import qs from "qs"     // frontend % npm install qs

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
