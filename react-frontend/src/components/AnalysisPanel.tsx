// src/components/AnalysisPanel.tsx
import React from "react";
import { markdownToHtml } from "../markdownToHtml";

// Diccionario de colores e íconos para cada IA
const IA_STYLES: Record<string, { color: string; icon: string }> = {
  ChatGPT: { color: 'text-green-600', icon: '🤖' },
  Gemini: { color: 'text-blue-600', icon: '🔷' },
  Mistral: { color: 'text-orange-500', icon: '🌬️' },
  Cohere: { color: 'text-purple-600', icon: '🟣' },
  Perplexity: { color: 'text-gray-600', icon: '❓' },
  default: { color: 'text-gray-700', icon: '💡' },
};

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
    <div className="w-full space-y-4">
      <h2 className="text-xl font-bold mb-4">Summary & Analysis</h2>

      {/* Question */}
      <div className="p-4 border rounded bg-white mb-2">
        <h3 className="font-semibold mb-1">Question</h3>
        <p className="text-base text-gray-800">{text}</p>
      </div>

      {/* Responses */}
      <div className="p-4 border rounded bg-white mb-2">
        <h3 className="font-semibold mb-2">AI Responses</h3>
        <ul className="space-y-6">
          {responses && responses.length > 0 ? (
            responses.map((r: any, index: number) => {
              const style = IA_STYLES[r.iaName] || IA_STYLES.default;
              return (
                <li key={index} className="p-4 bg-gray-50 rounded shadow-sm">
                  <div className="flex items-center mb-2">
                    <span className={`text-xl mr-2 ${style.color}`}>{style.icon}</span>
                    <span className="font-bold text-lg">{r.iaName}</span>
                  </div>
                  <div
                    className="text-gray-800"
                    dangerouslySetInnerHTML={{ __html: markdownToHtml(r.text) }}
                  />
                </li>
              );
            })
          ) : (
            <li className="text-gray-400 italic">No responses available.</li>
          )}
        </ul>
      </div>

      {/* Summary */}
      <div className="p-4 border rounded bg-white mb-2">
        <h3 className="font-semibold mb-2">Summary</h3>
        <p className="text-base text-gray-900 font-medium">
          {summary || <span className="text-gray-400 italic">No summary available.</span>}
        </p>
      </div>

      {/* Similarity */}
      <div className="p-4 border rounded bg-white mb-2">
        <h3 className="font-semibold mb-2">Similarity</h3>
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
      <div className="p-4 border rounded bg-white mb-2">
        <h3 className="font-semibold mb-2">Semantic Similarity</h3>
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
      <div className="p-4 border rounded bg-white mb-2">
        <h3 className="font-semibold mb-2">Contradictions</h3>
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
      <div className="p-4 border rounded bg-white mb-2">
        <h3 className="font-semibold mb-2">Sentiments</h3>
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
      <div className="p-4 border rounded bg-white mb-2">
        <h3 className="font-semibold mb-2">Named Entities</h3>
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
