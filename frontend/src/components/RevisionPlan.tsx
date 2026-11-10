import React, { useState } from 'react';
import { Calendar, Clock, CheckSquare, Sparkles, ArrowRight } from 'lucide-react';
import { RevisionPlanResponse } from '../types';

interface RevisionPlanProps {
  plan: RevisionPlanResponse | null;
  onUpdateBudget: (days: number, dailyHours: number) => Promise<void>;
  onExplainTopic: (topicId: string, topicTitle: string) => void;
  onRetestTopic: () => void;
}

export const RevisionPlan: React.FC<RevisionPlanProps> = ({
  plan,
  onUpdateBudget,
  onExplainTopic,
  onRetestTopic,
}) => {
  const [days, setDays] = useState(plan?.available_days || 5);
  const [hours, setHours] = useState(plan?.daily_hours || 2.0);
  const [isUpdating, setIsUpdating] = useState(false);

  if (!plan) {
    return (
      <div className="p-8 text-center text-slate-400 bg-slate-900 border border-slate-800 rounded-2xl">
        Generating personalized revision trajectory...
      </div>
    );
  }

  const handleApply = async () => {
    setIsUpdating(true);
    try {
      await onUpdateBudget(days, hours);
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between pb-6 border-b border-slate-800 gap-4">
          <div>
            <div className="flex items-center space-x-2 text-indigo-400 text-xs font-semibold uppercase tracking-wider">
              <Sparkles className="w-4 h-4" />
              <span>Prioritized Treatment Plan</span>
            </div>
            <h2 className="text-2xl font-bold text-white tracking-tight mt-1">
              Personalized Revision Roadmap
            </h2>
            <p className="text-slate-400 text-sm mt-1">
              Order determined by gap severity + exam weightage. Automatically updates as you re-test and improve.
            </p>
          </div>

          <button
            onClick={onRetestTopic}
            className="flex items-center space-x-2 px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-sm font-semibold shadow-lg shadow-emerald-600/30 transition self-start sm:self-auto"
          >
            <span>Retest to Update Plan</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        {/* Budget Controller */}
        <div className="mt-6 bg-slate-950/50 p-5 rounded-xl border border-slate-800 grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
          <div>
            <label className="text-xs font-semibold text-slate-300 flex items-center space-x-1.5">
              <Calendar className="w-3.5 h-3.5 text-indigo-400" />
              <span>Available Days to Exam: <strong className="text-indigo-400">{days} Days</strong></span>
            </label>
            <input
              type="range"
              min="1"
              max="14"
              value={days}
              onChange={(e) => setDays(Number(e.target.value))}
              className="w-full mt-2 accent-indigo-500 cursor-pointer"
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-300 flex items-center space-x-1.5">
              <Clock className="w-3.5 h-3.5 text-indigo-400" />
              <span>Daily Study Time: <strong className="text-indigo-400">{hours} Hours/day</strong></span>
            </label>
            <input
              type="range"
              min="0.5"
              max="8"
              step="0.5"
              value={hours}
              onChange={(e) => setHours(Number(e.target.value))}
              className="w-full mt-2 accent-indigo-500 cursor-pointer"
            />
          </div>

          <div className="flex items-center space-x-3 md:justify-end">
            <div className="text-right mr-2">
              <span className="text-xs text-slate-400">Total Revision Budget</span>
              <div className="text-base font-bold text-slate-200">{(days * hours).toFixed(1)} Hours</div>
            </div>
            <button
              onClick={handleApply}
              disabled={isUpdating}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold shadow-md shadow-indigo-600/20 transition disabled:opacity-50"
            >
              {isUpdating ? 'Recalculating...' : 'Recalculate Plan'}
            </button>
          </div>
        </div>

        {/* Schedule Timeline */}
        <div className="mt-8 space-y-4">
          <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Daily Study Schedule ({plan.schedule.length} Days)
          </div>

          {plan.schedule.map((item) => (
            <div
              key={item.day}
              className="p-5 rounded-xl border border-slate-800 bg-slate-950/40 hover:border-slate-700 transition flex flex-col md:flex-row md:items-center md:justify-between gap-4"
            >
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex flex-col items-center justify-center text-indigo-300 font-bold shrink-0">
                  <span className="text-[10px] uppercase font-semibold text-indigo-400">Day</span>
                  <span className="text-lg leading-none">{item.day}</span>
                </div>

                <div>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                      Priority #{item.priority_order}
                    </span>
                    <span className="text-xs font-semibold">{item.status_tag}</span>
                    <span className="text-xs text-slate-500">•</span>
                    <span className="text-xs text-amber-400/90 font-medium">{item.exam_weight_desc}</span>
                  </div>

                  <h3 className="text-base font-semibold text-slate-100 mt-1">{item.topic_title}</h3>

                  <ul className="mt-2 space-y-1 text-xs text-slate-400">
                    {item.target_actions.map((act, idx) => (
                      <li key={idx} className="flex items-center space-x-1.5">
                        <CheckSquare className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
                        <span>{act}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="flex items-center space-x-3 self-end md:self-center">
                <div className="text-right">
                  <div className="text-xs text-slate-400">Allocated Time</div>
                  <div className="text-sm font-bold text-indigo-300">{item.allocated_hours} hrs</div>
                </div>

                <button
                  onClick={() => onExplainTopic(item.topic_id, item.topic_title)}
                  className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-medium border border-slate-700 transition"
                >
                  Open Tutor
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

