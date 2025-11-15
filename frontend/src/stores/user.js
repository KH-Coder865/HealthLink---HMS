import { defineStore } from "pinia";
import api from "@/utils/api";

const useUserStore = defineStore("user", {
    state: () => ({
        token: localStorage.getItem("token") || "",
        user: (() => {
            try {
                const raw = localStorage.getItem("user");
                return raw ? JSON.parse(raw) : null;
            }
            catch (e) {
                console.warn("Failed to parse user from localStorage:", e);
                return null;
            }

        })(),
    }),

    getters: {
        isAuthenticated: (state) => !!state.token,
        role: (state) => (state.user && state.user.role ? state.user.role : null),
        isAdmin: (state) => state.user && state.user.role === 'admin',
    },

    actions: {
        setToken(token) {
            this.token = token;
            if(token){
                localStorage.setItem("token", token);
            } else {
                localStorage.removeItem("token");
            }
        },
        setUser(user) {
            this.user = user;
            if(user){
                localStorage.setItem("user", JSON.stringify(user));
            } else {
                localStorage.removeItem("user");
            }
        },

        logout() {
            this.setToken("");
            this.setUser(null);
        },

        loginWithToken(token, user=null) {
            this.setToken(token);
            if(user) this.setUser(user);
        },

        async loginWithCredentials(endpoint="/auth/login", credentials = {}) {
        const res = await api.post(endpoint, credentials); // res = { token, id, name, email }
        if (!res.token) {
            throw new Error("Login failed: No token received");
        }
        this.setToken(res.token);
        this.setUser(res); // save the full user object
}

    },
});

export default useUserStore;