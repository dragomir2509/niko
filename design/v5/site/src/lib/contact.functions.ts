import { createServerFn } from "@tanstack/react-start";
import { getRequestHeader } from "@tanstack/react-start/server";
import { z } from "zod";
import { SITE } from "@/config/site";
import { contactSchema } from "./form";

const envelope = z.object({
  values: contactSchema,
  requestId: z.string().uuid(),
  /** Honeypot. Real visitors leave it empty. */
  website: z.string().max(200),
  startedAt: z.number(),
});

export type ContactResult =
  | { ok: true }
  | { ok: false; code: "invalid" | "rate_limited" | "unavailable" | "failed"; error: string };

const MIN_FILL_MS = 2500;
const MAX_FORM_AGE_MS = 24 * 60 * 60 * 1000;

function sameOrigin(): boolean {
  const origin = getRequestHeader("origin");
  const host = getRequestHeader("x-forwarded-host") ?? getRequestHeader("host");
  if (!origin || !host) return false;
  try {
    return new URL(origin).host === host;
  } catch {
    return false;
  }
}

function clientKey(): string {
  const forwarded = getRequestHeader("x-forwarded-for")?.split(",")[0]?.trim();
  return getRequestHeader("cf-connecting-ip") ?? forwarded ?? "unknown";
}

/**
 * Validates a contact request and hands it to the mail provider.
 * ok: true is returned only after the provider accepted the message for delivery.
 * The request is not stored by the application.
 */
export const submitContact = createServerFn({ method: "POST" })
  .validator((input: unknown) => envelope.parse(input))
  .handler(async ({ data }): Promise<ContactResult> => {
    if (!sameOrigin())
      return {
        ok: false,
        code: "invalid",
        error: "Die Sicherheitsprüfung ist fehlgeschlagen. Bitte laden Sie die Seite neu.",
      };
    const age = Date.now() - data.startedAt;
    if (data.website || age < MIN_FILL_MS || age > MAX_FORM_AGE_MS)
      return {
        ok: false,
        code: "invalid",
        error:
          "Die Anfrage konnte nicht geprüft werden. Bitte versuchen Sie es in einem Moment erneut.",
      };
    const limiter = await import("./rate-limit.server");
    if (limiter.wasDelivered(data.requestId)) return { ok: true };
    if (!limiter.allowRequest(clientKey()))
      return {
        ok: false,
        code: "rate_limited",
        error: `Zu viele Anfragen in kurzer Zeit. Bitte versuchen Sie es später erneut oder schreiben Sie direkt an ${SITE.email}.`,
      };
    const { deliverContactMail } = await import("./mail.server");
    const result = await deliverContactMail(data.values, data.requestId);
    if (result.ok) {
      limiter.markDelivered(data.requestId);
      return { ok: true };
    }
    if (result.reason === "not_configured")
      return {
        ok: false,
        code: "unavailable",
        error: `Der Versand über das Formular ist derzeit nicht verfügbar. Ihre Anfrage wurde nicht übermittelt. Bitte schreiben Sie direkt an ${SITE.email}.`,
      };
    return {
      ok: false,
      code: "failed",
      error: `Die Anfrage konnte nicht zugestellt werden. Ihre Eingaben bleiben erhalten. Bitte versuchen Sie es erneut oder schreiben Sie direkt an ${SITE.email}.`,
    };
  });
