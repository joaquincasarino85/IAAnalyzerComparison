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

// Extended interface for questions with full analysis data
export interface QuestionWithData {
  id: number;
  text: string;
  summary?: string;
  similarity?: Array<{
    ai1: string;
    ai2: string;
    score: number;
  }>;
  semantic_similarity?: Array<{
    ai1: string;
    ai2: string;
    score: number;
  }>;
  contradictions?: Array<{
    ai1: string;
    ai2: string;
    label: string;
    score: number;
  }>;
  named_entities?: {
    [aiName: string]: Array<{
      entity: string;
      label: string;
    }>;
  };
  sentiments?: {
    [aiName: string]: Array<{
      label: string;
      score: number;
    }>;
  };
  responses?: Array<{
    iaName: string;
    text: string;
  }>;
}
