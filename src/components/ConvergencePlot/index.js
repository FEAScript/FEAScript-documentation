import React, { useState } from "react";
import styles from "./styles.module.css";

// Log-log convergence plot: error against element size, one line per element order.
// Series take the categorical slots in fixed order (slot 1 blue, slot 2 orange); the tables next
// to each plot in the docs are its table view.

const WIDTH = 640;
const HEIGHT = 360;
const MARGIN = { top: 16, right: 24, bottom: 52, left: 72 };
const PADDING = 0.25; // Decades of padding around the data on each logarithmic axis
const LABEL_ROOM = 0.45; // Extra decades left of the data for the direct labels

// Decades inside [min, max]
function logTicks(min, max) {
  const ticks = [];
  for (let e = Math.ceil(Math.log10(min)); e <= Math.floor(Math.log10(max)); e++) ticks.push(10 ** e);
  return ticks;
}

// Tick label as a power of ten: 10 followed by a superscript exponent
function PowerLabel({ value }) {
  const exponent = Math.round(Math.log10(value));
  if (exponent === 0) return "1";
  if (exponent === 1) return "10";
  return (
    <>
      10
      <tspan dy="-0.5em" fontSize="0.75em">
        {exponent}
      </tspan>
    </>
  );
}

export default function ConvergencePlot({ title, xLabel, yLabel, series }) {
  const [hovered, setHovered] = useState(null);

  const allX = series.flatMap((s) => s.points.map(([x]) => x));
  const allY = series.flatMap((s) => s.points.map(([, y]) => y));
  const xMin = 10 ** (Math.log10(Math.min(...allX)) - PADDING - LABEL_ROOM);
  const xMax = 10 ** (Math.log10(Math.max(...allX)) + PADDING);
  const yMin = 10 ** (Math.log10(Math.min(...allY)) - PADDING);
  const yMax = 10 ** (Math.log10(Math.max(...allY)) + PADDING);
  const xTicks = logTicks(xMin, xMax);
  const yTicks = logTicks(yMin, yMax);

  const plotWidth = WIDTH - MARGIN.left - MARGIN.right;
  const plotHeight = HEIGHT - MARGIN.top - MARGIN.bottom;
  const scaleX = (x) =>
    MARGIN.left + ((Math.log10(x) - Math.log10(xMin)) / (Math.log10(xMax) - Math.log10(xMin))) * plotWidth;
  const scaleY = (y) =>
    MARGIN.top +
    plotHeight -
    ((Math.log10(y) - Math.log10(yMin)) / (Math.log10(yMax) - Math.log10(yMin))) * plotHeight;

  return (
    <figure className={styles.figure}>
      {title && <figcaption className={styles.title}>{title}</figcaption>}
      <div className={styles.legend}>
        {series.map((s, index) => (
          <span key={s.name} className={styles.legendItem}>
            <span className={`${styles.swatch} ${styles[`series${index + 1}`]}`} />
            {s.name}
          </span>
        ))}
      </div>
      <div className={styles.plotArea}>
        <svg
          viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
          className={styles.svg}
          role="img"
          aria-label={`${title}: ${yLabel} against ${xLabel}, logarithmic axes`}
        >
          {xTicks.map((tick) => (
            <g key={`x${tick}`}>
              <line
                className={styles.grid}
                x1={scaleX(tick)}
                x2={scaleX(tick)}
                y1={MARGIN.top}
                y2={MARGIN.top + plotHeight}
              />
              <text
                className={styles.tick}
                x={scaleX(tick)}
                y={MARGIN.top + plotHeight + 18}
                textAnchor="middle"
              >
                <PowerLabel value={tick} />
              </text>
            </g>
          ))}
          {yTicks.map((tick) => (
            <g key={`y${tick}`}>
              <line
                className={styles.grid}
                x1={MARGIN.left}
                x2={MARGIN.left + plotWidth}
                y1={scaleY(tick)}
                y2={scaleY(tick)}
              />
              <text className={styles.tick} x={MARGIN.left - 8} y={scaleY(tick) + 4} textAnchor="end">
                <PowerLabel value={tick} />
              </text>
            </g>
          ))}
          <line
            className={styles.axis}
            x1={MARGIN.left}
            x2={MARGIN.left + plotWidth}
            y1={MARGIN.top + plotHeight}
            y2={MARGIN.top + plotHeight}
          />
          <text
            className={styles.axisLabel}
            x={MARGIN.left + plotWidth / 2}
            y={HEIGHT - 10}
            textAnchor="middle"
          >
            {xLabel}
          </text>
          <text
            className={styles.axisLabel}
            transform={`translate(16 ${MARGIN.top + plotHeight / 2}) rotate(-90)`}
            textAnchor="middle"
          >
            {yLabel}
          </text>

          {series.map((s, index) => {
            const seriesClass = styles[`series${index + 1}`];
            const path = s.points
              .map(([x, y], i) => `${i === 0 ? "M" : "L"}${scaleX(x)},${scaleY(y)}`)
              .join(" ");
            const [lastX, lastY] = s.points.reduce((a, b) => (a[0] < b[0] ? a : b));
            return (
              <g key={s.name}>
                <path className={`${styles.line} ${seriesClass}`} d={path} />
                {s.points.map(([x, y]) => (
                  <circle
                    key={x}
                    className={`${styles.marker} ${seriesClass}`}
                    cx={scaleX(x)}
                    cy={scaleY(y)}
                    r={4.5}
                  />
                ))}
                <text
                  className={styles.directLabel}
                  x={scaleX(lastX) - 10}
                  y={scaleY(lastY) + 4}
                  textAnchor="end"
                >
                  {s.name}
                </text>
              </g>
            );
          })}

          {series.map((s) =>
            s.points.map(([x, y]) => (
              <circle
                key={`${s.name}${x}`}
                className={styles.hitTarget}
                cx={scaleX(x)}
                cy={scaleY(y)}
                r={12}
                tabIndex={0}
                aria-label={`${s.name}: ${xLabel} ${x}, ${yLabel} ${y.toExponential(1)}`}
                onMouseEnter={() => setHovered({ name: s.name, x, y })}
                onMouseLeave={() => setHovered(null)}
                onFocus={() => setHovered({ name: s.name, x, y })}
                onBlur={() => setHovered(null)}
              />
            )),
          )}
        </svg>
        {hovered && (
          <div
            className={styles.tooltip}
            style={{
              left: `${(scaleX(hovered.x) / WIDTH) * 100}%`,
              top: `${(scaleY(hovered.y) / HEIGHT) * 100}%`,
            }}
          >
            <strong>{hovered.name}</strong>
            <span>
              {xLabel}: {hovered.x}
            </span>
            <span>
              {yLabel}: {hovered.y.toExponential(1)}
            </span>
          </div>
        )}
      </div>
    </figure>
  );
}
