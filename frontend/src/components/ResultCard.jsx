export default function ResultCard({ title, content }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      <pre>{content}</pre>
    </div>
  )
}
