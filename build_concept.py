# Converts the Activity 1.1 Excalidraw concept map into an inline, clickable SVG.
import json, html, sys
d = json.load(open(sys.argv[1]))
els = [e for e in d['elements'] if not e.get('isDeleted')]
byid = {e['id']: e for e in els}
out = []
minx = min(e['x'] for e in els) - 20; miny = 150
maxx = max(e['x'] + e['width'] for e in els) + 20; maxy = 860
out.append(f'<svg class="cmap" viewBox="{minx} {miny} {maxx-minx} {maxy-miny}" role="img" aria-labelledby="cmap-title cmap-desc">')
out.append('<title id="cmap-title">Concept map: Plastic Bag Ban in New York State</title><desc id="cmap-desc">Formal institutions (left column) and informal institutions (right column) push on store-owner and shopper behavior (middle column), which adds up to the outcome: fewer bags overall but uneven compliance. A purple dashed feedback loop runs from the outcome back to advocates who complain to the DEC.</desc>')
out.append('<defs>' + ''.join(f'<marker id="ah-{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for c in ['#1e1e1e','#22c55e','#ef4444','#8b5cf6']) + '</defs>')
# arrows first
for e in els:
    if e['type'] != 'arrow': continue
    pts = ' '.join(f"{e['x']+px},{e['y']+py}" for px, py in e['points'])
    dash = ' stroke-dasharray="8 6"' if e.get('strokeStyle') == 'dashed' else ''
    out.append(f'<polyline class="edge" points="{pts}" fill="none" stroke="{e["strokeColor"]}" stroke-width="2.5"{dash} marker-end="url(#ah-{e["strokeColor"][1:]})"/>')
n = 0
for e in els:
    if e['type'] != 'rectangle': continue
    legend = e['y'] >= 800
    cls = 'legend' if legend else 'node'
    attrs = '' if legend else f' tabindex="0" role="button" data-node="{n}"'
    out.append(f'<g class="{cls}"{attrs}><rect x="{e["x"]}" y="{e["y"]}" width="{e["width"]}" height="{e["height"]}" rx="14" fill="{e["backgroundColor"]}" stroke="{e["strokeColor"]}" stroke-width="2"/>')
    # bound text
    for t in els:
        if t['type'] == 'text' and t.get('containerId') == e['id']:
            lines = t['text'].split('\n'); lh = t['fontSize'] * 1.25
            cy = e['y'] + e['height'] / 2 - (len(lines) - 1) * lh / 2
            tsp = ''.join(f'<tspan x="{e["x"]+e["width"]/2}" y="{cy+i*lh}">{html.escape(l)}</tspan>' for i, l in enumerate(lines))
            out.append(f'<text class="nt" text-anchor="middle" dominant-baseline="middle" font-size="{t["fontSize"]}">{tsp}</text>')
    out.append('</g>')
    if not legend: n += 1
# arrow labels
for t in els:
    if t['type'] != 'text': continue
    c = byid.get(t.get('containerId'))
    if not c or c['type'] != 'arrow': continue
    lines = t['text'].split('\n'); lh = 19
    cx = t['x'] + t['width'] / 2; cy = t['y'] + t['height'] / 2 - (len(lines)-1)*lh/2
    w = t['width'] + 12; h = len(lines) * lh + 6
    out.append(f'<rect class="lblbg" x="{cx-w/2}" y="{cy-lh/2-3}" width="{w}" height="{h}" rx="5"/>')
    out.append('<text class="el" text-anchor="middle" dominant-baseline="middle" font-size="15">' + ''.join(f'<tspan x="{cx}" y="{cy+i*lh}">{html.escape(l)}</tspan>' for i, l in enumerate(lines)) + '</text>')
out.append('</svg>')
print('\n'.join(out))
