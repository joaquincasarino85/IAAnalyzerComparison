import React, { useState } from 'react';
import LoadingSpinner from './LoadingSpinner';

interface QuestionInputProps {
  onQuestionAsked: (question: string) => void;
  loading: boolean;
}

const QuestionInput: React.FC<QuestionInputProps> = ({ onQuestionAsked, loading }) => {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (question.trim() && !loading) {
      onQuestionAsked(question.trim());
      setQuestion('');
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4">Ask a Question</h2>
      
      {loading ? (
        <LoadingSpinner 
          message="Processing your question with multiple AI models..."
          size="large"
          showProgress={true}
          progress={75}
        />
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="question" className="block text-sm font-medium text-gray-700 mb-2">
              Enter your question:
            </label>
            <textarea
              id="question"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask anything you want to compare across different AI models..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              rows={4}
              disabled={loading}
            />
          </div>
          
          <div className="flex justify-between items-center">
            <div className="text-sm text-gray-500">
              Your question will be sent to ChatGPT, Gemini, Mistral, Cohere, and Perplexity for comparison
            </div>
            <button
              type="submit"
              disabled={!question.trim() || loading}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
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