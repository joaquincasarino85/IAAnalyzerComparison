import React from 'react';
import { ProcessingStep } from '../types';

interface DetailedProgressIndicatorProps {
  processingSteps: ProcessingStep[];
  currentMessage: string;
  progress: number;
}

const DetailedProgressIndicator: React.FC<DetailedProgressIndicatorProps> = ({
  processingSteps,
  currentMessage,
  progress
}) => {
  const getStatusColor = (status: ProcessingStep['status']) => {
    switch (status) {
      case 'pending':
        return 'bg-gray-300';
      case 'processing':
        return 'bg-blue-500 animate-pulse';
      case 'completed':
        return 'bg-green-500';
      case 'error':
        return 'bg-red-500';
      default:
        return 'bg-gray-300';
    }
  };

  const getStatusIcon = (status: ProcessingStep['status']) => {
    switch (status) {
      case 'pending':
        return '⏳';
      case 'processing':
        return '🔄';
      case 'completed':
        return '✅';
      case 'error':
        return '❌';
      default:
        return '⏳';
    }
  };

  return (
    <div className="w-full max-w-6xl mx-auto space-y-4">
      {/* Progress Bar Principal */}
      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-base font-semibold text-gray-800">Overall Progress</h3>
          <span className="text-xs font-medium text-blue-600">{Math.round(progress)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
          <div 
            className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
        <p className="text-xs text-gray-600 text-center">{currentMessage}</p>
      </div>

      {/* Steps Detallados - Horizontal Layout */}
      <div className="bg-white rounded-lg shadow-md p-4">
        <h3 className="text-base font-semibold text-gray-800 mb-4">Processing Status</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {processingSteps.map((step) => (
            <div key={step.step} className="flex items-center p-3 bg-gray-50 rounded-lg border border-gray-200">
              <div className="flex items-center space-x-3 flex-1">
                <div className={`w-8 h-8 rounded-full ${getStatusColor(step.status)} flex items-center justify-center text-white text-sm font-bold flex-shrink-0`}>
                  {getStatusIcon(step.status)}
                </div>
                <div className="flex-1 min-w-0">
                  <span className="text-sm font-medium text-gray-800 block truncate">{step.name}</span>
                  <p className="text-xs text-gray-500 mt-1 line-clamp-2">{step.message}</p>
                </div>
              </div>
              <div className="ml-2 flex-shrink-0">
                <span className={`text-xs px-2 py-1 rounded-full ${
                  step.status === 'pending' ? 'bg-gray-100 text-gray-600' :
                  step.status === 'processing' ? 'bg-blue-100 text-blue-600' :
                  step.status === 'completed' ? 'bg-green-100 text-green-600' :
                  'bg-red-100 text-red-600'
                }`}>
                  {step.status === 'pending' ? 'Waiting' :
                   step.status === 'processing' ? 'Processing' :
                   step.status === 'completed' ? 'Completed' :
                   'Error'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {/* Información Adicional */}
      <div className="bg-blue-50 rounded-lg p-4">
        <div className="flex items-start space-x-3">
          <div className="text-blue-500 text-xl">ℹ️</div>
          <div>
            <h4 className="text-sm font-medium text-blue-800 mb-1">Process Information</h4>
            <p className="text-xs text-blue-600">
              The system is processing your question in an optimized way. All AIs are queried in parallel for speed, then a summary is generated, and finally a full analysis of similarities, contradictions, named entities, and sentiments is performed.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DetailedProgressIndicator; 