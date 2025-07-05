import React from 'react';
import AIProgressIndicator from './AIProgressIndicator';

interface LoadingSpinnerProps {
  message?: string;
  size?: 'small' | 'medium' | 'large';
  showProgress?: boolean;
  progress?: number;
  currentStep?: number;
  totalSteps?: number;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ 
  message = "Processing your question...", 
  size = 'medium',
  showProgress = false,
  progress = 0,
  currentStep = 0,
  totalSteps = 9
}) => {
  const sizeClasses: Record<string, string> = {
    small: 'w-6 h-6',
    medium: 'w-12 h-12',
    large: 'w-16 h-16'
  };

  const progressSteps = [
    "Initializing AI models (ChatGPT, Gemini, Mistral, Cohere, Perplexity)...",
    "Sending question to ChatGPT...",
    "Sending question to Gemini...",
    "Sending question to Mistral...",
    "Sending question to Cohere...",
    "Sending question to Perplexity...",
    "Receiving responses from all AI models...",
    "Analyzing responses and generating comparisons...",
    "Finalizing results and preparing analysis..."
  ];

  const calculatedStep = Math.floor((progress / 100) * progressSteps.length);
  const currentMessage = progressSteps[Math.min(calculatedStep, progressSteps.length - 1)] || message;

  return (
    <div className="flex flex-col items-center justify-center p-8 space-y-4">
      {/* Main Spinner */}
      <div className="relative">
        <div className={`${sizeClasses[size]} border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin`}></div>
        
        {/* Inner pulse effect */}
        <div className={`absolute inset-0 ${sizeClasses[size]} border-4 border-transparent border-t-blue-400 rounded-full animate-pulse`}></div>
      </div>

      {/* Progress Bar */}
      {showProgress && (
        <div className="w-64 bg-gray-200 rounded-full h-2">
          <div 
            className="bg-blue-600 h-2 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      )}

      {/* Message */}
      <div className="text-center space-y-2">
        <p className="text-gray-700 font-medium">{currentMessage}</p>
        {showProgress && (
          <p className="text-sm text-gray-500">{Math.round(progress)}% complete</p>
        )}
      </div>

      {/* Animated dots */}
      <div className="flex space-x-1">
        <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
        <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
        <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
      </div>

      {/* AI Progress Indicator */}
      <AIProgressIndicator 
        currentStep={currentStep} 
        totalSteps={totalSteps} 
      />
    </div>
  );
};

export default LoadingSpinner; 