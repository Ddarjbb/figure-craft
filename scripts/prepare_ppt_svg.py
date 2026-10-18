"""Prepare solid-color vector diagrams for PowerPoint without outlining text.

Inline local SVG <use> references, preserve semantic groups, and consolidate
data-latex math groups into compound paths when their paint is compatible.
Does not overwrite the source or create PPTX/PDF/PNG. Unsupported effects and
external resources fail explicitly instead of being silently discarded.
"""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from fontTools.misc.transform import Identity, Transform
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path

NS = 'http://www.w3.org/2000/svg'
XLINK = 'http://www.w3.org/1999/xlink'
ET.register_namespace('', NS)


def local(element):
    return element.tag.rsplit('}', 1)[-1]


def affine(value):
    result = Identity
    value = value or ''
    tokens = re.findall(r'([A-Za-z]+)\s*\(([^)]*)\)', value)
    if re.sub(r'([A-Za-z]+)\s*\(([^)]*)\)|[\s,]+', '', value):
        raise ValueError(f'Unsupported transform syntax: {value}')
    for name, args in tokens:
        v = [float(x) for x in re.findall(r'[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?', args)]
        if name == 'matrix' and len(v) == 6:
            t = Transform(*v)
        elif name == 'translate' and len(v) in (1, 2):
            t = Identity.translate(v[0], v[1] if len(v) == 2 else 0)
        elif name == 'scale' and len(v) in (1, 2):
            t = Identity.scale(v[0], v[-1])
        elif name == 'rotate' and len(v) in (1, 3):
            cx, cy = v[1:] if len(v) == 3 else (0, 0)
            t = Identity.translate(cx, cy).rotate(math.radians(v[0])).translate(-cx, -cy)
        elif name == 'skewX' and len(v) == 1:
            t = Transform(1, 0, math.tan(math.radians(v[0])), 1, 0, 0)
        elif name == 'skewY' and len(v) == 1:
            t = Transform(1, math.tan(math.radians(v[0])), 0, 1, 0, 0)
        else:
            raise ValueError(f'Unsupported transform: {name}({args})')
        result = result.transform(t)
    return result


def merge_formula(equation):
    """Return one path, or a reason to retain the already-inlined math group."""
    pen = SVGPathPen(None)
    colors = set()

    def walk(element, parent=Identity, inherited=None):
        paint = {**(inherited or {'fill': '#000000', 'stroke': 'none'})}
        for key in ('fill', 'stroke', 'stroke-width', 'stroke-linecap', 'opacity',
                    'fill-opacity', 'stroke-opacity', 'fill-rule'):
            if key in element.attrib:
                paint[key] = element.get(key)
        if any(key in element.attrib for key in ('style', 'clip-path', 'mask', 'filter')):
            raise ValueError('Formula has an unsupported style or effect; retain its paths.')
        if any(paint.get(k, '1') != '1' for k in ('opacity', 'fill-opacity', 'stroke-opacity')):
            raise ValueError('Formula transparency requires separate paths.')
        if paint.get('fill-rule', 'nonzero') != 'nonzero':
            raise ValueError('Formula fill rule requires separate paths.')
        t = parent.transform(affine(element.get('transform')))
        tag = local(element)
        if tag == 'path':
            fill, stroke = paint['fill'], paint['stroke']
            if fill != 'none':
                if stroke != 'none':
                    raise ValueError('A formula path has both fill and stroke.')
                colors.add(fill)
                parse_path(element.get('d', ''), TransformPen(pen, t))
            elif stroke != 'none':
                recording = RecordingPen()
                parse_path(element.get('d', ''), recording)
                ops = [op for op, _ in recording.value]
                if ops != ['moveTo', 'lineTo', 'endPath'] or paint.get('stroke-linecap', 'butt') != 'butt':
                    raise ValueError('Complex stroked formula paths are retained separately.')
                a, b = recording.value[0][1][0], recording.value[1][1][0]
                half = float(paint.get('stroke-width', '1')) / 2
                angle = math.atan2(b[1]-a[1], b[0]-a[0])
                dx, dy = -math.sin(angle)*half, math.cos(angle)*half
                points = [(a[0]+dx, a[1]+dy), (b[0]+dx, b[1]+dy),
                          (b[0]-dx, b[1]-dy), (a[0]-dx, a[1]-dy)]
                target = TransformPen(pen, t)
                target.moveTo(points[0])
                for point in points[1:]:
                    target.lineTo(point)
                target.closePath()
                colors.add(stroke)
        elif tag not in ('g', 'title', 'desc'):
            raise ValueError(f'Formula contains {tag}; retain its paths.')
        for child in element:
            walk(child, t, paint)

    # Keep the outer transform and place its inherited paint on the new path.
    root_paint = {'fill': equation.get('fill', '#000000'), 'stroke': equation.get('stroke', 'none')}
    try:
        if any(k in equation.attrib for k in ('opacity', 'style', 'fill-rule')):
            raise ValueError('Formula root has special paint; retain its paths.')
        for child in equation:
            walk(child, inherited=root_paint)
        if len(colors) != 1 or not pen.getCommands():
            raise ValueError('Formula uses multiple colors or has no drawable paths.')
    except (ValueError, TypeError) as error:
        return None, str(error)
    return ET.Element(f'{{{NS}}}path', {'d': pen.getCommands(), 'fill': next(iter(colors)), 'stroke': 'none'}), None


