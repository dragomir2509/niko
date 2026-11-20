import { INVEST_WORD, MONOGRAM, WORDMARK } from "./logo-paths";

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

/**
 * Logo: the RN monogram followed by the word INVEST on the same baseline.
 * The monogram is the "RN", so the letters are not repeated in the word.
 */
export function Logo({ className }: { className?: string }) {
  const m = MONOGRAM.text;
  const capHeight = 36;
  const scale = capHeight / INVEST_WORD.cap;
  const gap = 28;
  const width = m.w + gap + INVEST_WORD.w * scale;
  return (
    <svg
      className={className}
      viewBox={`0 0 ${width.toFixed(1)} 100`}
      fill="currentColor"
      aria-hidden="true"
    >
      <path d={m.d} />
      <g transform={`translate(${m.w + gap} ${100 - capHeight}) scale(${scale.toFixed(5)})`}>
        <path d={INVEST_WORD.d} />
      </g>
    </svg>
  );
}
