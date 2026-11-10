import {
  TopicMapResponse,
  DiagnosticQuizResponse,
  QuizSubmissionResponse,
  GapReportResponse,
  RevisionPlanResponse,
  ExplainResponse,
} from '../types';

const API_BASE = 'http://localhost:8000/api';

export const api = {
  async listMaterials(): Promise<any[]> {
    const res = await fetch(`${API_BASE}/materials`);
    if (!res.ok) throw new Error('Failed to fetch materials');
    return res.json();
  },

  async uploadMaterial(file: File, docType: string): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('doc_type', docType);
    const res = await fetch(`${API_BASE}/materials/upload`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) throw new Error('Failed to upload material');
    return res.json();
  },

  async getTopicMap(): Promise<TopicMapResponse> {
    const res = await fetch(`${API_BASE}/topic-map`);
    if (!res.ok) throw new Error('Failed to fetch topic map');
    return res.json();
  },

  async getDiagnosticQuiz(): Promise<DiagnosticQuizResponse> {
    const res = await fetch(`${API_BASE}/quiz/diagnostic`);
    if (!res.ok) throw new Error('Failed to fetch diagnostic quiz');
    return res.json();
  },

  async submitQuiz(quizId: string, responses: { question_id: string; selected_option_idx: number }[]): Promise<QuizSubmissionResponse> {
    const res = await fetch(`${API_BASE}/quiz/${quizId}/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ responses }),
    });
    if (!res.ok) throw new Error('Failed to submit quiz');
    return res.json();
  },

  async getGapReport(): Promise<GapReportResponse> {
    const res = await fetch(`${API_BASE}/gap-report/current`);
    if (!res.ok) throw new Error('Failed to fetch gap report');
    return res.json();
  },

  async getRevisionPlan(availableDays = 5, dailyHours = 2.0): Promise<RevisionPlanResponse> {
    const res = await fetch(`${API_BASE}/revision-plan/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ available_days: availableDays, daily_hours: dailyHours }),
    });
    if (!res.ok) throw new Error('Failed to generate revision plan');
    return res.json();
  },

  async explainTopic(topicId: string, query: string): Promise<ExplainResponse> {
    const res = await fetch(`${API_BASE}/explain`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic_id: topicId, query }),
    });
    if (!res.ok) throw new Error('Failed to get topic explanation');
    return res.json();
  },

  async getProgress(): Promise<any> {
    const res = await fetch(`${API_BASE}/analytics/progress`);
    if (!res.ok) throw new Error('Failed to fetch analytics');
    return res.json();
  },

  async getDemoAccounts(): Promise<any[]> {
    const res = await fetch(`${API_BASE}/auth/demo-accounts`);
    if (!res.ok) throw new Error('Failed to fetch demo accounts');
    return res.json();
  },
};
