import React, { useEffect, useState } from 'react';
import { TrendingUp, BarChart3 } from 'lucide-react';
import { api } from '../services/api';

interface DashboardProps {
  currentUserRole: string;
}

export const Dashboard: React.FC<DashboardProps> = ({ currentUserRole }) => {
  const [analytics, setAnalytics] = useState<any>(null);

  useEffect(() => {
    api.getProgress().then(setAnalytics).catch(console.error);
  }, []);

  const attempts = analytics?.attempts_history || [];

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between pb-6 border-b border-slate-800 gap-4">
          <div>
            <div className="flex items-center space-x-2 text-indigo-400 text-xs font-semibold uppercase tracking-wider">
              <BarChart3 className="w-4 h-4" />
              <span>Diagnostic Learning Analytics</span>
            </div>
            <h2 className="text-2xl font-bold text-white tracking-tight mt-1">
              {currentUserRole === 'teacher' ? 'Teacher Analytics Overview' : 'Student Mastery & Progress Trajectory'}
            </h2>
            <p className="text-slate-400 text-sm mt-1">
              Measurable diagnostic improvement across successive diagnostic attempts.
            </p>
          </div>

          <div className="flex items-center space-x-2 bg-emerald-500/10 border border-emerald-500/20 px-3.5 py-2 rounded-xl">
            <TrendingUp className="w-4 h-4 text-emerald-400" />
            <div className="text-xs">
              <span className="text-slate-400">Learning Velocity: </span>
              <strong className="text-emerald-400">
                {analytics ? `${analytics.learning_velocity_pct >= 0 ? '+' : ''}${analytics.learning_velocity_pct}%` : '0%'}
              </strong>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-6">
          <div className="p-4 bg-slate-950/50 rounded-xl border border-slate-800">
            <div className="text-xs text-slate-400">Total Quiz Attempts</div>
            <div className="text-2xl font-bold text-slate-100 mt-2">{attempts.length}</div>
          </div>
          <div className="p-4 bg-slate-950/50 rounded-xl border border-slate-800">
            <div className="text-xs text-slate-400">Strongest Topic</div>
            <div className="text-sm font-bold text-emerald-400 mt-2">{analytics?.strongest_topic || '-'}</div>
          </div>
          <div className="p-4 bg-slate-950/50 rounded-xl border border-slate-800">
            <div className="text-xs text-slate-400">Most Critical Gap</div>
            <div className="text-sm font-bold text-rose-400 mt-2">{analytics?.most_critical_gap || '-'}</div>
          </div>
        </div>

        <div className="mt-8">
          <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-3">
            Historical Attempt Timeline
          </h3>
          <div className="border border-slate-800 rounded-xl overflow-hidden divide-y divide-slate-800 bg-slate-950/40">
            {attempts.length === 0 ? (
              <div className="p-6 text-center text-xs text-slate-500">No quiz attempts recorded yet.</div>
            ) : (
              attempts.map((att: any) => (
                <div key={att.attempt_index} className="p-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                  <div>
                    <h4 className="text-sm font-semibold text-slate-200">Attempt #{att.attempt_index}</h4>
                    <span className="text-xs text-slate-500">{new Date(att.timestamp).toLocaleString()}</span>
                  </div>
                  <div className="text-sm font-bold text-indigo-300">{att.overall_score_pct}%</div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
