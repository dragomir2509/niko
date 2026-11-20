import { afterEach, describe, expect, it, vi } from "vitest";
import { deliverContactMail, renderMail } from "./mail.server";
import type { ContactData } from "./form";

const data: ContactData = {
  formType: "property",
  name: "Max <b>Muster</b>",
  email: "max@example.de",
  phone: "",
  location: "Pasing",
  propertyType: "Grundstück",
  exposeUrl: "",
  message: "Zeile 1\n<script>x</script>",
  consent: true,
};

afterEach(() => {
  vi.unstubAllEnvs();
  vi.unstubAllGlobals();
});

describe("contact mail", () => {
  it("escapes visitor input in the HTML body", () => {
    const mail = renderMail(data);
    expect(mail.subject).toBe("Objektangebot: Pasing");
    expect(mail.html).not.toContain("<script>");
    expect(mail.html).toContain("Max &lt;b&gt;Muster&lt;/b&gt;");
    expect(mail.text).toContain("Objektart: Grundstück");
  });
  it("reports not_configured without an API key and sends nothing", async () => {
    vi.stubEnv("RESEND_API_KEY", "");
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    expect(await deliverContactMail(data, "id-1")).toEqual({ ok: false, reason: "not_configured" });
    expect(fetchMock).not.toHaveBeenCalled();
  });
  it("succeeds only when the provider returns a message id", async () => {
    vi.stubEnv("RESEND_API_KEY", "test-key");
    const fetchMock = vi.fn(
      async () => new Response(JSON.stringify({ id: "msg_1" }), { status: 200 }),
    );
    vi.stubGlobal("fetch", fetchMock);
    expect(await deliverContactMail(data, "id-2")).toEqual({ ok: true, id: "msg_1" });
    const [url, init] = fetchMock.mock.calls[0] as unknown as [string, RequestInit];
    expect(url).toBe("https://api.resend.com/emails");
    const body = JSON.parse(String(init.body));
    expect(body.to).toEqual(["rn@rninvest.de"]);
    expect(body.reply_to).toBe("max@example.de");
    expect((init.headers as Record<string, string>)["Idempotency-Key"]).toBe("contact-id-2");
  });
  it("reports provider errors as failures", async () => {
    vi.stubEnv("RESEND_API_KEY", "test-key");
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => new Response("{}", { status: 422 })),
    );
    expect(await deliverContactMail(data, "id-3")).toEqual({ ok: false, reason: "provider_error" });
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => new Response("{}", { status: 200 })),
    );
    expect(await deliverContactMail(data, "id-4")).toEqual({ ok: false, reason: "provider_error" });
  });
});
