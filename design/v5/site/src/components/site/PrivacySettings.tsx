import { useEffect, useRef, useState } from "react";
import { ACTIVE_PURPOSES, PRIVACY_VERSION, savePrivacyChoices } from "@/lib/privacy-settings";
import { needsAnswer, onConsentChange, readChoice, type Purpose } from "@/lib/consent";
import { onPrivacyOpen } from "@/lib/privacy-open";
import { Eyebrow } from "./ui/Eyebrow";
import { Button } from "./ui/Button";

const PURPOSE_LABELS: Record<Purpose, { title: string; text: string }> = {
  analytics: { title: "Statistik", text: "Anonyme Auswertung von Seitenaufrufen" },
  advertising: { title: "Marketing", text: "Reichweitenmessung und Werbung" },
};
const NECESSARY = [
  "Auslieferung der Website und Schutz vor Missbrauch durch den Hoster",
  "Zuordnung zur aktuellen Website-Version",
  "Merken der Scrollposition während des Besuchs",
];

export function PrivacySettings() {
  const [open, setOpen] = useState(false);
  const [choices, setChoices] = useState<Record<Purpose, boolean>>({
    analytics: false,
    advertising: false,
  });
  const dialog = useRef<HTMLDivElement>(null);
  const opener = useRef<HTMLElement | null>(null);
  const optional = ACTIVE_PURPOSES.length > 0;

  useEffect(() => {
    const show = () => setOpen(true);
    const offOpen = onPrivacyOpen(show);
    const refresh = () =>
      setChoices({
        analytics: readChoice("analytics") === "granted",
        advertising: readChoice("advertising") === "granted",
      });
    refresh();
    // Only ask when an optional service is actually registered.
    if (optional)
      void needsAnswer(ACTIVE_PURPOSES).then((needed) => {
        if (needed) setOpen(true);
      });
    const off = onConsentChange(refresh);
    return () => {
      offOpen();
      off();
    };
  }, [optional]);

  useEffect(() => {
    if (!open) return;
    opener.current = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    const node = dialog.current;
    node?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
      if (e.key !== "Tab" || !node) return;
      const items = Array.from(
        node.querySelectorAll<HTMLElement>("a[href],button:not([disabled]),input:not([disabled])"),
      );
      const first = items[0];
      const last = items.at(-1);
      if (!first || !last) return;
      if (e.shiftKey && (document.activeElement === first || document.activeElement === node)) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    };
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("keydown", onKey);
      opener.current?.focus();
    };
  }, [open]);

  const save = (all?: boolean) => {
    savePrivacyChoices(
      Object.fromEntries(
        ACTIVE_PURPOSES.map((p) => [p, (all ?? choices[p]) ? "granted" : "denied"]),
      ),
    );
    setOpen(false);
  };

  if (!open) return null;
  return (
    <div
      className="dialog-backdrop"
      onMouseDown={(e) => {
        if (e.target === e.currentTarget && !optional) setOpen(false);
      }}
    >
      <div
        ref={dialog}
        className="dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="privacy-title"
        tabIndex={-1}
      >
        <Eyebrow>Datenschutz</Eyebrow>
        <h2 id="privacy-title">Datenschutzeinstellungen</h2>
        <p>
          {optional
            ? "Optionale Dienste werden erst nach Ihrer Einwilligung geladen. Sie können Ihre Auswahl jederzeit hier ändern oder widerrufen."
            : "Diese Website verwendet ausschließlich technisch notwendige Funktionen. Es sind keine Analyse-, Marketing- oder Drittanbieter-Dienste eingebunden. Eine Einwilligung ist deshalb nicht erforderlich."}
        </p>
        <div className="dialog-rows">
          <div className="dialog-row">
            <span>
              Technisch notwendig
              <small>{NECESSARY.join(" · ")}</small>
            </span>
            <span className="micro nowrap">Immer aktiv</span>
          </div>
          {(Object.keys(PURPOSE_LABELS) as Purpose[]).map((purpose) =>
            ACTIVE_PURPOSES.includes(purpose) ? (
              <label key={purpose} className="dialog-row">
                <span>
                  {PURPOSE_LABELS[purpose].title}
                  <small>{PURPOSE_LABELS[purpose].text}</small>
                </span>
                <input
                  type="checkbox"
                  role="switch"
                  className="switch"
                  checked={choices[purpose]}
                  onChange={(e) => setChoices((c) => ({ ...c, [purpose]: e.target.checked }))}
                />
              </label>
            ) : (
              <div key={purpose} className="dialog-row">
                <span>{PURPOSE_LABELS[purpose].title}</span>
                <span className="micro nowrap muted">Nicht im Einsatz</span>
              </div>
            ),
          )}
        </div>
        <div className="dialog-actions">
          {optional ? (
            <>
              <Button onClick={() => save(false)}>Alle ablehnen</Button>
              <Button onClick={() => save(true)}>Alle akzeptieren</Button>
              <Button onClick={() => save()}>Auswahl speichern</Button>
            </>
          ) : (
            <Button solid onClick={() => setOpen(false)}>
              Schließen
            </Button>
          )}
        </div>
        <p className="dialog-meta">
          <a className="link" href="/datenschutz">
            Datenschutzerklärung lesen
          </a>
          <span className="mono">Stand {PRIVACY_VERSION}</span>
        </p>
      </div>
    </div>
  );
}
