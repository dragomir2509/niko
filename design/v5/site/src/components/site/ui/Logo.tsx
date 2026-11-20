import { MONOGRAM, WORDMARK } from "./logo-paths";

type Size = keyof typeof MONOGRAM;

/** RN monogram. Pick the optical size that matches the rendered height. */
export function Monogram({ size = "text", className }: { size?: Size; className?: string }) {
  const m = MONOGRAM[size];
  return (
    <svg className={className} viewBox={`0 0 ${m.w} 100`} fill="currentColor" aria-hidden="true">
      <path d={m.d} />
    </svg>
  );
}

/** Wordmark "RN INVEST" as outlines, independent of loaded fonts. */
export function Wordmark({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox={`0 0 ${WORDMARK.w} ${WORDMARK.cap}`}
      fill="currentColor"
      aria-hidden="true"
    >
      <path d={WORDMARK.d} />
    </svg>
  );
}

/** Horizontal lockup: monogram plus wordmark at 30 % of the monogram height. */
export function Logo({ className }: { className?: string }) {
  const m = MONOGRAM.text;
  const scale = 30 / WORDMARK.cap;
  const gap = 34;
  const width = m.w + gap + WORDMARK.w * scale;
  return (
    <svg
      className={className}
      viewBox={`0 0 ${width.toFixed(1)} 100`}
      fill="currentColor"
      aria-hidden="true"
    >
      <path d={m.d} />
      <g transform={`translate(${m.w + gap} 35) scale(${scale.toFixed(5)})`}>
        <path d={WORDMARK.d} />
      </g>
    </svg>
  );
}
