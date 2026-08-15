// frontend/src/api/authApi.ts
import { apiClient } from './client';

export interface LoginPayload {
    email: string;
    password: string;
}

export interface PatientRegisterPayload {
    email: string;
    password: string;
    name: string;
    gender?: string;
    age?: number;
    country?: string;
    state?: string;
    city?: string;
    postal_code?: string;
    phone?: string;
    language?: string;
    conditions?: string;
    surgeries?: string;
    allergies?: string;
}

export interface DoctorRegisterPayload {
    email: string;
    password: string;
    name: string;
    speciality: string;
    qualification: string;
    experience: string;
    hospital: string;
    country?: string;
    state?: string;
    city?: string;
    postal_code?: string;
    phone?: string;
    fee: string;
    description?: string;
}

export const authApi = {
    login: async (payload: LoginPayload) => {
        const res = await apiClient.post('/auth/login', payload);
        return res.data;
    },
    registerPatient: async (payload: PatientRegisterPayload) => {
        const res = await apiClient.post('/auth/register/patient', payload);
        return res.data;
    },
    registerDoctor: async (payload: DoctorRegisterPayload) => {
        const res = await apiClient.post('/auth/register/doctor', payload);
        return res.data;
    },
    acceptTerms: async (email: string) => {
        const res = await apiClient.post('/auth/terms/accept', { email });
        return res.data;
    },
};