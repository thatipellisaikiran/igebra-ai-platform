import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { UploadZone } from './components/UploadZone';
import { TopicMapTree } from './components/TopicMapTree';
import { DiagnosticQuiz } from './components/DiagnosticQuiz';
import { GapReportView } from './components/GapReportView';
import { RevisionPlan } from './components/RevisionPlan';
import { ExplainChat } from './components/ExplainChat';
import { Dashboard } from './components/Dashboard';

import {
  TopicMapResponse,
  DiagnosticQuizResponse,
  GapReportResponse,
  RevisionPlanResponse,
  QuizSubmissionResponse,
} from './types';
import { api } from './services/api';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('upload');
  const [currentUser, setCurrentUser] = useState({
    name: 'Demo Student',
    role: 'student',
    email: 'student@gapfinder.ai',
  });

  const [topicMap, setTopicMap] = useState<TopicMapResponse | null>(null);
  const [quiz, setQuiz] = useState<DiagnosticQuizResponse | null>(null);
  const [gapReport, setGapReport] = useState<GapReportResponse | null>(null);
  const [revisionPlan, setRevisionPlan] = useState<RevisionPlanResponse | null>(null);
  const [backendOffline, setBackendOffline] = useState<boolean>(false);

  const [activeExplainTopic, setActiveExplainTopic] = useState({
    id: 'general',
    title: 'Uploaded Study Materials',
  });

  useEffect(() => {
    loadAllInitialData();
  }, []);

  const loadAllInitialData = async () => {
    try {
      const [tm, qz, gr, rp] = await Promise.allSettled([
        api.getTopicMap(),
        api.getDiagnosticQuiz(),
        api.getGapReport(),
        api.getRevisionPlan(5, 2.0),
      ]);

      const anySuccess =
        tm.status === 'fulfilled' ||
        qz.status === 'fulfilled' ||
        gr.status === 'fulfilled' ||
        rp.status === 'fulfilled';
      setBackendOffline(!anySuccess);

      if (tm.status === 'fulfilled') setTopicMap(tm.value);
      if (qz.status === 'fulfilled') setQuiz(qz.value);
      if (gr.status === 'fulfilled') setGapReport(gr.value);
      if (rp.status === 'fulfilled') setRevisionPlan(rp.value);
    } catch (e) {
      setBackendOffline(true);
      console.error('Failed to load backend state:', e);
    }
  };

  const handleSwitchUser = (newRole: string) => {
    if (newRole === 'teacher') {
      setCurrentUser({
        name: 'Demo Teacher',
        role: 'teacher',
        email: 'teacher@gapfinder.ai',
      });
      setActiveTab('dashboard');
    } else {
      setCurrentUser({
        name: 'Demo Student',
        role: 'student',
        email: 'student@gapfinder.ai',
      });
      setActiveTab('upload');
    }
  };

  const handleSubmitQuiz = async (
    responses: { question_id: string; selected_option_idx: number }[]
  ): Promise<QuizSubmissionResponse> => {
    const result = await api.submitQuiz(quiz?.quiz_id || 'qz_diag_01', responses);
    const [newGr, newTm] = await Promise.all([api.getGapReport(), api.getTopicMap()]);
    setGapReport(newGr);
    setTopicMap(newTm);
    return result;
  };

  const handleUpdateBudget = async (days: number, dailyHours: number) => {
    const updated = await api.getRevisionPlan(days, dailyHours);
    setRevisionPlan(updated);
  };

  const handleOpenExplain = (topicId: string, topicTitle: string) => {
    setActiveExplainTopic({ id: topicId, title: topicTitle });
    setActiveTab('explain');
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans antialiased">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        currentUser={currentUser}
        onSwitchUser={handleSwitchUser}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {backendOffline && (
          <div className="mb-6 p-4 rounded-xl border border-amber-500/40 bg-amber-950/30 text-amber-200 text-xs flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
            <div>
              <strong>Backend API Offline:</strong> Start the FastAPI server locally (<code className="bg-slate-900 px-1.5 py-0.5 rounded">uvicorn app.main:app --port 8000</code>) or configure <code className="bg-slate-900 px-1.5 py-0.5 rounded">VITE_API_BASE</code> to a hosted backend URL.
            </div>
            <button
              onClick={loadAllInitialData}
              className="px-3 py-1 bg-amber-500/20 hover:bg-amber-500/30 border border-amber-500/40 rounded-lg font-medium self-start sm:self-auto"
            >
              Retry Connection
            </button>
          </div>
        )}
        {activeTab === 'upload' && (
          <UploadZone
            onContinue={() => {
              loadAllInitialData();
              setActiveTab('topic-map');
            }}
          />
        )}

        {activeTab === 'topic-map' && (
          <TopicMapTree
            topicMap={topicMap}
            onStartQuiz={() => {
              loadAllInitialData();
              setActiveTab('quiz');
            }}
            onExplainTopic={handleOpenExplain}
          />
        )}

        {activeTab === 'quiz' && (
          <DiagnosticQuiz
            quiz={quiz}
            onSubmitQuiz={handleSubmitQuiz}
            onViewGapReport={() => setActiveTab('gap-report')}
          />
        )}

        {activeTab === 'gap-report' && (
          <GapReportView
            gapReport={gapReport}
            onGeneratePlan={() => setActiveTab('plan')}
            onExplainTopic={handleOpenExplain}
          />
        )}

        {activeTab === 'plan' && (
          <RevisionPlan
            plan={revisionPlan}
            onUpdateBudget={handleUpdateBudget}
            onExplainTopic={handleOpenExplain}
            onRetestTopic={() => setActiveTab('quiz')}
          />
        )}

        {activeTab === 'explain' && (
          <ExplainChat
            initialTopicId={activeExplainTopic.id}
            initialTopicTitle={activeExplainTopic.title}
            onAskGroundedExplanation={(tId, q) => api.explainTopic(tId, q)}
          />
        )}

        {activeTab === 'dashboard' && <Dashboard currentUserRole={currentUser.role} />}
      </main>

      <footer className="border-t border-slate-900 bg-slate-950/80 py-4 text-center text-xs text-slate-500">
        GapFinder AI • Strict Retrieval-Augmented Generation & Academic Diagnosis
      </footer>
    </div>
  );
};

export default App;
