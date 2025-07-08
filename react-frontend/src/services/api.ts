import { Question, Response, Analysis } from "../types";

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
  const res = await fetch(`${API_URL}/questions`);
  return res.json();
};

export const getQuestionDetail = async (
  id: number
): Promise<{ responses: Response[]; analysis: Analysis }> => {
  const res = await fetch(`${API_URL}/questions/${id}/full`);
  return res.json();
};

export { API_URL };
