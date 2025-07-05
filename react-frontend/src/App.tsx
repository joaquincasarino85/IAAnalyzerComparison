// src/App.tsx
import React, { useEffect, useState } from "react";
import QuestionInput from "./components/QuestionInput";
import QuestionList from "./components/QuestionList";
import AnalysisPanel from "./components/AnalysisPanel";
import { QuestionWithData } from "@/types";
import axios from "axios";

const App = () => {
  const [questions, setQuestions] = useState<QuestionWithData[]>([]);
  const [selectedQuestion, setSelectedQuestion] = useState<QuestionWithData | null>(null);
  const [loading, setLoading] = useState(false);

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
      const res = await axios.post("http://127.0.0.1:8000/questions/", { text });
      await fetchQuestions();
      const full = await axios.get(`http://127.0.0.1:8000/questions/${res.data.question_id}`);
      setSelectedQuestion(full.data);
    } catch (error) {
      console.error("Error asking question:", error);
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
      <QuestionInput onQuestionAsked={handleQuestionAsked} loading={loading} />
      <div className="flex gap-6">
        <QuestionList questions={questions} onSelect={handleSelectQuestion} />
        <AnalysisPanel question={selectedQuestion} />
      </div>
    </div>
  );
};

export default App;
