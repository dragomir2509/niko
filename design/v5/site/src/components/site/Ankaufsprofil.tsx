import { SITE } from "@/config/site";
import { CONTENT } from "@/content/site";
import { monthLabel } from "@/lib/date";
import { prefillContact } from "@/lib/topic";
import { Eyebrow } from "./ui/Eyebrow";
import { Button } from "./ui/Button";
import { Reveal } from "./ui/Reveal";

function goToContact() {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.getElementById("kontakt")?.scrollIntoView({ behavior: reduce ? "instant" : "smooth" });
  window.setTimeout(
    () => document.getElementById("f-location")?.focus({ preventScroll: true }),
    reduce ? 0 : 700,
  );
}

function Places({ items, propertyType }: { items: readonly string[]; propertyType: string }) {
  return (
    <ul className="places">
      {items.map((place) => (
        <li key={place}>
          <button
            type="button"
            title={`${place} im Kontaktformular übernehmen`}
            onClick={() => {
              prefillContact({ location: place, propertyType });
              goToContact();
            }}
          >
            {place}
          </button>
        </li>
      ))}
    </ul>
  );
}

function Figure({ value, note }: { value: string; note: string }) {
  return (
    <dd className="fig">
      <span className="nowrap">{value}</span> <small>{note}</small>
    </dd>
  );
}

export function Ankaufsprofil() {
  const c = CONTENT.profile;
  const stand = `Stand ${monthLabel()}`;
  return (
    <section id="ankaufsprofil" className="section" aria-labelledby="profile-title">
      <Reveal className="wrap">
        <div className="grid">
          <div className="profile-head">
            <Eyebrow index="03">{c.eyebrow}</Eyebrow>
          </div>
          <h2 id="profile-title" className="profile-title">
            {c.title[0]}
            <br />
            {c.title[1]}
          </h2>
          <p className="profile-lead muted">{c.lead}</p>
        </div>
        <div className="dossiers">
          <article className="dossier" aria-labelledby="profile-a-title">
            <div className="dossier-top">
              <span className="micro">Profil {c.a.key}</span>
              <span className="mono">{stand}</span>
            </div>
            <p className="dossier-letter" aria-hidden="true">
              {c.a.key}
            </p>
            <h3 id="profile-a-title">{c.a.title}</h3>
            <dl className="spec">
              <div>
                <dt className="micro">Objektarten</dt>
                <dd>{c.a.types}</dd>
              </div>
              <div>
                <dt className="micro">Lagen München</dt>
                <dd>
                  <Places items={c.a.city} propertyType={c.a.propertyType} />
                </dd>
              </div>
              <div>
                <dt className="micro">Lagen Landkreis</dt>
                <dd>
                  <Places items={c.a.county} propertyType={c.a.propertyType} />
                </dd>
              </div>
              <div>
                <dt className="micro">Grundstück</dt>
                <Figure {...c.a.plotCity} />
              </div>
              <div>
                <dt className="micro">
                  <span className="sr-only">Grundstück</span>
                </dt>
                <Figure {...c.a.plotCounty} />
              </div>
            </dl>
            <Button
              href="#kontakt"
              onClick={() => prefillContact({ propertyType: c.a.propertyType })}
            >
              {c.a.cta}
            </Button>
          </article>
          <article className="dossier" aria-labelledby="profile-b-title">
            <div className="dossier-top">
              <span className="micro">Profil {c.b.key}</span>
              <span className="mono">{stand}</span>
            </div>
            <p className="dossier-letter" aria-hidden="true">
              {c.b.key}
            </p>
            <h3 id="profile-b-title">{c.b.title}</h3>
            <dl className="spec">
              <div>
                <dt className="micro">Objektarten</dt>
                <dd>{c.b.types}</dd>
              </div>
              <div>
                <dt className="micro">Voraussetzungen</dt>
                <dd>{c.b.requirements}</dd>
              </div>
              <div>
                <dt className="micro">Lagen München</dt>
                <dd>
                  <Places items={c.b.city} propertyType={c.b.propertyType} />
                </dd>
              </div>
              <div>
                <dt className="micro">Fläche</dt>
                <Figure {...c.b.area} />
              </div>
              <div className="spec-key">
                <dt className="micro">{c.b.price.label}</dt>
                <Figure value={c.b.price.value} note={c.b.price.note} />
              </div>
            </dl>
            <Button
              href="#kontakt"
              onClick={() => prefillContact({ propertyType: c.b.propertyType })}
            >
              {c.b.cta}
            </Button>
          </article>
        </div>
        <p className="profile-note micro">
          <span>{c.note}</span>
          <a className="link" href={`mailto:${SITE.email}`}>
            {SITE.email}
          </a>
        </p>
      </Reveal>
    </section>
  );
}
