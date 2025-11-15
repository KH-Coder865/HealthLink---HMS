import router from "@/router";

const URL = "http://localhost:5000/api"

const api = {
    async request(endpoint, options = {}) {
        const path = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
        const url = `${URL}${path}`;
        const token = localStorage.getItem("token");
        console.log(token)
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };
        if (token) {
            headers['Authentication-Token'] = token;
        }
        const config = {
            ...options,
            headers,
        };

        try {
            const res = await fetch(url, config);
            if (res.status === 401) {
                alert("Unauthorized! Please login again.");
                router.push('/login');
                throw new Error("Unauthorized");
            }

            if (!res.ok) {
                const errorData = await res.json();
                const errorMessage = errorData.message || 'API request failed';
                throw new Error(errorMessage);
            }

            if (res.status === 204) {
                return null; // No Content
            }
            const text = await res.text();
            if (!text) return null;
            try {
                return JSON.parse(text);
            } catch (e) {
                return text
            }
        }
        catch (e) {
            return Promise.reject(e);
        }
    },

    get(endpoint, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: 'GET',
        });
    },

    post(endpoint, data = {}, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    put(endpoint, data = {}, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },

    delete(endpoint, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: 'DELETE',
        });
    }

};

export default api;