import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  ScatterChart,
  Scatter,
  ZAxis
} from 'recharts';

interface AnalysisGraphsProps {
  question: any | null;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];

const AnalysisGraphs: React.FC<AnalysisGraphsProps> = ({ question }) => {
  if (!question) {
    return <div className="text-gray-500 italic">Select a question to view analysis graphs.</div>;
  }

  const {
    similarity,
    semantic_similarity,
    contradictions,
    sentiments,
    named_entities,
    responses
  } = question;

  // Prepare similarity data for bar chart
  const similarityData = Array.isArray(similarity) ? similarity.map(item => ({
    name: `${item.ai1} vs ${item.ai2}`,
    similarity: (item.score * 100).toFixed(1),
    value: item.score * 100
  })) : [];

  // Prepare semantic similarity data
  const semanticData = Array.isArray(semantic_similarity) ? semantic_similarity.map(item => ({
    name: `${item.ai1} vs ${item.ai2}`,
    semantic: (item.score * 100).toFixed(1),
    value: item.score * 100
  })) : [];

  // Prepare contradiction data
  const contradictionData = Array.isArray(contradictions) ? contradictions.map(item => ({
    name: `${item.ai1} vs ${item.ai2}`,
    score: (item.score * 100).toFixed(1),
    label: item.label,
    value: item.score * 100
  })) : [];

  // Prepare sentiment data
  const sentimentData = sentiments && Object.keys(sentiments).length > 0 ? 
    Object.entries(sentiments).flatMap(([ai, sentimentList]) =>
      sentimentList.map((s: any) => ({
        ai: ai,
        sentiment: s.label,
        score: (s.score * 100).toFixed(1),
        value: s.score * 100
      }))
    ) : [];

  // Prepare named entities data
  const entityData = named_entities && Object.keys(named_entities).length > 0 ?
    Object.entries(named_entities).flatMap(([ai, entities]) =>
      entities.map((e: any) => ({
        ai: ai,
        entity: e.entity,
        label: e.label
      }))
    ) : [];

  // Count entities by type
  const entityCounts = entityData.reduce((acc: any, item) => {
    acc[item.label] = (acc[item.label] || 0) + 1;
    return acc;
  }, {});

  const entityPieData = Object.entries(entityCounts).map(([label, count]) => ({
    name: label,
    value: count
  }));

  // Prepare AI comparison radar data
  const aiNames = responses ? responses.map((r: any) => r.iaName) : [];
  const radarData = aiNames.map(ai => {
    const aiSentiments = sentimentData.filter((s: any) => s.ai === ai);
    const avgSentiment = aiSentiments.length > 0 ? 
      aiSentiments.reduce((sum: number, s: any) => sum + s.value, 0) / aiSentiments.length : 0;
    
    return {
      ai: ai,
      sentiment: avgSentiment,
      entities: entityData.filter((e: any) => e.ai === ai).length,
      responseLength: responses.find((r: any) => r.iaName === ai)?.text.length || 0
    };
  });

  return (
    <div className="w-full space-y-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Analysis Visualizations</h2>
      
      {/* Similarity Comparison */}
      {similarityData.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4">Text Similarity Between AI Responses</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={similarityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip formatter={(value) => [`${value}%`, 'Similarity']} />
              <Legend />
              <Bar dataKey="value" fill="#8884d8" name="Similarity %" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Semantic Similarity */}
      {semanticData.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4">Semantic Similarity (Cosine Similarity)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={semanticData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip formatter={(value) => [`${value}%`, 'Semantic Similarity']} />
              <Legend />
              <Bar dataKey="value" fill="#82ca9d" name="Semantic Similarity %" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Contradictions Analysis */}
      {contradictionData.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4">Contradiction Analysis (NLI)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={contradictionData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip 
                formatter={(value, name, props) => [
                  `${value}% - ${props.payload.label}`, 
                  'Confidence'
                ]} 
              />
              <Legend />
              <Bar dataKey="value" fill="#ffc658" name="Confidence %" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Sentiment Analysis */}
      {sentimentData.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4">Sentiment Analysis by AI</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={sentimentData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="ai" />
              <YAxis domain={[0, 100]} />
              <Tooltip formatter={(value, name, props) => [
                `${value}% - ${props.payload.sentiment}`, 
                'Sentiment Score'
              ]} />
              <Legend />
              <Bar dataKey="value" fill="#ff7300" name="Sentiment Score %" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Named Entities Distribution */}
      {entityPieData.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4">Named Entities Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={entityPieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {entityPieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* AI Comparison Radar Chart */}
      {radarData.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4">AI Response Comparison</h3>
          <ResponsiveContainer width="100%" height={400}>
            <RadarChart data={radarData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="ai" />
              <PolarRadiusAxis angle={30} domain={[0, 'dataMax']} />
              <Radar
                name="Sentiment Score"
                dataKey="sentiment"
                stroke="#8884d8"
                fill="#8884d8"
                fillOpacity={0.6}
              />
              <Radar
                name="Entity Count"
                dataKey="entities"
                stroke="#82ca9d"
                fill="#82ca9d"
                fillOpacity={0.6}
              />
              <Radar
                name="Response Length"
                dataKey="responseLength"
                stroke="#ffc658"
                fill="#ffc658"
                fillOpacity={0.6}
              />
              <Legend />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Combined Similarity Comparison */}
      {similarityData.length > 0 && semanticData.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4">Text vs Semantic Similarity Comparison</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip formatter={(value) => [`${value}%`, 'Similarity']} />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="similarity" 
                data={similarityData} 
                stroke="#8884d8" 
                name="Text Similarity" 
              />
              <Line 
                type="monotone" 
                dataKey="semantic" 
                data={semanticData} 
                stroke="#82ca9d" 
                name="Semantic Similarity" 
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
};

export default AnalysisGraphs; 