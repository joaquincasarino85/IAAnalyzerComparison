// src/components/QuestionList.tsx
import React from "react";

const QuestionList = ({
  questions,
  onSelect,
  selectedId,
  loadingId,
}: {
  questions: any[];
  onSelect: (id: number) => void;
  selectedId: number | undefined;
  loadingId: number | null;
}) => {
  return (
    <div className="w-1/3 space-y-2 overflow-y-auto max-h-[70vh]">
      <h2 className="text-xl font-semibold mb-2">Historial</h2>
      {questions.map((q) => {
        const isSelected = selectedId === q.id;
        const isLoading = loadingId === q.id;

        return (
          <div
            key={q.id}
            onClick={() => onSelect(q.id)}
            className={`p-3 rounded border cursor-pointer transition-all ${
              isSelected ? "bg-blue-100 border-blue-500" : "bg-white border-gray-300"
            } hover:bg-blue-50`}
          >
            <p className="font-medium truncate">{q.text}</p>
            {isLoading && <p className="text-sm text-blue-600">Analizando...</p>}
          </div>
        );
      })}
    </div>
  );
};

export default QuestionList;
