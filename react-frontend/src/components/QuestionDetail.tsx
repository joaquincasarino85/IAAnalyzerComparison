import React from "react";
import { QuestionDetailProps } from "../types";
import { AnalysisPanel } from "./AnalysisPanel";

export const QuestionDetail: React.FC<QuestionDetailProps> = ({ question, responses, analysis }) => (
  <div className="w-full md:w-2/3 p-4">
    <h2 className="text-xl font-bold mb-4">{question.text}</h2>
    <div className="space-y-4">
      <div>
        <h3 className="font-semibold">Responses</h3>
        <ul className="space-y-2">
          {responses.map((r) => (
            <li key={r.id} className="p-2 bg-white rounded shadow">
              <strong>{r.iaName}:</strong> {r.text}
            </li>
          ))}
        </ul>
      </div>
      <AnalysisPanel analysis={analysis} />
    </div>
  </div>
);
