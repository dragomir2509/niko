import type { ReactNode } from "react";
import { Nav } from "./Nav";
import { Footer } from "./Footer";
import { Eyebrow } from "./ui/Eyebrow";

export function LegalPage({
  eyebrow,
  title,
  children,
}: {
  eyebrow: string;
  title: string;
  children: ReactNode;
}) {
  return (
    <>
      <a className="skip-link micro" href="#main">
        Zum Inhalt springen
      </a>
      <Nav />
      <main id="main" className="legal">
        <div className="wrap grid">
          <div className="legal-head">
            <Eyebrow>{eyebrow}</Eyebrow>
          </div>
          <article className="legal-body">
            <h1>{title}</h1>
            {children}
          </article>
        </div>
      </main>
      <Footer />
    </>
  );
}
