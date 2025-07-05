import React, { useEffect, useState } from "react";
import { getQuestions, getQuestionDetail } from "../services/api";
import { Question, Response, Analysis } from "../types";
import { QuestionList } from "../components/QuestionList";
import { QuestionDetail } from "../components/QuestionDetail";

const Home: React.FC = () => {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [selectedQuestionId, setSelectedQuestionId] = useState<number | null>(null);
  const [responses, setResponses] = useState<Response[]>([]);
  const [analysis, setAnalysis] = useState<Analysis | null>(null);

  useEffect(() => {
    getQuestions().then(setQuestions);
  }, []);

  useEffect(() => {
    if (selectedQuestionId !== null) {
      getQuestionDetail(selectedQuestionId).then(({ responses, analysis }) => {
        setResponses(responses);
        setAnalysis(analysis);
      });
    }
  }, [selectedQuestionId]);

  const selectedQuestion = questions.find((q) => q.id === selectedQuestionId);

  return (
    <div className="min-h-screen flex bg-gray-100">
      <QuestionList questions={questions} onSelect={setSelectedQuestionId} />
      {selectedQuestion && analysis && (
        <QuestionDetail question={selectedQuestion} responses={responses} analysis={analysis} />
      )}
    </div>
  );
};

export default Home;
