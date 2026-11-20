import { useEffect, useRef, useState, type FormEvent, type ReactNode } from "react";
import { useServerFn } from "@tanstack/react-start";
import { CONTENT, PROPERTY_TYPES } from "@/content/site";
import { SITE } from "@/config/site";
import { useContactSelection } from "@/lib/topic";
import { submitContact } from "@/lib/contact.functions";
import {
  FIELD_ORDER,
  buildMailto,
  normalize,
  validate,
  type FormErrors,
  type FormField,
  type FormType,
  type FormValues,
} from "@/lib/form";
import { Eyebrow } from "./ui/Eyebrow";
import { Button } from "./ui/Button";
import { Reveal } from "./ui/Reveal";

type Status = "idle" | "sending" | "success" | "error";
type TextKey = "location" | "exposeUrl" | "name" | "email" | "phone";

const EMPTY: FormValues = {
  formType: "property",
  name: "",
  email: "",
  phone: "",
  location: "",
  propertyType: "",
  exposeUrl: "",
  message: "",
  consent: false,
};

function Field({
  id,
  label,
  error,
  full = false,
  children,
}: {
  id: string;
  label: string;
  error?: string | undefined;
  full?: boolean;
  children: ReactNode;
}) {
  return (
    <div className={`field ${full ? "field-full" : ""}`}>
      <label className="micro" htmlFor={id}>
        {label}
      </label>
      {children}
      {error && (
        <p id={`${id}-error`} className="field-error">
          {error}
        </p>
      )}
    </div>
  );
}

