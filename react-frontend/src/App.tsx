// src/App.tsx
import React, { useEffect, useState } from "react";
import QuestionInput from "./components/QuestionInput";
import QuestionList from "./components/QuestionList";
import AnalysisPanel from "./components/AnalysisPanel";
import AnalysisGraphs from "./components/AnalysisGraphs";
import LoadingSpinner from "./components/LoadingSpinner";
import { QuestionWithData } from "./types";
import { useProgressSimulation } from "./hooks/useProgressSimulation";
import axios from "axios";

const App = () => {
  const [questions, setQuestions] = useState<QuestionWithData[]>([]);
  const [selectedQuestion, setSelectedQuestion] = useState<QuestionWithData | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'analysis' | 'graphs'>('analysis');
  
  // Progress simulation for better UX
  const {
    progress,
    currentMessage,
    isRunning: progressRunning,
    startProgress,
    stopProgress
  } = useProgressSimulation({
    duration: 12000, // 12 seconds
    onComplete: () => {
      // Progress simulation completed
    }
  });

  const fetchQuestions = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/questions/");
      const sorted = res.data.sort((a: any, b: any) => b.id - a.id);
      setQuestions(sorted);
    } catch (err) {
      console.error("Error fetching questions:", err);
    }
  };

  useEffect(() => {
    fetchQuestions();
  }, []);

  const handleQuestionAsked = async (text: string) => {
    try {
      setLoading(true);
      startProgress(); // Start progress simulation
      
      const res = await axios.post("http://127.0.0.1:8000/questions/", { text });
      await fetchQuestions();
      const full = await axios.get(`http://127.0.0.1:8000/questions/${res.data.question_id}`);
      setSelectedQuestion(full.data);
      
      stopProgress(); // Stop progress simulation
    } catch (error) {
      console.error("Error asking question:", error);
      stopProgress(); // Stop progress on error
    } finally {
      setLoading(false);
    }
  };

  const handleSelectQuestion = async (id: number) => {
    try {
      const res = await axios.get(`http://127.0.0.1:8000/questions/${id}`);
      setSelectedQuestion(res.data);
    } catch (error) {
      console.error("Error loading question:", error);
    }
  };

  return (
    <div className="p-8 space-y-6">
      <h1 className="text-3xl font-bold">IA Analyzer Comparison</h1>
      {loading ? (
        <div className="bg-white rounded-lg shadow-md p-6">
          <LoadingSpinner 
            message={currentMessage}
            size="large"
            showProgress={true}
            progress={progress}
            currentStep={Math.floor((progress / 100) * 9)}
            totalSteps={9}
          />
        </div>
      ) : (
        <QuestionInput onQuestionAsked={handleQuestionAsked} loading={loading} />
      )}
      <div className="flex gap-6">
        <QuestionList 
          questions={questions} 
          onSelect={handleSelectQuestion} 
          selectedId={selectedQuestion?.id}
          loadingId={loading ? selectedQuestion?.id || null : null}
        />
        
        <div className="w-full md:w-2/3">
          {selectedQuestion && (
            <>
              {/* Tab Navigation */}
              <div className="flex border-b border-gray-200 mb-6">
                <button
                  onClick={() => setActiveTab('analysis')}
                  className={`px-4 py-2 font-medium text-sm ${
                    activeTab === 'analysis'
                      ? 'border-b-2 border-blue-500 text-blue-600'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Text Analysis
                </button>
                <button
                  onClick={() => setActiveTab('graphs')}
                  className={`px-4 py-2 font-medium text-sm ${
                    activeTab === 'graphs'
                      ? 'border-b-2 border-blue-500 text-blue-600'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Graphs & Charts
                </button>
              </div>

              {/* Tab Content */}
              {activeTab === 'analysis' ? (
                <AnalysisPanel question={selectedQuestion} />
              ) : (
                <AnalysisGraphs question={selectedQuestion} />
              )}
            </>
          )}
          
          {!selectedQuestion && (
            <div className="text-gray-500 italic">Select a question to view analysis.</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
