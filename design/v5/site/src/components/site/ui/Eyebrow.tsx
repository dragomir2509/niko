import { Slashes } from "./Icons";

export function Eyebrow({ index, children }: { index?: string; children: string }) {
  return (
    <p className="micro eyebrow">
      <Slashes />
      <span>{index ? `${index} — ${children}` : children}</span>
    </p>
  );
}
