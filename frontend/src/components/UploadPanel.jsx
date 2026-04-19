import { useState } from 'react'

export default function UploadPanel({ onAnalyze, loading }) {
  const [file, setFile] = useState(null)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!file) return
    onAnalyze(file)
  }

  return (
    <div className="card">
      <h2>Upload file</h2>
      <p>Upload a PDF or TXT file to generate academic outputs.</p>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".pdf,.txt" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button type="submit" disabled={!file || loading}>
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </form>
    </div>
  )
}
