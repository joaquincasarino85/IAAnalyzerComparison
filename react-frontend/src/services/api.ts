import { Question, Response, Analysis, AIProgress } from "../types";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

declare global {
  interface ImportMetaEnv {
    readonly VITE_API_URL: string;
  }
  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }
}

export const getQuestions = async (): Promise<Question[]> => {
  const res = await fetch(`${API_URL}/questions/`);
  return res.json();
};

export const getQuestionDetail = async (
  id: number
): Promise<{ responses: Response[]; analysis: Analysis }> => {
  const res = await fetch(`${API_URL}/questions/${id}`);
  return res.json();
};

// Nueva API para requests paralelos
export const querySingleAI = async (question: string, aiName: string): Promise<any> => {
  const res = await fetch(`${API_URL}/ai/query-single-ai`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text: question, ai_name: aiName }),
  });
  return res.json();
};

export const queryAllAIs = async (question: string): Promise<any> => {
  const res = await fetch(`${API_URL}/ai/query-all-ais`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text: question }),
  });
  return res.json();
};

export const generateSummary = async (questionId: number): Promise<any> => {
  const res = await fetch(`${API_URL}/analysis/generate-summary`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ question_id: questionId }),
  });
  return res.json();
};

export const performFullAnalysis = async (questionId: number): Promise<any> => {
  const res = await fetch(`${API_URL}/analysis/full-analysis`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ question_id: questionId }),
  });
  return res.json();
};

export { API_URL };
