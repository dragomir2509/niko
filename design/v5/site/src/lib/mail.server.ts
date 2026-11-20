// Server-only: delivers a contact request as an e-mail to RN INVEST through the Resend API.
// Requires the secret RESEND_API_KEY. Optional: CONTACT_FROM (verified sender) and CONTACT_TO.
// The request is not stored anywhere by this application.
import { SITE } from "@/config/site";
import { mailRows, subjectFor, type ContactData } from "./form";

export type DeliveryResult =
  { ok: true; id: string } | { ok: false; reason: "not_configured" | "provider_error" };

const escapeHtml = (value: string) =>
  value.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

export function renderMail(v: ContactData): { subject: string; text: string; html: string } {
  const rows = mailRows(v);
  const message = v.message.trim();
  const text =
    rows.map(([key, value]) => `${key}: ${value}`).join("\n") +
    (message ? `\n\nNachricht:\n${message}` : "") +
    "\n\nGesendet über das Kontaktformular der RN INVEST Website.";
  const html =
    `<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.55;color:#171719">` +
    `<table style="border-collapse:collapse">` +
    rows
      .map(
        ([key, value]) =>
          `<tr><td style="padding:6px 24px 6px 0;color:#5c5c60;vertical-align:top">${escapeHtml(key)}</td>` +
          `<td style="padding:6px 0">${escapeHtml(value)}</td></tr>`,
      )
      .join("") +
    `</table>` +
    (message
      ? `<p style="margin:20px 0 6px;color:#5c5c60">Nachricht</p><p style="margin:0;white-space:pre-wrap">${escapeHtml(message)}</p>`
      : "") +
    `<p style="margin:28px 0 0;font-size:12px;color:#5c5c60">Gesendet über das Kontaktformular der RN INVEST Website.</p></div>`;
  return { subject: subjectFor(v), text, html };
}

export async function deliverContactMail(
  v: ContactData,
  requestId: string,
): Promise<DeliveryResult> {
  const apiKey = process.env["RESEND_API_KEY"];
  if (!apiKey) return { ok: false, reason: "not_configured" };
  const from = process.env["CONTACT_FROM"] || "RN INVEST Website <onboarding@resend.dev>";
  const to = process.env["CONTACT_TO"] || SITE.email;
  const mail = renderMail(v);
  try {
    const response = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
        "Idempotency-Key": `contact-${requestId}`,
      },
      body: JSON.stringify({
        from,
        to: [to],
        reply_to: v.email,
        subject: mail.subject,
        text: mail.text,
        html: mail.html,
      }),
      signal: AbortSignal.timeout(12_000),
    });
    if (!response.ok) {
      console.error("Contact mail rejected by provider", response.status);
      return { ok: false, reason: "provider_error" };
    }
    const body = (await response.json().catch(() => null)) as { id?: unknown } | null;
    if (!body || typeof body.id !== "string") return { ok: false, reason: "provider_error" };
    return { ok: true, id: body.id };
  } catch (error) {
    console.error("Contact mail request failed", error instanceof Error ? error.name : "unknown");
    return { ok: false, reason: "provider_error" };
  }
}
