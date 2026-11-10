import React, { useState } from 'react';
import { MessageSquare, Send, BookOpen, FileText, CheckCircle2, AlertCircle } from 'lucide-react';
import { ExplainResponse, CitationRef } from '../types';

interface ExplainChatProps {
  initialTopicId?: string;
  initialTopicTitle?: string;
  onAskGroundedExplanation: (topicId: string, query: string) => Promise<ExplainResponse>;
}

export const ExplainChat: React.FC<ExplainChatProps> = ({
  initialTopicId = 'sub_01_03',
  initialTopicTitle = 'Light Reactions: Non-Cyclic Z-Scheme & Photolysis',
  onAskGroundedExplanation,
}) => {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<Array<{
    sender: 'user' | 'assistant';
    text: string;
    citations?: CitationRef[];
    grounded?: boolean;
  }>>([
    {
      sender: 'assistant',
      text: `Hello! I am your Guarded Academic Tutor. I explain concepts **strictly using your uploaded notes and textbook chapters**. Ask me anything about "${initialTopicTitle}" or other topics in your syllabus.`,
      grounded: true,
    }
  ]);
  const [loading, setLoading] = useState(false);

  const presetQueries = [
    "Why does cyclic photophosphorylation not release oxygen or make NADPH?",
    "Explain what is the Z-scheme and why it is named so.",
    "How many ATP and NADPH are used in the Calvin cycle per glucose?"
  ];

  const handleSend = async (textToSend?: string) => {
    const q = textToSend || query;
    if (!q.trim()) return;

    setMessages(prev => [...prev, { sender: 'user', text: q }]);
    if (!textToSend) setQuery('');
    setLoading(true);

    try {
      const response = await onAskGroundedExplanation(initialTopicId, q);
      setMessages(prev => [
        ...prev,
        {
          sender: 'assistant',
          text: response.explanation_markdown,
          citations: response.citations,
          grounded: response.is_grounded_in_material
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 flex flex-col h-[700px]">
      <div className="pb-4 border-b border-slate-800 flex items-center justify-between">
        <div>
          <div className="flex items-center space-x-2 text-indigo-400 text-xs font-semibold uppercase tracking-wider">
            <BookOpen className="w-4 h-4" />
            <span>Strict RAG Study Assistant</span>
          </div>
          <h2 className="text-xl font-bold text-white tracking-tight mt-0.5">
            Explain-This-Topic Helper
          </h2>
          <p className="text-xs text-slate-400">
            Current Focus: <span className="text-indigo-300 font-medium">{initialTopicTitle}</span> (Confined to uploaded material only)
          </p>
        </div>

        <div className="flex items-center space-x-1.5 text-xs text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20">
          <CheckCircle2 className="w-3.5 h-3.5" />
          <span>Strict Guardrails Active</span>
        </div>
      </div>

      {/* Preset Queries */}
      <div className="py-3 flex items-center space-x-2 overflow-x-auto no-scrollbar">
        <span className="text-xs text-slate-500 shrink-0">Try asking:</span>
        {presetQueries.map((preset, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(preset)}
            className="text-[11px] bg-slate-800 hover:bg-slate-700 text-slate-300 px-2.5 py-1 rounded-md whitespace-nowrap border border-slate-700/60 transition"
          >
            {preset}
          </button>
        ))}
      </div>

      {/* Message Stream */}
      <div className="flex-1 overflow-y-auto space-y-4 py-4 pr-1">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`flex ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[85%] rounded-2xl p-4 text-xs sm:text-sm leading-relaxed ${
                m.sender === 'user'
                  ? 'bg-indigo-600 text-white rounded-tr-none'
                  : 'bg-slate-950/70 text-slate-200 border border-slate-800 rounded-tl-none'
              }`}
            >
              <div className="whitespace-pre-line">{m.text}</div>

              {/* Citations Envelope */}
              {m.citations && m.citations.length > 0 && (
                <div className="mt-3 pt-3 border-t border-slate-800/80 space-y-2">
                  <div className="text-[11px] font-semibold text-amber-400 uppercase tracking-wider flex items-center space-x-1">
                    <FileText className="w-3 h-3" />
                    <span>Verified Citations ({m.citations.length})</span>
                  </div>
                  {m.citations.map((c, cIdx) => (
                    <div key={cIdx} className="bg-slate-900 p-2.5 rounded-lg border border-slate-800 text-xs">
                      <div className="font-medium text-slate-200">{c.document_name}</div>
                      <div className="text-slate-400 text-[11px] mt-0.5">
                        {c.section} • {c.page_or_anchor}
                      </div>
                      {c.verbatim_quote && (
                        <div className="mt-1 text-[11px] text-slate-400 italic border-l border-amber-500/50 pl-2">
                          "{c.verbatim_quote}"
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-slate-950/70 text-slate-400 text-xs p-3 rounded-xl border border-slate-800 animate-pulse">
              Retrieving relevant textbook chunks & synthesizing explanation...
            </div>
          </div>
        )}
      </div>

      {/* Input Field */}
      <div className="pt-3 border-t border-slate-800 flex items-center space-x-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask a question about this topic (only uploaded material will be used)..."
          className="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
        />
        <button
          onClick={() => handleSend()}
          disabled={loading || !query.trim()}
          className="p-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl shadow-md shadow-indigo-600/20 transition disabled:opacity-50"
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

