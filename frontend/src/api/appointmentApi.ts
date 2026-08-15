// frontend/src/api/appointmentApi.ts
import { apiClient } from './client';

export interface BookAppointmentPayload {
    patient_email: string;
    doctor_info_str: string;
    date: string;
    slot: string;
    reason?: string;
}

export interface UpdateStatusPayload {
    appointment_id: number;
    new_status: 'Confirmed' | 'Rejected' | 'Completed';
    doctor_email: string;
}

export const appointmentApi = {
    book: async (payload: BookAppointmentPayload) => {
        const res = await apiClient.post('/appointments/book', payload);
        return res.data;
    },
    getPatientAppointments: async (patientEmail: string) => {
        const res = await apiClient.get(`/appointments/patient/${encodeURIComponent(patientEmail)}`);
        return res.data;
    },
    getDoctorAppointments: async (doctorEmail: string) => {
        const res = await apiClient.get(`/appointments/doctor/${encodeURIComponent(doctorEmail)}`);
        return res.data;
    },
    updateStatus: async (payload: UpdateStatusPayload) => {
        const res = await apiClient.patch('/appointments/status', payload);
        return res.data;
    },
};