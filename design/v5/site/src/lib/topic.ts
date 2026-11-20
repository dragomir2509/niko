import { useSyncExternalStore } from "react";

/** Shared prefill between the acquisition profile and the contact form. */
type Selection = { location: string; propertyType: string; stamp: number };
const initial: Selection = { location: "", propertyType: "", stamp: 0 };
let current = initial;
const subs = new Set<() => void>();

export function prefillContact(values: { location?: string; propertyType?: string }) {
  current = { ...current, ...values, stamp: current.stamp + 1 };
  subs.forEach((s) => s());
}

export function useContactSelection() {
  return useSyncExternalStore(
    (cb) => {
      subs.add(cb);
      return () => {
        subs.delete(cb);
      };
    },
    () => current,
    () => initial,
  );
}
