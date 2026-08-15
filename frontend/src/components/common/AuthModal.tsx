// frontend/src/components/common/AuthModal.tsx
import React, { useState } from 'react';
import { authApi } from '../../api';
import { useAuth } from '../../hooks/useAuth';
import { useToast } from '../../context/ToastContext';
import { X, Lock, Mail, User } from 'lucide-react';
import { Button } from './Button';

export default function AuthModal({ onClose, onLoginSuccess }: { onClose: () => void; onLoginSuccess: () => void }) {
    const [isRegister, setIsRegister] = useState(false);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');
    const [city, setCity] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { setUserSession } = useAuth();
    const { showToast } = useToast();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            if (isRegister) {
                await authApi.registerPatient({ email, password, name, city, language: 'English' });
            }
            const res = await authApi.login({ email, password });
            setUserSession(res.session);
            showToast('Signed in successfully!', 'success');
            onLoginSuccess();
        } catch (err: any) {
            setError(err.message || 'Authentication failed.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-xl border border-slate-100 relative">
                <button onClick={onClose} className="absolute right-4 top-4 text-slate-400 hover:text-slate-600">
                    <X className="w-5 h-5" />
                </button>

                <h3 className="text-xl font-bold text-slate-900 mb-1">
                    {isRegister ? 'Patient Registration' : 'Patient & Doctor Portal'}
                </h3>
                <p className="text-xs text-slate-500 mb-5">Sign in to access your consultations and appointments.</p>

                {error && <div className="p-3 mb-4 rounded-xl bg-rose-50 text-rose-700 text-xs font-semibold">{error}</div>}

                <form onSubmit={handleSubmit} className="space-y-3.5">
                    {isRegister && (
                        <>
                            <div>
                                <label className="text-xs font-semibold text-slate-600">Full Name</label>
                                <div className="relative mt-1">
                                    <User className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
                                    <input
                                        type="text"
                                        required
                                        value={name}
                                        onChange={(e) => setName(e.target.value)}
                                        placeholder="Amit Sharma"
                                        className="w-full pl-9 p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                    />
                                </div>
                            </div>
                            <div>
                                <label className="text-xs font-semibold text-slate-600">City</label>
                                <input
                                    type="text"
                                    required
                                    value={city}
                                    onChange={(e) => setCity(e.target.value)}
                                    placeholder="Nagpur"
                                    className="w-full p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none mt-1"
                                />
                            </div>
                        </>
                    )}

                    <div>
                        <label className="text-xs font-semibold text-slate-600">Email Address</label>
                        <div className="relative mt-1">
                            <Mail className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
                            <input
                                type="email"
                                required
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="patient@example.com"
                                className="w-full pl-9 p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                            />
                        </div>
                    </div>

                    <div>
                        <label className="text-xs font-semibold text-slate-600">Password</label>
                        <div className="relative mt-1">
                            <Lock className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
                            <input
                                type="password"
                                required
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="••••••••"
                                className="w-full pl-9 p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                            />
                        </div>
                    </div>

                    <Button
                        type="submit"
                        isLoading={loading}
                        className="w-full mt-2"
                    >
                        {isRegister ? 'Register Account' : 'Sign In'}
                    </Button>
                </form>

                <div className="mt-4 text-center">
                    <button
                        onClick={() => { setIsRegister(!isRegister); setError(''); }}
                        className="text-xs text-teal-700 hover:underline font-semibold"
                    >
                        {isRegister ? 'Already registered? Sign In' : 'New patient? Create an account'}
                    </button>
                </div>
            </div>
        </div>
    );
}