// frontend/src/types/auth.types.ts

export type UserRole = 'Patient' | 'Doctor';

export interface UserSession {
    email: string;
    role: UserRole;
    name: string;
    terms_accepted: boolean;
}

export interface PatientProfile {
    email: string;
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

export interface DoctorProfile {
    email: string;
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