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
        users: [],
        singuser: null,
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

        async register(endpoint, credentials) {
            const res = await api.post(endpoint, credentials);
            if (!res.token) {
                throw new Error("Registration failed: No token received");
            }
            this.setToken(res.token);
            this.setUser(res);
            
        },

        

        async loginWithCredentials(endpoint="/auth/login", credentials = {}) {
            const res = await api.post(endpoint, credentials); // res = { token, id, name, email }
            if (!res.token) {
                throw new Error("Login failed: No token received");
            }
            console.log(res)
            if(res.active) {
                this.setToken(res.token);
                this.setUser(res); // save the full user object
            }
            return res;
        },


        async getAll(){
            const res=await api.get("/users");
            this.users=res;
            return res;
        },
        
        async getbyId(id){
            const res=await api.get(`/users/${id}`);
            this.singuser=res;
            return res;
        },

        async del(id){
            const res=await api.delete(`/users/${id}`);
            this.getAll(); 
            return res;
        },

        async update(id,data){
            const res=await api.put(`/users/${id}`, data);
            this.getAll();
            this.singuser = res; // Update the single user state
            console.log("Updated user:", this.singuser);
            return res;
        },

        async edit(id,data){
            const res=await api.patch(`/users/${id}`, data);
            this.getAll(); // Refresh the user list after editing
            this.singuser = res; // Update the single user state
            console.log("Updated user:", this.singuser);
            return res;
        },

    },
});

export default useUserStore;