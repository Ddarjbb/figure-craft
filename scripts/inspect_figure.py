"""Inspect SVG/PDF structure and optionally render color previews at two sizes."""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

SVG='{http://www.w3.org/2000/svg}'

def inspect(args):
    report={'issues':[],'scope':'Structural checks; scientific content and visual readability require review.'}
    if args.svg:
        path=Path(args.svg).resolve();root=ET.parse(path).getroot()
        if root.tag!=SVG+'svg':report['issues'].append('Input root is not SVG.')
        report['svg']={'path':str(path),'width':root.get('width'),'height':root.get('height'),
            'viewBox':root.get('viewBox'),'raster_elements':len(root.findall('.//'+SVG+'image')),
            'foreign_objects':len(root.findall('.//'+SVG+'foreignObject')),
            'live_text_elements':len(root.findall('.//'+SVG+'text')),
            'latex_label_groups':sum('data-latex' in e.attrib for e in root.iter())}
        if args.require_vector and report['svg']['raster_elements']:
            report['issues'].append('SVG contains raster image elements.')
    if args.pdf:
        try:import fitz
        except ImportError:raise SystemExit('PDF inspection requires PyMuPDF: python -m pip install PyMuPDF')
        pages=[]
        with fitz.open(args.pdf) as doc:
            for i,page in enumerate(doc):
                fonts=[]
                for f in page.get_fonts():
                    try:embedded=bool(doc.extract_font(f[0])[3])
                    except Exception:embedded=False
                    fonts.append({'name':f[3],'type':f[2],'embedded':embedded})
                spans=[s for b in page.get_text('dict')['blocks'] if 'lines' in b
                       for line in b['lines'] for s in line['spans'] if s['text'].strip()]
                fs=sorted(s['size'] for s in spans)
                outside=[{'text':s['text'],'bbox':list(s['bbox'])} for s in spans
                         if not (page.rect+(-.5,-.5,.5,.5)).contains(fitz.Rect(s['bbox']))]
                p={'page':i+1,'width_mm':page.rect.width*25.4/72,'height_mm':page.rect.height*25.4/72,
                   'raster_images':len(page.get_images()),'fonts':fonts,
                   'live_text_min_pt':min(fs) if fs else None,
                   'live_text_median_pt':fs[len(fs)//2] if fs else None,
                   'live_text_outside_page':outside,
                   'font_metric_scope':'Live PDF text only; outlined mathematical glyphs are not measured.'}
                if args.require_vector and p['raster_images']:
                    report['issues'].append(f'PDF page {i+1} contains raster images.')
                if any(not f['embedded'] for f in fonts):
                    report['issues'].append(f'PDF page {i+1} has fonts without embedded font data.')
                if outside:report['issues'].append(f'PDF page {i+1} has live text outside the page.')
                for key,target in [('width_mm',args.width_mm),('height_mm',args.height_mm)]:
                    if target is not None and abs(p[key]-target)>.05:
                        report['issues'].append(f'PDF page {i+1} {key} differs from the requested value.')
                if args.render_dir:
                    folder=Path(args.render_dir);folder.mkdir(parents=True,exist_ok=True)
                    for name,width in [('detail',1400),('print',660)]:
                        pix=page.get_pixmap(matrix=fitz.Matrix(width/page.rect.width,width/page.rect.width),alpha=False)
                        out=folder/f'page_{i+1}_{name}.png';pix.save(out)
                pages.append(p)
        report['pdf']={'path':str(Path(args.pdf).resolve()),'pages':pages}
    return report

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--svg');parser.add_argument('--pdf')
    parser.add_argument('--require-vector',action='store_true')
    parser.add_argument('--width-mm',type=float);parser.add_argument('--height-mm',type=float)
    parser.add_argument('--render-dir');parser.add_argument('--output')
    args=parser.parse_args()
    if not args.svg and not args.pdf:parser.error('Supply --svg and/or --pdf.')
    report=inspect(args)
    text=json.dumps(report,ensure_ascii=False,indent=2)
    if args.output:
        out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text,encoding='utf-8')
    else:print(text)
    print('Issues:',len(report['issues']))
    raise SystemExit(1 if report['issues'] else 0)

if __name__=='__main__':main()
