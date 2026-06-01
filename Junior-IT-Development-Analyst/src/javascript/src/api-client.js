class MouraApiClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            headers: { 'Content-Type': 'application/json', ...options.headers },
            ...options,
        };

        if (config.body && typeof config.body === 'object') {
            config.body = JSON.stringify(config.body);
        }

        try {
            const response = await fetch(url, config);
            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.message || `HTTP ${response.status}`);
            }
            return response.status === 204 ? null : await response.json();
        } catch (error) {
            console.error(`API Error [${endpoint}]:`, error);
            throw error;
        }
    }

    // Processos
    getProcesses() {
        return this.request('/api/processes/');
    }

    createProcess(data) {
        return this.request('/api/processes/', { method: 'POST', body: data });
    }

    updateProcessStatus(id, status) {
        return this.request(`/api/processes/${id}`, {
            method: 'PUT',
            body: { ...this.getProcess(id), status },
        });
    }

    deleteProcess(id) {
        return this.request(`/api/processes/${id}`, { method: 'DELETE' });
    }

    // Integração
    syncSystems(source, target, payload) {
        return this.request('/api/integration/sync', {
            method: 'POST',
            body: { source_system: source, target_system: target, payload, action: 'sync' },
        });
    }

    getSystems() {
        return this.request('/api/integration/systems');
    }

    // ML
    predict(features, modelType) {
        return this.request('/api/ml/predict', {
            method: 'POST',
            body: { features, model_type: modelType },
        });
    }

    trainModels() {
        return this.request('/api/ml/train', { method: 'POST' });
    }

    // LLM
    generateText(prompt, context) {
        return this.request('/api/llm/generate', {
            method: 'POST',
            body: { prompt, system_context: context },
        });
    }

    // Health
    healthCheck() {
        return this.request('/health');
    }
}
