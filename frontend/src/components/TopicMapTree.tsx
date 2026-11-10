import React from 'react';
import { Layers, HelpCircle, ArrowRight, BookOpen, AlertTriangle } from 'lucide-react';
import { TopicMapResponse } from '../types';

interface TopicMapTreeProps {
  topicMap: TopicMapResponse | null;
  onStartQuiz: () => void;
  onExplainTopic: (topicId: string, topicTitle: string) => void;
}

export const TopicMapTree: React.FC<TopicMapTreeProps> = ({
  topicMap,
  onStartQuiz,
  onExplainTopic,
}) => {
  if (!topicMap) {
    return (
      <div className="p-8 text-center text-slate-400 bg-slate-900 border border-slate-800 rounded-2xl">
        Loading topic map and past paper linkages...
      </div>
    );
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'weak':
        return <span className="px-2 py-0.5 text-xs font-semibold rounded-md bg-rose-500/10 text-rose-400 border border-rose-500/20">🔴 Weak Gap</span>;
      case 'medium':
        return <span className="px-2 py-0.5 text-xs font-semibold rounded-md bg-amber-500/10 text-amber-400 border border-amber-500/20">🟡 Medium</span>;
      case 'strong':
        return <span className="px-2 py-0.5 text-xs font-semibold rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">🟢 Strong</span>;
      default:
        return <span className="px-2 py-0.5 text-xs font-semibold rounded-md bg-slate-700 text-slate-300">⚪ Untested</span>;
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 text-indigo-400 text-xs font-semibold tracking-wider uppercase">
              <Layers className="w-4 h-4" />
              <span>Syllabus Decomposition & Weightage</span>
            </div>
            <h2 className="text-2xl font-bold text-white tracking-tight mt-1">
              Curriculum Topic Map: {topicMap.subject}
            </h2>
            <p className="text-slate-400 text-sm mt-1">
              Correlated with past paper question frequency to highlight high-yield exam areas.
            </p>
          </div>

          <button
            onClick={onStartQuiz}
            className="flex items-center space-x-2 px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-sm font-semibold shadow-lg shadow-indigo-600/30 transition self-start sm:self-auto"
          >
            <span>Run Diagnostic Quiz</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        {/* Chapters */}
        <div className="mt-8 space-y-6">
          {topicMap.topics.map((chapter) => (
            <div key={chapter.id} className="border border-slate-800 rounded-xl overflow-hidden bg-slate-950/40">
              <div className="bg-slate-800/60 p-4 border-b border-slate-800 flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-1.5 bg-indigo-500/10 text-indigo-400 rounded-md">
                    <BookOpen className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-slate-200 text-sm">{chapter.chapter_title}</h3>
                    <p className="text-xs text-slate-400">{chapter.subtopics.length} Subtopics Mapped</p>
                  </div>
                </div>

                <div className="text-right">
                  <span className="text-xs font-bold text-indigo-300 bg-indigo-950/60 border border-indigo-800/40 px-2.5 py-1 rounded-md">
                    {chapter.exam_weightage_pct}% Exam Share
                  </span>
                  <div className="text-[11px] text-slate-400 mt-1">{chapter.exam_frequency_count} past exam questions</div>
                </div>
              </div>

              {/* Subtopics Table */}
              <div className="divide-y divide-slate-800/60">
                {chapter.subtopics.map((sub) => (
                  <div key={sub.id} className="p-3.5 sm:px-5 flex items-center justify-between hover:bg-slate-800/30 transition">
                    <div className="flex-1 pr-4">
                      <div className="flex items-center space-x-2">
                        <span className="text-sm font-medium text-slate-300">{sub.title}</span>
                        {getStatusBadge(sub.status)}
                      </div>
                      <div className="flex items-center space-x-4 text-xs text-slate-500 mt-1">
                        <span>Past Exam Frequency: <strong className="text-slate-400">{sub.past_paper_occurrences} questions</strong></span>
                        <span>•</span>
                        <span>Weightage: <strong className={sub.weightage_category === 'High' ? 'text-amber-400' : 'text-slate-400'}>{sub.weightage_category}</strong></span>
                      </div>
                    </div>

                    <div className="flex items-center space-x-3">
                      <div className="hidden sm:block text-right">
                        <div className="text-xs text-slate-400 font-medium">Mastery</div>
                        <div className="text-xs font-bold text-slate-200">{Math.round(sub.current_mastery * 100)}%</div>
                      </div>

                      <button
                        onClick={() => onExplainTopic(sub.id, sub.title)}
                        className="px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white rounded-lg text-xs font-medium border border-slate-700 transition"
                      >
                        Explain
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

