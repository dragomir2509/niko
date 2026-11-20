import { createFileRoute } from "@tanstack/react-router";
import { SITE } from "@/config/site";
import { getSiteUrl } from "@/lib/site-url";
import { PRIVACY_VERSION } from "@/lib/privacy-settings";
import { LegalPage } from "@/components/site/LegalPage";
import { openPrivacySettings } from "@/lib/privacy-open";

const URL = `${getSiteUrl(SITE.url)}/datenschutz`;
const TITLE = "Datenschutzerklärung | RN INVEST";
const DESC =
  "Datenschutzhinweise der RN INVEST Website: Hosting, Kontaktformular, technisch notwendige Speicherung und Ihre Rechte.";

export const Route = createFileRoute("/datenschutz")({
  staticData: { sitemap: true },
  component: Datenschutz,
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

function Datenschutz() {
  const mail = <a href={`mailto:${SITE.email}`}>{SITE.email}</a>;
  return (
    <LegalPage eyebrow="Rechtliches" title="Datenschutzerklärung">
      <p className="legal-intro">
        Diese Website ist bewusst datensparsam aufgebaut. Sie kommt ohne Analyse- und
        Marketingdienste, ohne Werbe-Cookies, ohne extern geladene Schriften und ohne eingebettete
        Inhalte Dritter aus. Die folgenden Hinweise beschreiben, welche personenbezogenen Daten beim
        Besuch und bei einer Kontaktaufnahme verarbeitet werden.
      </p>

      <h2>1. Verantwortlicher</h2>
      <address>
        {SITE.legalName}
        <br />
        vertreten durch den Geschäftsführer {SITE.managingDirector}
        <br />
        {SITE.street}, {SITE.postalCode} {SITE.city}, {SITE.country}
        <br />
        E-Mail: {mail}
      </address>

      <h2>2. Hosting und Server-Protokolle</h2>
      <p>
        Die Website wird über die Plattform Lovable bereitgestellt (Lovable Labs Incorporated, 1111B
        South Governors Avenue, Dover, DE 19904, USA) und über das Netzwerk von Cloudflare
        ausgeliefert. Beim Aufruf einer Seite verarbeiten diese Dienstleister die technisch
        erforderlichen Verbindungsdaten: IP-Adresse, Datum und Uhrzeit, aufgerufene Adresse,
        übertragene Datenmenge, verweisende Seite sowie Angaben zu Browser und Betriebssystem.
      </p>
      <p>
        Die Verarbeitung dient der Auslieferung der Website, ihrer Stabilität und der Abwehr von
        Angriffen. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO; das berechtigte Interesse liegt
        im sicheren und zuverlässigen Betrieb. Die Dienstleister werden als Auftragsverarbeiter
        tätig. Dabei können Daten in die USA übermittelt werden; Grundlage hierfür sind die
        Standardvertragsklauseln der Europäischen Kommission (Art. 46 Abs. 2 lit. c DSGVO). Die
        Speicherdauer der Protokolldaten richtet sich nach den Vorgaben der Dienstleister.
      </p>

      <h2>3. Technisch notwendige Speicherung im Browser</h2>
      <p>
        Es werden ausschließlich Einträge gesetzt, die für den Betrieb der Website erforderlich sind
        (§ 25 Abs. 2 Nr. 2 TDDDG). Eine Einwilligung ist dafür nicht erforderlich.
      </p>
      <ul>
        <li>
          Cookie <code>__cf_bm</code> (Cloudflare): Erkennung automatisierter Zugriffe, Laufzeit bis
          zu 30 Minuten.
        </li>
        <li>
          Cookie <code>__dpl</code> (Hosting): ordnet den Besuch der aktuell veröffentlichten
          Version der Website zu, Laufzeit bis zu 24 Stunden.
        </li>
        <li>
          Sitzungsspeicher <code>tsr-scroll-restoration</code>: merkt sich die Scrollposition, wird
          beim Schließen des Tabs gelöscht.
        </li>
      </ul>
      <p>
        Optionale Dienste sind derzeit nicht eingebunden. Sollten künftig solche Dienste eingesetzt
        werden, werden sie erst nach Ihrer Einwilligung geladen (§ 25 Abs. 1 TDDDG, Art. 6 Abs. 1
        lit. a DSGVO). Den aktuellen Stand können Sie jederzeit einsehen:{" "}
        <button type="button" className="legal-button" onClick={openPrivacySettings}>
          Datenschutzeinstellungen öffnen
        </button>
        .
      </p>

      <h2>4. Kontaktformular</h2>
      <p>
        Wenn Sie das Kontaktformular nutzen, werden die von Ihnen eingegebenen Angaben verarbeitet:
        Anliegen, Name, E-Mail-Adresse sowie, soweit angegeben, Telefonnummer, Nachricht,
        Objektadresse oder Lage, Objektart und Exposé-Link.
      </p>
      <p>
        Die Angaben werden verschlüsselt an eine Serverfunktion dieser Website übertragen, dort
        geprüft und als E-Mail an {SITE.email} weitergeleitet. Für den Versand wird der
        E-Mail-Dienst Resend (Resend, Inc., USA) als Auftragsverarbeiter eingesetzt; dabei werden
        Daten in die USA übermittelt, abgesichert durch Standardvertragsklauseln. Die Website selbst
        speichert Ihre Anfrage nicht in einer Datenbank. Zum Schutz vor Missbrauch wird die
        IP-Adresse kurzzeitig im Arbeitsspeicher des Servers verarbeitet, um die Zahl der Anfragen
        je Anschluss zu begrenzen.
      </p>
      <p>
        Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO, soweit Ihre Anfrage auf die Anbahnung eines
        Vertrags gerichtet ist, im Übrigen Art. 6 Abs. 1 lit. f DSGVO (Bearbeitung von Anfragen).
        Die Angaben werden gelöscht, sobald die Anfrage abschließend bearbeitet ist und keine
        gesetzlichen Aufbewahrungspflichten entgegenstehen.
      </p>

      <h2>5. Kontakt per E-Mail</h2>
      <p>
        Wenn Sie eine E-Mail an {SITE.email} senden, werden Ihre Angaben zur Bearbeitung des
        Anliegens verarbeitet und im E-Mail-Postfach der Gesellschaft gespeichert. Rechtsgrundlage
        und Speicherdauer entsprechen Ziffer 4.
      </p>

      <h2>6. Schriften, Analyse und Dienste Dritter</h2>
      <p>
        Die verwendeten Schriften werden vom eigenen Server ausgeliefert. Es findet keine
        Reichweitenmessung, kein Tracking und keine Profilbildung statt. Karten, Videos, Social
        Media oder andere Inhalte Dritter sind nicht eingebunden.
      </p>

      <h2>7. Ihre Rechte</h2>
      <p>Ihnen stehen nach der DSGVO folgende Rechte zu:</p>
      <ul>
        <li>Auskunft über die zu Ihrer Person verarbeiteten Daten (Art. 15)</li>
        <li>Berichtigung unrichtiger Daten (Art. 16)</li>
        <li>Löschung (Art. 17) und Einschränkung der Verarbeitung (Art. 18)</li>
        <li>Datenübertragbarkeit (Art. 20)</li>
        <li>Widerspruch gegen Verarbeitungen auf Grundlage berechtigter Interessen (Art. 21)</li>
        <li>Widerruf einer erteilten Einwilligung mit Wirkung für die Zukunft (Art. 7 Abs. 3)</li>
      </ul>
      <p>
        Zur Ausübung Ihrer Rechte genügt eine Nachricht an {mail}. Sie haben außerdem das Recht,
        sich bei einer Datenschutzaufsichtsbehörde zu beschweren, zum Beispiel beim Bayerischen
        Landesamt für Datenschutzaufsicht, Promenade 18, 91522 Ansbach.
      </p>

      <h2>8. Pflicht zur Bereitstellung, automatisierte Entscheidungen</h2>
      <p>
        Sie sind nicht verpflichtet, personenbezogene Daten bereitzustellen. Ohne die als
        Pflichtfeld gekennzeichneten Angaben kann eine Anfrage über das Formular jedoch nicht
        bearbeitet werden. Eine automatisierte Entscheidungsfindung einschließlich Profiling findet
        nicht statt.
      </p>

      <h2>9. Stand</h2>
      <p>
        Stand dieser Datenschutzerklärung:{" "}
        {PRIVACY_VERSION.slice(0, 10).split("-").reverse().join(".")}. Die Hinweise werden
        angepasst, sobald sich die eingesetzten Dienste oder die Rechtslage ändern.
      </p>
    </LegalPage>
  );
}
