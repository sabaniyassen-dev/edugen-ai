export default function HistoryPanel({ items, onSelect }) {
  return (
    <div className="card">
      <h2>History</h2>
      {items.length === 0 ? <p>No previous analyses yet.</p> : null}
      <div className="history-list">
        {items.map((item) => (
          <button key={item.id} className="history-item" onClick={() => onSelect(item)}>
            <strong>{item.filename}</strong>
            <span>Analysis #{item.id}</span>
          </button>
        ))}
      </div>
    </div>
  )
}
