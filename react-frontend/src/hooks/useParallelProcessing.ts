import { useState, useCallback } from 'react';
import { AIProgress, ProcessingStep } from '../types';
import { querySingleAI, queryAllAIs, generateSummary, performFullAnalysis } from '../services/api';

export const useParallelProcessing = () => {
  const [progress, setProgress] = useState<AIProgress>({
    currentStep: 0,
    totalSteps: 8, // 5 IAs + summary + analysis + final
    currentAI: '',
    status: 'pending',
    message: 'Initializing...',
    progress: 0
  });

  const [processingSteps, setProcessingSteps] = useState<ProcessingStep[]>([
    { step: 1, name: 'ChatGPT', status: 'pending', message: 'Waiting...' },
    { step: 2, name: 'Gemini', status: 'pending', message: 'Waiting...' },
    { step: 3, name: 'Mistral', status: 'pending', message: 'Waiting...' },
    { step: 4, name: 'Cohere', status: 'pending', message: 'Waiting...' },
    { step: 5, name: 'Perplexity', status: 'pending', message: 'Waiting...' },
    { step: 6, name: 'Generating Summary', status: 'pending', message: 'Waiting...' },
    { step: 7, name: 'Full Analysis', status: 'pending', message: 'Waiting...' },
    { step: 8, name: 'Finalizing', status: 'pending', message: 'Waiting...' }
  ]);

  const updateStep = useCallback((step: number, status: ProcessingStep['status'], message: string) => {
    setProcessingSteps(prev => 
      prev.map(s => 
        s.step === step 
          ? { ...s, status, message }
          : s
      )
    );
  }, []);

  const updateProgress = useCallback((currentStep: number, currentAI: string, message: string, status: AIProgress['status'] = 'processing') => {
    const progressPercent = (currentStep / progress.totalSteps) * 100;
    setProgress({
      currentStep,
      totalSteps: progress.totalSteps,
      currentAI,
      status,
      message,
      progress: progressPercent
    });
  }, [progress.totalSteps]);

  const processQuestion = useCallback(async (question: string) => {
    try {
      setProgress(prev => ({ ...prev, status: 'processing', message: 'Starting processing...' }));
      // Step 1-5: Query all AIs in parallel
      updateProgress(1, 'All AIs', 'Querying all AIs in parallel...');
      const aiNames = ['ChatGPT', 'Gemini', 'Mistral', 'Cohere', 'Perplexity'];
      // Update all AI steps to 'processing'
      aiNames.forEach((ai, index) => {
        updateStep(index + 1, 'processing', `Querying ${ai}...`);
      });
      // Query all AIs in parallel
      const responses = await queryAllAIs(question);
      // Mark all AIs as completed
      aiNames.forEach((ai, index) => {
        updateStep(index + 1, 'completed', `${ai} completed`);
      });
      updateProgress(6, 'Summary', 'Generating summary of all responses...');
      updateStep(6, 'processing', 'Generating summary...');
      // Step 6: Generate summary
      const summaryResult = await generateSummary(responses.question_id);
      updateStep(6, 'completed', 'Summary generated');
      updateProgress(7, 'Analysis', 'Performing full analysis...');
      updateStep(7, 'processing', 'Analyzing similarities, contradictions, entities, and sentiments...');
      // Step 7: Full analysis
      const analysisResult = await performFullAnalysis(responses.question_id);
      updateStep(7, 'completed', 'Analysis completed');
      updateProgress(8, 'Finalizing', 'Finalizing process...');
      updateStep(8, 'processing', 'Finalizing...');
      // Step 8: Finalize
      setTimeout(() => {
        updateStep(8, 'completed', 'Process completed');
        setProgress(prev => ({ ...prev, status: 'completed', message: 'Process completed successfully' }));
      }, 1000);
      return {
        questionId: responses.question_id,
        responses: responses.responses,
        summary: summaryResult.summary,
        analysis: analysisResult
      };
    } catch (error) {
      console.error('Error in parallel processing:', error);
      setProgress(prev => ({ 
        ...prev, 
        status: 'error', 
        message: `Error: ${error instanceof Error ? error.message : 'Unknown error'}` 
      }));
      throw error;
    }
  }, [updateProgress, updateStep]);

  const resetProgress = useCallback(() => {
    setProgress({
      currentStep: 0,
      totalSteps: 8,
      currentAI: '',
      status: 'pending',
      message: 'Initializing...',
      progress: 0
    });
    setProcessingSteps([
      { step: 1, name: 'ChatGPT', status: 'pending', message: 'Waiting...' },
      { step: 2, name: 'Gemini', status: 'pending', message: 'Waiting...' },
      { step: 3, name: 'Mistral', status: 'pending', message: 'Waiting...' },
      { step: 4, name: 'Cohere', status: 'pending', message: 'Waiting...' },
      { step: 5, name: 'Perplexity', status: 'pending', message: 'Waiting...' },
      { step: 6, name: 'Generating Summary', status: 'pending', message: 'Waiting...' },
      { step: 7, name: 'Full Analysis', status: 'pending', message: 'Waiting...' },
      { step: 8, name: 'Finalizing', status: 'pending', message: 'Waiting...' }
    ]);
  }, []);

  return {
    progress,
    processingSteps,
    processQuestion,
    resetProgress
  };
}; 