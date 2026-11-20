import { SITE } from "@/config/site";

export const NAV = [
  { id: "ueber", label: "Über RN INVEST" },
  { id: "ansatz", label: "Investmentansatz" },
  { id: "ankaufsprofil", label: "Ankaufsprofil" },
  { id: "kontakt", label: "Kontakt" },
] as const;

export const PROPERTY_TYPES = [
  "Grundstück",
  "Einfamilienhaus",
  "Doppelhaushälfte",
  "Reihenhaus",
  "Gewerbehaus",
  "Mehrfamilienhaus",
  "Hotel",
  "Sonstiges",
] as const;

/** Upper purchase price limit. Applies to apartment buildings (Mehrfamilienhäuser) only. */
export const MFH_MAX_PURCHASE_PRICE = 5_000_000;

export const CONTENT = {
  hero: {
    metaLeft: "Private Investmentgesellschaft",
    metaRight: "München und Münchner Umland",
    lines: ["Unabhängig", "im Denken."],
    accentLine: ["Klar", "im Handeln."],
    lead: "RN INVEST ist eine private Investmentgesellschaft mit Fokus auf ausgewählte Immobilien und Grundstücke in München und im Münchner Umland.",
    primaryCta: "Ankaufsprofil ansehen",
    secondaryCta: "Objekt anbieten",
  },
  about: {
    eyebrow: "Über RN INVEST",
    title: ["Persönlich geführt.", "Selektiv investiert."],
    lead: "RN INVEST ist die private Investmentgesellschaft von Niko Roncevic. Sie konzentriert sich auf ausgewählte Immobilien, Grundstücke und Immobilienentwicklungen sowie auf eigene Beteiligungen.",
    text: "Der Schwerpunkt liegt in München und im Münchner Umland. Ausgewählte Investitionen werden gemeinsam mit langjährigen Partnern realisiert.",
    person: {
      label: "Geschäftsführung",
      name: SITE.managingDirector,
      role: "Gründer und Geschäftsführer",
      quote:
        "Ich investiere nur in das, was ich selbst geprüft habe und persönlich verantworten kann.",
      points: [
        "Prüft jedes Objekt selbst.",
        "Trifft jede Entscheidung selbst.",
        "Steht persönlich für jede Zusage ein.",
      ],
    },
  },
  approach: {
    eyebrow: "Investmentansatz",
    title: ["Wenige Entscheidungen.", "Jede aus Überzeugung."],
    principles: [
      {
        title: "Substanz",
        text: "Lage, Grundstück und Bausubstanz zählen mehr als die Stimmung am Markt.",
      },
      {
        title: "Unternehmerisch",
        text: "Chancen, Risiken und Aufwand werden nüchtern abgewogen, bevor investiert wird.",
      },
      {
        title: "Unabhängig",
        text: "Keine Gremien, keine Vertriebsziele, kein Anlagedruck. Entschieden wird in der Sache.",
      },
      {
        title: "Persönlich verantwortet",
        text: "Hinter jeder Zusage steht eine Person: Niko Roncevic.",
      },
      {
        title: "Selektiv",
        text: "Nicht jedes gute Objekt passt. Erworben wird nur, was dem Profil und der eigenen Überzeugung entspricht.",
      },
      {
        title: "Langfristig",
        text: "Der Maßstab ist die Entwicklung über Jahre, nicht das nächste Quartal.",
      },
    ],
  },
  profile: {
    eyebrow: "Ankaufsprofil",
    title: ["Zwei Profile.", "Klar abgegrenzt."],
    lead: "Die Kriterien dienen der schnellen Einordnung eines Objekts. Sie beschreiben das Suchprofil und stellen keine Kaufzusage dar.",
    note: "Für eine erste Einordnung genügen Adresse oder Exposé",
    a: {
      key: "A",
      title: "Grundstücke und Häuser",
      types:
        "Baugrundstücke (bevorzugt), stark renovierungsbedürftige Ein- und Zweifamilienhäuser, Doppelhaushälften, Reihenhäuser, kleine Gewerbehäuser",
      city: [
        "Obermenzing",
        "Pasing",
        "Solln",
        "Obersendling",
        "Harlaching",
        "Berg am Laim",
        "Moosach",
        "Milbertshofen",
        "Bogenhausen",
      ],
      county: ["Gräfelfing", "Pullach", "Grünwald"],
      plotCity: { value: "bis ca. 1.000\u00a0m²", note: "im Stadtgebiet München" },
      plotCounty: { value: "bis ca. 1.500\u00a0m²", note: "im Landkreis München" },
      cta: "Objekt für Profil A anbieten",
      propertyType: "Grundstück",
    },
    b: {
      key: "B",
      title: "Mehrfamilienhäuser und ausgewählte Bestandsobjekte",
      types: "Kleine Mehrfamilienhäuser, kleine Hotels",
      requirements: "Entwicklungspotenzial, kein Denkmalschutz",
      city: [
        "Maxvorstadt",
        "Lehel",
        "Schwabing",
        "Milbertshofen",
        "Au",
        "Haidhausen",
        "Obergiesing",
      ],
      area: { value: "ab ca. 350\u00a0m²", note: "Bruttogrundfläche" },
      price: {
        label: "Ankaufspreis",
        value: `bis ${new Intl.NumberFormat("de-DE").format(MFH_MAX_PURCHASE_PRICE)}\u00a0€`,
        note: "gilt für Mehrfamilienhäuser",
      },
      cta: "Objekt für Profil B anbieten",
      propertyType: "Mehrfamilienhaus",
    },
  },
  process: {
    eyebrow: "Ankaufsprozess",
    title: ["Vom ersten Kontakt", "zur klaren Antwort."],
    steps: [
      {
        title: "Objekt vorstellen",
        text: "Adresse, Eckdaten oder Exposé genügen für den Anfang: über das Formular oder direkt per E-Mail.",
      },
      {
        title: "Persönliche Prüfung",
        text: "Niko Roncevic prüft jedes Angebot selbst: Lage, Substanz, Potenzial und Passung zum Ankaufsprofil.",
      },
      {
        title: "Entscheidung und weitere Abstimmung",
        text: "Sie erhalten eine persönliche Rückmeldung. Passt das Objekt, werden die nächsten Schritte gemeinsam abgestimmt.",
      },
    ],
    note: "Persönlich · Transparent · Diskret",
  },
  contact: {
    eyebrow: "Kontakt",
    title: ["Ihr Objekt.", "Ihr Anliegen."],
    lead: "Jede Nachricht wird persönlich gelesen und vertraulich behandelt.",
    directLabel: "Direkt per E-Mail",
    modeLegend: "Anliegen *",
    modes: { property: "Immobilie anbieten", general: "Allgemeine Anfrage" },
    labels: {
      location: "Objektadresse oder Lage *",
      propertyType: "Objektart *",
      exposeUrl: "Exposé-Link (optional)",
      name: "Name *",
      email: "E-Mail *",
      phone: "Telefon (optional)",
      message: "Nachricht (optional)",
    },
    placeholders: {
      location: "z. B. Pasing, Straße oder Flurstück",
      propertyType: "Bitte wählen",
      exposeUrl: "https://",
      messageProperty: "Grundstücksgröße, Zustand, zeitlicher Rahmen",
      messageGeneral: "Ihr Anliegen in wenigen Sätzen",
    },
    consentBefore: "Ich habe die",
    consentLink: "Datenschutzhinweise",
    consentAfter:
      "gelesen und bin einverstanden, dass meine Angaben zur Bearbeitung der Anfrage verarbeitet werden. *",
    required: "* Pflichtfeld",
    submit: "Anfrage senden",
    sending: "Wird gesendet",
    successEyebrow: "Übermittelt",
    successTitle: "Vielen Dank.",
    successText:
      "Ihre Anfrage wurde an RN INVEST übermittelt. Sie erhalten eine persönliche Rückmeldung.",
    again: "Weitere Anfrage senden",
    fallbackLink: "E-Mail mit diesen Angaben öffnen",
    networkError:
      "Die Anfrage konnte nicht übertragen werden. Ihre Eingaben bleiben erhalten. Bitte versuchen Sie es erneut oder schreiben Sie direkt an",
  },
  footer: {
    address: "Anschrift",
    contact: "Kontakt",
    legal: "Rechtliches",
    imprint: "Impressum",
    privacy: "Datenschutz",
    settings: "Datenschutzeinstellungen",
  },
  errorPage: {
    notFound: "Diese Seite gibt es nicht.",
    home: "Zur Startseite",
    error: "Diese Seite konnte nicht geladen werden.",
    retry: "Erneut laden",
  },
  seo: {
    title: "RN INVEST | Private Investmentgesellschaft für Immobilien in München",
    description:
      "RN INVEST ist die private Investmentgesellschaft von Niko Roncevic. Ankauf ausgewählter Grundstücke, Häuser und Mehrfamilienhäuser in München und im Münchner Umland.",
    ogAlt: "RN INVEST. Unabhängig im Denken. Klar im Handeln.",
  },
} as const;

/** All search locations of both acquisition profiles, without duplicates. */
export const ALL_PLACES: string[] = Array.from(
  new Set([...CONTENT.profile.a.city, ...CONTENT.profile.a.county, ...CONTENT.profile.b.city]),
);
