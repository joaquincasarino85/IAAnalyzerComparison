import { Question, Response, Analysis } from "../types";

export const getQuestions = async (): Promise<Question[]> => {
  const res = await fetch("http://localhost:8000/questions");
  return res.json();
};

export const getQuestionDetail = async (
  id: number
): Promise<{ responses: Response[]; analysis: Analysis }> => {
  const res = await fetch(`http://localhost:8000/questions/${id}/full`);
  return res.json();
};
