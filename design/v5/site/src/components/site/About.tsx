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
        <aside className="about-person" aria-labelledby="about-person-name">
          <p className="micro muted">{c.person.label}</p>
          <h3 id="about-person-name">{c.person.name}</h3>
          <p className="about-role muted">{c.person.role}</p>
          <blockquote>
            <p>„{c.person.quote}“</p>
          </blockquote>
          <ul>
            {c.person.points.map((point) => (
              <li key={point}>{point}</li>
            ))}
          </ul>
        </aside>
      </Reveal>
    </section>
  );
}
