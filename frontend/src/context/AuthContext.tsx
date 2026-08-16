// frontend/src/context/AuthContext.tsx
import React, { createContext, useState, useEffect } from 'react';
import type { UserSession } from '../types';
import { authApi, type LoginPayload } from '../api';


interface AuthContextType {
    user: UserSession | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (credentials: LoginPayload) => Promise<void>;
    logout: () => void;
    setUserSession: (session: UserSession | null) => void;
    register: (payload: any) => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

const AUTH_STORAGE_KEY = 'vaiddisha_user_session';

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<UserSession | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(true);

    // Restore session from localStorage on initial mount
    useEffect(() => {
        try {
            const stored = localStorage.getItem(AUTH_STORAGE_KEY);
            if (stored) {
                setUser(JSON.parse(stored));
            }
        } catch (e) {
            console.error('Failed to parse stored session:', e);
            localStorage.removeItem(AUTH_STORAGE_KEY);
        } finally {
            setIsLoading(false);
        }
    }, []);

    const setUserSession = (session: UserSession | null) => {
        setUser(session);
        if (session) {
            localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(session));
        } else {
            localStorage.removeItem(AUTH_STORAGE_KEY);
        }
    };

    const login = async (credentials: LoginPayload) => {
        setIsLoading(true);
        try {
            const response = await authApi.login(credentials);
            if (response && response.session) {
                setUserSession(response.session);
            } else {
                throw new Error(response.message || 'Login failed');
            }
        } finally {
            setIsLoading(false);
        }
    };

    const logout = () => {
        setUserSession(null);
    };

    const register = async (payload: any) => {
        setIsLoading(true);
        try {
            if (payload.role === 'doctor') {
                await authApi.registerDoctor({
                    email: payload.email,
                    password: payload.password,
                    name: payload.name,
                    speciality: payload.speciality,
                    qualification: payload.qualification,
                    hospital: payload.hospital,
                    fee: payload.fee,
                    city: payload.city,
                    experience: '1',
                });
            } else {
                await authApi.registerPatient({
                    email: payload.email,
                    password: payload.password,
                    name: payload.name,
                    city: payload.city,
                });
            }

            // Auto login after registration
            const response = await authApi.login({
                email: payload.email,
                password: payload.password,
            });
            if (response && response.session) {
                setUserSession(response.session);
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                isAuthenticated: !!user,
                isLoading,
                login,
                logout,
                setUserSession,
                register,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};