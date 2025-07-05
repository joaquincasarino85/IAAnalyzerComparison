import { useState, useEffect, useCallback } from 'react';

interface UseProgressSimulationProps {
  duration?: number; // Duration in milliseconds
  steps?: string[];
  onComplete?: () => void;
}

export const useProgressSimulation = ({
  duration = 15000, // 15 seconds default
  steps = [
    "Initializing AI models (ChatGPT, Gemini, Mistral, Cohere, Perplexity)...",
    "Sending question to ChatGPT...",
    "Sending question to Gemini...",
    "Sending question to Mistral...",
    "Sending question to Cohere...",
    "Sending question to Perplexity...",
    "Receiving responses from all AI models...",
    "Analyzing responses and generating comparisons...",
    "Finalizing results and preparing analysis..."
  ],
  onComplete
}: UseProgressSimulationProps = {}) => {
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [currentMessage, setCurrentMessage] = useState('');

  const startProgress = useCallback(() => {
    setIsRunning(true);
    setProgress(0);
    setCurrentStep(0);
    setCurrentMessage(steps[0]);
  }, [steps]);

  const stopProgress = useCallback(() => {
    setIsRunning(false);
    setProgress(100);
    setCurrentStep(steps.length - 1);
    setCurrentMessage(steps[steps.length - 1]);
  }, [steps]);

  const resetProgress = useCallback(() => {
    setIsRunning(false);
    setProgress(0);
    setCurrentStep(0);
    setCurrentMessage('');
  }, []);

  useEffect(() => {
    if (!isRunning) return;

    const stepDuration = duration / steps.length;
    const progressIncrement = 100 / steps.length;

    const interval = setInterval(() => {
      setProgress(prev => {
        const newProgress = prev + progressIncrement;
        
        if (newProgress >= 100) {
          setIsRunning(false);
          setProgress(100);
          setCurrentStep(steps.length - 1);
          setCurrentMessage(steps[steps.length - 1]);
          onComplete?.();
          return 100;
        }

        const nextStep = Math.floor(newProgress / progressIncrement);
        if (nextStep !== currentStep && nextStep < steps.length) {
          setCurrentStep(nextStep);
          setCurrentMessage(steps[nextStep]);
        }

        return newProgress;
      });
    }, stepDuration);

    return () => clearInterval(interval);
  }, [isRunning, duration, steps, currentStep, onComplete]);

  return {
    progress,
    currentStep,
    currentMessage,
    isRunning,
    startProgress,
    stopProgress,
    resetProgress
  };
}; 