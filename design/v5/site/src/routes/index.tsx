import { createFileRoute } from "@tanstack/react-router";
import { SITE } from "@/config/site";
import { ALL_PLACES, CONTENT } from "@/content/site";
import { getSiteUrl } from "@/lib/site-url";
import { Nav } from "@/components/site/Nav";
import { Hero } from "@/components/site/Hero";
import { About } from "@/components/site/About";
import { Approach } from "@/components/site/Approach";
import { Ankaufsprofil } from "@/components/site/Ankaufsprofil";
import { Process } from "@/components/site/Process";
import { Kontakt } from "@/components/site/Kontakt";
import { Footer } from "@/components/site/Footer";

const TITLE = CONTENT.seo.title;
const DESC = CONTENT.seo.description;
const URL = getSiteUrl(SITE.url);
const OG_IMAGE = `${URL}/og-image.png`;

export const Route = createFileRoute("/")({
  staticData: { sitemap: true },
  component: Index,
  head: () => ({
    meta: [
      { title: TITLE },
      { name: "description", content: DESC },
      { property: "og:title", content: TITLE },
      { property: "og:description", content: DESC },
      { property: "og:type", content: "website" },
      { property: "og:url", content: URL },
      { property: "og:image", content: OG_IMAGE },
      { property: "og:image:width", content: "1200" },
      { property: "og:image:height", content: "630" },
      { property: "og:image:alt", content: CONTENT.seo.ogAlt },
      { name: "twitter:card", content: "summary_large_image" },
      { name: "twitter:title", content: TITLE },
      { name: "twitter:description", content: DESC },
      { name: "twitter:image", content: OG_IMAGE },
    ],
    links: [{ rel: "canonical", href: URL }],
    scripts: [
      {
        type: "application/ld+json",
        children: JSON.stringify({
          "@context": "https://schema.org",
          "@type": "Organization",
          "@id": `${URL}/#organization`,
          name: SITE.name,
          legalName: SITE.legalName,
          url: URL,
          logo: `${URL}/icon-512.png`,
          image: OG_IMAGE,
          email: SITE.email,
          description: DESC,
          founder: { "@type": "Person", name: SITE.founder },
          address: {
            "@type": "PostalAddress",
            streetAddress: SITE.street,
            postalCode: SITE.postalCode,
            addressLocality: SITE.city,
            addressRegion: "Bayern",
            addressCountry: SITE.countryCode,
          },
          geo: { "@type": "GeoCoordinates", latitude: SITE.geo.lat, longitude: SITE.geo.lng },
          areaServed: ALL_PLACES.map((name) => ({ "@type": "Place", name })),
          knowsAbout: ["Immobilienankauf", "Grundstücksankauf", "Immobilienentwicklung"],
        }),
      },
      {
        type: "application/ld+json",
        children: JSON.stringify({
          "@context": "https://schema.org",
          "@type": "WebSite",
          "@id": `${URL}/#website`,
          url: URL,
          name: SITE.name,
          inLanguage: "de-DE",
          publisher: { "@id": `${URL}/#organization` },
        }),
      },
    ],
  }),
});

function Index() {
  return (
    <>
      <a className="skip-link micro" href="#main">
        Zum Inhalt springen
      </a>
      <Nav />
      <main id="main">
        <Hero />
        <About />
        <Approach />
        <Ankaufsprofil />
        <Process />
        <Kontakt />
      </main>
      <Footer />
    </>
  );
}
