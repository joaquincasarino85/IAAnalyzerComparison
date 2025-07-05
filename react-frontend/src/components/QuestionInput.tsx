import { useState } from "react";

interface Props {
  onQuestionAsked: (question: string) => void;
  loading: boolean;
}

export default function QuestionInput({ onQuestionAsked, loading }: Props) {
  const [question, setQuestion] = useState("");

  const askQuestion = () => {
    if (!question.trim()) return;
    onQuestionAsked(question);
    setQuestion("");
  };

  return (
    <div className="flex gap-2 mb-6">
      <input
        type="text"
        placeholder="Ask a question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        className="flex-1 p-2 border rounded-xl shadow"
        disabled={loading}
      />
      <button
        onClick={askQuestion}
        disabled={loading}
        className="px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700"
      >
        {loading ? "Sending..." : "Ask"}
      </button>
    </div>
  );
}