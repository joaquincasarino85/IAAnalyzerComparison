// src/components/QuestionList.tsx
import React from "react";
import { QuestionWithData } from '../types';

interface QuestionListProps {
  questions: QuestionWithData[];
  onSelect: (id: number) => void;
  selectedId?: number;
  loadingId?: number | null;
}

const QuestionList: React.FC<QuestionListProps> = ({ 
  questions, 
  onSelect, 
  selectedId, 
  loadingId 
}) => {
  return (
    <div className="w-full md:w-1/3 bg-white rounded-lg shadow-md p-4">
      <h2 className="text-xl font-semibold mb-4">Question History</h2>
      
      <div className="space-y-2 max-h-96 overflow-y-auto">
        {questions.length === 0 ? (
          <div className="text-gray-500 text-center py-8">
            No questions yet. Ask your first question!
          </div>
        ) : (
          questions.map((question) => {
            const isSelected = question.id === selectedId;
            const isLoading = question.id === loadingId;
            
            return (
              <div
                key={question.id}
                onClick={() => !isLoading && onSelect(question.id)}
                className={`
                  p-3 rounded-lg cursor-pointer transition-all duration-200 border
                  ${isSelected 
                    ? 'bg-blue-50 border-blue-200 shadow-sm' 
                    : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
                  }
                  ${isLoading ? 'opacity-75 cursor-not-allowed' : ''}
                `}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {question.text}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      {new Date(question.created_at).toLocaleDateString()}
                    </p>
                    
                    {/* Loading indicator */}
                    {isLoading && (
                      <div className="flex items-center space-x-2 mt-2">
                        <div className="w-3 h-3 border-2 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
                        <span className="text-xs text-blue-600">Processing...</span>
                      </div>
                    )}
                    
                    {/* Response count */}
                    {!isLoading && question.responses && (
                      <div className="flex items-center space-x-1 mt-2">
                        <span className="text-xs text-gray-500">
                          {question.responses.length} AI responses
                        </span>
                        {question.responses.length > 0 && (
                          <div className="flex space-x-1">
                            {question.responses.map((response, index) => (
                              <div
                                key={index}
                                className="w-2 h-2 bg-green-500 rounded-full"
                                title={response.ai_name}
                              ></div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                  
                  {/* Status indicator */}
                  {isSelected && !isLoading && (
                    <div className="ml-2">
                      <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                    </div>
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>
      
      {/* Summary */}
      {questions.length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="text-sm text-gray-600">
            <div className="flex justify-between">
              <span>Total questions:</span>
              <span className="font-medium">{questions.length}</span>
            </div>
            <div className="flex justify-between">
              <span>With responses:</span>
              <span className="font-medium">
                {questions.filter(q => q.responses && q.responses.length > 0).length}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default QuestionList;
