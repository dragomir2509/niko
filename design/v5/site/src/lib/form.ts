import { z } from "zod";
import { PROPERTY_TYPES } from "@/content/site";

export type FormType = "property" | "general";
export type FormValues = {
  formType: FormType;
  name: string;
  email: string;
  phone: string;
  location: string;
  propertyType: string;
  exposeUrl: string;
  message: string;
  consent: boolean;
};
export type FormField =
  "name" | "email" | "phone" | "location" | "propertyType" | "exposeUrl" | "message" | "consent";
export type FormErrors = Partial<Record<FormField, string>>;

export const MESSAGES = {
  name: "Bitte geben Sie Ihren Namen an.",
  email: "Bitte geben Sie eine gültige E-Mail-Adresse an.",
  consent: "Bitte bestätigen Sie die Datenschutzhinweise.",
  location: "Bitte geben Sie die Objektadresse oder Lage an.",
  propertyType: "Bitte wählen Sie eine Objektart.",
  exposeUrl: "Bitte geben Sie einen gültigen Link mit https:// an.",
  singleLine: "Bitte verwenden Sie hier keine Zeilenumbrüche.",
} as const;

/** Single-line fields end up in e-mail headers (subject, reply-to): no control characters. */
const singleLine = (max: number) =>
  z
    .string()
    .trim()
    .max(max)
    .refine((v) => !/\p{Cc}/u.test(v), MESSAGES.singleLine);

export const contactSchema = z
  .object({
    formType: z.enum(["property", "general"]),
    name: singleLine(100).pipe(z.string().min(1, MESSAGES.name)),
    email: singleLine(254).pipe(z.string().email(MESSAGES.email)),
    phone: singleLine(60),
    location: singleLine(250),
    propertyType: singleLine(60),
    exposeUrl: singleLine(2000).refine((v) => {
      if (!v) return true;
      try {
        return ["http:", "https:"].includes(new URL(v).protocol);
      } catch {
        return false;
      }
    }, MESSAGES.exposeUrl),
    message: z.string().trim().max(5000),
    consent: z.boolean().refine(Boolean, MESSAGES.consent),
  })
  .superRefine((v, ctx) => {
    if (v.formType !== "property") return;
    if (!v.location)
      ctx.addIssue({ code: "custom", path: ["location"], message: MESSAGES.location });
    if (!(PROPERTY_TYPES as readonly string[]).includes(v.propertyType))
      ctx.addIssue({ code: "custom", path: ["propertyType"], message: MESSAGES.propertyType });
  });

export type ContactData = z.infer<typeof contactSchema>;

/** Field order used to focus the first invalid field. */
export const FIELD_ORDER: FormField[] = [
  "location",
  "propertyType",
  "exposeUrl",
  "name",
  "email",
  "phone",
  "message",
  "consent",
];

export function validate(v: FormValues): FormErrors {
  const result = contactSchema.safeParse(v);
  if (result.success) return {};
  const errors: FormErrors = {};
  for (const issue of result.error.issues) {
    const key = issue.path[0] as FormField;
    if (!errors[key]) errors[key] = issue.message;
  }
  return errors;
}

/** Fields that belong to a general enquiry are sent empty for property-only inputs. */
export function normalize(v: FormValues): FormValues {
  return v.formType === "general" ? { ...v, location: "", propertyType: "", exposeUrl: "" } : v;
}

export function subjectFor(v: Pick<FormValues, "formType" | "location" | "name">): string {
  const raw =
    v.formType === "property" ? `Objektangebot: ${v.location}` : `Allgemeine Anfrage: ${v.name}`;
  return raw.replace(/\p{Cc}+/gu, " ").slice(0, 140);
}

export function mailRows(v: FormValues): [string, string][] {
  const rows: [string, string][] = [
    ["Anliegen", v.formType === "property" ? "Immobilie anbieten" : "Allgemeine Anfrage"],
    ["Name", v.name],
    ["E-Mail", v.email],
    ["Telefon", v.phone],
    ["Objektadresse oder Lage", v.location],
    ["Objektart", v.propertyType],
    ["Exposé-Link", v.exposeUrl],
  ];
  return rows.filter(([, value]) => value.trim());
}

/** Fallback for visitors: opens their own mail program with the entered data. */
export function buildMailto(to: string, values: FormValues): string {
  const v = normalize(values);
  const body =
    mailRows(v)
      .map(([key, value]) => `${key}: ${value}`)
      .join("\n") + (v.message.trim() ? `\n\nNachricht:\n${v.message.trim()}` : "");
  return `mailto:${to}?subject=${encodeURIComponent(subjectFor(v))}&body=${encodeURIComponent(body)}`;
}
