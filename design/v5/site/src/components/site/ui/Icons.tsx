export function Arrow() {
  return (
    <svg
      className="arrow"
      viewBox="0 0 21 14"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.2"
      aria-hidden="true"
    >
      <path d="M0 7h19M13 1l6 6-6 6" />
    </svg>
  );
}

/** Two parallel strokes at the angle of the monogram diagonals. */
export function Slashes() {
  return (
    <svg className="slashes" viewBox="0 0 22 20" fill="currentColor" aria-hidden="true">
      <path d="M0 0h5l6.4 20h-5zM10.6 0h5l6.4 20h-5z" />
    </svg>
  );
}
