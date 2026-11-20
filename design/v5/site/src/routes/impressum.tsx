import { createFileRoute } from "@tanstack/react-router";
import { SITE } from "@/config/site";
import { getSiteUrl } from "@/lib/site-url";
import { LegalPage } from "@/components/site/LegalPage";

const URL = `${getSiteUrl(SITE.url)}/impressum`;
const TITLE = "Impressum | RN INVEST";
const DESC = `Impressum und Anbieterkennzeichnung der ${SITE.legalName}, ${SITE.city}.`;

export const Route = createFileRoute("/impressum")({
  staticData: { sitemap: true },
  component: Impressum,
  head: () => ({
    meta: [
      { title: TITLE },
      { name: "description", content: DESC },
      { property: "og:title", content: TITLE },
      { property: "og:description", content: DESC },
      { property: "og:url", content: URL },
      { property: "og:type", content: "website" },
    ],
    links: [{ rel: "canonical", href: URL }],
  }),
});

function Impressum() {
  return (
    <LegalPage eyebrow="Rechtliches" title="Impressum">
      <h2>Angaben gemäß § 5 DDG</h2>
      <address>
        {SITE.legalName}
        <br />
        {SITE.street}
        <br />
        {SITE.postalCode} {SITE.city}
        <br />
        {SITE.country}
      </address>

      <h2>Vertretung</h2>
      <p>Geschäftsführer: {SITE.managingDirector}</p>

      <h2>Kontakt</h2>
      <p>
        E-Mail: <a href={`mailto:${SITE.email}`}>{SITE.email}</a>
      </p>

      <h2>Registereintrag</h2>
      <p>
        Registergericht: {SITE.registerCourt}
        <br />
        Registernummer: {SITE.registerNumber}
      </p>

      <h2>Verantwortlich für den Inhalt</h2>
      <p>{SITE.managingDirector}, Anschrift wie oben (§ 18 Abs. 2 MStV).</p>

      <h2>Hinweis zum Angebot dieser Website</h2>
      <p>
        Diese Website informiert über {SITE.name} und über das Ankaufsprofil der Gesellschaft. Sie
        richtet sich nicht an Kapitalanleger und enthält weder ein Angebot noch eine Aufforderung
        zum Erwerb von Beteiligungen, Wertpapieren oder sonstigen Finanzinstrumenten. Das
        Ankaufsprofil beschreibt Suchkriterien und begründet keine Verpflichtung zum Ankauf.
      </p>

      <h2>Haftung für Inhalte und Links</h2>
      <p>
        Die Inhalte dieser Website werden mit Sorgfalt erstellt. Für die Richtigkeit,
        Vollständigkeit und Aktualität wird keine Gewähr übernommen. Für Inhalte externer Websites,
        auf die verwiesen wird, sind ausschließlich deren Betreiber verantwortlich.
      </p>

      <h2>Urheberrecht</h2>
      <p>
        Texte, Gestaltung, Logo und Monogramm dieser Website sind urheberrechtlich geschützt. Eine
        Verwendung über die Grenzen des Urheberrechts hinaus bedarf der vorherigen Zustimmung der{" "}
        {SITE.legalName}.
      </p>
    </LegalPage>
  );
}
