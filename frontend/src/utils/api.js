import router from "@/router";

const URL = "http://192.168.137.1:5000/api"
// const URL = "http://localhost:5000/api"

const api = {
    async request(endpoint, options = {}) {
        const path = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
        const url = `${URL}${path}`;
        const token = localStorage.getItem("token");

        const headers = {
            "Content-Type": "application/json",
            ...options.headers,
        };

        if (token) {
            headers["Authentication-Token"] = token;
        }

        const config = {
            ...options,
            headers,
        };

        try {
            const res = await fetch(url, config);

            if (res.status === 401) {
                alert("Unauthorized! Please login again.");
                router.push("/login");
                throw new Error("Unauthorized");
            }

            if (res.status === 404) {
                alert("URL not found!");
                throw new Error("404 Not found");
            }

            if (res.status === 403) {
                alert("Access denied! You do not have the required role.");
                throw new Error("Forbidden");
            }

            if (!res.ok) {
                let errorMessage = "API request failed";
                try {
                    const errorData = await res.json();
                    errorMessage = errorData.message || errorMessage;
                } catch (err) {}
                throw new Error(errorMessage);
            }

            if (res.status === 204) return null;

            const text = await res.text();
            if (!text) return null;

            try {
                return JSON.parse(text);
            } catch {
                return text;
            }

        } catch (err) {
            return Promise.reject(err);
        }
    },

    get(endpoint, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: "GET",
        });
    },

    post(endpoint, data = {}, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: "POST",
            body: JSON.stringify(data),
        });
    },

    put(endpoint, data = {}, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: "PUT",
            body: JSON.stringify(data),
        });
    },

    patch(endpoint, data = {}, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: "PATCH",
            body: JSON.stringify(data),
        });
    },

    delete(endpoint, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: "DELETE",
        });
    },
};

export default api;
