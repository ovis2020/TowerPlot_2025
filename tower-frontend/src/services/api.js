import axios from 'axios';

const API_URL = '/api';  // Automatically uses Vite proxy

export const getTowerData = async (towerId) => {
    try {
        const response = await axios.get(`${API_URL}/download_json/${towerId}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching tower data:", error);
        return null;
    }
};

export const createTower = async (towerData) => {
    try {
        const response = await axios.post(`${API_URL}/`, towerData);
        return response.data;
    } catch (error) {
        console.error("Error creating tower:", error);
        return null;
    }
};
                                     