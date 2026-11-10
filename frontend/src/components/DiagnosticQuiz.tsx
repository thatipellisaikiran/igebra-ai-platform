import React, { useState } from 'react';
import { HelpCircle, CheckCircle, XCircle, FileText, ArrowRight, RotateCcw } from 'lucide-react';
import { DiagnosticQuizResponse, QuizSubmissionResponse } from '../types';

interface DiagnosticQuizProps {
  quiz: DiagnosticQuizResponse | null;
  onSubmitQuiz: (responses: { question_id: string; selected_option_idx: number }[]) => Promise<QuizSubmissionResponse>;
  onViewGapReport: () => void;
}

export const DiagnosticQuiz: React.FC<DiagnosticQuizProps> = ({
  quiz,
  onSubmitQuiz,
  onViewGapReport,
}) => {
  const [selectedAnswers, setSelectedAnswers] = useState<{ [qId: string]: number }>({});
  const [submissionResult, setSubmissionResult] = useState<QuizSubmissionResponse | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!quiz) {
    return (
      <div className="p-8 text-center text-slate-400 bg-slate-900 border border-slate-800 rounded-2xl">
        Generating grounded diagnostic questions from uploaded notes...
      </div>
    );
  }

  const handleSelectOption = (questionId: string, optionIdx: number) => {
    if (submissionResult) return; // Prevent changing after submission
    setSelectedAnswers(prev => ({
      ...prev,
      [questionId]: optionIdx
    }));
  };

  const handleSubmit = async () => {
    const responses = quiz.questions.map(q => ({
      question_id: q.id,
      selected_option_idx: selectedAnswers[q.id] ?? 0
    }));

    setIsSubmitting(true);
    try {
      const result = await onSubmitQuiz(responses);
      setSubmissionResult(result);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleRetest = () => {
    setSubmissionResult(null);
    setSelectedAnswers({});
  };

  const answeredCount = Object.keys(selectedAnswers).length;

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between pb-6 border-b border-slate-800 gap-4">
          <div>
            <div className="flex items-center space-x-2 text-indigo-400 text-xs font-semibold uppercase tracking-wider">
              <HelpCircle className="w-4 h-4" />
              <span>Grounded Testing Engine</span>
            </div>
            <h2 className="text-2xl font-bold text-white tracking-tight mt-1">{quiz.title}</h2>
            <p className="text-slate-400 text-sm mt-1">
              All questions are generated directly from your uploaded textbook chapters. Citations confirm the source section.
            </p>
          </div>

          {!submissionResult ? (
            <div className="bg-slate-800 px-4 py-2 rounded-xl text-right">
              <div className="text-xs text-slate-400">Progress</div>
              <div className="text-sm font-bold text-indigo-400">
                {answeredCount} / {quiz.total_questions} Answered
              </div>
            </div>
          ) : (
            <div className="bg-slate-800 px-4 py-2 rounded-xl text-right border border-indigo-500/30">
              <div className="text-xs text-slate-400">Diagnostic Score</div>
              <div className="text-lg font-extrabold text-emerald-400">
                {submissionResult.score} / {submissionResult.total_questions} ({submissionResult.score_percentage}%)
              </div>
            </div>
          )}
        </div>

        {/* Questions List */}
        <div className="mt-8 space-y-8">
          {quiz.questions.map((q, qIndex) => {
            const evalResult = submissionResult?.evaluations.find(e => e.question_id === q.id);
            const userChoice = selectedAnswers[q.id];

            return (
              <div
                key={q.id}
                className={`p-6 rounded-xl border transition-all ${
                  evalResult
                    ? evalResult.is_correct
                      ? 'border-emerald-500/40 bg-emerald-950/10'
                      : 'border-rose-500/40 bg-rose-950/10'
                    : 'border-slate-800 bg-slate-950/40'
                }`}
              >
                {/* Header with Topic and Citation */}
                <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
                  <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
                    Q{qIndex + 1}: {q.topic_name}
                  </span>

                  {/* Verifiable Citation Badge */}
                  <div className="flex items-center space-x-1 text-xs text-amber-400/90 bg-amber-500/10 px-2.5 py-1 rounded-md border border-amber-500/20">
                    <FileText className="w-3.5 h-3.5" />
                    <span>Citation: <strong>{q.citation.section}</strong> ({q.citation.page_or_anchor})</span>
                  </div>
                </div>

                <h3 className="text-base font-medium text-slate-200 mt-2">{q.question_text}</h3>

                {/* Options */}
                <div className="mt-4 space-y-2.5">
                  {q.options.map((option, optIdx) => {
                    const isSelected = userChoice === optIdx;
                    let optionStyle = 'border-slate-800 bg-slate-900/60 hover:bg-slate-800/80 text-slate-300';

                    if (submissionResult && evalResult) {
                      if (evalResult.correct_answer === option) {
                        optionStyle = 'border-emerald-500 bg-emerald-500/20 text-emerald-200 font-semibold';
                      } else if (isSelected && !evalResult.is_correct) {
                        optionStyle = 'border-rose-500 bg-rose-500/20 text-rose-200 font-semibold';
                      } else {
                        optionStyle = 'border-slate-800/50 opacity-40 text-slate-500';
                      }
                    } else if (isSelected) {
                      optionStyle = 'border-indigo-500 bg-indigo-600/20 text-white font-medium shadow-md shadow-indigo-500/10';
                    }

                    return (
                      <div
                        key={optIdx}
                        onClick={() => handleSelectOption(q.id, optIdx)}
                        className={`p-3.5 rounded-lg border text-sm flex items-center justify-between cursor-pointer transition ${optionStyle}`}
                      >
                        <div className="flex items-center space-x-3">
                          <span className="w-6 h-6 rounded-full border border-slate-700 flex items-center justify-center text-xs font-bold text-slate-400">
                            {String.fromCharCode(65 + optIdx)}
                          </span>
                          <span>{option}</span>
                        </div>

                        {submissionResult && evalResult && evalResult.correct_answer === option && (
                          <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
                        )}
                        {submissionResult && evalResult && isSelected && !evalResult.is_correct && (
                          <XCircle className="w-4 h-4 text-rose-400 shrink-0" />
                        )}
                      </div>
                    );
                  })}
                </div>

                {/* Explanation Box post-submission */}
                {evalResult && (
                  <div className="mt-4 p-4 rounded-lg bg-slate-900/90 border border-slate-700/60 text-xs">
                    <div className="font-semibold text-slate-300 mb-1 flex items-center space-x-1">
                      <span>Diagnostic Rationale:</span>
                    </div>
                    <p className="text-slate-400 leading-relaxed">{evalResult.explanation}</p>
                    {evalResult.citation.verbatim_quote && (
                      <div className="mt-2 text-slate-500 italic border-l-2 border-indigo-500 pl-2">
                        "{evalResult.citation.verbatim_quote}"
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Footer Actions */}
        <div className="mt-8 flex items-center justify-between pt-6 border-t border-slate-800">
          {!submissionResult ? (
            <button
              onClick={handleSubmit}
              disabled={isSubmitting || answeredCount === 0}
              className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 text-white rounded-xl text-sm font-semibold shadow-lg shadow-indigo-600/30 transition disabled:opacity-50 ml-auto"
            >
              {isSubmitting ? 'Evaluating Responses...' : `Submit Answers & Diagnose Gaps (${answeredCount}/${quiz.total_questions})`}
            </button>
          ) : (
            <div className="flex items-center justify-between w-full">
              <button
                onClick={handleRetest}
                className="flex items-center space-x-2 px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold transition border border-slate-700"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Retake Diagnostic Quiz</span>
              </button>

              <button
                onClick={onViewGapReport}
                className="flex items-center space-x-2 px-6 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-sm font-semibold shadow-lg shadow-emerald-600/30 transition"
              >
                <span>View Full Diagnostic Gap Report</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

