// frontend/src/types/appointment.types.ts

export type AppointmentStatus = 'Pending' | 'Confirmed' | 'Rejected' | 'Completed';

export interface Appointment {
    id: number;
    patient_email: string;
    patient_name?: string;
    doctor_email: string;
    doctor_name?: string;
    date: string;
    slot: string;
    reason?: string;
    status: AppointmentStatus;
    created_at: string;
}