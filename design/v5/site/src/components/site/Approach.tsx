import { CONTENT } from "@/content/site";
import { Eyebrow } from "./ui/Eyebrow";
import { Reveal } from "./ui/Reveal";

export function Approach() {
  const c = CONTENT.approach;
  return (
    <section id="ansatz" className="section on-dark" aria-labelledby="approach-title">
      <Reveal className="wrap grid">
        <div className="approach-head">
          <Eyebrow index="02">{c.eyebrow}</Eyebrow>
        </div>
        <h2 id="approach-title" className="approach-statement">
          {c.title[0]}
          <br />
          {c.title[1]}
        </h2>
        <ol className="principles">
          {c.principles.map((p) => (
            <li key={p.title}>
              <h3>{p.title}</h3>
              <p>{p.text}</p>
            </li>
          ))}
        </ol>
      </Reveal>
    </section>
  );
}
