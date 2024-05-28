
// From: https://profy.dev/article/react-architecture-api-client
class APIClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    async request(url, options) {
        const response = await fetch(`${this.baseURL}${url}`, options);
        if (!response.ok) {
            const error = new Error('HTTP Error');
            error.status = response.status;
            error.response = await response.json();
            throw error;
        }
        return response.json();
    }

    get(url, params) {
        url = params ? url + '?' + params : url;
        return this.request(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
    }

    post(url, data) {
        return this.request(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
    }

    // You can add more methods (put, delete, etc.) here as needed
}

export const apiClient = new APIClient(`${import.meta.env.VITE_BACKEND_URL}:${import.meta.env.VITE_BACKEND_PORT}/api`);