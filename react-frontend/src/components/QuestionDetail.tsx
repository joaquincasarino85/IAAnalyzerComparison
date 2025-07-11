import React from "react";
import { QuestionWithData } from "../types";
import AnalysisPanel from "./AnalysisPanel";

interface Props {
  question: QuestionWithData;
}

export const QuestionDetail: React.FC<Props> = ({ question }) => (
  <div className="w-full p-4">
    <h2 className="text-xl font-bold mb-4">{question.text}</h2>
    <div className="space-y-4">
      <AnalysisPanel question={question} />
    </div>
  </div>
);
