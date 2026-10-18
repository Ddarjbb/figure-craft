"""Real LaTeX (NewTX Math) to inline SVG paths, with editable TeX sources."""
from pathlib import Path
import hashlib
import html
import json
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
import fitz
from PIL import ImageFont
from matplotlib.font_manager import findfont,FontProperties

NS='http://www.w3.org/2000/svg'
ET.register_namespace('',NS)

class Typography:
    def __init__(self,base,sans='Arial'):
        self.base=Path(base)
        self.base.mkdir(parents=True,exist_ok=True)
        self.sans=sans
        self.labels=[]
        self.math={}
        self.audit=[]

    def label(self,x,y,text,size=19,weight='normal',anchor='start',fill='#202b3a'):
        text=str(text)
        if size<=0:raise ValueError('Label size must be positive.')
        if anchor not in ('start','middle','end'):raise ValueError('Unsupported text anchor.')
        family='Times New Roman' if re.match(r'^\([abc]\)',text) else self.sans
        token=f'<!--TYPO-LABEL-{len(self.labels)}-->'
        self.labels.append(dict(x=x,y=y,text=text,size=size,weight=weight,anchor=anchor,fill=fill,family=family))
        return token

    def _compile(self,expressions):
        folder=self.base/'math_source';folder.mkdir(exist_ok=True)
        expressions=list(dict.fromkeys(expressions))
        self.expressions=expressions
        if not expressions:
            (folder/'expressions.json').write_text('[]\n',encoding='utf-8')
            return
        digest=hashlib.sha256(('v2-tight-textstyle:'+json.dumps(expressions)).encode()).hexdigest()
        manifest=folder/'expressions.json'
        cache=folder/'metrics.json'
        if cache.exists() and json.loads(cache.read_text())['digest']==digest and (folder/'equations.pdf').is_file():
            data=json.loads(cache.read_text())
        else:
            if not shutil.which('pdflatex'):
                raise RuntimeError('pdflatex is required for math labels. Install a TeX distribution with standalone, amsmath, amssymb, newtxtext and newtxmath, and add its executables to PATH.')
            tex=[r'\documentclass[multi=eqscene,border=0pt]{standalone}',
                 r'\usepackage[T1]{fontenc}',r'\usepackage{amsmath,amssymb}',
                 r'\usepackage{newtxtext,newtxmath}',r'\newenvironment{eqscene}{}{}',
                 r'\newsavebox{\eqbox}',r'\begin{document}']
            for i,expr in enumerate(expressions):
                tex.extend([r'\begin{eqscene}',r'\sbox{\eqbox}{$\textstyle '+expr+r'$}',
                  rf'\typeout{{MATHDIM|{i}|\the\wd\eqbox|\the\ht\eqbox|\the\dp\eqbox}}',
                  r'\usebox{\eqbox}',r'\end{eqscene}'])
            tex.append(r'\end{document}')
            (folder/'equations.tex').write_text('%\n'.join(tex)+'\n',encoding='utf-8')
            proc=subprocess.run(['pdflatex','-no-shell-escape','-halt-on-error','-interaction=nonstopmode','equations.tex'],cwd=folder,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=100)
            (folder/'compile_stdout.txt').write_text(proc.stdout+'\n'+proc.stderr,encoding='utf-8')
            if proc.returncode:raise RuntimeError(proc.stdout[-5000:])
            dims={int(i):[float(w),float(h),float(d)] for i,w,h,d in re.findall(r'MATHDIM\|(\d+)\|([\d.]+)pt\|([\d.]+)pt\|([\d.]+)pt',proc.stdout)}
            if len(dims)!=len(expressions):raise RuntimeError('Incomplete LaTeX metrics; see math_source/compile_stdout.txt.')
            data=dict(digest=digest,dimensions=dims)
            cache.write_text(json.dumps(data,indent=2),encoding='utf-8')
        manifest.write_text(json.dumps([dict(id=i,latex=e) for i,e in enumerate(expressions)],ensure_ascii=False,indent=2),encoding='utf-8')
        for old in folder.glob('equation_*.svg'):
            if int(old.stem.split('_')[-1])>=len(expressions):old.unlink()
        with fitz.open(folder/'equations.pdf') as pdf:
            if len(pdf)!=len(expressions):raise RuntimeError('LaTeX page count does not match the expressions.')
            for i,(expr,page) in enumerate(zip(expressions,pdf)):
                # TeX points are 1/72.27 in; PDF/SVG points are 1/72 in.
                width,height,depth=data['dimensions'].get(str(i),data['dimensions'].get(i))
                conv=72/72.27
                raw=page.get_svg_image(text_as_path=True)
                (folder/f'equation_{i:03d}.svg').write_text(raw,encoding='utf-8')
                self.math[expr]=dict(svg=raw,width=width*conv,baseline=height*conv,height=page.rect.height)

    def resolve(self,svg):
        self.audit=[]
        expressions=[run[1:-1] for label in self.labels for run in re.split(r'(\$[^$]+\$)',label['text']) if run.startswith('$')]
        self._compile(expressions)
        for n,label in enumerate(self.labels):
            svg=svg.replace(f'<!--TYPO-LABEL-{n}-->',self._render(label,n))
        (self.base/'label_layout.json').write_text(json.dumps(self.audit,ensure_ascii=False,indent=2),encoding='utf-8')
        return svg

    def _render(self,label,n):
        size=label['size'];runs=[]
        requested=label['family']
        try:
            fontpath=findfont(FontProperties(family=requested,weight=label['weight']),fallback_to_default=False)
        except ValueError:
            fallback='DejaVu Serif' if requested=='Times New Roman' else 'DejaVu Sans'
            fontpath=findfont(FontProperties(family=fallback,weight=label['weight']))
        actual=FontProperties(fname=fontpath).get_name()
        font=ImageFont.truetype(fontpath,round(size*16))
        for run in re.split(r'(\$[^$]+\$)',label['text']):
            if not run:continue
            if run.startswith('$'):
                eq=self.math[run[1:-1]];scale=size/(10*72/72.27)
                runs.append(dict(math=True,text=run[1:-1],width=eq['width']*scale,eq=eq,scale=scale))
            else:runs.append(dict(math=False,text=run,width=font.getlength(run)/16))
        total=sum(r['width'] for r in runs)
        x=label['x']-({'middle':total/2,'end':total}.get(label['anchor'],0))
        start=x;out=[f'<g data-label-id="{n}" aria-label="{html.escape(label["text"],quote=True)}">']
        for j,run in enumerate(runs):
            if run['math']:
                eq=run['eq'];root=ET.fromstring(eq['svg']);prefix=f'm{n}_{j}_'
                for el in root.iter():
                    if el.get('id'):el.set('id',prefix+el.get('id'))
                    for attr,value in list(el.attrib.items()):
                        if attr.endswith('href') and value.startswith('#'):el.set(attr,'#'+prefix+value[1:])
                        elif 'url(#' in value:el.set(attr,re.sub(r'url\(#([^)]*)\)',lambda m:'url(#'+prefix+m.group(1)+')',value))
                        if attr in ['fill','stroke'] and value in ['#000000','#000','black','rgb(0%, 0%, 0%)']:el.set(attr,label['fill'])
                body=''.join(ET.tostring(el,encoding='unicode') for el in root)
                ty=label['y']-eq['baseline']*run['scale']
                out.append(f'<g data-latex="{html.escape(run["text"],quote=True)}" fill="{label["fill"]}" transform="translate({x:.5f},{ty:.5f}) scale({run["scale"]:.8f})">{body}</g>')
            else:
                out.append(f'<text xml:space="preserve" x="{x:.4f}" y="{label["y"]}" font-family="{html.escape(actual,quote=True)}" font-size="{size}" font-weight="{html.escape(label["weight"],quote=True)}" fill="{html.escape(label["fill"],quote=True)}">{html.escape(run["text"])}</text>')
            x+=run['width']
        out.append('</g>')
        self.audit.append({**label,'actual_family':actual,'font_fallback':actual!=requested,'rendered_x_min':start,'rendered_x_max':x,'math_runs':sum(r['math'] for r in runs)})
        return '\n'.join(out)

def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--demo',action='store_true',help='Render a mixed-text/vector-math example.')
    parser.add_argument('--output-dir',type=Path,default=Path('math_demo'))
    parser.add_argument('--font',default='DejaVu Sans',help='Installed ordinary-label font family.')
    args=parser.parse_args()
    if not args.demo:parser.error('Use --demo, or import Typography in a drawing script.')
    typo=Typography(args.output_dir,args.font)
    labels=[typo.label(28,38,'User vector: $\\mathbf{z}_u\\in\\mathbb{R}^{d}$',18),
            typo.label(28,82,'Score: $s(u,i)=\\mathbf{z}_u^{\\mathsf{T}}\\mathbf{z}_i$',18),
            typo.label(28,139,r'$\displaystyle\mathcal{L}=-\log\frac{\exp(s^{+})}{\sum_j\exp(s_j)}$',18)]
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="150mm" height="65mm" viewBox="0 0 430 185"><rect width="430" height="185" fill="white"/>'+''.join(labels)+'</svg>'
    output=typo.resolve(svg)
    target=args.output_dir/'demo.svg'
    target.write_text(output,encoding='utf-8')
    print(f'Created {target.resolve()} and math_source/ with LaTeX inputs and vector equations.')

if __name__=='__main__':main()