def prepare(source, output, report_path=None, merge_math=True):
    source, output = Path(source), Path(output)
    if source.resolve() == output.resolve():
        raise ValueError('Keep the editable source separate from the output.')
    if report_path and Path(report_path).resolve() in (source.resolve(), output.resolve()):
        raise ValueError('The validation report must have its own path.')
    root = ET.parse(source).getroot()
    if root.tag != f'{{{NS}}}svg':
        raise ValueError('Expected an SVG root in the SVG namespace.')
    unsupported = {'image', 'foreignObject', 'script', 'style', 'clipPath', 'filter',
                   'mask', 'linearGradient', 'radialGradient', 'pattern', 'marker',
                   'symbol', 'animate', 'animateTransform'}
    ids = {}
    for element in root.iter():
        if local(element) in unsupported:
            raise ValueError(f'Unsupported {local(element)}; use an exporter that preserves this feature.')
        if element.get('id'):
            if element.get('id') in ids:
                raise ValueError('Duplicate SVG IDs must be resolved before expanding references.')
            ids[element.get('id')] = element
        for key, value in element.attrib.items():
            if 'url(' in value:
                raise ValueError('Paint/effect URL references require a different exporter.')
            if key.endswith('href') and (local(element) != 'use' or not value.startswith('#')):
                raise ValueError('Only local <use> references are supported; no external resources are loaded.')
    text_before = [ET.tostring(e) for e in root.iter() if local(e) == 'text']
    counts = Counter()

    def expand(element, active=(), clone=False):
        tag = local(element)
        if tag == 'defs':
            return None
        if tag == 'use':
            href = element.get(f'{{{XLINK}}}href', element.get('href', ''))
            if not href.startswith('#') or href[1:] not in ids:
                raise ValueError(f'Unresolved glyph reference: {href}')
            if href in active:
                raise ValueError(f'Cyclic reference: {href}')
            attrs = {k:v for k,v in element.attrib.items()
                     if k not in (f'{{{XLINK}}}href', 'href', 'x', 'y', 'width', 'height')}
            if clone:
                attrs.pop('id', None)
            wrapper = ET.Element(f'{{{NS}}}g', attrs)
            x, y = element.get('x', '0'), element.get('y', '0')
            if x != '0' or y != '0':
                wrapper.set('transform', (wrapper.get('transform', '')+f' translate({x},{y})').strip())
            target = expand(ids[href[1:]], active+(href,), True)
            if target is None:
                raise ValueError('Cannot reference a definition container.')
            wrapper.append(target)
            counts['expanded_references'] += 1
            return wrapper
        attrs = dict(element.attrib)
        if clone:
            attrs.pop('id', None)
        result = ET.Element(element.tag, attrs)
        result.text, result.tail = element.text, element.tail
        for child in element:
            converted = expand(child, active, clone)
            if converted is not None:
                result.append(converted)
        return result

    converted = expand(root)
    if merge_math:
        for equation in list(converted.iter()):
            if 'data-latex' not in equation.attrib:
                continue
            path, reason = merge_formula(equation)
            if path is None:
                counts['retained_formula_groups'] += 1
                counts['reason: '+reason] += 1
                continue
            for child in list(equation):
                equation.remove(child)
            equation.append(path)
            counts['merged_formulas'] += 1
    text_after = [ET.tostring(e) for e in converted.iter() if local(e) == 'text']
    if text_before != text_after:
        raise ValueError('Ordinary text changed during preparation.')
    tags = Counter(local(e) for e in converted.iter())
    if tags['use'] or tags['image'] or tags['defs']:
        raise ValueError('References, raster content or definitions remain.')
    converted.set('version', '1.1')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(ET.tostring(converted, encoding='utf-8', xml_declaration=True))
    report = {'input': str(source.resolve()), 'output': str(output.resolve()),
              'ordinary_text_labels_preserved': len(text_after), 'counts': dict(counts),
              'output_elements': dict(tags), 'scope': 'SVG structure only; render and review separately. No PowerPoint import test.'}
    if report_path:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--no-merge-math', action='store_true')
    args = parser.parse_args()
    try:
        report = prepare(args.input, args.output, args.report, not args.no_merge_math)
    except (ValueError, ET.ParseError, OSError) as error:
        parser.exit(1, f'Cannot prepare SVG: {error}\n')
    print(json.dumps(report, ensure_ascii=False))
