import React from 'react';

interface AIProgressIndicatorProps {
  currentStep: number;
  totalSteps: number;
}

const AIProgressIndicator: React.FC<AIProgressIndicatorProps> = ({ currentStep, totalSteps }) => {
  const ais = [
    { name: 'ChatGPT', color: 'bg-green-500', step: 1 },
    { name: 'Gemini', color: 'bg-blue-500', step: 2 },
    { name: 'Mistral', color: 'bg-purple-500', step: 3 },
    { name: 'Cohere', color: 'bg-orange-500', step: 4 },
    { name: 'Perplexity', color: 'bg-red-500', step: 5 }
  ];

  const getAIStatus = (aiStep: number) => {
    if (currentStep < aiStep) {
      return { status: 'pending', color: 'bg-gray-300', text: 'Waiting...' };
    } else if (currentStep === aiStep) {
      return { status: 'active', color: aiStep === 1 ? 'bg-green-500' : aiStep === 2 ? 'bg-blue-500' : aiStep === 3 ? 'bg-purple-500' : aiStep === 4 ? 'bg-orange-500' : 'bg-red-500', text: 'Processing...' };
    } else {
      return { status: 'completed', color: 'bg-green-500', text: 'Completed' };
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <h3 className="text-sm font-medium text-gray-700 mb-3 text-center">AI Processing Status</h3>
      <div className="space-y-3">
        {ais.map((ai, index) => {
          const status = getAIStatus(ai.step);
          return (
            <div key={ai.name} className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className={`w-3 h-3 rounded-full ${status.color} ${status.status === 'active' ? 'animate-pulse' : ''}`}></div>
                <span className="text-sm font-medium text-gray-700">{ai.name}</span>
              </div>
              <span className={`text-xs ${
                status.status === 'pending' ? 'text-gray-500' : 
                status.status === 'active' ? 'text-blue-600' : 
                'text-green-600'
              }`}>
                {status.text}
              </span>
            </div>
          );
        })}
      </div>
      
      {/* Overall Progress */}
      <div className="mt-4">
        <div className="flex justify-between text-xs text-gray-500 mb-1">
          <span>Overall Progress</span>
          <span>{Math.round((currentStep / totalSteps) * 100)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-gradient-to-r from-green-500 via-blue-500 to-purple-500 h-2 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${(currentStep / totalSteps) * 100}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default AIProgressIndicator; 