// frontend/src/api/doctorApi.ts
import { apiClient } from './client';

export const doctorApi = {
    getChoices: async () => {
        const res = await apiClient.get('/doctors/choices');
        return res.data;
    },
    searchDoctors: async (params?: { speciality?: string; city?: string }) => {
        const res = await apiClient.get('/doctors/search', { params });
        return res.data;
    },
};