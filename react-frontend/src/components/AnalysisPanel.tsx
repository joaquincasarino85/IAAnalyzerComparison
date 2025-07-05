// src/components/AnalysisPanel.tsx
import React from "react";

interface Props {
  question: any | null;
}

const AnalysisPanel = ({ question }: Props) => {
  if (!question) {
    return <div className="text-gray-500 italic">Select a question to view analysis.</div>;
  }

  const {
    text,
    summary,
    similarity,
    semantic_similarity,
    contradictions,
    named_entities,
    sentiments,
    responses,
  } = question;

  return (
    <div className="w-full md:w-2/3 space-y-4">
      <h2 className="text-xl font-bold">Analysis Summary</h2>

      {/* Question Text */}
      <div className="p-4 border rounded bg-white">
        <h3 className="font-semibold">Question</h3>
        <p>{text}</p>
      </div>

      {/* Responses */}
      <div className="p-4 border rounded bg-gray-50">
        <h3 className="font-semibold">Responses</h3>
        <ul className="space-y-2">
          {responses && responses.length > 0 ? (
            responses.map((r: any, index: number) => (
              <li key={index} className="p-2 bg-white rounded shadow">
                <strong>{r.iaName}:</strong> {r.text}
              </li>
            ))
          ) : (
            <li className="text-gray-400 italic">No responses available.</li>
          )}
        </ul>
      </div>

      {/* Summary */}
      <div className="p-4 border rounded bg-gray-50">
        <h3 className="font-semibold">Summary</h3>
        <p>{summary || <span className="text-gray-400 italic">No summary available.</span>}</p>
      </div>

      {/* Similarity */}
      <div className="p-4 border rounded bg-gray-50">
        <h3 className="font-semibold">Similarity</h3>
        {Array.isArray(similarity) && similarity.length > 0 ? (
          <ul className="list-disc ml-5">
            {similarity.map((item: any, idx: number) => (
              <li key={idx}>
                <strong>{item.ai1} vs {item.ai2}:</strong> {(item.score * 100).toFixed(1)}%
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-400 italic">No similarity data available.</p>
        )}
      </div>

      {/* Semantic Similarity */}
      <div className="p-4 border rounded bg-gray-50">
        <h3 className="font-semibold">Semantic Similarity</h3>
        {Array.isArray(semantic_similarity) && semantic_similarity.length > 0 ? (
          <ul className="list-disc ml-5">
            {semantic_similarity.map((item: any, idx: number) => (
              <li key={idx}>
                <strong>{item.ai1} vs {item.ai2}:</strong> {(item.score * 100).toFixed(1)}%
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-400 italic">No semantic similarity data available.</p>
        )}
      </div>

      {/* Contradictions */}
      <div className="p-4 border rounded bg-gray-50">
        <h3 className="font-semibold">Contradictions</h3>
        <ul className="list-disc ml-5">
          {Array.isArray(contradictions) && contradictions.length > 0 ? (
            contradictions.map((c: any, index: number) => (
              <li key={index}>
                {c.ai1} vs {c.ai2}: <strong>{c.label}</strong> ({(c.score * 100).toFixed(1)}%)
              </li>
            ))
          ) : (
            <li className="text-gray-400 italic">No contradictions found.</li>
          )}
        </ul>
      </div>

      {/* Sentiments */}
      <div className="p-4 border rounded bg-gray-50">
        <h3 className="font-semibold">Sentiments</h3>
        <ul>
          {sentiments && Object.keys(sentiments).length > 0 ? (
            Object.entries(sentiments).map(([ia, sentimentList]) => (
              <li key={ia}>
                <strong>{ia}:</strong>{" "}
                {sentimentList.map((s: any) => `${s.label} (${(s.score * 100).toFixed(1)}%)`).join(", ")}
              </li>
            ))
          ) : (
            <li className="text-gray-400 italic">No sentiment data available.</li>
          )}
        </ul>
      </div>

      {/* Named Entities */}
      <div className="p-4 border rounded bg-gray-50">
        <h3 className="font-semibold">Named Entities</h3>
        <ul>
          {named_entities && Object.keys(named_entities).length > 0 ? (
            Object.entries(named_entities).map(([ia, entities]) => (
              <li key={ia}>
                <strong>{ia}:</strong>{" "}
                {entities.map((e: any) => `${e.entity} (${e.label})`).join(", ")}
              </li>
            ))
          ) : (
            <li className="text-gray-400 italic">No named entities found.</li>
          )}
        </ul>
      </div>
    </div>
  );
};

export default AnalysisPanel;
