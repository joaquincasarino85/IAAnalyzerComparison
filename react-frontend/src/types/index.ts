export interface Question {
  id: number;
  text: string;
}

export interface Response {
  id: number;
  iaName: string;
  text: string;
}

export interface Analysis {
  summary: string;
  similarity: number;
  semantic_similarity: number;
  contradictions: string[];
  entities: string[];
  sentiments: string[];
}

export interface QuestionDetailProps {
  question: Question;
  responses: Response[];
  analysis: Analysis;
}
