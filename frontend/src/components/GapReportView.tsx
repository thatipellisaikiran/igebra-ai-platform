import React from 'react';
import { AlertOctagon, AlertTriangle, CheckCircle2, ArrowRight, MessageSquareText, ShieldAlert } from 'lucide-react';
import { GapReportResponse } from '../types';

interface GapReportViewProps {
  gapReport: GapReportResponse | null;
  onGeneratePlan: () => void;
  onExplainTopic: (topicId: string, topicTitle: string) => void;
}

export const GapReportView: React.FC<GapReportViewProps> = ({
  gapReport,
  onGeneratePlan,
  onExplainTopic,
}) => {
  if (!gapReport) {
    return (
      <div className="p-8 text-center text-slate-400 bg-slate-900 border border-slate-800 rounded-2xl">
        Loading Diagnostic Gap Report...
      </div>
    );
  }

  const { summary, weak_topics, medium_topics, strong_topics } = gapReport;

  return (
    <div className="space-y-6">
      {/* Overview Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6 pb-6 border-b border-slate-800">
          <div>
            <div className="flex items-center space-x-2 text-rose-400 text-xs font-semibold tracking-wider uppercase">
              <ShieldAlert className="w-4 h-4" />
              <span>Core Diagnostic Output</span>
            </div>
            <h2 className="text-2xl font-bold text-white tracking-tight mt-1">
              Knowledge Gap Diagnosis: {gapReport.student_name}
            </h2>
            <p className="text-slate-400 text-sm mt-1">
              "A student can't ask about a gap they don't know they have." Here is your clinical study diagnosis.
            </p>
          </div>

          <button
            onClick={onGeneratePlan}
            className="flex items-center space-x-2 px-5 py-2.5 bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 text-white rounded-xl text-sm font-semibold shadow-lg shadow-indigo-600/30 transition self-start md:self-auto"
          >
            <span>Build Prioritized Revision Plan</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        {/* 3 Metric Summary Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 mt-6">
          <div className="bg-rose-950/20 border border-rose-500/30 rounded-xl p-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-rose-300 uppercase">🔴 Weak Topics</span>
              <AlertOctagon className="w-4 h-4 text-rose-400" />
            </div>
            <div className="text-2xl font-extrabold text-rose-400 mt-2">{summary.weak_count}</div>
            <p className="text-[11px] text-rose-300/80 mt-1">Requires immediate intervention</p>
          </div>

          <div className="bg-amber-950/20 border border-amber-500/30 rounded-xl p-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-amber-300 uppercase">🟡 Medium Topics</span>
              <AlertTriangle className="w-4 h-4 text-amber-400" />
            </div>
            <div className="text-2xl font-extrabold text-amber-400 mt-2">{summary.medium_count}</div>
            <p className="text-[11px] text-amber-300/80 mt-1">Partly understood; formula review</p>
          </div>

          <div className="bg-emerald-950/20 border border-emerald-500/30 rounded-xl p-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-emerald-300 uppercase">🟢 Strong Topics</span>
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="text-2xl font-extrabold text-emerald-400 mt-2">{summary.strong_count}</div>
            <p className="text-[11px] text-emerald-300/80 mt-1">Exam ready; periodic refresher</p>
          </div>

          <div className="bg-slate-800/60 border border-slate-700 rounded-xl p-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-300 uppercase">Preparedness</span>
              <span className="text-xs text-indigo-400 font-bold">Overall</span>
            </div>
            <div className="text-2xl font-extrabold text-white mt-2">{summary.overall_preparedness_pct}%</div>
            <p className="text-[11px] text-slate-400 mt-1">Based on diagnostic responses</p>
          </div>
        </div>

        {/* Section 1: 🔴 Weak Topics (Needs Serious Work) */}
        <div className="mt-10">
          <div className="flex items-center space-x-2 mb-4">
            <span className="w-3 h-3 rounded-full bg-rose-500 inline-block animate-pulse"></span>
            <h3 className="text-lg font-bold text-slate-100">🔴 Weak Topics (Needs Serious Work)</h3>
          </div>

          <div className="space-y-3">
            {weak_topics.map((item) => (
              <div
                key={item.topic_id}
                className="p-5 rounded-xl border border-rose-500/30 bg-rose-950/10 hover:border-rose-500/50 transition flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
              >
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <h4 className="font-semibold text-slate-100 text-sm">{item.title}</h4>
                    <span className="text-[11px] font-bold px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30">
                      Mastery: {Math.round(item.mastery_score * 100)}%
                    </span>
                  </div>

                  <div className="mt-2 text-xs text-rose-200/90 leading-relaxed bg-rose-950/30 p-2.5 rounded-lg border border-rose-900/40">
                    <strong>Diagnostic Reason:</strong> {item.diagnostic_reason}
                  </div>

                  <div className="mt-2 text-xs text-slate-400">
                    <span className="text-slate-300 font-medium">Prescription:</span> {item.recommended_action}
                  </div>
                </div>

                <div className="flex items-center space-x-2 self-end sm:self-center">
                  <button
                    onClick={() => onExplainTopic(item.topic_id, item.title)}
                    className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-semibold border border-slate-700 transition"
                  >
                    <MessageSquareText className="w-3.5 h-3.5 text-indigo-400" />
                    <span>Explain Topic</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Section 2: 🟡 Medium Topics (Partly Understood) */}
        <div className="mt-8">
          <div className="flex items-center space-x-2 mb-4">
            <span className="w-3 h-3 rounded-full bg-amber-500 inline-block"></span>
            <h3 className="text-lg font-bold text-slate-100">🟡 Medium Topics (Partly Understood)</h3>
          </div>

          <div className="space-y-3">
            {medium_topics.map((item) => (
              <div
                key={item.topic_id}
                className="p-4 rounded-xl border border-amber-500/20 bg-amber-950/10 hover:border-amber-500/40 transition flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
              >
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <h4 className="font-semibold text-slate-200 text-sm">{item.title}</h4>
                    <span className="text-[11px] font-bold px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">
                      Mastery: {Math.round(item.mastery_score * 100)}%
                    </span>
                  </div>
                  <p className="mt-1.5 text-xs text-amber-200/80">{item.diagnostic_reason}</p>
                </div>

                <button
                  onClick={() => onExplainTopic(item.topic_id, item.title)}
                  className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-medium border border-slate-700 transition self-end sm:self-center"
                >
                  Quick Review
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Section 3: 🟢 Strong Topics (Already Good) */}
        <div className="mt-8">
          <div className="flex items-center space-x-2 mb-4">
            <span className="w-3 h-3 rounded-full bg-emerald-500 inline-block"></span>
            <h3 className="text-lg font-bold text-slate-100">🟢 Strong Topics (Already Good)</h3>
          </div>

          <div className="space-y-3">
            {strong_topics.map((item) => (
              <div
                key={item.topic_id}
                className="p-4 rounded-xl border border-emerald-500/20 bg-emerald-950/10 flex items-center justify-between"
              >
                <div>
                  <div className="flex items-center space-x-2">
                    <h4 className="font-semibold text-slate-200 text-sm">{item.title}</h4>
                    <span className="text-[11px] font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                      Mastery: {Math.round(item.mastery_score * 100)}%
                    </span>
                  </div>
                  <p className="mt-1 text-xs text-slate-400">{item.diagnostic_reason}</p>
                </div>

                <span className="text-xs text-emerald-400 font-medium">Exam Ready ✓</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

