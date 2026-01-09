import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001/v1';

/**
 * Axios client instance for API communication.
 * 
 * Configuration includes:
 * - Base URL for all API requests
 * - Default headers for JSON content type
 * - CORS credentials enabled for cross-origin requests
 * - Request/response interceptors for error handling
 */
const client = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true,  // Enable CORS credentials
    timeout: 30000,  // 30 second timeout
});

/**
 * Request interceptor to add logging and handle errors.
 */
client.interceptors.request.use(
    (config) => {
        console.log(`[API] ${config.method.toUpperCase()} ${config.url}`, config.data);
        return config;
    },
    (error) => {
        console.error('[API] Request error:', error);
        return Promise.reject(error);
    }
);

/**
 * Response interceptor to handle errors and log responses.
 */
client.interceptors.response.use(
    (response) => {
        console.log(`[API] Response ${response.status}:`, response.data);
        return response;
    },
    (error) => {
        if (error.response) {
            // Server responded with error status
            console.error('[API] Response error:', {
                status: error.response.status,
                data: error.response.data,
                url: error.config.url,
            });
            
            // Handle specific error cases
            if (error.response.status === 401) {
                console.error('[API] Unauthorized - Check authentication');
            } else if (error.response.status === 403) {
                console.error('[API] Forbidden - Check permissions');
            } else if (error.response.status === 404) {
                console.error('[API] Not found - Check endpoint URL');
            } else if (error.response.status === 405) {
                console.error('[API] Method not allowed - CORS or routing issue');
            } else if (error.response.status >= 500) {
                console.error('[API] Server error - Check backend logs');
            }
        } else if (error.request) {
            // Request made but no response received
            console.error('[API] No response received:', error.message);
            if (error.message.includes('Network Error')) {
                console.error('[API] Network error - Check if backend is running');
            }
        } else {
            // Error in request configuration
            console.error('[API] Request configuration error:', error.message);
        }
        
        return Promise.reject(error);
    }
);

/**
 * API client object with methods for interacting with the backend.
 */
export const api = {
    /**
     * Create a new session for conversation tracking.
     * 
     * @param {string} userId - User identifier (default: 'demo_user')
     * @returns {Promise<Object>} Session object containing session_id
     * @throws {Error} If session creation fails
     */
    createSession: async (userId = 'demo_user') => {
        try {
            const response = await client.post('/sessions/', {
                user_id: userId
            });
            return response.data; // { session_id: "..." }
        } catch (error) {
            console.error('[API] Error creating session:', error);
            throw error;
        }
    },

    /**
     * Get conversation history for a specific session.
     * 
     * @param {string} sessionId - Session identifier
     * @returns {Promise<Array>} Array of conversation messages
     * @throws {Error} If history retrieval fails
     */
    getSessionHistory: async (sessionId) => {
        try {
            const response = await client.get(`/sessions/${sessionId}/history`);
            return response.data;
        } catch (error) {
            console.error('[API] Error fetching history:', error);
            throw error;
        }
    },

    /**
     * Send a message to the agent and get a response.
     * 
     * @param {string} sessionId - Session identifier for context
     * @param {string} message - User message content
     * @param {string} userId - User identifier (default: 'demo_user')
     * @returns {Promise<Object>} Agent response object
     * @throws {Error} If message sending fails
     */
    sendMessage: async (sessionId, message, userId = 'demo_user') => {
        try {
            const response = await client.post('/chat/completions', {
                messages: [{ role: 'user', content: message }],
                session_id: sessionId,
                user: userId
            });
            return response.data;
        } catch (error) {
            console.error('[API] Error sending message:', error);
            throw error;
        }
    },

    /**
     * Health check endpoint to verify backend is running.
     * 
     * @returns {Promise<Object>} Health status object
     * @throws {Error} If health check fails
     */
    healthCheck: async () => {
        try {
            const response = await client.get('/health');
            return response.data;
        } catch (error) {
            console.error('[API] Health check failed:', error);
            throw error;
        }
    }
};

export default api;
