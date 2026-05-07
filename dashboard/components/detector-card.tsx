import type { DetectorMeta } from "@/lib/detectors";
import { SeverityBadge } from "./severity-badge";

export function DetectorCard({ detector }: { detector: DetectorMeta }) {
  const isRoadmap = detector.status === "roadmap";
  const isAdjacent = detector.chainLabel === "Adjacent vector";
  return (
    <div
      className={`flex flex-col gap-3 rounded-lg border p-5 transition-colors ${
        isRoadmap
          ? "border-dashed border-border bg-surface/30 opacity-75"
          : "border-border bg-surface hover:border-border-strong"
      }`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <div className="mb-1.5 flex items-center gap-2">
            <span
              className={`inline-flex items-center rounded px-1.5 py-0.5 font-mono text-[10px] font-semibold uppercase tracking-wider ${
                isAdjacent
                  ? "bg-surface-elevated text-muted"
                  : "bg-accent/10 text-accent"
              }`}
            >
              {detector.chainLabel}
            </span>
          </div>
          <h3 className="font-semibold tracking-tight">{detector.name}</h3>
          <p className="mt-0.5 text-xs text-muted">{detector.subtitle}</p>
        </div>
        {isRoadmap ? (
          <span className="inline-flex items-center rounded border border-border px-1.5 py-0.5 font-mono text-[10px] font-semibold uppercase tracking-wider text-muted-strong">
            Roadmap
          </span>
        ) : (
          <SeverityBadge severity={detector.severity} />
        )}
      </div>
      <div className="font-mono text-xs text-muted-strong">
        <span className="text-muted">attack step · </span>
        {detector.attackStep}
      </div>
      <p className="text-sm leading-relaxed text-muted-strong">{detector.description}</p>
      <div className="border-t border-border pt-3">
        <p className="font-mono text-[11px] text-muted">
          <span className="text-muted-strong">if undetected · </span>
          {detector.impact}
        </p>
      </div>
    </div>
  );
}
