import { CONTENT } from "@/content/site";
import { Monogram } from "./ui/Logo";
import { Button } from "./ui/Button";

export function Hero() {
  const c = CONTENT.hero;
  return (
    <section id="top" className="hero" aria-labelledby="hero-title">
      <div className="wrap hero-inner">
        <Monogram size="display" className="hero-mark" />
        <div className="hero-meta micro">
          <span>{c.metaLeft}</span>
          <span>{c.metaRight}</span>
        </div>
        <h1 id="hero-title">
          {c.lines.map((line) => (
            <span className="line" key={line}>
              <span>{line} </span>
            </span>
          ))}
          <span className="line accent">
            <span>
              {c.accentLine[0]} <br className="br-s" />
              {c.accentLine[1]}
            </span>
          </span>
        </h1>
        <div className="hero-foot">
          <p className="lead">{c.lead}</p>
          <div className="hero-actions">
            <Button href="#ankaufsprofil" solid>
              {c.primaryCta}
            </Button>
            <Button href="#kontakt">{c.secondaryCta}</Button>
          </div>
        </div>
      </div>
    </section>
  );
}
