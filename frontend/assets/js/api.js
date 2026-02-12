// ========== CONFIGURACIÓN GLOBAL DE API ==========
const API_CONFIG = {
    baseURL: 'http://127.0.0.1:8000',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
};

// ========== CLIENTE HTTP ==========
const api = {
    // GET request
    async get(endpoint) {
        try {
            const response = await fetch(`${API_CONFIG.baseURL}${endpoint}`, {
                method: 'GET',
                headers: this.getHeaders()
            });
            return this.handleResponse(response);
        } catch (error) {
            return this.handleError(error);
        }
    },

    // POST request
    async post(endpoint, data, isFormData = false) {
        try {
            const headers = this.getHeaders();
            if (isFormData) {
                delete headers['Content-Type'];
            }
            
            const response = await fetch(`${API_CONFIG.baseURL}${endpoint}`, {
                method: 'POST',
                headers: headers,
                body: isFormData ? data : JSON.stringify(data)
            });
            return this.handleResponse(response);
        } catch (error) {
            return this.handleError(error);
        }
    },

    // PUT request
    async put(endpoint, data, isFormData = false) {
        try {
            const headers = this.getHeaders();
            if (isFormData) {
                delete headers['Content-Type'];
            }
            
            const response = await fetch(`${API_CONFIG.baseURL}${endpoint}`, {
                method: 'PUT',
                headers: headers,
                body: isFormData ? data : JSON.stringify(data)
            });
            return this.handleResponse(response);
        } catch (error) {
            return this.handleError(error);
        }
    },

    // DELETE request
    async delete(endpoint) {
        try {
            const response = await fetch(`${API_CONFIG.baseURL}${endpoint}`, {
                method: 'DELETE',
                headers: this.getHeaders()
            });
            return this.handleResponse(response);
        } catch (error) {
            return this.handleError(error);
        }
    },

    // Headers con autorización
    getHeaders() {
        const headers = { ...API_CONFIG.headers };
        const token = localStorage.getItem('token');
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    },

    // Manejar respuesta
    async handleResponse(response) {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    },

    // Manejar error
    handleError(error) {
        console.error('API Error:', error);
        throw error;
    }
};

// ========== SERVICIOS API ==========
const serviciosAPI = {
    getAll: () => api.get('/servicios'),
    getPublic: () => api.get('/servicios'),
    getAdmin: () => api.get('/admin/servicios'),
    create: (formData) => api.post('/admin/servicios/', formData, true),
    update: (id, formData) => api.put(`/admin/servicios/${id}`, formData, true),
    delete: (id) => api.delete(`/admin/servicios/${id}`)
};

// ========== CITAS API ==========
const citasAPI = {
    create: (data) => api.post('/citas', data),
    getAll: () => api.get('/citas'),
    cancel: (id) => api.delete(`/citas/${id}`),
    confirm: (id) => api.patch(`/citas/${id}/confirmar`, {})
};

// ========== DISPONIBILIDAD API ==========
const disponibilidadAPI = {
    get: (fecha) => api.get(`/disponibilidad?fecha=${fecha}`)
};

// ========== AUTENTICACIÓN API ==========
const authAPI = {
    login: (username, password) => {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        return api.post('/auth/login', formData, true);
    },
    register: (userData) => api.post('/auth/register', userData),
    me: () => api.get('/auth/me')
};