export function Kontakt() {
  const c = CONTENT.contact;
  const send = useServerFn(submitContact);
  const selection = useContactSelection();
  const startedAt = useRef(Date.now());
  const requestId = useRef("");
  const [v, setV] = useState<FormValues>(EMPTY);
  const [honeypot, setHoneypot] = useState("");
  const [errors, setErrors] = useState<FormErrors>({});
  const [status, setStatus] = useState<Status>("idle");
  const [failure, setFailure] = useState<{ text: string; mailto: boolean }>({
    text: "",
    mailto: false,
  });

  useEffect(() => {
    if (!selection.stamp) return;
    setStatus((s) => (s === "success" ? "idle" : s));
    setV((p) => ({
      ...p,
      formType: "property",
      ...(selection.location ? { location: selection.location } : {}),
      ...(selection.propertyType ? { propertyType: selection.propertyType } : {}),
    }));
  }, [selection]);

  const clearError = (key: FormField) =>
    setErrors((prev) => {
      if (!prev[key]) return prev;
      const next = { ...prev };
      delete next[key];
      return next;
    });
  const update = (key: Exclude<keyof FormValues, "consent" | "formType">) => (value: string) => {
    setV((p) => ({ ...p, [key]: value }));
    clearError(key);
  };
  const aria = (key: FormField) => ({
    "aria-invalid": errors[key] ? (true as const) : undefined,
    "aria-describedby": errors[key] ? `f-${key}-error` : undefined,
  });

  async function submit(e: FormEvent) {
    e.preventDefault();
    if (status === "sending") return;
    const values = normalize(v);
    const found = validate(values);
    setErrors(found);
    const first = FIELD_ORDER.find((key) => found[key]);
    if (first) {
      document.getElementById(`f-${first}`)?.focus();
      return;
    }
    setStatus("sending");
    try {
      if (!requestId.current) requestId.current = crypto.randomUUID();
      const result = await send({
        data: {
          values,
          requestId: requestId.current,
          website: honeypot,
          startedAt: startedAt.current,
        },
      });
      if (result.ok) {
        setStatus("success");
        return;
      }
      setFailure({ text: result.error, mailto: result.code !== "invalid" });
      setStatus("error");
    } catch {
      setFailure({ text: `${c.networkError} ${SITE.email}.`, mailto: true });
      setStatus("error");
    }
  }

  function reset() {
    requestId.current = "";
    startedAt.current = Date.now();
    setV(EMPTY);
    setErrors({});
    setStatus("idle");
  }

  const text = (key: TextKey, full = false) => (
    <Field id={`f-${key}`} label={c.labels[key]} error={errors[key]} full={full}>
      <input
        id={`f-${key}`}
        name={key}
        className="input"
        value={v[key]}
        onChange={(e) => update(key)(e.target.value)}
        type={
          key === "email" ? "email" : key === "phone" ? "tel" : key === "exposeUrl" ? "url" : "text"
        }
        inputMode={key === "exposeUrl" ? "url" : undefined}
        placeholder={
          key === "location"
            ? c.placeholders.location
            : key === "exposeUrl"
              ? c.placeholders.exposeUrl
              : undefined
        }
        maxLength={
          key === "exposeUrl"
            ? 2000
            : key === "email"
              ? 254
              : key === "name"
                ? 100
                : key === "phone"
                  ? 60
                  : 250
        }
        required={key === "name" || key === "email" || key === "location"}
        autoComplete={
          key === "name" ? "name" : key === "email" ? "email" : key === "phone" ? "tel" : "off"
        }
        {...aria(key)}
      />
    </Field>
  );

  const property = v.formType === "property";

  return (
    <section id="kontakt" className="section" aria-labelledby="kontakt-title">
      <Reveal className="wrap grid">
        <div className="contact-aside">
          <Eyebrow index="05">{c.eyebrow}</Eyebrow>
          <h2 id="kontakt-title" className="contact-title">
            {c.title[0]}
            <br />
            {c.title[1]}
          </h2>
          <p className="lead muted">{c.lead}</p>
          <div className="contact-direct">
            <span className="micro muted">{c.directLabel}</span>
            <br />
            <a className="contact-mail link" href={`mailto:${SITE.email}`}>
              {SITE.email}
            </a>
            <address className="contact-address">
              {SITE.legalName}
              <br />
              {SITE.street}
              <br />
              {SITE.postalCode} {SITE.city}
            </address>
          </div>
        </div>
        <div className="contact-form">
          {status === "success" ? (
            <div className="form-success" role="status" tabIndex={-1}>
              <Eyebrow>{c.successEyebrow}</Eyebrow>
              <h3>{c.successTitle}</h3>
              <p className="muted">{c.successText}</p>
              <div className="form-actions">
                <Button onClick={reset}>{c.again}</Button>
              </div>
            </div>
          ) : (
            <form noValidate onSubmit={submit} aria-labelledby="kontakt-title">
              <fieldset className="mode">
                <legend className="micro muted">{c.modeLegend}</legend>
                <div className="segmented micro">
                  {(["property", "general"] as FormType[]).map((mode) => (
                    <label key={mode}>
                      <input
                        type="radio"
                        name="formType"
                        value={mode}
                        checked={v.formType === mode}
                        onChange={() => {
                          setV((p) => ({ ...p, formType: mode }));
                          setErrors({});
                        }}
                      />
                      <span>{c.modes[mode]}</span>
                    </label>
                  ))}
                </div>
              </fieldset>
              <div className="fields">
                {property && (
                  <>
                    {text("location", true)}
                    <Field
                      id="f-propertyType"
                      label={c.labels.propertyType}
                      error={errors.propertyType}
                    >
                      <select
                        id="f-propertyType"
                        name="propertyType"
                        className="input"
                        value={v.propertyType}
                        onChange={(e) => update("propertyType")(e.target.value)}
                        required
                        {...aria("propertyType")}
                      >
                        <option value="" disabled>
                          {c.placeholders.propertyType}
                        </option>
                        {PROPERTY_TYPES.map((type) => (
                          <option key={type} value={type}>
                            {type}
                          </option>
                        ))}
                      </select>
                    </Field>
                    {text("exposeUrl")}
                  </>
                )}
                {text("name")}
                {text("email")}
                {text("phone", true)}
                <Field id="f-message" label={c.labels.message} error={errors.message} full>
                  <textarea
                    id="f-message"
                    name="message"
                    className="input"
                    rows={4}
                    maxLength={5000}
                    value={v.message}
                    onChange={(e) => update("message")(e.target.value)}
                    placeholder={
                      property ? c.placeholders.messageProperty : c.placeholders.messageGeneral
                    }
                    {...aria("message")}
                  />
                </Field>
              </div>
              <div className="honeypot" aria-hidden="true">
                <label htmlFor="f-website">Website</label>
                <input
                  id="f-website"
                  name="website"
                  tabIndex={-1}
                  autoComplete="off"
                  value={honeypot}
                  onChange={(e) => setHoneypot(e.target.value)}
                />
              </div>
              <label className="consent" htmlFor="f-consent">
                <input
                  id="f-consent"
                  name="consent"
                  type="checkbox"
                  required
                  checked={v.consent}
                  onChange={(e) => {
                    setV((p) => ({ ...p, consent: e.target.checked }));
                    clearError("consent");
                  }}
                  {...aria("consent")}
                />
                <span>
                  {c.consentBefore}{" "}
                  <a href="/datenschutz" target="_blank" rel="noopener">
                    {c.consentLink}
                  </a>{" "}
                  {c.consentAfter}
                </span>
              </label>
              {errors.consent && (
                <p id="f-consent-error" className="field-error">
                  {errors.consent}
                </p>
              )}
              {status === "error" && (
                <div className="form-status" role="alert">
                  <p>{failure.text}</p>
                  {failure.mailto && (
                    <p>
                      <a href={buildMailto(SITE.email, v)}>{c.fallbackLink}</a>
                    </p>
                  )}
                </div>
              )}
              <div className="form-actions">
                <Button type="submit" solid disabled={status === "sending"}>
                  {status === "sending" ? c.sending : c.submit}
                </Button>
                <span className="form-hint">{c.required}</span>
              </div>
            </form>
          )}
        </div>
      </Reveal>
    </section>
  );
}
