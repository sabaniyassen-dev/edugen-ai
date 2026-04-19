import { useEffect, useState } from 'react'
import UploadPanel from './components/UploadPanel'
import ResultCard from './components/ResultCard'
import HistoryPanel from './components/HistoryPanel'
import { analyzeFile, getHistory } from './lib/api'

export default function App() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [history, setHistory] = useState([])
  const [current, setCurrent] = useState(null)

  async function loadHistory() {
    try {
      const data = await getHistory()
      setHistory(data)
      if (!current && data.length > 0) setCurrent(data[0])
    } catch {
      // ignore load errors on startup
    }
  }

  useEffect(() => {
    loadHistory()
  }, [])

  async function handleAnalyze(file) {
    setLoading(true)
    setError('')
    try {
      const result = await analyzeFile(file)
      setCurrent(result)
      await loadHistory()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <header className="hero">
        <h1>EduGen AI</h1>
        <p>Upload academic content and generate summary, questions, rubric, and study plan.</p>
      </header>

      <div className="grid">
        <div className="left-col">
          <UploadPanel onAnalyze={handleAnalyze} loading={loading} />
          <HistoryPanel items={history} onSelect={setCurrent} />
        </div>

        <div className="right-col">
          {error ? <div className="error">{error}</div> : null}
          {current ? (
            <>
              <ResultCard title="Summary" content={current.summary} />
              <ResultCard title="Questions" content={current.questions} />
              <ResultCard title="Rubric" content={current.rubric} />
              <ResultCard title="Study Plan" content={current.study_plan} />
            </>
          ) : (
            <div className="card">
              <h2>No analysis selected</h2>
              <p>Upload a file to begin.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
