import React, { useEffect, useState } from "react";
import { getQuestions, getQuestionDetail } from "../services/api";
import { Question, QuestionWithData } from "../types";
import QuestionList from "../components/QuestionList";
import { QuestionDetail } from "../components/QuestionDetail";
import QuestionInput from "../components/QuestionInput";
import { useParallelProcessing } from "../hooks/useParallelProcessing";
import AnalysisGraphs from "../components/AnalysisGraphs";

const Home: React.FC = () => {
  const [questions, setQuestions] = useState<QuestionWithData[]>([]);
  const [selectedQuestionId, setSelectedQuestionId] = useState<number | null>(null);
  const [selectedQuestion, setSelectedQuestion] = useState<QuestionWithData | null>(null);
  const [activeTab, setActiveTab] = useState<'analysis' | 'graphs'>('analysis');

  const { 
    progress, 
    processingSteps, 
    processQuestion, 
    resetProgress 
  } = useParallelProcessing();

  useEffect(() => {
    getQuestions().then(setQuestions);
  }, []);

  useEffect(() => {
    if (selectedQuestionId !== null) {
      getQuestionDetail(selectedQuestionId).then((data) => {
        setSelectedQuestion(data);
      });
    }
  }, [selectedQuestionId]);

  const handleQuestionAsked = async (question: string) => {
    try {
      resetProgress();
      const result = await processQuestion(question);
      await getQuestions().then(setQuestions);
      setSelectedQuestionId(result.questionId);
      setSelectedQuestion({
        id: result.questionId,
        text: question,
        summary: result.summary,
        similarity: result.analysis.similarities,
        semantic_similarity: result.analysis.semantic_similarities,
        contradictions: result.analysis.contradictions,
        named_entities: result.analysis.named_entities,
        sentiments: result.analysis.sentiments,
        responses: Object.entries(result.responses).map(([iaName, text]) => ({ iaName, text }))
      });
    } catch (error) {
      console.error('Error processing question:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="w-full px-4 sm:px-6 md:px-12">
          <div className="flex justify-between items-center py-4 sm:py-6">
            <h1 className="text-2xl sm:text-4xl font-extrabold text-gray-900">IA Analyzer Comparison</h1>
          </div>
        </div>
      </div>
      {/* Main layout - vertical stack, full width */}
      <div className="flex-1 flex flex-col w-full items-center">
        {/* Ask a Question - full width */}
        <div className="w-full px-2 sm:px-4 md:px-12 mt-4 sm:mt-8">
          <div className="bg-white rounded-xl shadow-lg p-4 sm:p-8 w-full">
            <QuestionInput 
              onQuestionAsked={handleQuestionAsked}
              loading={progress.status === 'processing'}
              processingSteps={processingSteps}
              currentMessage={progress.message}
              progress={progress.progress}
            />
          </div>
        </div>
        {/* Question History and Results - below, full width */}
        <div className="w-full flex flex-col lg:flex-row gap-4 lg:gap-8 px-2 sm:px-4 md:px-12 mt-4 sm:mt-8">
          {/* Question History */}
          <aside className="w-full lg:w-[420px] min-h-[200px] bg-white shadow-md flex flex-col p-4 sm:p-6 rounded-xl mb-4 lg:mb-0">
            <h2 className="text-lg sm:text-xl font-bold mb-4 sm:mb-6">Question History</h2>
            <QuestionList questions={questions} onSelect={setSelectedQuestionId} />
          </aside>
          {/* Main Panel - Results */}
          <main className="flex-1">
            <div className="w-full">
              {selectedQuestion ? (
                <div className="bg-white border rounded-lg p-4 sm:p-8 w-full">
                  {/* Tabs */}
                  <div className="flex border-b border-gray-200 mb-4 sm:mb-6 flex-wrap">
                    <button
                      onClick={() => setActiveTab('analysis')}
                      className={`px-2 sm:px-4 py-2 font-medium text-sm ${
                        activeTab === 'analysis'
                          ? 'border-b-2 border-blue-500 text-blue-600'
                          : 'text-gray-500 hover:text-gray-700'
                      }`}
                    >
                      Text Analysis
                    </button>
                    <button
                      onClick={() => setActiveTab('graphs')}
                      className={`px-2 sm:px-4 py-2 font-medium text-sm ${
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
                    <QuestionDetail question={selectedQuestion} />
                  ) : (
                    <AnalysisGraphs question={selectedQuestion} />
                  )}
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center h-64 sm:h-96 w-full">
                  <span className="text-gray-400 italic text-base sm:text-lg">Select a question to view analysis.</span>
                </div>
              )}
            </div>
          </main>
        </div>
      </div>
    </div>
  );
};

export default Home;
