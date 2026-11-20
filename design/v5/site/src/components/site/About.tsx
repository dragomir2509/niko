import { CONTENT } from "@/content/site";
import { Eyebrow } from "./ui/Eyebrow";
import { Reveal } from "./ui/Reveal";

export function About() {
  const c = CONTENT.about;
  return (
    <section id="ueber" className="section" aria-labelledby="about-title">
      <Reveal className="wrap grid">
        <div className="about-head">
          <Eyebrow index="01">{c.eyebrow}</Eyebrow>
        </div>
        <h2 id="about-title" className="about-statement">
          {c.title[0]}
          <br />
          {c.title[1]}
        </h2>
        <div className="about-body">
          <p className="lead">{c.lead}</p>
          <p className="muted">{c.text}</p>
        </div>
        <dl className="about-facts facts">
          {c.facts.map((f) => (
            <div key={f.label}>
              <dt className="micro">{f.label}</dt>
              <dd>{f.value}</dd>
            </div>
          ))}
        </dl>
      </Reveal>
    </section>
  );
}
