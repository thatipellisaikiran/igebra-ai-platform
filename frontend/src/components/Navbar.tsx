import React from 'react';
import { UserCheck, Stethoscope, RefreshCw } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  currentUser: { name: string; role: string; email: string };
  onSwitchUser: (role: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  currentUser,
  onSwitchUser,
}) => {
  const navItems = [
    { id: 'upload', label: '1. Ingest Materials' },
    { id: 'topic-map', label: '2. Topic Map' },
    { id: 'quiz', label: '3. Diagnostic Quiz' },
    { id: 'gap-report', label: '4. Gap Report (Diagnosis)' },
    { id: 'plan', label: '5. Revision Plan' },
    { id: 'explain', label: '6. Grounded Tutor' },
    { id: 'dashboard', label: '7. Progress Dashboard' },
  ];

  return (
    <header className="bg-slate-900 border-b border-slate-800 text-white sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('gap-report')}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-emerald-400 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <Stethoscope className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-bold text-lg tracking-tight">GapFinder AI</span>
                <span className="text-[10px] uppercase font-semibold bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded-full border border-indigo-500/30">
                  Doctor for Studying
                </span>
              </div>
              <p className="text-xs text-slate-400 hidden sm:block">Find what the student doesn't know</p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            {/* Persona Switcher */}
            <div className="flex items-center space-x-2 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700 text-xs">
              <UserCheck className="w-4 h-4 text-emerald-400" />
              <div className="text-left">
                <div className="font-medium text-slate-200">{currentUser.name}</div>
                <div className="text-[10px] text-slate-400 capitalize">{currentUser.role} Mode</div>
              </div>
              <button
                onClick={() => onSwitchUser(currentUser.role === 'student' ? 'teacher' : 'student')}
                title="Switch demo persona"
                className="ml-2 p-1 hover:bg-slate-700 rounded text-slate-400 hover:text-white transition"
              >
                <RefreshCw className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex space-x-1 overflow-x-auto py-2 border-t border-slate-800/60 no-scrollbar">
          {navItems.map((item) => {
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all ${
                  isActive
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                }`}
              >
                {item.label}
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
};

