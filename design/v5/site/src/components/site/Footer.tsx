import { CONTENT } from "@/content/site";
import { SITE } from "@/config/site";
import { Monogram, Wordmark } from "./ui/Logo";
import { PrivacySettings } from "./PrivacySettings";
import { openPrivacySettings } from "@/lib/privacy-open";

export function Footer() {
  const c = CONTENT.footer;
  return (
    <footer className="footer on-dark">
      <div className="wrap">
        <div className="footer-grid">
          <a className="footer-mark" href="/#top" aria-label="RN INVEST, zur Startseite">
            <Monogram size="text" />
          </a>
          <div className="footer-col">
            <span className="micro">{c.address}</span>
            <address>
              {SITE.legalName}
              <br />
              {SITE.street}
              <br />
              {SITE.postalCode} {SITE.city}
              <br />
              {SITE.country}
            </address>
          </div>
          <div className="footer-col">
            <span className="micro">{c.contact}</span>
            <a className="link" href={`mailto:${SITE.email}`}>
              {SITE.email}
            </a>
          </div>
          <nav className="footer-col" aria-label={c.legal}>
            <span className="micro">{c.legal}</span>
            <ul>
              <li>
                <a className="link" href="/impressum">
                  {c.imprint}
                </a>
              </li>
              <li>
                <a className="link" href="/datenschutz">
                  {c.privacy}
                </a>
              </li>
              <li>
                <button type="button" className="link" onClick={openPrivacySettings}>
                  {c.settings}
                </button>
              </li>
            </ul>
          </nav>
        </div>
        <div className="footer-base micro">
          <span>
            © {new Date().getFullYear()} {SITE.legalName}
          </span>
          <span>
            {SITE.registerCourt} · {SITE.registerNumber}
          </span>
        </div>
        <Wordmark className="footer-word" />
      </div>
      <PrivacySettings />
    </footer>
  );
}
