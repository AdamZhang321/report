import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'

export default function Component() {
  const [agreed, setAgreed] = useState(false);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleUpload = async () => {
    if (!agreed) {
      alert('请先同意隐私协议');
      return;
    }

    fileInputRef.current.click();
  };

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file || file.type !== 'application/pdf') {
      alert('请选择PDF文件');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/uploadReport', {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      if (data.reportId) {
        navigate(`/result?reportId=${data.reportId}`);
      }
    } catch (error) {
      console.error('Upload failed:', error);
      alert('上传失败，请重试');
    } finally {
      setUploading(false);
    }
  };

  // 在返回的JSX中修改相关部分
  return (
    <div className="min-h-screen bg-blue-600 p-4 space-y-6">
      {/* ... 其他部分保持不变 ... */}
      
      {/* Footer Section */}
      <div className="max-w-2xl mx-auto space-y-4">
        <div className="flex items-center gap-2 justify-center">
          <Checkbox 
            id="terms" 
            checked={agreed}
            onCheckedChange={setAgreed}
          />
          <label htmlFor="terms" className="text-white text-sm">
            勾选即同意《报告解读助手隐私协议》
          </label>
        </div>
        <input
          type="file"
          accept=".pdf"
          ref={fileInputRef}
          onChange={handleFileChange}
          className="hidden"
        />
        <Button 
          className="w-full bg-white text-blue-600 hover:bg-white/90" 
          size="lg"
          onClick={handleUpload}
          disabled={uploading}
        >
          {uploading ? '正在上传...' : '上传报告'}
        </Button>
      </div>
    </div>
  )
} 