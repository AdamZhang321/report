import { useEffect, useState } from 'react';

export default function ReportResult() {
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 从URL参数中获取报告ID
    const reportId = new URLSearchParams(window.location.search).get('reportId');
    
    if (reportId) {
      fetch(`/api/getReportResult?reportId=${reportId}`)
        .then(res => res.json())
        .then(data => {
          setResult(data.result);
          setLoading(false);
        });
    }
  }, []);

  if (loading) {
    return <div className="min-h-screen bg-blue-600 p-4 flex items-center justify-center">
      <div className="text-white">正在解析报告...</div>
    </div>;
  }

  return (
    <div className="min-h-screen bg-blue-600 p-4">
      <div className="max-w-2xl mx-auto bg-white rounded-lg p-6">
        <h1 className="text-2xl font-bold mb-4">体检报告解读结果</h1>
        <div className="whitespace-pre-wrap">{result}</div>
      </div>
    </div>
  );
} 