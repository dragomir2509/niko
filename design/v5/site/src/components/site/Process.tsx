import { CONTENT } from "@/content/site";
import { Eyebrow } from "./ui/Eyebrow";
import { Reveal } from "./ui/Reveal";

export function Process() {
  const c = CONTENT.process;
  return (
    <section id="prozess" className="section on-ultra" aria-labelledby="process-title">
      <Reveal className="wrap grid">
        <div className="process-head">
          <Eyebrow index="04">{c.eyebrow}</Eyebrow>
        </div>
        <h2 id="process-title" className="process-title">
          {c.title[0]}
          <br />
          {c.title[1]}
        </h2>
        <ol className="steps">
          {c.steps.map((s, i) => (
            <li key={s.title}>
              <span className="step-no" aria-hidden="true">
                0{i + 1}
              </span>
              <h3>{s.title}</h3>
              <p>{s.text}</p>
            </li>
          ))}
        </ol>
        <p className="process-note micro">{c.note}</p>
      </Reveal>
    </section>
  );
}
