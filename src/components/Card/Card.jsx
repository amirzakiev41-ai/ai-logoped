function Card({ children, className = "" }) {
  return (
    <div className={`word-card ${className}`}>
      {children}
    </div>
  );
}

export default Card;