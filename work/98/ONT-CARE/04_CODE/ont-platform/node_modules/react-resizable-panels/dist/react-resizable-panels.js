"use client";
import { jsx as Y, jsxs as En } from "react/jsx-runtime";
import { useId as Mn, useLayoutEffect as tn, useEffect as He, useRef as B, useCallback as re, createContext as nn, useContext as on, useState as ge, useMemo as Me, useImperativeHandle as mt, useSyncExternalStore as tt, Children as Pn, isValidElement as rn } from "react";
function et(e) {
  return (typeof e == "number" || typeof e == "string") && e !== "";
}
function Te(e) {
  const t = Mn();
  return et(e) ? `${e}` : t;
}
const ne = typeof window < "u" ? tn : He;
function Se(e) {
  const t = B(e);
  return ne(() => {
    t.current = e;
  }, [e]), re(
    (...n) => t.current?.(...n),
    [t]
  );
}
function Ve(...e) {
  return Se((t) => {
    e.forEach((n) => {
      if (n)
        switch (typeof n) {
          case "function": {
            n(t);
            break;
          }
          case "object": {
            n.current = t;
            break;
          }
        }
    });
  });
}
function je(e, t) {
  const n = e?.["data-testid"];
  return et(n) ? `${n}` : et(t) ? `${t}` : void 0;
}
function lt(e, t) {
  return t ? e * 2 + 1 : e + 1;
}
function Tn(e, t) {
  return t ? e * 2 - 1 : e;
}
function Lt(e, t, n) {
  const o = lt(e, n);
  return t === void 0 ? `${o} / -1` : `${o} / span ${Tn(t, n)}`;
}
function Dn(e) {
  return `${e * 2} / span 1`;
}
function kn({
  crossCount: e,
  crossSpan: t,
  crossStart: n,
  hasGutters: o
}) {
  const r = t === void 0 ? e : n + t;
  if (n === 0 && r === e)
    return "1 / -1";
  let i = lt(n, o), a = lt(r - 1, o) + 1;
  return o && (n > 0 && i--, r < e && a++), `${i} / ${a}`;
}
function pt(e, t) {
  return Number.isInteger(e) && e >= 1 && e < t;
}
function N(e, t = "Assertion error") {
  if (!e)
    throw Error(t);
}
const sn = nn(null);
function an() {
  const e = on(sn);
  return N(
    e,
    "Grid Context not found; did you render a Cell or Gridline outside of a Grid?"
  ), e;
}
function An({
  children: e,
  className: t,
  column: n,
  columnSpan: o = 1,
  elementRef: r,
  id: i,
  row: a,
  rowSpan: c = 1,
  style: s,
  ...u
}) {
  const l = Te(i), { gutters: d, registerCell: h } = an(), p = B(null), m = Ve(p, r);
  return ne(() => {
    const f = p.current;
    if (f !== null)
      return h({
        column: n,
        columnSpan: o,
        element: f,
        id: l,
        row: a,
        rowSpan: c
      });
  }, [n, o, l, h, a, c]), /* @__PURE__ */ Y(
    "div",
    {
      ...u,
      className: t,
      "data-cell": !0,
      "data-testid": je(u, i),
      id: l,
      ref: m,
      style: {
        overflow: "auto",
        ...s,
        // Allow cells to shrink smaller than their content
        minHeight: 0,
        minWidth: 0,
        gridColumn: Lt(n, o, d.column),
        gridRow: Lt(a, c, d.row)
      },
      children: e
    }
  );
}
An.displayName = "Cell";
let Xe;
function $n() {
  return Xe === void 0 && (typeof matchMedia == "function" ? Xe = !!matchMedia("(pointer:coarse)").matches : Xe = !1), Xe;
}
function ut({
  expandHitTargets: e,
  axis: t,
  rect: n
}) {
  const o = e ? $n() ? t.resizeTargetMinimumSize.coarse : t.resizeTargetMinimumSize.fine : 0;
  if (n.width < o) {
    const r = o - n.width;
    n = new DOMRect(
      n.x - r / 2,
      n.y,
      n.width + r,
      n.height
    );
  }
  if (n.height < o) {
    const r = o - n.height;
    n = new DOMRect(
      n.x,
      n.y - r / 2,
      n.width,
      n.height + r
    );
  }
  return n;
}
function Ct({
  axis: e,
  cells: t,
  index: n,
  rect: o
}) {
  let r = [o];
  for (const i of t) {
    const a = e === "column" ? i.column : i.row, c = e === "column" ? i.columnSpan : i.rowSpan;
    if (a >= n || a + c <= n)
      continue;
    const s = i.element.getBoundingClientRect(), u = e === "column" ? s.top : s.left, l = e === "column" ? s.bottom : s.right;
    l <= u || (r = r.flatMap((d) => {
      const h = e === "column" ? d.top : d.left, p = e === "column" ? d.bottom : d.right;
      if (u >= p || l <= h)
        return [d];
      const m = [], f = (y, g) => {
        m.push(
          e === "column" ? new DOMRect(d.x, y, d.width, g - y) : new DOMRect(y, d.y, g - y, d.height)
        );
      };
      return h < u && f(h, u), p > l && f(l, p), m;
    }));
  }
  return r;
}
function On({
  axis: e,
  cells: t,
  crossTrackCount: n,
  expandHitTargets: o,
  resizeAxis: r,
  axisSize: i,
  includeDisabled: a,
  separatorPlacements: c
}) {
  const { items: s, separators: u } = r, l = s.length;
  let d = -1, h = -1, p = 0;
  if (s.forEach((x, w) => {
    x.constraintProps.disabled || (p++, d === -1 && (d = w), h = w);
  }), !a && p < 2)
    return [];
  const m = (x) => a || x > d && x <= h, f = [], y = (x, w, v) => ({
    axis: r,
    axisSize: i,
    items: [s[x - 1], s[x]],
    rect: w,
    separator: v
  }), g = (x, w) => {
    let v;
    for (const M of t) {
      const k = e === "column" ? M.row : M.column, P = e === "column" ? M.rowSpan : M.columnSpan;
      if (w === "start" ? k === x : k + P - 1 === x) {
        const $ = M.element.getBoundingClientRect();
        if (w === "start") {
          const C = e === "column" ? $.top : $.left;
          v = v === void 0 ? C : Math.min(v, C);
        } else {
          const C = e === "column" ? $.bottom : $.right;
          v = v === void 0 ? C : Math.max(v, C);
        }
      }
    }
    return v;
  }, S = /* @__PURE__ */ new Set();
  for (const x of u) {
    const w = c.get(x);
    if (!w || w.index < 1 || w.index >= l || (S.add(w.index), !a && (x.disabled || x.element.hasAttribute("aria-disabled"))) || !m(w.index))
      continue;
    let v = x.element.getBoundingClientRect();
    const { crossSpan: M, crossStart: k } = w, P = M === void 0 ? n : k + M;
    let $ = e === "column" ? v.top : v.left, C = e === "column" ? v.bottom : v.right;
    if (k > 0) {
      const I = g(k - 1, "end");
      I !== void 0 && I < $ && ($ = I);
    }
    if (P < n) {
      const I = g(P, "start");
      I !== void 0 && I > C && (C = I);
    }
    v = e === "column" ? new DOMRect(v.x, $, v.width, C - $) : new DOMRect($, v.y, C - $, v.height), v = ut({ expandHitTargets: o, axis: r, rect: v }), a ? f.push(y(w.index, v, x)) : Ct({
      axis: e,
      cells: t,
      index: w.index,
      rect: v
    }).forEach((I) => {
      f.push(y(w.index, I, x));
    });
  }
  const z = (x, w) => {
    Ct({
      axis: e,
      cells: t,
      index: x,
      rect: ut({ expandHitTargets: o, axis: r, rect: w })
    }).forEach((v) => {
      f.push(y(x, v));
    });
  }, b = Array.from(
    { length: n },
    () => new Array(l)
  );
  for (const x of t) {
    const [w, v, M, k] = e === "column" ? [x.column, x.columnSpan, x.row, x.rowSpan] : [x.row, x.rowSpan, x.column, x.columnSpan];
    for (let P = Math.max(0, M); P < Math.min(n, M + k); P++)
      for (let $ = Math.max(0, w); $ < Math.min(l, w + v); $++)
        b[P][$] ??= x;
  }
  const R = /* @__PURE__ */ new Map(), O = (x) => {
    let w = R.get(x);
    if (!w) {
      const v = x.element.getBoundingClientRect();
      w = e === "column" ? {
        crossEnd: v.bottom,
        crossStart: v.top,
        end: v.right,
        start: v.left
      } : {
        crossEnd: v.right,
        crossStart: v.left,
        end: v.bottom,
        start: v.top
      }, R.set(x, w);
    }
    return w;
  }, A = ({ crossEnd: x, crossStart: w, end: v, start: M }) => e === "column" ? new DOMRect(M, w, v - M, x - w) : new DOMRect(w, M, x - w, v - M);
  for (let x = 1; x < l; x++) {
    if (S.has(x) || !m(x))
      continue;
    let w;
    for (let v = 0; v < n; v++) {
      const M = b[v][x - 1], k = b[v][x];
      let P;
      if ((M || k) && M !== k) {
        const $ = M ? O(M) : void 0, C = k ? O(k) : void 0, I = $?.end ?? C.start, E = C?.start ?? $.end, q = Math.max(
          $?.crossStart ?? -1 / 0,
          C?.crossStart ?? -1 / 0
        ), Z = Math.min(
          $?.crossEnd ?? 1 / 0,
          C?.crossEnd ?? 1 / 0
        );
        P = {
          crossEnd: Math.max(q, Z),
          crossStart: q,
          end: Math.max(I, E),
          start: Math.min(I, E)
        };
      }
      P ? w = w ? {
        crossEnd: Math.max(w.crossEnd, P.crossEnd),
        crossStart: Math.min(w.crossStart, P.crossStart),
        end: Math.max(w.end, P.end),
        start: Math.min(w.start, P.start)
      } : P : w && (z(x, A(w)), w = void 0);
    }
    w && z(x, A(w));
  }
  return f;
}
function le(e) {
  const t = parseFloat(e ?? "");
  return Number.isFinite(t) ? t : 0;
}
function Nn({
  axis: e,
  element: t,
  gutterSizes: n,
  hasGutters: o,
  layout: r,
  trackIds: i
}) {
  const a = i.length, c = o ? a * 2 - 1 : a, s = t.ownerDocument.defaultView?.getComputedStyle(t), u = e === "column" ? s?.gridTemplateColumns : s?.gridTemplateRows;
  if (u) {
    const f = u.trim().split(/\s+/);
    if (f.length === c && f.every((y) => /^-?[\d.]+px$/.test(y))) {
      const y = i.map(
        (g, S) => le(f[o ? S * 2 : S])
      );
      return {
        availableSize: y.reduce((g, S) => g + S, 0),
        trackSizes: y
      };
    }
  }
  const l = e === "column" ? t.offsetWidth : t.offsetHeight, d = e === "column" ? le(s?.paddingLeft) + le(s?.paddingRight) + le(s?.borderLeftWidth) + le(s?.borderRightWidth) : le(s?.paddingTop) + le(s?.paddingBottom) + le(s?.borderTopWidth) + le(s?.borderBottomWidth), h = le(e === "column" ? s?.columnGap : s?.rowGap), p = n.reduce((f, y) => f + y, 0), m = Math.max(
    0,
    l - d - h * Math.max(0, c - 1) - p
  );
  return {
    availableSize: m,
    trackSizes: i.map(
      (f) => r && r[f] !== void 0 ? r[f] / 100 * m : m / a
    )
  };
}
function cn(e) {
  switch (typeof e) {
    case "number":
      return [e, "px"];
    case "string": {
      const t = parseFloat(e);
      return e.endsWith("%") ? [t, "%"] : e.endsWith("px") ? [t, "px"] : e.endsWith("rem") ? [t, "rem"] : e.endsWith("em") ? [t, "em"] : e.endsWith("vh") ? [t, "vh"] : e.endsWith("vw") ? [t, "vw"] : [t, "%"];
    }
  }
}
class ln {
  #e = {};
  addListener(t, n) {
    const o = this.#e[t];
    return o === void 0 ? this.#e[t] = [n] : o.includes(n) || o.push(n), () => {
      this.removeListener(t, n);
    };
  }
  emit(t, n) {
    const o = this.#e[t];
    if (o !== void 0) {
      if (o.length === 1) {
        o[0].call(null, n);
        return;
      }
      let r;
      const i = Array.from(o);
      for (let a = 0; a < i.length; a++) {
        const c = i[a];
        try {
          c.call(null, n);
        } catch (s) {
          r ??= { error: s };
        }
      }
      if (r)
        throw r.error;
    }
  }
  removeAllListeners() {
    this.#e = {};
  }
  removeListener(t, n) {
    const o = this.#e[t];
    if (o !== void 0) {
      const r = o.indexOf(n);
      r >= 0 && o.splice(r, 1);
    }
  }
}
let H = {
  cursorFlags: 0,
  state: "inactive"
};
const ht = new ln();
function ie() {
  return H;
}
function gt(e) {
  return ht.addListener("change", e);
}
function Gn(e, t = [], n, o = !1) {
  const r = H, i = { ...H };
  i.cursorFlags = e, i.state === "active" && (i.didPointerMove ||= o, i.previews = t, n && (i.previewLayoutMap = n)), H = i, ht.emit("change", {
    prev: r,
    next: i
  });
}
function fe(e) {
  const t = H;
  H = e, t.state === "active" && e.state !== "active" && t.didPointerMove && t.hitRegions.forEach(({ separator: n }) => {
    n && n.element.ownerDocument.activeElement === n.element && n.element.blur();
  }), ht.emit("change", {
    prev: t,
    next: e
  });
}
function Fn(e) {
  H.state !== "active" || !H.previews.some((t) => t.separator === e) || fe({
    ...H,
    previews: H.previews.map(
      (t) => t.separator === e ? { ...t } : t
    )
  });
}
function _n(e) {
  if (H.state === "inactive")
    return;
  const t = H.hitRegions.filter((o) => o.axis !== e), n = H.state === "active" && H.previews.some((o) => o.axis === e);
  if (!(t.length === H.hitRegions.length && !n))
    if (t.length === 0)
      fe({ cursorFlags: 0, state: "inactive" });
    else if (H.state === "active") {
      const o = new Map(H.initialLayoutMap), r = new Map(H.previewLayoutMap);
      o.delete(e), r.delete(e), fe({
        ...H,
        cursorFlags: 0,
        hitRegions: t,
        initialLayoutMap: o,
        previewLayoutMap: r,
        previews: H.previews.filter((i) => i.axis !== e)
      });
    } else
      fe({ ...H, hitRegions: t });
}
const Bn = (e) => e, ct = () => {
}, un = 1, dn = 2, fn = 4, mn = 8, Rt = 3, Et = 12;
let Ke;
function Mt() {
  return Ke === void 0 && (Ke = !1, typeof window < "u" && (window.navigator.userAgent.includes("Chrome") || window.navigator.userAgent.includes("Firefox")) && (Ke = !0)), Ke;
}
function qn({
  cursorFlags: e,
  axes: t,
  state: n
}) {
  let o = 0, r = 0;
  switch (n) {
    case "active":
    case "hover":
      t.forEach((i) => {
        if (!i.mutableState.disableCursor)
          switch (i.orientation) {
            case "horizontal": {
              o++;
              break;
            }
            case "vertical": {
              r++;
              break;
            }
          }
      });
  }
  if (!(o === 0 && r === 0)) {
    switch (n) {
      case "active": {
        if (e && Mt()) {
          const i = (e & un) !== 0, a = (e & dn) !== 0, c = (e & fn) !== 0, s = (e & mn) !== 0;
          if (i)
            return c ? "se-resize" : s ? "ne-resize" : "e-resize";
          if (a)
            return c ? "sw-resize" : s ? "nw-resize" : "w-resize";
          if (c)
            return "s-resize";
          if (s)
            return "n-resize";
        }
        break;
      }
    }
    return Mt() ? o > 0 && r > 0 ? "move" : o > 0 ? "ew-resize" : "ns-resize" : o > 0 && r > 0 ? "grab" : o > 0 ? "col-resize" : "row-resize";
  }
}
const Pt = /* @__PURE__ */ new WeakMap();
function Tt(e) {
  if (!e.defaultView || !e.adoptedStyleSheets)
    return;
  let { prevStyle: t, styleSheet: n } = Pt.get(e) ?? {};
  n === void 0 && (n = new e.defaultView.CSSStyleSheet(), e.adoptedStyleSheets && (Object.isExtensible(e.adoptedStyleSheets) ? e.adoptedStyleSheets.push(n) : e.adoptedStyleSheets = [
    ...e.adoptedStyleSheets,
    n
  ]));
  let o = ie();
  switch (o.state !== "inactive" && o.ownerDocument !== e && (o = { cursorFlags: 0, state: "inactive" }), o.state) {
    case "active":
    case "hover": {
      const r = qn({
        cursorFlags: o.cursorFlags,
        axes: o.hitRegions.map((a) => a.axis),
        state: o.state
      }), i = `*, *:hover {cursor: ${r} !important; }`;
      if (t === i)
        return;
      t = i, r ? n.cssRules.length === 0 ? n.insertRule(i) : n.replaceSync(i) : n.cssRules.length === 1 && n.deleteRule(0);
      break;
    }
    case "inactive": {
      t = void 0, n.cssRules.length === 1 && n.deleteRule(0);
      break;
    }
  }
  Pt.set(e, {
    prevStyle: t,
    styleSheet: n
  });
}
function Dt(e) {
  return e.state === "inactive" ? void 0 : e.ownerDocument;
}
function Hn({
  next: e,
  prev: t
}) {
  const n = Dt(t), o = Dt(e);
  n && n !== o && Tt(n), o && Tt(o);
}
function Pe({
  axis: e
}) {
  const { layoutStrategy: t, orientation: n, items: o } = e;
  return t ? t.calculateAvailableSize() : o.reduce((r, i) => (r += n === "horizontal" ? i.element.offsetWidth : i.element.offsetHeight, r), 0);
}
function yt(e, t) {
  const n = e.compareDocumentPosition(t);
  return n & Node.DOCUMENT_POSITION_DISCONNECTED ? 0 : n & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : n & Node.DOCUMENT_POSITION_PRECEDING ? 1 : 0;
}
function Ge(e, t) {
  return Array.from(t).sort((n, o) => {
    const r = e === "horizontal" ? Vn(n, o) : jn(n, o);
    return r !== 0 ? r : yt(n.element, o.element);
  });
}
function Vn(e, t) {
  const n = e.element.offsetLeft - t.element.offsetLeft;
  return n !== 0 ? n : e.element.offsetWidth - t.element.offsetWidth;
}
function jn(e, t) {
  const n = e.element.offsetTop - t.element.offsetTop;
  return n !== 0 ? n : e.element.offsetHeight - t.element.offsetHeight;
}
function dt(e) {
  return e !== null && typeof e == "object" && "nodeType" in e && e.nodeType === Node.ELEMENT_NODE;
}
function pn(e, t) {
  return {
    x: e.x >= t.left && e.x <= t.right ? 0 : Math.min(
      Math.abs(e.x - t.left),
      Math.abs(e.x - t.right)
    ),
    y: e.y >= t.top && e.y <= t.bottom ? 0 : Math.min(
      Math.abs(e.y - t.top),
      Math.abs(e.y - t.bottom)
    )
  };
}
function Un({
  orientation: e,
  rects: t,
  targetRect: n
}) {
  const o = {
    x: n.x + n.width / 2,
    y: n.y + n.height / 2
  };
  let r, i = Number.MAX_VALUE;
  for (const a of t) {
    const { x: c, y: s } = pn(o, a), u = e === "horizontal" ? c : s;
    u < i && (i = u, r = a);
  }
  return N(r, "No rect found"), r;
}
function St({
  expandHitTargets: e = !0,
  axis: t,
  includeDisabled: n = !1
}) {
  if (t.layoutStrategy)
    return t.layoutStrategy.calculateHitRegions({
      expandHitTargets: e,
      axis: t,
      includeDisabled: n
    });
  const { element: o, orientation: r, items: i, separators: a } = t, c = Ge(
    r,
    Array.from(o.children).filter(dt).filter((g) => !g.hasAttribute("data-resize-preview")).map((g) => ({ element: g }))
  ).map(({ element: g }) => g), s = [];
  let u = !1, l = !1, d = -1, h, p = -1, m = 0, f, y = [];
  {
    let g = -1;
    for (const S of c)
      S.hasAttribute("data-panel") && (g++, S.hasAttribute("data-disabled") || (m++, d === -1 && (d = g), p = g));
  }
  if (n || m > 1) {
    let g = -1;
    for (const S of c)
      if (S.hasAttribute("data-panel")) {
        g++;
        const z = i.find(
          (b) => b.element === S
        );
        if (z) {
          if (f) {
            const b = f.element.getBoundingClientRect(), R = S.getBoundingClientRect();
            let O;
            if (l) {
              const A = r === "horizontal" ? new DOMRect(
                b.right,
                b.top,
                0,
                b.height
              ) : new DOMRect(
                b.left,
                b.bottom,
                b.width,
                0
              ), x = r === "horizontal" ? new DOMRect(R.left, R.top, 0, R.height) : new DOMRect(R.left, R.top, R.width, 0);
              switch (y.length) {
                case 0: {
                  O = [
                    A,
                    x
                  ];
                  break;
                }
                case 1: {
                  const w = y[0], v = Un({
                    orientation: r,
                    rects: [b, R],
                    targetRect: w.element.getBoundingClientRect()
                  });
                  O = [
                    w,
                    v === b ? x : A
                  ];
                  break;
                }
                default: {
                  O = y;
                  break;
                }
              }
            } else
              y.length ? O = y : O = [
                r === "horizontal" ? new DOMRect(
                  b.right,
                  R.top,
                  R.left - b.right,
                  R.height
                ) : new DOMRect(
                  R.left,
                  b.bottom,
                  R.width,
                  R.top - b.bottom
                )
              ];
            for (const A of O) {
              const x = ut({
                expandHitTargets: e,
                axis: t,
                rect: "width" in A ? A : A.element.getBoundingClientRect()
              }), w = g <= d || g > p;
              (n || !u && !w) && (h ??= Pe({ axis: t }), s.push({
                axis: t,
                axisSize: h,
                items: [f, z],
                separator: "width" in A ? void 0 : A,
                rect: x
              })), u = !1;
            }
          }
          l = !1, f = z, y = [];
        }
      } else if (S.hasAttribute("data-separator")) {
        S.ariaDisabled !== null && (u = !0);
        const z = a.find(
          (b) => b.element === S
        );
        z ? y.push(z) : (f = void 0, y = []);
      } else
        l = !0;
  }
  return s;
}
function Wn(e, t) {
  const n = getComputedStyle(e), o = parseFloat(n.fontSize);
  return t * o;
}
function Yn(e, t) {
  const n = getComputedStyle(e.ownerDocument.documentElement), o = parseFloat(n.fontSize);
  return t * o;
}
function Xn(e) {
  return e / 100 * window.innerHeight;
}
function Kn(e) {
  return e / 100 * window.innerWidth;
}
function Le({
  axisSize: e,
  itemElement: t,
  styleProp: n
}) {
  let o;
  const [r, i] = cn(n);
  switch (i) {
    case "%": {
      o = r / 100 * e;
      break;
    }
    case "px": {
      o = r;
      break;
    }
    case "rem": {
      o = Yn(t, r);
      break;
    }
    case "em": {
      o = Wn(t, r);
      break;
    }
    case "vh": {
      o = Xn(r);
      break;
    }
    case "vw": {
      o = Kn(r);
      break;
    }
  }
  return o;
}
function J(e) {
  return parseFloat(e.toFixed(3));
}
function ft(e) {
  const { items: t } = e, n = Pe({ axis: e });
  return n === 0 ? t.map((o) => ({
    groupResizeBehavior: o.constraintProps.groupResizeBehavior,
    collapsedSize: 0,
    collapsible: o.constraintProps.collapsible === !0,
    defaultSize: void 0,
    disabled: o.constraintProps.disabled,
    minSize: 0,
    maxSize: 100,
    itemId: o.id
  })) : t.map((o) => {
    const { element: r, constraintProps: i } = o;
    let a = 0;
    if (i.collapsedSize !== void 0) {
      const d = Le({
        axisSize: n,
        itemElement: r,
        styleProp: i.collapsedSize
      });
      a = J(d / n * 100);
    }
    let c;
    if (i.collapsedThreshold !== void 0) {
      const d = Le({
        axisSize: n,
        itemElement: r,
        styleProp: i.collapsedThreshold
      });
      c = J(d / n * 100);
    }
    let s;
    if (i.defaultSize !== void 0) {
      const d = Le({
        axisSize: n,
        itemElement: r,
        styleProp: i.defaultSize
      });
      s = J(d / n * 100);
    }
    let u = 0;
    if (i.minSize !== void 0) {
      const d = Le({
        axisSize: n,
        itemElement: r,
        styleProp: i.minSize
      });
      u = J(d / n * 100);
    }
    let l = 100;
    if (i.maxSize !== void 0) {
      const d = Le({
        axisSize: n,
        itemElement: r,
        styleProp: i.maxSize
      });
      l = J(d / n * 100);
    }
    return {
      groupResizeBehavior: i.groupResizeBehavior,
      collapsedSize: a,
      collapsedThreshold: c,
      collapsible: i.collapsible === !0,
      defaultSize: s,
      disabled: i.disabled,
      minSize: u,
      maxSize: l,
      itemId: o.id
    };
  });
}
let de = /* @__PURE__ */ new Map();
const vt = new ln();
let Fe = 0;
const Je = [];
let Ze;
function nt() {
  Fe++;
}
function bt() {
  for (let e = 0; e < Je.length; e++)
    try {
      vt.emit("axisChange", Je[e]);
    } catch (t) {
      Ze ??= { error: t };
    }
  Je.length = 0;
}
function ot() {
  if (Fe === 1 && bt(), Fe--, Fe === 0 && Ze) {
    const { error: e } = Ze;
    throw Ze = void 0, e;
  }
}
function Jn(e) {
  de = new Map(de), de.delete(e);
}
function Re(e, t) {
  for (const [n] of de)
    if (n.id === e)
      return n;
}
function ce(e, t) {
  for (const [n, o] of de)
    if (n.id === e)
      return o;
  if (t)
    throw Error(`Could not find data for Group with id ${e}`);
}
function ye() {
  return de;
}
function Be(e, t) {
  return vt.addListener("axisChange", (n) => {
    n.axis.id === e && t(n);
  });
}
function me(e, t, n) {
  const o = de.get(e);
  de = new Map(de), de.set(e, t);
  const r = {
    axis: e,
    isUserInteraction: n?.isUserInteraction === !0,
    prev: o,
    next: t
  };
  Fe > 0 ? Je.push(r) : vt.emit("axisChange", r);
}
function hn(e, { pointerId: t, pointerType: n }) {
  return t === e.pointerId || // There is only one pen, but it may be assigned a new pointerId each time it comes into range
  n === "pen" && e.pointerType === "pen";
}
function rt(e, t, n = {}) {
  return e.ownerDocument === t && (n.pointerId === void 0 || hn(e, n));
}
function Zn(e, t) {
  if (e.length !== t.length)
    return !1;
  for (let n = 0; n < e.length; n++)
    if (e[n] != t[n])
      return !1;
  return !0;
}
function W(e, t, n = 0) {
  return Math.abs(J(e) - J(t)) <= n;
}
function ue(e, t) {
  return W(e, t) ? 0 : e > t ? 1 : -1;
}
function Ee({
  overrideDisabledItems: e,
  itemConstraints: t,
  prevSize: n,
  size: o
}) {
  const {
    collapsedSize: r = 0,
    collapsedThreshold: i,
    collapsible: a,
    disabled: c,
    maxSize: s = 100,
    minSize: u = 0
  } = t;
  if (c && !e)
    return n;
  if (ue(o, u) < 0)
    if (a) {
      const l = i ?? (u - r) / 2, d = ue(n, r) <= 0, h = d ? r + l : u - l, p = ue(o, h);
      ue(o, r) <= 0 || p < 0 || i !== void 0 && d && p === 0 ? o = r : o = u;
    } else
      o = u;
  return o = Math.min(s, o), o = J(o), o;
}
function qe({
  delta: e,
  initialLayout: t,
  itemConstraints: n,
  pivotIndices: o,
  prevLayout: r,
  trigger: i
}) {
  if (W(e, 0))
    return t;
  const a = i === "imperative-api", c = n.map(
    ({ itemId: m }) => t[m]
  ), s = n.map(
    ({ itemId: m }) => r[m]
  ), u = [...c], [l, d] = o;
  N(l != null, "Invalid first pivot index"), N(d != null, "Invalid second pivot index");
  let h = 0;
  switch (i) {
    case "keyboard": {
      {
        const m = e < 0 ? d : l, f = n[m];
        N(
          f,
          `Panel constraints not found for index ${m}`
        );
        const {
          collapsedSize: y = 0,
          collapsible: g,
          minSize: S = 0
        } = f;
        if (g) {
          const z = c[m];
          if (N(
            z != null,
            `Previous layout not found for panel index ${m}`
          ), W(z, y)) {
            const b = S - z;
            ue(b, Math.abs(e)) > 0 && (e = e < 0 ? 0 - b : b);
          }
        }
      }
      {
        const m = e < 0 ? l : d, f = n[m];
        N(
          f,
          `No panel constraints found for index ${m}`
        );
        const {
          collapsedSize: y = 0,
          collapsible: g,
          minSize: S = 0
        } = f;
        if (g) {
          const z = c[m];
          if (N(
            z != null,
            `Previous layout not found for panel index ${m}`
          ), W(z, S)) {
            const b = z - y;
            ue(b, Math.abs(e)) > 0 && (e = e < 0 ? 0 - b : b);
          }
        }
      }
      break;
    }
    default: {
      const m = e < 0 ? d : l, f = n[m];
      N(
        f,
        `Panel constraints not found for index ${m}`
      );
      const y = c[m], { collapsedSize: g, collapsedThreshold: S, collapsible: z, minSize: b } = f;
      if (z && ue(y, b) < 0) {
        const R = b - g, O = S ?? R / 2, A = y + Math.abs(e);
        if (ue(A, b) < 0) {
          const x = ue(Math.abs(e), O), w = S === void 0 && e < 0;
          x > 0 || x === 0 && w ? e = e < 0 ? -R : R : e = 0;
        }
      }
      break;
    }
  }
  {
    const m = e < 0 ? 1 : -1;
    let f = e < 0 ? d : l, y = 0;
    for (; ; ) {
      const S = c[f];
      N(
        S != null,
        `Previous layout not found for panel index ${f}`
      );
      const b = Ee({
        overrideDisabledItems: a,
        itemConstraints: n[f],
        prevSize: S,
        size: 100
      }) - S;
      if (y += b, f += m, f < 0 || f >= n.length)
        break;
    }
    const g = Math.min(Math.abs(e), Math.abs(y));
    e = e < 0 ? 0 - g : g;
  }
  {
    let f = e < 0 ? l : d;
    for (; f >= 0 && f < n.length; ) {
      const y = Math.abs(e) - Math.abs(h), g = c[f];
      N(
        g != null,
        `Previous layout not found for panel index ${f}`
      );
      const S = g - y, z = Ee({
        overrideDisabledItems: a,
        itemConstraints: n[f],
        prevSize: g,
        size: S
      });
      if (!W(g, z) && (h += g - z, u[f] = z, h.toFixed(3).localeCompare(Math.abs(e).toFixed(3), void 0, {
        numeric: !0
      }) >= 0))
        break;
      e < 0 ? f-- : f++;
    }
  }
  if (Zn(s, u))
    return r;
  {
    const m = e < 0 ? d : l, f = c[m];
    N(
      f != null,
      `Previous layout not found for panel index ${m}`
    );
    const y = f + h, g = Ee({
      overrideDisabledItems: a,
      itemConstraints: n[m],
      prevSize: f,
      size: y
    });
    if (u[m] = g, !W(g, y)) {
      let S = y - g, b = e < 0 ? d : l;
      for (; b >= 0 && b < n.length; ) {
        const R = u[b];
        N(
          R != null,
          `Previous layout not found for panel index ${b}`
        );
        const O = R + S, A = Ee({
          overrideDisabledItems: a,
          itemConstraints: n[b],
          prevSize: R,
          size: O
        });
        if (W(R, A) || (S -= A - R, u[b] = A), W(S, 0))
          break;
        e > 0 ? b-- : b++;
      }
    }
  }
  const p = Object.values(u).reduce(
    (m, f) => f + m,
    0
  );
  return W(p, 100, 0.1) ? u.reduce((m, f, y) => (m[n[y].itemId] = f, m), {}) : r;
}
function se(e, t) {
  if (Object.keys(e).length !== Object.keys(t).length)
    return !1;
  for (const n in e)
    if (t[n] === void 0 || ue(e[n], t[n]) !== 0)
      return !1;
  return !0;
}
function xt(e) {
  nt();
  try {
    Qn(e);
  } finally {
    ot();
  }
}
function Qn({
  commit: e,
  event: t,
  hitRegions: n,
  initialLayoutMap: o,
  mountedAxes: r,
  pointerDownAtPoint: i,
  prevCursorFlags: a
}) {
  let c = 0;
  const s = ie();
  let u = s.state === "active" ? s.previews : [];
  const l = new Map(
    s.state === "active" ? s.previewLayoutMap : void 0
  );
  n.forEach((p) => {
    const { axis: m, axisSize: f } = p, { orientation: y, items: g } = m;
    if (e && m.resizePreviewMode !== "separator")
      return;
    const { disableCursor: S } = m.mutableState;
    let z = 0;
    i ? y === "horizontal" ? z = (t.clientX - i.x) / f * 100 : z = (t.clientY - i.y) / f * 100 : y === "horizontal" ? z = t.clientX < 0 ? -100 : 100 : z = t.clientY < 0 ? -100 : 100;
    const b = o.get(m), R = r.get(m);
    if (!b || !R)
      return;
    const {
      defaultLayoutDeferred: O,
      derivedItemConstraints: A,
      axisSize: x,
      layout: w,
      separatorToItems: v
    } = R;
    if (A && w && v) {
      const M = m.resizePreviewMode === "separator" ? l.get(m) ?? w : w, k = qe({
        delta: z,
        initialLayout: b,
        itemConstraints: A,
        pivotIndices: p.items.map((P) => g.indexOf(P)),
        prevLayout: M,
        trigger: "mouse-or-touch"
      });
      if (m.resizePreviewMode === "separator" && !e && !se(k, M)) {
        l.set(m, k);
        let P = 0;
        const $ = g.map((C) => (P += k[C.id] - b[C.id], P * (f / 100)));
        u = u.map((C) => {
          if (C.axis !== m)
            return C;
          const I = $[C.itemIndex];
          return I === C.offset ? C : { ...C, offset: I };
        });
      }
      if (se(k, M) && z !== 0 && !S)
        switch (y) {
          case "horizontal": {
            c |= z < 0 ? un : dn;
            break;
          }
          case "vertical": {
            c |= z < 0 ? fn : mn;
            break;
          }
        }
      (m.resizePreviewMode !== "separator" || e) && !se(k, w) && me(p.axis, {
        defaultLayoutDeferred: O,
        derivedItemConstraints: A,
        axisSize: x,
        layout: k,
        requestedAxisSize: x,
        requestedLayout: k,
        separatorToItems: v
      });
    }
  });
  let d = 0;
  t.movementX === 0 ? d |= a & Rt : d |= c & Rt, t.movementY === 0 ? d |= a & Et : d |= c & Et;
  const h = s.state === "active" && (t.clientX !== s.pointerDownAtPoint.x || t.clientY !== s.pointerDownAtPoint.y);
  Gn(d, u, l, h);
}
function gn(e, t) {
  const n = ie();
  if (n.state !== "active" || !rt(n, e, t))
    return;
  const o = ye();
  nt();
  try {
    xt({
      commit: !0,
      event: t,
      hitRegions: n.hitRegions,
      initialLayoutMap: n.initialLayoutMap,
      mountedAxes: o,
      pointerDownAtPoint: n.pointerDownAtPoint,
      prevCursorFlags: n.cursorFlags
    }), bt(), fe({
      cursorFlags: 0,
      state: "inactive"
    }), n.hitRegions.length > 0 && (t.preventDefault?.(), n.hitRegions.forEach((r) => {
      if (!o.has(r.axis))
        return;
      const i = ce(r.axis.id, !0);
      me(r.axis, i, {
        isUserInteraction: !0
      });
    }));
  } finally {
    ot();
  }
}
function kt(e) {
  if (e.defaultPrevented)
    return;
  const { clientX: t, clientY: n, movementX: o, movementY: r } = e;
  gn(e.currentTarget, {
    clientX: t,
    clientY: n,
    movementX: o,
    movementY: r
  });
}
function eo(e, t, n) {
  let o, r = {
    x: 1 / 0,
    y: 1 / 0
  };
  for (const i of t) {
    const a = pn(n, i.rect);
    switch (e) {
      case "horizontal": {
        (a.x < r.x || a.x === r.x && a.y <= r.y) && (o = i, r = a);
        break;
      }
      case "vertical": {
        (a.y < r.y || a.y === r.y && a.x <= r.x) && (o = i, r = a);
        break;
      }
    }
  }
  return o ? {
    distance: r,
    hitRegion: o
  } : void 0;
}
function to(e) {
  return e !== null && typeof e == "object" && "nodeType" in e && e.nodeType === Node.DOCUMENT_FRAGMENT_NODE;
}
function no(e, t) {
  if (e === t) throw new Error("Cannot compare node with itself");
  const n = {
    a: Ot(e),
    b: Ot(t)
  };
  let o;
  for (; n.a.at(-1) === n.b.at(-1); )
    o = n.a.pop(), n.b.pop();
  N(
    o,
    "Stacking order can only be calculated for elements with a common ancestor"
  );
  const r = {
    a: $t(At(n.a)),
    b: $t(At(n.b))
  };
  if (r.a === r.b) {
    const i = o.childNodes, a = {
      a: n.a.at(-1),
      b: n.b.at(-1)
    };
    let c = i.length;
    for (; c--; ) {
      const s = i[c];
      if (s === a.a) return 1;
      if (s === a.b) return -1;
    }
  }
  return Math.sign(r.a - r.b);
}
const oo = /\b(?:position|zIndex|opacity|transform|webkitTransform|mixBlendMode|filter|webkitFilter|isolation)\b/;
function ro(e) {
  const t = getComputedStyle(yn(e) ?? e).display;
  return t === "flex" || t === "inline-flex";
}
function io(e) {
  const t = getComputedStyle(e);
  return !!(t.position === "fixed" || t.zIndex !== "auto" && (t.position !== "static" || ro(e)) || +t.opacity < 1 || "transform" in t && t.transform !== "none" || "webkitTransform" in t && t.webkitTransform !== "none" || "mixBlendMode" in t && t.mixBlendMode !== "normal" || "filter" in t && t.filter !== "none" || "webkitFilter" in t && t.webkitFilter !== "none" || "isolation" in t && t.isolation === "isolate" || oo.test(t.willChange) || t.webkitOverflowScrolling === "touch");
}
function At(e) {
  let t = e.length;
  for (; t--; ) {
    const n = e[t];
    if (N(n, "Missing node"), io(n)) return n;
  }
  return null;
}
function $t(e) {
  return e && Number(getComputedStyle(e).zIndex) || 0;
}
function Ot(e) {
  const t = [];
  for (; e; )
    t.push(e), e = yn(e);
  return t;
}
function yn(e) {
  const { parentNode: t } = e;
  return to(t) ? t.host : t;
}
function so(e, t) {
  return e.x < t.x + t.width && e.x + e.width > t.x && e.y < t.y + t.height && e.y + e.height > t.y;
}
function ao(e) {
  try {
    return e.matches(":modal");
  } catch {
    return !1;
  }
}
function co({
  axisElement: e,
  hitRegion: t,
  pointerEventTarget: n
}) {
  if (dt(n)) {
    const o = n.closest("dialog");
    if (o && !o.contains(e) && ao(o))
      return !1;
  }
  if (!dt(n) || n.contains(e) || e.contains(n))
    return !0;
  if (no(n, e) > 0) {
    let o = n;
    for (; o; ) {
      if (o.contains(e))
        return !0;
      if (so(o.getBoundingClientRect(), t))
        return !1;
      o = o.parentElement;
    }
  }
  return !0;
}
function wt(e, t, n) {
  const o = [];
  return t.forEach((r, i) => {
    if (i.disabled || i.element.ownerDocument !== n)
      return;
    const a = St({ axis: i }), c = eo(i.orientation, a, {
      x: e.clientX,
      y: e.clientY
    });
    c && c.distance.x <= 0 && c.distance.y <= 0 && co({
      axisElement: i.element,
      hitRegion: c.hitRegion.rect,
      pointerEventTarget: e.target
    }) && o.push(c.hitRegion);
  }), o;
}
function ve({
  layout: e,
  itemConstraints: t
}) {
  const n = t.map(({ itemId: a }) => e[a]), o = [...n], r = o.reduce(
    (a, c) => a + c,
    0
  );
  if (Object.keys(e).length !== t.length)
    throw Error(
      `Invalid ${t.length} panel layout: ${Object.values(e).map((a) => `${a}%`).join(", ")}`
    );
  if (!W(r, 100) && o.length > 0)
    for (let a = 0; a < t.length; a++) {
      const c = o[a];
      N(c != null, `No layout data found for index ${a}`);
      const s = 100 / r * c;
      o[a] = s;
    }
  let i = 0;
  for (let a = 0; a < t.length; a++) {
    const c = n[a];
    N(c != null, `No layout data found for index ${a}`);
    const s = o[a];
    N(s != null, `No layout data found for index ${a}`);
    const u = Ee({
      overrideDisabledItems: !0,
      itemConstraints: t[a],
      prevSize: c,
      size: s
    });
    s != u && (i += s - u, o[a] = u);
  }
  if (!W(i, 0))
    for (let a = 0; a < t.length; a++) {
      const c = o[a];
      N(c != null, `No layout data found for index ${a}`);
      const s = c + i, u = Ee({
        overrideDisabledItems: !0,
        itemConstraints: t[a],
        prevSize: c,
        size: s
      });
      if (c !== u && (i -= u - c, o[a] = u, W(i, 0)))
        break;
    }
  return o.reduce((a, c, s) => (a[t[s].itemId] = c, a), {});
}
function zt({
  axisId: e,
  itemId: t
}) {
  const n = () => {
    const s = ye();
    for (const [
      u,
      {
        defaultLayoutDeferred: l,
        derivedItemConstraints: d,
        layout: h,
        axisSize: p,
        separatorToItems: m
      }
    ] of s)
      if (u.id === e)
        return {
          defaultLayoutDeferred: l,
          derivedItemConstraints: d,
          axis: u,
          axisSize: p,
          layout: h,
          separatorToItems: m
        };
    throw Error(`Group ${e} not found`);
  }, o = () => {
    const s = n().derivedItemConstraints.find(
      (u) => u.itemId === t
    );
    if (s !== void 0)
      return s;
    throw Error(`Panel constraints not found for Panel ${t}`);
  }, r = () => {
    const s = n().axis.items.find((u) => u.id === t);
    if (s !== void 0)
      return s;
    throw Error(`Layout not found for Panel ${t}`);
  }, i = () => {
    const s = n().layout[t];
    if (s !== void 0)
      return s;
    throw Error(`Layout not found for Panel ${t}`);
  }, a = ({
    nextSize: s,
    items: u,
    prevLayout: l,
    derivedItemConstraints: d
  }) => {
    const h = i(), p = u.findIndex((g) => g.id === t), m = p === 0, f = p === u.length - 1;
    if (f && s < h && (m || u.slice(0, p).every((g, S) => {
      const z = d[S];
      return z?.collapsible && W(z.collapsedSize, l[z.itemId]);
    }))) {
      const g = u.slice(0, p).reduce((S, z) => S + l[z.id], 0);
      return {
        ...l,
        [t]: J(100 - g)
      };
    }
    return qe({
      delta: f ? h - s : s - h,
      initialLayout: l,
      itemConstraints: d,
      pivotIndices: f ? [p - 1, p] : [p, p + 1],
      prevLayout: l,
      trigger: "imperative-api"
    });
  }, c = (s) => {
    const u = i();
    if (s === u)
      return;
    const {
      defaultLayoutDeferred: l,
      derivedItemConstraints: d,
      axis: h,
      axisSize: p,
      layout: m,
      separatorToItems: f
    } = n(), y = a({
      nextSize: s,
      items: h.items,
      prevLayout: m,
      derivedItemConstraints: d
    }), g = ve({
      layout: y,
      itemConstraints: d
    });
    se(m, g) || me(h, {
      defaultLayoutDeferred: l,
      derivedItemConstraints: d,
      axisSize: p,
      layout: g,
      requestedAxisSize: p,
      requestedLayout: g,
      separatorToItems: f
    });
  };
  return {
    collapse: () => {
      const { collapsible: s, collapsedSize: u } = o(), { mutableValues: l } = r(), d = i();
      s && d !== u && (l.expandToSize = d, c(u));
    },
    expand: () => {
      const { collapsible: s, collapsedSize: u, minSize: l } = o(), { mutableValues: d } = r(), h = i();
      if (s && h === u) {
        let p = d.expandToSize ?? l;
        p === 0 && (p = 1), c(p);
      }
    },
    getSize: () => {
      const { axis: s } = n(), u = i(), { element: l } = r(), d = s.layoutStrategy ? s.layoutStrategy.getItemSizeInPixels(t) : s.orientation === "horizontal" ? l.offsetWidth : l.offsetHeight;
      return {
        asPercentage: u,
        inPixels: d
      };
    },
    isCollapsed: () => {
      const { collapsible: s, collapsedSize: u } = o(), l = i();
      return s && W(u, l);
    },
    resize: (s) => {
      const { axis: u } = n(), { element: l } = r(), d = Pe({ axis: u }), h = Le({
        axisSize: d,
        itemElement: l,
        styleProp: s
      }), p = J(h / d * 100);
      c(p);
    }
  };
}
function Nt(e) {
  if (e.defaultPrevented)
    return;
  const t = ye();
  wt(
    e,
    t,
    e.currentTarget
  ).forEach((o) => {
    if (o.separator && !o.separator.disableDoubleClick) {
      const r = o.items.find(
        (i) => i.constraintProps.defaultSize !== void 0
      );
      if (r) {
        const i = r.constraintProps.defaultSize, a = zt({
          axisId: o.axis.id,
          itemId: r.id
        });
        a && i !== void 0 && (a.resize(i), e.preventDefault());
      }
    }
  });
}
function Sn(e) {
  const t = ye();
  for (const [n] of t)
    if (n.separators.some(
      (o) => o.element === e
    ))
      return n;
  throw Error("Could not find parent Group for separator element");
}
function _e({
  axisId: e
}) {
  const t = () => {
    const n = ye();
    for (const [o, r] of n)
      if (o.id === e)
        return { axis: o, ...r };
    throw Error(`Could not find Group with id "${e}"`);
  };
  return {
    getLayout() {
      const { defaultLayoutDeferred: n, layout: o } = t();
      return n ? {} : o;
    },
    setLayout(n) {
      const {
        defaultLayoutDeferred: o,
        derivedItemConstraints: r,
        axis: i,
        axisSize: a,
        layout: c,
        separatorToItems: s
      } = t(), u = ve({
        layout: n,
        itemConstraints: r
      });
      return o ? c : (se(c, u) || me(i, {
        defaultLayoutDeferred: o,
        derivedItemConstraints: r,
        axisSize: a,
        layout: u,
        requestedAxisSize: a,
        requestedLayout: u,
        separatorToItems: s
      }), u);
    }
  };
}
function xe(e, t) {
  const n = Sn(e), o = ce(n.id, !0), r = n.separators.find(
    (d) => d.element === e
  );
  N(r, "Matching separator not found");
  const i = o.separatorToItems.get(r);
  N(i, "Matching panels not found");
  const a = i.map((d) => n.items.indexOf(d)), s = _e({ axisId: n.id }).getLayout(), u = qe({
    delta: t,
    initialLayout: s,
    itemConstraints: o.derivedItemConstraints,
    pivotIndices: a,
    prevLayout: s,
    trigger: "keyboard"
  }), l = ve({
    layout: u,
    itemConstraints: o.derivedItemConstraints
  });
  se(s, l) || me(
    n,
    {
      defaultLayoutDeferred: o.defaultLayoutDeferred,
      derivedItemConstraints: o.derivedItemConstraints,
      axisSize: o.axisSize,
      layout: l,
      requestedAxisSize: o.axisSize,
      requestedLayout: l,
      separatorToItems: o.separatorToItems
    },
    // Keyboard resizes (arrow keys, Home/End, Enter collapse/expand) originate
    // from a real DOM event on the separator, so they are user interactions
    // just like pointer drags. This function is only reached from
    // onDocumentKeyDown. See #716.
    { isUserInteraction: !0 }
  );
}
function Gt(e) {
  if (e.defaultPrevented)
    return;
  const t = e.currentTarget, n = Sn(t);
  if (!(n.disabled || n.separators.find(
    (r) => r.element === t
  )?.disabled))
    switch (e.key) {
      case "ArrowDown": {
        e.preventDefault(), n.orientation === "vertical" && xe(t, 5);
        break;
      }
      case "ArrowLeft": {
        e.preventDefault(), n.orientation === "horizontal" && xe(t, -5);
        break;
      }
      case "ArrowRight": {
        e.preventDefault(), n.orientation === "horizontal" && xe(t, 5);
        break;
      }
      case "ArrowUp": {
        e.preventDefault(), n.orientation === "vertical" && xe(t, -5);
        break;
      }
      case "End": {
        e.preventDefault(), xe(t, 100);
        break;
      }
      case "Enter": {
        e.preventDefault();
        const r = ce(n.id, !0), { derivedItemConstraints: i, layout: a, separatorToItems: c } = r, s = n.separators.find(
          (h) => h.element === t
        );
        N(s, "Matching separator not found");
        const u = c.get(s);
        N(u, "Matching panels not found");
        const l = u[0], d = i.find(
          (h) => h.itemId === l.id
        );
        if (N(d, "Panel metadata not found"), d.collapsible) {
          const h = a[l.id], p = d.collapsedSize === h ? n.mutableState.expandedItemSizes[l.id] ?? d.minSize : d.collapsedSize;
          xe(t, p - h);
        }
        break;
      }
      case "F6": {
        e.preventDefault();
        const r = n.separators.map(
          (s) => s.element
        ), i = Array.from(r).findIndex(
          (s) => s === e.currentTarget
        );
        N(i !== null, "Index not found");
        const a = e.shiftKey ? i > 0 ? i - 1 : r.length - 1 : i + 1 < r.length ? i + 1 : 0;
        r[a].focus({
          preventScroll: !0
        });
        break;
      }
      case "Home": {
        e.preventDefault(), xe(t, -100);
        break;
      }
    }
}
function De(e, t) {
  const n = ie();
  if (n.state !== "active" || !rt(n, e, t))
    return !1;
  const o = ye();
  nt();
  try {
    n.previewLayoutMap.forEach((r, i) => {
      const a = o.get(i);
      i.resizePreviewMode === "separator" && a && !se(r, a.layout) && me(i, {
        ...a,
        layout: r,
        requestedAxisSize: a.axisSize,
        requestedLayout: r
      });
    }), bt(), fe({
      cursorFlags: 0,
      state: "inactive"
    }), n.hitRegions.forEach((r) => {
      if (!o.has(r.axis))
        return;
      const i = ce(r.axis.id, !0);
      me(r.axis, i, {
        isUserInteraction: !0
      });
    });
  } finally {
    ot();
  }
  return !0;
}
function Ft(e) {
  const t = ie();
  if (t.state !== "active")
    return;
  const n = t.hitRegions.flatMap(
    ({ separator: o }) => o ? [o.element] : []
  );
  !n.some((o) => o === e.target) || n.some(
    (o) => o.hasPointerCapture?.(e.pointerId)
  ) || De(e.currentTarget, e);
}
function _t(e) {
  De(e.currentTarget, e);
}
function lo(e, t) {
  const { element: n, orientation: o, items: r } = e, i = n.getBoundingClientRect(), a = o === "horizontal";
  return St({
    expandHitTargets: !1,
    axis: e,
    includeDisabled: !0
  }).map(({ items: s, rect: u, separator: l }, d) => {
    const h = r.indexOf(s[0]), p = a ? u.left + u.width / 2 : u.top + u.height / 2;
    return {
      active: t.some((f) => {
        if (f.axis !== e || f.items[0] !== s[0])
          return !1;
        if (l || f.separator)
          return f.separator === l;
        const y = a ? f.rect.left + f.rect.width / 2 : f.rect.top + f.rect.height / 2;
        return W(p, y);
      }),
      axis: e,
      key: l ? `separator-${l.id}` : `panel-${s[0].id}-${d}`,
      offset: 0,
      itemIndex: h,
      rect: new DOMRect(
        (a && !l ? p : u.left) - i.left - n.clientLeft + n.scrollLeft,
        (!a && !l ? p : u.top) - i.top - n.clientTop + n.scrollTop,
        a && !l ? 0 : u.width,
        !a && !l ? 0 : u.height
      ),
      separator: l
    };
  });
}
function Bt(e) {
  if (e.defaultPrevented)
    return;
  if (e.pointerType === "mouse" && e.button > 0)
    return;
  const t = ie();
  if (t.state === "active") {
    hn(t, e) && De(
      t.ownerDocument,
      t
    );
    return;
  }
  const n = ye(), o = wt(
    e,
    n,
    e.currentTarget
  );
  if (o.length === 0)
    return;
  const r = /* @__PURE__ */ new Map();
  let i = !1;
  o.forEach((c) => {
    c.separator && (i || (i = !0, c.separator.element.focus({
      // @ts-expect-error https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus#browser_compatibility
      focusVisible: !1,
      preventScroll: !0
    })));
    const s = n.get(c.axis);
    s && r.set(c.axis, s.layout);
  });
  const a = Array.from(r.keys()).flatMap(
    (c) => c.resizePreviewMode === "separator" ? lo(c, o) : []
  );
  fe({
    cursorFlags: 0,
    didPointerMove: !1,
    hitRegions: o,
    initialLayoutMap: r,
    ownerDocument: e.currentTarget,
    pointerDownAtPoint: { x: e.clientX, y: e.clientY },
    pointerId: e.pointerId,
    pointerType: e.pointerType,
    previewLayoutMap: new Map(r),
    previews: a,
    state: "active"
  }), e.preventDefault();
}
function qt(e) {
  const t = e.currentTarget, n = ye(), o = ie();
  switch (o.state) {
    case "active": {
      if (!rt(o, t, e))
        return;
      xt({
        commit: !1,
        event: e,
        hitRegions: o.hitRegions,
        initialLayoutMap: o.initialLayoutMap,
        mountedAxes: n,
        prevCursorFlags: o.cursorFlags
      });
    }
  }
}
function Ht(e) {
  if (e.defaultPrevented)
    return;
  const t = e.currentTarget, n = ie(), o = ye();
  switch (n.state) {
    case "active": {
      if (!rt(n, t, e))
        return;
      if (
        // Skip this check for "pointerleave" events, else Firefox triggers a false positive (see #514)
        e.buttons === 0
      ) {
        De(t, e);
        return;
      }
      for (const r of n.hitRegions)
        if (r.separator) {
          const { element: i } = r.separator;
          i.isConnected && !i.hasPointerCapture?.(e.pointerId) && i.setPointerCapture?.(e.pointerId);
        }
      xt({
        commit: !1,
        event: e,
        hitRegions: n.hitRegions,
        initialLayoutMap: n.initialLayoutMap,
        mountedAxes: o,
        pointerDownAtPoint: n.pointerDownAtPoint,
        prevCursorFlags: n.cursorFlags
      });
      break;
    }
    default: {
      const r = wt(
        e,
        o,
        t
      );
      r.length === 0 ? n.state !== "inactive" && fe({
        cursorFlags: 0,
        state: "inactive"
      }) : fe({
        cursorFlags: 0,
        hitRegions: r,
        ownerDocument: t,
        state: "hover"
      });
      break;
    }
  }
}
function Vt(e) {
  if (e.relatedTarget instanceof HTMLIFrameElement) {
    const t = ie();
    switch (t.state) {
      case "hover":
        t.ownerDocument === e.currentTarget && fe({
          cursorFlags: 0,
          state: "inactive"
        });
    }
  }
}
function jt(e) {
  e.defaultPrevented || e.pointerType === "mouse" && e.button > 0 || gn(e.currentTarget, e);
}
function Ut(e) {
  e.target === e.currentTarget && De(e.currentTarget.document);
}
function Wt(e) {
  De(e.currentTarget.document);
}
function uo(e) {
  let t = 0, n = 0;
  const o = {};
  for (const i of e)
    if (i.defaultSize !== void 0) {
      t++;
      const a = J(i.defaultSize);
      n += a, o[i.itemId] = a;
    } else
      o[i.itemId] = void 0;
  const r = e.length - t;
  if (r !== 0) {
    const i = J((100 - n) / r);
    for (const a of e)
      a.defaultSize === void 0 && (o[a.itemId] = i);
  }
  return o;
}
function fo(e, t) {
  const n = e.map((r) => r.id), o = Object.keys(t);
  if (n.length !== o.length)
    return !1;
  for (const r of n)
    if (!o.includes(r))
      return !1;
  return !0;
}
function Yt({
  axis: e,
  itemConstraints: t
}) {
  const n = e.items.map(({ id: r }) => r).join(","), o = e.mutableState.defaultLayout;
  return e.mutableState.layouts[n] ?? (o && fo(e.items, o) ? o : uo(t));
}
function Xt({
  itemIds: e,
  layout: t
}) {
  return ve({
    layout: t,
    itemConstraints: e.map((n) => ({
      collapsedSize: 0,
      collapsible: !1,
      defaultSize: void 0,
      disabled: void 0,
      itemId: n,
      maxSize: 100,
      minSize: 0
    }))
  });
}
function mo(e, t, n) {
  if (!n[0])
    return;
  const r = e.items.find((u) => u.element === t);
  if (!r || !r.onResize)
    return;
  const i = Pe({ axis: e }), a = e.orientation === "horizontal" ? r.element.offsetWidth : r.element.offsetHeight, c = r.mutableValues.prevSize, s = {
    asPercentage: J(a / i * 100),
    inPixels: a
  };
  r.mutableValues.prevSize = s, r.onResize(s, r.id, c);
}
function vn(e, t) {
  if (Object.keys(e).length !== Object.keys(t).length)
    return !1;
  for (const o in e)
    if (e[o] !== t[o])
      return !1;
  return !0;
}
function po(e, t) {
  return e.length !== t.length ? !1 : e.every((n, o) => vn(n, t[o]));
}
function ho({
  axis: e,
  nextAxisSize: t,
  prevAxisSize: n,
  prevLayout: o
}) {
  if (n <= 0 || t <= 0 || n === t)
    return o;
  let r = 0, i = 0, a = !1;
  const c = /* @__PURE__ */ new Map(), s = [];
  for (const d of e.items) {
    const h = o[d.id] ?? 0;
    switch (d.constraintProps.groupResizeBehavior) {
      case "preserve-pixel-size": {
        a = !0;
        const p = h / 100 * n, m = J(
          p / t * 100
        );
        c.set(d.id, m), r += m;
        break;
      }
      case "preserve-relative-size":
      default: {
        s.push(d.id), i += h;
        break;
      }
    }
  }
  if (!a || s.length === 0)
    return o;
  const u = 100 - r, l = { ...o };
  if (c.forEach((d, h) => {
    l[h] = d;
  }), i > 0)
    for (const d of s) {
      const h = o[d] ?? 0;
      l[d] = J(
        h / i * u
      );
    }
  else {
    const d = J(u / s.length);
    for (const h of s)
      l[h] = d;
  }
  return l;
}
const Ie = /* @__PURE__ */ new Map();
let Kt = !1;
function bn(e) {
  let t = !0;
  N(
    e.element.ownerDocument.defaultView,
    "Cannot register an unmounted Group"
  );
  const n = e.element.ownerDocument.defaultView.ResizeObserver, o = /* @__PURE__ */ new Set(), r = /* @__PURE__ */ new Set(), i = new n((m) => {
    let f;
    nt();
    try {
      for (const y of m) {
        const { borderBoxSize: g, target: S } = y;
        if (S === e.element) {
          if (t) {
            const z = Pe({ axis: e });
            if (z === 0)
              break;
            const b = ce(e.id);
            if (!b)
              break;
            const R = ft(e);
            let O = b.requestedAxisSize, A = b.requestedLayout;
            b.defaultLayoutDeferred && (O = z, A = Xt({
              itemIds: e.items.map(({ id: v }) => v),
              layout: Yt({
                axis: e,
                itemConstraints: R
              })
            }));
            const x = ho({
              axis: e,
              nextAxisSize: z,
              prevAxisSize: O,
              prevLayout: A
            }), w = ve({
              layout: x,
              itemConstraints: R
            });
            if (!b.defaultLayoutDeferred && se(b.layout, w) && po(
              b.derivedItemConstraints,
              R
            ) && b.axisSize === z)
              continue;
            me(e, {
              defaultLayoutDeferred: !1,
              derivedItemConstraints: R,
              axisSize: z,
              layout: w,
              requestedAxisSize: O,
              requestedLayout: A,
              separatorToItems: b.separatorToItems
            });
          }
        } else
          try {
            mo(e, S, g);
          } catch (z) {
            f ??= { error: z };
          }
      }
    } finally {
      ot();
    }
    if (f)
      throw f.error;
  });
  i.observe(e.element), e.items.forEach((m) => {
    N(
      !o.has(m.id),
      `Panel ids must be unique; id "${m.id}" was used more than once`
    ), o.add(m.id), m.onResize && i.observe(m.element);
  });
  const a = Pe({ axis: e }), c = ft(e), s = Yt({
    axis: e,
    itemConstraints: c
  }), u = ve({
    layout: s,
    itemConstraints: c
  }), l = e.element.ownerDocument, d = l.defaultView;
  Ie.set(
    l,
    (Ie.get(l) ?? 0) + 1
  );
  const h = /* @__PURE__ */ new Map();
  return St({ axis: e, includeDisabled: !0 }).forEach((m) => {
    m.separator && h.set(m.separator, m.items);
  }), me(e, {
    defaultLayoutDeferred: a === 0,
    derivedItemConstraints: c,
    axisSize: a,
    layout: u,
    requestedAxisSize: a,
    requestedLayout: Xt({
      itemIds: e.items.map(({ id: m }) => m),
      layout: s
    }),
    separatorToItems: h
  }), e.separators.forEach((m) => {
    N(
      !r.has(m.id),
      `Separator ids must be unique; id "${m.id}" was used more than once`
    ), r.add(m.id), m.element.addEventListener("keydown", Gt);
  }), Kt || (Kt = !0, gt(Hn)), Ie.get(l) === 1 && (l.addEventListener("contextmenu", kt, !0), l.addEventListener("dblclick", Nt, !0), l.addEventListener(
    "lostpointercapture",
    Ft,
    !0
  ), l.addEventListener(
    "pointercancel",
    _t,
    !0
  ), l.addEventListener("pointerdown", Bt, !0), l.addEventListener("pointerleave", qt), l.addEventListener("pointermove", Ht), l.addEventListener("pointerout", Vt), l.addEventListener("pointerup", jt, !0), d?.addEventListener("blur", Ut), d?.addEventListener("pagehide", Wt)), function() {
    t = !1, Ie.set(
      l,
      Math.max(0, (Ie.get(l) ?? 0) - 1)
    ), Jn(e), _n(e), e.separators.forEach((f) => {
      f.element.removeEventListener("keydown", Gt);
    }), Ie.get(l) || (l.removeEventListener(
      "contextmenu",
      kt,
      !0
    ), l.removeEventListener(
      "dblclick",
      Nt,
      !0
    ), l.removeEventListener(
      "lostpointercapture",
      Ft,
      !0
    ), l.removeEventListener(
      "pointercancel",
      _t,
      !0
    ), l.removeEventListener(
      "pointerdown",
      Bt,
      !0
    ), l.removeEventListener("pointerleave", qt), l.removeEventListener("pointermove", Ht), l.removeEventListener("pointerout", Vt), l.removeEventListener("pointerup", jt, !0), d?.removeEventListener("blur", Ut), d?.removeEventListener("pagehide", Wt)), i.disconnect();
  };
}
function xn({
  derivedItemConstraints: e,
  axis: t,
  layout: n,
  prevLayout: o,
  requestedLayout: r
}) {
  const i = t.items.map(({ id: a }) => a).join(",");
  t.mutableState.layouts[i] = r, o && e.forEach((a) => {
    if (a.collapsible) {
      const c = W(
        a.collapsedSize,
        n[a.itemId]
      ), s = W(
        a.collapsedSize,
        o[a.itemId]
      );
      c && !s && (t.mutableState.expandedItemSizes[a.itemId] = o[a.itemId]);
    }
  });
}
function wn() {
  const [e, t] = ge({}), n = re(() => t({}), []);
  return [e, n];
}
function it(e) {
  const t = B({ ...e });
  return ne(() => {
    for (const n in e)
      t.current[n] = e[n];
  }, [e]), t.current;
}
const It = nn(null);
function go({
  layout: e,
  itemConstraints: t,
  itemId: n,
  itemIndex: o
}) {
  let r, i;
  const a = e[n], c = t.find(
    (s) => s.itemId === n
  );
  if (c) {
    const s = c.maxSize, u = c.collapsible ? c.collapsedSize : c.minSize, l = [o, o + 1];
    i = ve({
      layout: qe({
        delta: u - a,
        initialLayout: e,
        itemConstraints: t,
        pivotIndices: l,
        prevLayout: e
      }),
      itemConstraints: t
    })[n], r = ve({
      layout: qe({
        delta: s - a,
        initialLayout: e,
        itemConstraints: t,
        pivotIndices: l,
        prevLayout: e
      }),
      itemConstraints: t
    })[n];
  }
  return {
    valueControls: n,
    valueMax: r,
    valueMin: i,
    valueNow: a
  };
}
function zn({
  attributes: e,
  axisId: t,
  axisOrientation: n,
  children: o,
  className: r,
  "data-testid": i,
  disableCursor: a,
  disabled: c,
  disableDoubleClick: s,
  elementRef: u,
  id: l,
  isSharedHitRegion: d,
  preview: h,
  registerSeparator: p,
  requiredStyle: m,
  style: f,
  styleDefaults: y,
  tabIndex: g = 0,
  updateSeparatorProps: S
}) {
  const z = it({
    disabled: c,
    disableDoubleClick: s,
    children: o,
    className: r,
    preview: h,
    style: f
  }), [b, R] = ge({}), [O, A] = ge("inactive"), [x, w] = ge(!1), v = B(null), M = B(null), k = Ve(v, u), P = n === "horizontal" ? "vertical" : "horizontal";
  ne(() => {
    const I = v.current;
    if (I !== null) {
      const E = {
        disabled: z.disabled,
        disableDoubleClick: z.disableDoubleClick,
        element: I,
        id: l,
        get children() {
          return z.children;
        },
        get className() {
          return z.className;
        },
        get preview() {
          return z.preview;
        },
        get style() {
          return z.style;
        }
      };
      M.current = E;
      const q = p(E), Z = gt(
        (K) => {
          A(
            K.next.state !== "inactive" && K.next.hitRegions.some(
              (ae) => ae.separator === E || (d?.(ae) ?? !1)
            ) ? K.next.state : "inactive"
          );
        }
      ), X = Be(
        t,
        (K) => {
          const { derivedItemConstraints: ae, layout: we, separatorToItems: ke } = K.next, ze = ke.get(E);
          if (ze) {
            const L = ze[0], T = ae.findIndex(
              (G) => G.itemId === L.id
            ), { layoutStrategy: F } = K.axis;
            R({
              ...go({
                layout: we,
                itemConstraints: ae,
                itemId: L.id,
                itemIndex: T
              }),
              // Items without DOM elements of their own (e.g. Grid tracks) control other elements
              ...F?.getItemAriaControls && {
                valueControls: F.getItemAriaControls(
                  L.id
                )
              }
            });
          }
        }
      );
      return () => {
        M.current = null, Z(), X(), q();
      };
    }
  }, [t, l, d, p, z]), ne(() => {
    const I = M.current;
    I && Fn(I);
  }, [h]), He(() => {
    S(l, { disabled: c, disableDoubleClick: s });
  }, [c, s, l, S]);
  let $;
  c && !a && ($ = "not-allowed");
  let C;
  if (c)
    C = "disabled";
  else
    switch (O) {
      case "active": {
        C = "active";
        break;
      }
      default:
        x ? C = "focus" : C = O;
    }
  return /* @__PURE__ */ Y(
    "div",
    {
      ...e,
      "aria-controls": b.valueControls,
      "aria-disabled": c || void 0,
      "aria-orientation": P,
      "aria-valuemax": b.valueMax,
      "aria-valuemin": b.valueMin,
      "aria-valuenow": b.valueNow,
      children: o,
      className: r,
      "data-separator": C,
      "data-testid": i,
      id: l,
      onBlur: () => w(!1),
      onFocus: () => w(!0),
      ref: k,
      role: "separator",
      style: {
        ...y,
        cursor: $,
        ...f,
        ...m,
        // Inform the browser that the library is handling touch events for this element
        // See github.com/bvaughn/react-resizable-panels/issues/662
        touchAction: "none"
      },
      tabIndex: c ? void 0 : g
    }
  );
}
function Jt({
  axis: e,
  children: t,
  className: n,
  crossSpan: o,
  crossStart: r,
  disabled: i,
  elementRef: a,
  index: c,
  style: s
}) {
  const u = Te(void 0), {
    getDisableCursor: l,
    getResizeAxisId: d,
    gutters: h,
    registerSeparator: p,
    separatorPlacements: m,
    trackCounts: f,
    updateSeparatorProps: y
  } = an(), g = d(e), S = e === "column" ? "row" : "column", z = f[S], b = !!i || !pt(c, f[e]);
  let R = !0;
  for (const v of m.values())
    if (v.axis === e && v.index === c && !v.disabled && v.crossStart < r) {
      R = !1;
      break;
    }
  const O = re(
    (v) => v.axis.id === g && v.axis.items.indexOf(v.items[1]) === c,
    [g, c]
  ), A = re(
    (v) => p(
      {
        axis: e,
        crossSpan: o,
        crossStart: r,
        disabled: !!i,
        index: c
      },
      v
    ),
    [e, o, r, i, c, p]
  ), x = Dn(c), w = kn({
    crossCount: z,
    crossSpan: o,
    crossStart: r,
    hasGutters: h[S]
  });
  return /* @__PURE__ */ Y(
    zn,
    {
      axisId: g,
      axisOrientation: e === "column" ? "horizontal" : "vertical",
      className: n,
      disableCursor: l(),
      disabled: b,
      disableDoubleClick: void 0,
      elementRef: a,
      id: u,
      isSharedHitRegion: O,
      registerSeparator: A,
      requiredStyle: {
        gridColumn: e === "column" ? x : w,
        gridRow: e === "row" ? x : w
      },
      style: s,
      tabIndex: R ? 0 : -1,
      updateSeparatorProps: y,
      children: t
    }
  );
}
function In(e) {
  const { children: t, className: n, disabled: o, elementRef: r, style: i } = e;
  return e.type === "column" ? /* @__PURE__ */ Y(
    Jt,
    {
      axis: "column",
      className: n,
      crossSpan: e.rowSpan,
      crossStart: e.row ?? 0,
      disabled: o,
      elementRef: r,
      index: e.column,
      style: i,
      children: t
    }
  ) : /* @__PURE__ */ Y(
    Jt,
    {
      axis: "row",
      className: n,
      crossSpan: e.columnSpan,
      crossStart: e.column ?? 0,
      disabled: o,
      elementRef: r,
      index: e.row,
      style: i,
      children: t
    }
  );
}
In.displayName = "Gridline";
const Ce = ["column", "row"], Zt = { columns: {}, rows: {} };
function yo({
  children: e,
  className: t,
  columns: n,
  defaultLayout: o,
  disableCursor: r,
  disabled: i,
  elementRef: a,
  gridRef: c,
  id: s,
  onLayoutChange: u,
  onLayoutChanged: l,
  resizeTargetMinimumSize: d = {
    coarse: 20,
    fine: 10
  },
  rows: h,
  style: p,
  ...m
}) {
  const f = Te(s), y = re(
    (L) => L === "column" ? `${f}:columns` : `${f}:rows`,
    [f]
  ), g = Qt(n, "columns"), S = Qt(h, "rows"), z = (L) => L === "column" ? g : S, b = B({
    onLayoutChange: Zt,
    onLayoutChanged: Zt
  }), R = Se((L) => {
    en(b.current.onLayoutChange, L) || (b.current.onLayoutChange = L, u?.(L));
  }), O = Se(
    (L, T, F) => {
      en(b.current.onLayoutChanged, L) || (b.current.onLayoutChanged = L, l?.(L, { isUserInteraction: T, requestedLayout: F }));
    }
  ), A = B(null), x = Ve(A, a), [w, v] = wn(), M = B({
    cells: [],
    column: { expandedItemSizes: {}, layouts: {} },
    loggedErrors: /* @__PURE__ */ new Set(),
    row: { expandedItemSizes: {}, layouts: {} },
    separators: /* @__PURE__ */ new Map()
  }), k = { column: !1, row: !1 };
  for (const L of M.current.separators.values())
    k[L.axis] = !0;
  Ln(e, k);
  const P = it({
    defaultLayout: o,
    disableCursor: r,
    resizeTargetMinimumSize: d
  }), $ = Se(() => !!P.disableCursor), C = re(
    (L) => {
      const T = M.current;
      return T.cells = [...T.cells, L], v(), () => {
        T.cells = T.cells.filter(
          (F) => F !== L
        ), v();
      };
    },
    [v]
  ), I = re(
    (L, T) => {
      const F = M.current;
      return F.separators = new Map(F.separators), F.separators.set(T, L), v(), () => {
        F.separators = new Map(F.separators), F.separators.delete(T), v();
      };
    },
    [v]
  ), E = re(
    (L, {
      disabled: T,
      disableDoubleClick: F
    }) => {
      for (const G of M.current.separators.keys())
        G.id === L && (G.disabled = T, G.disableDoubleClick = F);
    },
    []
  ), q = M.current.separators, Z = Me(
    () => ({
      getDisableCursor: $,
      getResizeAxisId: y,
      gutters: {
        column: k.column,
        row: k.row
      },
      id: f,
      registerCell: C,
      registerSeparator: I,
      separatorPlacements: q,
      trackCounts: {
        column: g.length,
        row: S.length
      },
      updateSeparatorProps: E
    }),
    [
      g.length,
      $,
      y,
      k.column,
      k.row,
      f,
      C,
      I,
      S.length,
      q,
      E
    ]
  ), X = B([]);
  ne(() => {
    const L = A.current;
    if (L === null)
      return;
    const T = M.current, F = vo({
      cells: T.cells,
      separatorPlacements: T.separators,
      trackCounts: { column: g.length, row: S.length }
    });
    F.forEach((D) => {
      T.loggedErrors.has(D) || console.error(D);
    }), T.loggedErrors = new Set(F);
    const G = (D) => Array.from(T.separators.entries()).filter(([, U]) => U.axis === D).sort(([, U], [, pe]) => U.index - pe.index).map(([U]) => U), _ = (D) => {
      const U = D === "column" ? g : S, pe = D === "column" ? S : g, he = U.map((Q) => Q.id), Ue = y(D), We = G(D), be = We.length > 0, Ye = U.map(
        ({ id: Q, ...oe }, ee) => ({
          // Tracks don't have DOM elements of their own;
          // the Grid element is used to resolve relative size constraints (e.g. "em")
          element: L,
          id: he[ee],
          idIsStable: !0,
          mutableValues: {
            expandToSize: void 0,
            prevSize: void 0
          },
          onResize: void 0,
          constraintProps: oe
        })
      ), $e = () => {
        const Q = [];
        if (be) {
          for (const [oe, ee] of T.separators)
            if (ee.axis === D && pt(ee.index, U.length)) {
              const Ne = oe.element.getBoundingClientRect();
              Q[ee.index] = Math.max(
                Q[ee.index] ?? 0,
                D === "column" ? Ne.width : Ne.height
              );
            }
        }
        return Nn({
          axis: D,
          element: L,
          gutterSizes: Q.filter((oe) => oe !== void 0),
          hasGutters: be,
          layout: ce(Ue)?.layout,
          trackIds: he
        });
      };
      let Oe;
      const at = P.defaultLayout?.[D === "column" ? "columns" : "rows"];
      if (at !== void 0 && Object.keys(at).length === he.length) {
        Oe = {};
        for (const Q of he) {
          const oe = at[Q];
          oe !== void 0 && (Oe[Q] = oe);
        }
      }
      return {
        disabled: !!i,
        element: L,
        id: Ue,
        layoutStrategy: {
          getItemAriaControls: (Q) => {
            const oe = he.indexOf(Q);
            return T.cells.filter((ee) => {
              const Ne = D === "column" ? ee.column : ee.row, Rn = D === "column" ? ee.columnSpan : ee.rowSpan;
              return Ne <= oe && oe < Ne + Rn;
            }).map((ee) => ee.element.id).filter(Boolean).join(" ") || void 0;
          },
          calculateAvailableSize: () => $e().availableSize,
          calculateHitRegions: ({
            expandHitTargets: Q,
            axis: oe,
            includeDisabled: ee
          }) => On({
            axis: D,
            cells: T.cells,
            crossTrackCount: pe.length,
            expandHitTargets: Q,
            resizeAxis: oe,
            axisSize: $e().availableSize,
            includeDisabled: ee,
            separatorPlacements: T.separators
          }),
          getItemSizeInPixels: (Q) => $e().trackSizes[he.indexOf(Q)] ?? 0
        },
        mutableState: {
          defaultLayout: Oe,
          disableCursor: !!P.disableCursor,
          expandedItemSizes: T[D].expandedItemSizes,
          layouts: T[D].layouts
        },
        orientation: D === "column" ? "horizontal" : "vertical",
        items: Ye,
        resizePreviewMode: "panel",
        get resizeTargetMinimumSize() {
          return P.resizeTargetMinimumSize;
        },
        separators: We
      };
    }, V = Ce.map(_);
    X.current = V;
    const j = V.map((D) => bn(D)), te = () => {
      const [D, U] = V.map(
        (pe) => ce(pe.id)
      );
      if (!(!D || !U || D.defaultLayoutDeferred || U.defaultLayoutDeferred))
        return {
          layout: { columns: D.layout, rows: U.layout },
          requestedLayout: {
            columns: D.requestedLayout,
            rows: U.requestedLayout
          }
        };
    };
    {
      const D = te();
      if (D)
        try {
          try {
            R(D.layout);
          } finally {
            O(
              D.layout,
              !1,
              D.requestedLayout
            );
          }
        } catch (U) {
          throw X.current = [], j.forEach((pe) => pe()), U;
        }
    }
    const Ae = V.map(
      (D) => Be(D.id, (U) => {
        const {
          defaultLayoutDeferred: pe,
          derivedItemConstraints: he,
          layout: Ue,
          requestedLayout: We
        } = U.next;
        if (pe || he.length === 0)
          return;
        xn({
          derivedItemConstraints: he,
          axis: D,
          layout: Ue,
          prevLayout: U.prev?.layout,
          requestedLayout: We
        });
        const be = te();
        if (be) {
          const Ye = ie(), $e = Ye.state !== "active" || !Ye.hitRegions.some(
            (Oe) => V.includes(Oe.axis)
          );
          try {
            R(be.layout);
          } finally {
            $e && O(
              be.layout,
              U.isUserInteraction,
              be.requestedLayout
            );
          }
        }
      })
    );
    return () => {
      X.current = [], j.forEach((D) => D()), Ae.forEach((D) => D());
    };
  }, [
    g,
    i,
    y,
    f,
    O,
    R,
    S,
    w,
    P
  ]), He(() => {
    X.current.forEach((L) => {
      L.mutableState.defaultLayout = o?.[L.orientation === "horizontal" ? "columns" : "rows"], L.mutableState.disableCursor = !!r;
    });
  }), mt(c, () => {
    const L = () => {
      const [G, _] = Ce.map(y);
      return !Re(G) || !Re(_) ? { columns: {}, rows: {} } : {
        columns: _e({
          axisId: G
        }).getLayout(),
        rows: _e({ axisId: _ }).getLayout()
      };
    }, T = (G) => G.map((_) => `"${_}"`).join(", "), F = (G, _) => {
      const V = y(G), j = () => {
        const te = Re(V);
        return N(te, `Grid "${f}" has not been mounted`), N(
          te.items.some((Ae) => Ae.id === _),
          `Grid "${f}" no longer contains a ${G} with id "${_}"; ${G} ids are ${T(te.items.map((Ae) => Ae.id))}`
        ), zt({ axisId: V, itemId: _ });
      };
      return {
        collapse: () => j().collapse(),
        expand: () => j().expand(),
        getSize: () => j().getSize(),
        isCollapsed: () => j().isCollapsed(),
        resize: (te) => j().resize(te)
      };
    };
    return {
      getLayout: L,
      getTrackById: (G, _) => {
        const V = G === "column" ? g : S, j = `${_}`;
        return N(
          V.some((te) => te.id === j),
          `Grid "${f}" does not contain a ${G} with id "${j}"; ${G} ids are ${T(V.map((te) => te.id))}`
        ), F(G, j);
      },
      getTrackByIndex: (G, _) => {
        const V = G === "column" ? g : S, j = Number.isInteger(_) ? V[_] : void 0;
        return N(
          j,
          `Grid "${f}" does not contain a ${G} at index ${_}; it has ${V.length} ${G}s`
        ), F(G, j.id);
      },
      setLayout: (G) => (Ce.forEach((_) => {
        const V = G[_ === "column" ? "columns" : "rows"], j = y(_);
        V && Re(j) && _e({ axisId: j }).setLayout(V);
      }), L())
    };
  }, [g, y, f, S]);
  const K = () => Ce.map((L) => {
    const T = ce(y(L)), F = z(L);
    return (T && !T.defaultLayoutDeferred ? F.map((_) => `minmax(0, ${T.layout[_.id] ?? 1}fr)`) : So(
      F,
      o?.[L === "column" ? "columns" : "rows"]
    )).join(k[L] ? " auto " : " ");
  }).join("|"), ae = re(
    (L) => {
      const T = Ce.map(
        (F) => Be(y(F), L)
      );
      return () => T.forEach((F) => F());
    },
    [y]
  ), we = tt(
    ae,
    K,
    K
  ), [ke, ze] = we.split("|");
  return /* @__PURE__ */ Y(sn.Provider, { value: Z, children: /* @__PURE__ */ Y(
    "div",
    {
      ...m,
      className: t,
      "data-grid": !0,
      "data-testid": je(m, s),
      id: f,
      ref: x,
      style: {
        height: "100%",
        width: "100%",
        overflow: "hidden",
        ...p,
        display: "grid",
        gridTemplateColumns: ke,
        gridTemplateRows: ze,
        // Inform the browser that the library is handling touch events for this element
        // NOTE This is not an inherited style
        touchAction: "none"
      },
      children: /* @__PURE__ */ Y(It.Provider, { value: null, children: e })
    }
  ) });
}
yo.displayName = "Grid";
function Qt(e, t) {
  const n = JSON.stringify(e);
  return Me(() => {
    const o = typeof e == "number" ? Array.from({ length: e }, (r, i) => ({ id: `${i}` })) : e.map((r, i) => ({
      ...r,
      id: `${r.id ?? i}`
    }));
    return N(
      o.length > 0,
      `Grid must have at least one track; "${t}" is ${n}`
    ), o;
  }, [n]);
}
function Ln(e, t) {
  Pn.forEach(e, (n) => {
    if (rn(n))
      if (n.type === In) {
        const { type: o } = n.props;
        o === "column" ? t.column = !0 : o === "row" && (t.row = !0);
      } else // Fragments
      typeof n.type == "symbol" && n.props !== null && typeof n.props == "object" && "children" in n.props && Ln(n.props.children, t);
  });
}
function So(e, t) {
  if (t)
    return e.map(
      (i) => `minmax(0, ${t[i.id] ?? 1}fr)`
    );
  const n = e.map(
    (i) => i.defaultSize === void 0 ? void 0 : cn(i.defaultSize)
  );
  let o = 100, r = 0;
  return n.forEach((i) => {
    i === void 0 ? r++ : i[1] === "%" && (o -= i[0]);
  }), n.map((i) => {
    if (i === void 0)
      return `minmax(0, ${Math.max(0, o) / Math.max(1, r)}fr)`;
    const [a, c] = i;
    return c === "%" ? `minmax(0, ${a}fr)` : `${a}${c}`;
  });
}
function vo({
  cells: e,
  separatorPlacements: t,
  trackCounts: n
}) {
  const o = [];
  for (const c of e)
    Ce.forEach((s) => {
      const [u, l] = s === "column" ? [c.column, c.columnSpan] : [c.row, c.rowSpan], d = n[s];
      (!Number.isInteger(u) || !Number.isInteger(l) || u < 0 || l < 1 || u + l > d) && o.push(
        `Invalid Cell ${s} placement (${s}: ${u}, ${s}Span: ${l}); Grid has ${d} ${s}s`
      );
    });
  const r = ({
    axis: c,
    crossSpan: s,
    crossStart: u,
    disabled: l,
    index: d
  }) => {
    const h = c === "column" ? "row" : "column";
    let p = `type="${c}" ${c}={${d}}`;
    return (u !== 0 || s !== void 0) && (p += ` ${h}={${u}}`), s !== void 0 && (p += ` ${h}Span={${s}}`), l && (p += " disabled"), `<Gridline ${p} />`;
  }, i = Array.from(t.values()).filter(
    (c) => {
      const { axis: s, crossSpan: u, crossStart: l, index: d } = c, h = s === "column" ? "row" : "column", p = n[s], m = n[h];
      let f = !0;
      return pt(d, p) || (o.push(
        `Invalid ${s} Gridline ${s} (${d}); must be between 1 and ${p - 1}`
      ), f = !1), !Number.isInteger(l) || l < 0 || l >= m ? (o.push(
        `Invalid ${s} Gridline ${h} (${l}); must be between 0 and ${m - 1}`
      ), f = !1) : u !== void 0 && (!Number.isInteger(u) || u < 1 || l + u > m) && (o.push(
        `Invalid ${s} Gridline ${h}Span (${u}); Grid has ${m} ${h}s`
      ), f = !1), f;
    }
  ), a = (c) => {
    const s = n[c.axis === "column" ? "row" : "column"];
    return [
      c.crossStart,
      c.crossSpan === void 0 ? s : c.crossStart + c.crossSpan
    ];
  };
  return i.forEach((c, s) => {
    const { axis: u, index: l } = c, [d, h] = a(c);
    for (const p of e) {
      const [m, f, y, g] = u === "column" ? [p.column, p.columnSpan, p.row, p.rowSpan] : [p.row, p.rowSpan, p.column, p.columnSpan];
      if (m < l && l < m + f && y < h && d < y + g) {
        const S = u === "column" ? "row" : "column";
        o.push(
          `${r(c)} overlaps a Cell that spans across it (${u}: ${m}, ${u}Span: ${f}, ${S}: ${y}, ${S}Span: ${g}); use the ${S} and ${S}Span props to render gridlines beside the Cell instead`
        );
      }
    }
    for (const p of i.slice(s + 1))
      if (p.axis === u && p.index === l) {
        const [m, f] = a(p);
        m < h && d < f && o.push(`${r(c)} overlaps ${r(p)}`);
      }
  }), o;
}
function en(e, t) {
  return se(e.columns, t.columns) && se(e.rows, t.rows);
}
function Fo({
  id: e,
  onlySaveAfterUserInteractions: t,
  storage: n = localStorage
}) {
  const o = `react-resizable-panels:grid:${e}`, r = tt(
    bo,
    () => n.getItem(o),
    () => n.getItem(o)
  ), i = Me(() => {
    if (r)
      try {
        const c = JSON.parse(r);
        if (c !== null && typeof c == "object")
          return c;
      } catch {
      }
  }, [r]), a = re(
    (c, s) => {
      if (!(t && !s.isUserInteraction))
        try {
          n.setItem(
            o,
            JSON.stringify(s.requestedLayout ?? c)
          );
        } catch (u) {
          console.error(u);
        }
    },
    [t, n, o]
  );
  return {
    /**
     * Pass this value to `Grid` as the `defaultLayout` prop.
     */
    defaultLayout: i,
    /**
     * Attach this callback on the `Grid` as the `onLayoutChanged` prop.
     */
    onLayoutChanged: a
  };
}
function bo() {
  return function() {
  };
}
function _o() {
  return ge(null);
}
function Bo() {
  return B(null);
}
function xo(e) {
  for (let t = 1; t < e.length; t++)
    if (yt(e[t - 1], e[t]) > 0)
      return !1;
  return !0;
}
function wo({
  separator: e
}) {
  const { element: t } = e, n = B(null);
  return ne(() => {
    const o = t.cloneNode(!0), r = [t, ...t.querySelectorAll("*")], i = [o, ...o.querySelectorAll("*")], a = t.ownerDocument.defaultView;
    return r.forEach((c, s) => {
      const u = i[s];
      if (u instanceof a.HTMLElement || u instanceof a.SVGElement) {
        const l = a.getComputedStyle(c);
        for (let d = 0; d < l.length; d++) {
          const h = l.item(d);
          u.style.setProperty(
            h,
            l.getPropertyValue(h)
          );
        }
      }
      u.removeAttribute("data-testid"), u.removeAttribute("id");
    }), Object.assign(o.style, {
      boxSizing: "border-box",
      height: "100%",
      margin: "0",
      position: "static",
      transform: "none",
      width: "100%"
    }), n.current.appendChild(o), () => o.remove();
  }, [t]), /* @__PURE__ */ Y(
    "div",
    {
      ref: n,
      style: {
        height: "100%",
        opacity: 0.65,
        pointerEvents: "none",
        width: "100%"
      }
    }
  );
}
function st() {
  const e = on(It);
  return N(
    e,
    "Group Context not found; did you render a Panel or Separator outside of a Group?"
  ), e;
}
function Cn(e) {
  const { registerOverlay: t } = st(), n = B(e);
  vn(n.current, e) || (n.current = e);
  const o = n.current;
  return ne(
    () => t(o),
    [t, o]
  ), null;
}
Cn.displayName = "SeparatorOverlay";
function zo({
  active: e,
  orientation: t,
  style: n,
  ...o
}) {
  let r;
  switch (t) {
    case "horizontal": {
      r = {
        height: "100%",
        minWidth: "1px"
      };
      break;
    }
    case "vertical": {
      r = {
        minHeight: "1px",
        width: "100%"
      };
      break;
    }
  }
  return /* @__PURE__ */ Y(
    "div",
    {
      ...o,
      "data-separator-overlay": e ? "active" : "inactive",
      style: {
        ...r,
        ...n,
        flexShrink: 0,
        pointerEvents: "none"
      }
    }
  );
}
function Io({
  overlay: e,
  preview: t
}) {
  const { axis: n, offset: o, rect: r, separator: i } = t, a = n.orientation === "horizontal";
  let c = i?.preview, s = e;
  return rn(c) && c.type === Cn && (s = c.props, c = void 0), c == null && (s ? c = /* @__PURE__ */ Y(
    zo,
    {
      ...s,
      active: t.active,
      orientation: n.orientation
    }
  ) : i && (c = /* @__PURE__ */ Y(wo, { separator: i }))), /* @__PURE__ */ Y(
    "div",
    {
      "aria-hidden": "true",
      "data-resize-preview": !0,
      inert: !0,
      style: {
        height: r.height,
        left: r.left,
        pointerEvents: "none",
        position: "absolute",
        top: r.top,
        transform: a ? `translateX(${o}px)` : `translateY(${o}px)`,
        width: r.width
      },
      children: c
    }
  );
}
function Lo(e) {
  return Array.from(e).sort(yt);
}
function Co(e, t) {
  const n = B({
    getLayout: () => ({}),
    setLayout: Bn
  });
  mt(t, () => n.current, []), ne(() => {
    Object.assign(
      n.current,
      _e({ axisId: e })
    );
  });
}
function Ro({
  groupId: e,
  resizePreviewMode: t
}) {
  const [n, o] = ge([]), r = B(n);
  return ne(() => {
    const i = (c) => {
      const s = Re(e), u = t === "separator" && c.state === "active" ? c.previews.filter(
        (d) => d.axis === s && (d.active || !W(d.offset, 0))
      ) : [], l = r.current;
      l.length === u.length && u.every(
        (d, h) => d === l[h]
      ) || (r.current = u, o(u));
    };
    if (t !== "separator") {
      i(ie());
      return;
    }
    const a = gt(
      ({ next: c }) => i(c)
    );
    return i(ie()), a;
  }, [e, t]), n;
}
function Eo({
  children: e,
  className: t,
  defaultLayout: n,
  disableCursor: o,
  disabled: r,
  elementRef: i,
  groupRef: a,
  id: c,
  onLayoutChange: s,
  onLayoutChanged: u,
  orientation: l = "horizontal",
  resizePreviewMode: d = "panel",
  resizeTargetMinimumSize: h = {
    coarse: 20,
    fine: 10
  },
  style: p,
  ...m
}) {
  const f = B({
    onLayoutChange: {},
    onLayoutChanged: {}
  }), y = Se((I) => {
    se(f.current.onLayoutChange, I) || (f.current.onLayoutChange = I, s?.(I));
  }), g = Se(
    (I, E, q) => {
      se(f.current.onLayoutChanged, I) || (f.current.onLayoutChanged = I, u?.(I, { isUserInteraction: E, requestedLayout: q }));
    }
  ), S = Te(c), [z, b] = ge(), R = Ro({
    groupId: S,
    resizePreviewMode: d
  }), O = B(null), [A, x] = wn(), w = B([]), v = B({
    lastExpandedPanelSizes: {},
    layouts: {},
    panels: [],
    separators: []
  }), M = Ve(O, i);
  Co(S, a);
  const k = Se(
    (I, E) => {
      const q = ce(I);
      if (q)
        return {
          flexGrow: q.layout[E] ?? 1
        };
      if (n?.[E])
        return {
          flexGrow: n?.[E]
        };
    }
  ), P = it({
    defaultLayout: n,
    disableCursor: o,
    resizeTargetMinimumSize: h
  }), $ = Me(
    () => ({
      get disableCursor() {
        return !!P.disableCursor;
      },
      getPanelStyles: k,
      id: S,
      orientation: l,
      registerPanel: (I) => {
        const E = v.current;
        return E.panels = Ge(l, [
          ...E.panels,
          I
        ]), x(), () => {
          E.panels = E.panels.filter(
            (q) => q !== I
          ), x();
        };
      },
      registerOverlay: (I) => (b(I), () => {
        b(void 0);
      }),
      registerSeparator: (I) => {
        const E = v.current;
        return E.separators = Ge(l, [
          ...E.separators,
          I
        ]), x(), () => {
          E.separators = E.separators.filter(
            (q) => q !== I
          ), x();
        };
      },
      updatePanelProps: (I, { disabled: E }) => {
        const Z = v.current.panels.find(
          (ae) => ae.id === I
        );
        Z && (Z.constraintProps.disabled = E);
        const X = Re(S), K = ce(S);
        X && K && me(X, {
          ...K,
          derivedItemConstraints: ft(X)
        });
      },
      updateSeparatorProps: (I, {
        disabled: E,
        disableDoubleClick: q
      }) => {
        const X = v.current.separators.find(
          (K) => K.id === I
        );
        X && (X.disabled = E, X.disableDoubleClick = q);
      }
    }),
    [k, S, x, l, P]
  ), C = B(null);
  return ne(() => {
    const I = O.current;
    if (I === null)
      return;
    const E = v.current;
    E.panels = Ge(
      l,
      E.panels
    ), E.separators = Ge(
      l,
      E.separators
    ), w.current = Lo([
      ...E.panels.map(({ element: L }) => L),
      ...E.separators.map(({ element: L }) => L)
    ]);
    let q;
    if (P.defaultLayout !== void 0 && Object.keys(P.defaultLayout).length === E.panels.length) {
      q = {};
      for (const L of E.panels) {
        const T = P.defaultLayout[L.id];
        T !== void 0 && (q[L.id] = T);
      }
    }
    const Z = {
      disabled: !!r,
      element: I,
      id: S,
      mutableState: {
        defaultLayout: q,
        disableCursor: !!P.disableCursor,
        expandedItemSizes: v.current.lastExpandedPanelSizes,
        layouts: v.current.layouts
      },
      orientation: l,
      items: E.panels,
      resizePreviewMode: d,
      get resizeTargetMinimumSize() {
        return P.resizeTargetMinimumSize;
      },
      separators: E.separators
    };
    C.current = Z;
    const X = bn(Z), {
      defaultLayoutDeferred: K,
      derivedItemConstraints: ae,
      layout: we,
      requestedLayout: ke
    } = ce(Z.id, !0);
    if (!K && ae.length > 0)
      try {
        try {
          y(we);
        } finally {
          g(we, !1, ke);
        }
      } catch (L) {
        throw C.current = null, X(), L;
      }
    const ze = Be(S, (L) => {
      const {
        defaultLayoutDeferred: T,
        derivedItemConstraints: F,
        layout: G,
        requestedLayout: _
      } = L.next;
      if (T || F.length === 0)
        return;
      xn({
        derivedItemConstraints: F,
        axis: Z,
        layout: G,
        prevLayout: L.prev?.layout,
        requestedLayout: _
      });
      const V = ie(), j = V.state !== "active" || !V.hitRegions.some((te) => te.axis === Z);
      try {
        y(G);
      } finally {
        j && g(
          G,
          L.isUserInteraction,
          _
        );
      }
    });
    return () => {
      C.current = null, X(), ze();
    };
  }, [
    r,
    S,
    g,
    y,
    l,
    A,
    d,
    P
  ]), ne(() => {
    xo(w.current) || x();
  }), He(() => {
    const I = C.current;
    I && (I.mutableState.defaultLayout = n, I.mutableState.disableCursor = !!o);
  }), /* @__PURE__ */ Y(It.Provider, { value: $, children: /* @__PURE__ */ En(
    "div",
    {
      ...m,
      className: t,
      "data-group": !0,
      "data-testid": je(m, c),
      id: S,
      ref: M,
      style: {
        height: "100%",
        width: "100%",
        overflow: "hidden",
        position: d === "separator" ? "relative" : void 0,
        ...p,
        display: "flex",
        flexDirection: l === "horizontal" ? "row" : "column",
        flexWrap: "nowrap",
        // Inform the browser that the library is handling touch events for this element
        // but still allow users to scroll content within panels in the non-resizing direction
        // NOTE This is not an inherited style
        // See github.com/bvaughn/react-resizable-panels/issues/662
        touchAction: l === "horizontal" ? "pan-y" : "pan-x"
      },
      children: [
        e,
        R.map((I) => /* @__PURE__ */ Y(
          Io,
          {
            overlay: z,
            preview: I
          },
          I.key
        ))
      ]
    }
  ) });
}
Eo.displayName = "Group";
function Qe(e, t) {
  return `react-resizable-panels:${[e, ...t].join(":")}`;
}
function Mo({
  id: e,
  panelIds: t,
  storage: n
}) {
  const o = Qe(e, []), r = n.getItem(o);
  if (r)
    try {
      const i = JSON.parse(r);
      if (t) {
        const a = t.join(","), c = i[a];
        if (c && Array.isArray(c.layout) && t.length === c.layout.length) {
          const s = {};
          for (let u = 0; u < t.length; u++)
            s[t[u]] = c.layout[u];
          return s;
        }
      } else {
        const a = Object.keys(i);
        if (a.length === 1) {
          const c = i[a[0]];
          if (c && Array.isArray(c.layout)) {
            const s = a[0].split(",");
            if (s.length === c.layout.length) {
              const u = {};
              for (let l = 0; l < s.length; l++)
                u[s[l]] = c.layout[l];
              return u;
            }
          }
        }
      }
    } catch {
    }
}
function qo({
  debounceSaveMs: e = 100,
  onlySaveAfterUserInteractions: t,
  panelIds: n,
  storage: o = localStorage,
  ...r
}) {
  const i = n !== void 0, a = "id" in r ? r.id : r.groupId, c = Qe(a, n ?? []), s = tt(
    Po,
    () => o.getItem(c),
    () => o.getItem(c)
  ), u = Me(() => {
    if (s) {
      const y = JSON.parse(s), g = Object.values(y);
      if (Array.from(g).every((S) => typeof S == "number"))
        return y;
    }
  }, [s]), l = Me(() => {
    if (!u)
      return Mo({
        id: a,
        panelIds: n,
        storage: o
      });
  }, [u, a, n, o]), d = u ?? l, h = B(null), p = re(() => {
    const y = h.current;
    y && (h.current = null, clearTimeout(y));
  }, []);
  tn(() => () => {
    p();
  }, [p]);
  const m = re(
    // The hook persists every layout commit -- including library-driven ones --
    // because it owns its own storage and the goal is to remember whatever
    // layout the user is currently looking at. Consumers that only want to
    // persist on user interaction should branch on `isUserInteraction` in
    // their own callback (see #716) rather than via this hook.
    (y, g) => {
      if (t && !g.isUserInteraction)
        return;
      p();
      const S = g.requestedLayout ?? y;
      let z;
      i ? z = Qe(a, Object.keys(S)) : z = Qe(a, []);
      try {
        o.setItem(z, JSON.stringify(S));
      } catch (b) {
        console.error(b);
      }
    },
    [
      p,
      i,
      a,
      t,
      o
    ]
  ), f = re(
    (y) => {
      p(), e === 0 ? m(y, { isUserInteraction: !1 }) : h.current = setTimeout(() => {
        m(y, { isUserInteraction: !1 });
      }, e);
    },
    [p, e, m]
  );
  return {
    /**
     * Pass this value to `Group` as the `defaultLayout` prop.
     */
    defaultLayout: d,
    /**
     * Attach this callback on the `Group` as the `onLayoutChange` prop.
     *
     * @deprecated Use the {@link onLayoutChanged} prop instead.
     */
    onLayoutChange: f,
    /**
     * Attach this callback on the `Group` as the `onLayoutChanged` prop.
     */
    onLayoutChanged: m
  };
}
function Po() {
  return function() {
  };
}
function Ho() {
  return ge(null);
}
function Vo() {
  return B(null);
}
function To(e, t) {
  const { id: n } = st(), o = B({
    collapse: ct,
    expand: ct,
    getSize: () => ({
      asPercentage: 0,
      inPixels: 0
    }),
    isCollapsed: () => !1,
    resize: ct
  });
  mt(t, () => o.current, []), ne(() => {
    Object.assign(
      o.current,
      zt({ axisId: n, itemId: e })
    );
  });
}
function Do({
  children: e,
  className: t,
  collapsedSize: n = "0%",
  collapsedThreshold: o,
  collapsible: r = !1,
  defaultSize: i,
  disabled: a,
  elementRef: c,
  groupResizeBehavior: s = "preserve-relative-size",
  id: u,
  maxSize: l = "100%",
  minSize: d = "0%",
  onResize: h,
  panelRef: p,
  style: m,
  ...f
}) {
  const y = et(u), g = Te(u), S = it({
    disabled: a
  }), z = B(null), b = Ve(z, c), {
    getPanelStyles: R,
    id: O,
    orientation: A,
    registerPanel: x,
    updatePanelProps: w
  } = st(), v = h !== null, M = Se(
    (C, I, E) => {
      h?.(C, u, E);
    }
  );
  ne(() => {
    const C = z.current;
    if (C !== null) {
      const I = {
        element: C,
        id: g,
        idIsStable: y,
        mutableValues: {
          expandToSize: void 0,
          prevSize: void 0
        },
        onResize: v ? M : void 0,
        constraintProps: {
          groupResizeBehavior: s,
          collapsedSize: n,
          collapsedThreshold: o,
          collapsible: r,
          defaultSize: i,
          disabled: S.disabled,
          maxSize: l,
          minSize: d
        }
      };
      return x(I);
    }
  }, [
    s,
    n,
    o,
    r,
    i,
    v,
    g,
    y,
    l,
    d,
    M,
    x,
    S
  ]), He(() => {
    w(g, { disabled: a });
  }, [a, g, w]), To(g, p);
  const k = () => {
    const C = R(O, g);
    if (C)
      return JSON.stringify(C);
  }, P = tt(
    (C) => Be(O, C),
    k,
    k
  );
  let $;
  return P ? $ = JSON.parse(P) : i !== void 0 ? $ = {
    flexGrow: void 0,
    flexShrink: void 0,
    flexBasis: i
  } : $ = { flexGrow: 1 }, /* @__PURE__ */ Y(
    "div",
    {
      ...f,
      "data-disabled": a || void 0,
      "data-panel": !0,
      "data-testid": je(f, u),
      id: g,
      ref: b,
      style: {
        ...ko,
        display: "flex",
        flexBasis: 0,
        flexShrink: 1,
        overflow: "visible",
        ...$
      },
      children: /* @__PURE__ */ Y(
        "div",
        {
          className: t,
          style: {
            maxHeight: "100%",
            maxWidth: "100%",
            flexGrow: 1,
            overflow: "auto",
            ...m,
            // Inform the browser that the library is handling touch events for this element
            // but still allow users to scroll content within panels in the non-resizing direction
            // NOTE This is not an inherited style
            // See github.com/bvaughn/react-resizable-panels/issues/662
            touchAction: A === "horizontal" ? "pan-y" : "pan-x"
          },
          children: e
        }
      )
    }
  );
}
Do.displayName = "Panel";
const ko = {
  minHeight: 0,
  maxHeight: "100%",
  height: "auto",
  minWidth: 0,
  maxWidth: "100%",
  width: "auto",
  border: "none",
  borderWidth: 0,
  padding: 0,
  margin: 0
};
function jo() {
  return ge(null);
}
function Uo() {
  return B(null);
}
const Ao = { flexBasis: "auto" }, $o = { flexGrow: 0, flexShrink: 0 };
function Oo({
  children: e,
  className: t,
  disabled: n,
  disableDoubleClick: o,
  elementRef: r,
  id: i,
  preview: a,
  style: c,
  ...s
}) {
  const u = Te(i), {
    disableCursor: l,
    id: d,
    orientation: h,
    registerSeparator: p,
    updateSeparatorProps: m
  } = st();
  return /* @__PURE__ */ Y(
    zn,
    {
      attributes: s,
      axisId: d,
      axisOrientation: h,
      className: t,
      "data-testid": je(s, i),
      disableCursor: l,
      disabled: n,
      disableDoubleClick: o,
      elementRef: r,
      id: u,
      preview: a,
      registerSeparator: p,
      requiredStyle: $o,
      style: c,
      styleDefaults: Ao,
      updateSeparatorProps: m,
      children: e
    }
  );
}
Oo.displayName = "Separator";
export {
  An as Cell,
  yo as Grid,
  In as Gridline,
  Eo as Group,
  Do as Panel,
  Oo as Separator,
  Cn as SeparatorOverlay,
  $n as isCoarsePointer,
  Fo as useDefaultGridLayout,
  qo as useDefaultLayout,
  _o as useGridCallbackRef,
  Bo as useGridRef,
  Ho as useGroupCallbackRef,
  Vo as useGroupRef,
  jo as usePanelCallbackRef,
  Uo as usePanelRef
};
//# sourceMappingURL=react-resizable-panels.js.map
