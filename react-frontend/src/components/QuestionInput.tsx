import React, { useState } from 'react';
import DetailedProgressIndicator from './DetailedProgressIndicator';
import { ProcessingStep } from '../types';

interface QuestionInputProps {
  onQuestionAsked: (question: string) => void;
  loading: boolean;
  processingSteps?: ProcessingStep[];
  currentMessage?: string;
  progress?: number;
}

const QuestionInput: React.FC<QuestionInputProps> = ({ 
  onQuestionAsked, 
  loading, 
  processingSteps = [], 
  currentMessage = "Processing your question...", 
  progress = 0 
}) => {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (question.trim() && !loading) {
      onQuestionAsked(question.trim());
      setQuestion('');
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-8 mb-4 w-full">
      <h2 className="text-2xl font-bold mb-2 text-gray-900">Ask a Question</h2>
      <p className="text-gray-500 mb-4">Type your question below to compare answers from multiple AI models.</p>
      {loading ? (
        <div className="space-y-6">
          <DetailedProgressIndicator 
            processingSteps={processingSteps}
            currentMessage={currentMessage}
            progress={progress}
          />
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <textarea
              id="question"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask anything you want to compare across different AI models..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none text-base"
              rows={3}
              disabled={loading}
            />
          </div>
          <div className="flex justify-end">
            <button
              type="submit"
              disabled={!question.trim() || loading}
              className="px-8 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-semibold text-base"
            >
              {loading ? 'Processing...' : 'Ask Question'}
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default QuestionInput;