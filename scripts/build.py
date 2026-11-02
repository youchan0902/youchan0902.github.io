from pathlib import Path
from html import escape as e
import json, shutil, hashlib

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist';DIST.mkdir(exist_ok=True)
PROJECTS=json.loads((ROOT/'content/projects.json').read_text(encoding='utf-8'))
for name in ['site.css','site.js']:
    shutil.copy2(ROOT/'src'/name,DIST/name)
VERSION=hashlib.sha256((ROOT/'src/site.css').read_bytes()+(ROOT/'src/site.js').read_bytes()).hexdigest()[:10]

def head(title,description):
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(description,quote=True)}"><meta name="theme-color" content="#183536"><meta property="og:type" content="website"><meta property="og:title" content="{e(title,quote=True)}"><meta property="og:description" content="{e(description,quote=True)}"><title>{e(title)}</title><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="site.css?v={VERSION}"><script src="site.js?v={VERSION}" defer></script></head><body><a class="skip" href="#main">본문으로 건너뛰기</a>'''

def nav():
    return '''<header class="site-header"><nav class="wrap nav" aria-label="주요 메뉴"><a class="brand" href="index.html">최유찬<small>YOUCHAN CHOI / RESEARCH</small></a><button class="menu-toggle" aria-expanded="false" aria-controls="nav-links">메뉴 +</button><div class="nav-links" id="nav-links"><a href="index.html#research">연구 활동</a><a href="index.html#approach">연구 과정</a><a href="index.html#about">소개</a><a class="github-link" href="https://github.com/youchan0902" target="_blank" rel="noopener noreferrer">GitHub ↗</a></div></nav></header>'''

def footer():
    return '''<footer class="wrap footer"><span>© 2026 YOUCHAN CHOI · TACTILE SENSING &amp; ROBOTICS</span><a href="https://github.com/youchan0902" target="_blank" rel="noopener noreferrer">GitHub / youchan0902 ↗</a></footer>'''

def tags(values):return '<div class="tags">'+''.join('<span>'+e(x)+'</span>' for x in values)+'</div>'
def paragraphs(values):return ''.join('<p>'+e(x)+'</p>' for x in values)
def img(src,alt,lazy=True,cls=''):
    assert (DIST/'assets'/src).is_file(),src
    return f'<img src="assets/{e(src)}" alt="{e(alt,quote=True)}" '+('loading="lazy" decoding="async"' if lazy else 'fetchpriority="high"')+(f' class="{cls}"' if cls else '')+'>'

def gallery(items):
    out='<div class="gallery">'
    for item in items:
        out+=f'<figure class="{"full" if item.get("full") else ""}"><button class="image-button {"clean" if item.get("clean") else ""}" data-lightbox="assets/{e(item["src"])}" aria-label="{e(item["caption"],quote=True)} — 이미지 확대">'+img(item['src'],item['caption'])+'<span class="zoom-mark" aria-hidden="true">+</span></button><figcaption>'+e(item['caption'])+'</figcaption></figure>'
    return out+'</div>'

def lightbox():
    return '''<dialog class="lightbox" aria-label="연구 이미지 확대 보기"><div class="lightbox-head"><span class="lightbox-count" aria-live="polite"></span><div class="lightbox-actions"><a class="lightbox-original" target="_blank" rel="noopener noreferrer">원본 보기 ↗</a><button class="close-lightbox">닫기 ×</button></div></div><div class="lightbox-body"><img alt=""></div><div class="lightbox-foot"><p class="lightbox-caption" aria-live="polite"></p><div class="lightbox-controls"><button data-prev aria-label="이전 이미지">←</button><button data-next aria-label="다음 이미지">→</button></div></div></dialog>'''

def project_page(p,index):
    out=head(p['shortTitle']+' | 최유찬',p['intro'])+nav()
    out+='<main id="main"><div class="wrap"><a class="back" href="index.html#research">← 전체 연구 보기</a><header class="project-hero"><div><div class="eyebrow">'+p['number']+' / '+p['label']+'</div><h1>'+e(p['title']).replace('\n','<br>')+'</h1><p class="lead">'+e(p['intro'])+'</p>'+tags(p['tags'])+'</div><figure class="hero-figure '+('wide' if p.get('heroWide') else '')+'">'+img(p['hero'],p['heroCaption'],False)+'<figcaption>'+e(p['heroCaption'])+'</figcaption></figure></header></div>'
    out+='<div class="research-band"><div class="wrap project-meta"><strong>'+e(p['stage'])+'</strong><span>RESEARCH PROJECT / '+p['number']+'</span></div></div><div class="wrap"><div class="metrics">'
    for value,label,detail in p['metrics']:
        out+='<div class="metric"><div class="metric-label">'+e(label)+'</div><div class="metric-value">'+e(value)+'</div><div class="metric-detail">'+e(detail)+'</div></div>'
    out+='</div><div class="project-body"><aside class="toc" aria-label="이 연구의 목차"><strong>IN THIS PROJECT</strong>'
    out+=''.join(f'<a href="#{s["id"]}">{i+1:02d} / {e(s["title"])}</a>' for i,s in enumerate(p['sections']))+'</aside><div>'
    for i,s in enumerate(p['sections']):
        out+=f'<section class="story-section" id="{s["id"]}"><span class="section-index">{i+1:02d} / RESEARCH NOTES</span><h2>{e(s["title"])}</h2>'+paragraphs(s['paragraphs'])
        if 'specs' in s:out+='<dl class="spec-list">'+''.join('<div><dt>'+e(k)+'</dt><dd>'+e(v)+'</dd></div>' for k,v in s['specs'])+'</dl>'
        if 'note' in s:out+='<p class="small" style="margin-top:18px">'+e(s['note'])+'</p>'
        if 'flow' in s:out+='<div class="process-flow" aria-label="연구 절차">'+'<i aria-hidden="true">→</i>'.join('<span>'+e(x)+'</span>' for x in s['flow'])+'</div>'
        if 'table' in s:
            t=s['table'];out+='<div class="data-scroll" tabindex="0" role="region" aria-label="'+e(t['caption'],quote=True)+'"><table class="data-table"><caption>'+e(t['caption'])+'</caption><thead><tr>'+''.join('<th scope="col">'+e(v)+'</th>' for v in t['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+e(v)+'</td>' for v in row)+'</tr>' for row in t['rows'])+'</tbody></table></div>'
        if 'after' in s:out+=paragraphs(s['after'])
        if 'figures' in s:out+=gallery(s['figures'])
        if 'scope' in s:out+='<div class="scope"><strong>연구 범위</strong><br>'+e(s['scope'])+'</div>'
        out+='</section>'
    refs=''.join('<p><a href="'+e(ref['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">'+e(ref['title'])+' ↗</a></p>' for ref in p.get('references',[]))
    out+='<div class="source-note"><span class="note-title">자료와 해석</span>'+e(p['sourceNote'])+refs+'</div></div></div></div></main>'
    nxt=PROJECTS[(index+1)%len(PROJECTS)]
    out+='<div class="next-project"><div class="wrap next-inner"><div class="eyebrow">NEXT PROJECT / '+nxt['number']+'</div><a href="'+nxt['id']+'.html">'+e(nxt['shortTitle'])+' ↗</a></div></div>'+footer()+lightbox()+'</body></html>'
    (DIST/(p['id']+'.html')).write_text(out,encoding='utf-8')

hero='hand-hero-clean.png' if (DIST/'assets/hand-hero-clean.png').exists() else 'hand-hero.png'
home=head('최유찬 | Tactile Sensing & Robotics','최유찬의 촉각 센서와 로봇 연구. 3축 손끝 센서, 그리퍼 센서, 웨어러블 로봇 장갑과 프린징 효과 기반 손바닥 센서 설계를 소개합니다.')+nav()
home+='''<main id="main"><div class="wrap"><section class="home-hero" aria-labelledby="hero-title"><div class="hero-copy"><div class="eyebrow">TACTILE SENSING &amp; ROBOTICS</div><h1 id="hero-title">로봇의 손끝에<br>감각을 더하다<em>.</em></h1><p class="lead">만지는 힘과 위치를 측정하고,<br>그 정보를 로봇의 동작으로 연결합니다.<br>센서 구조부터 회로, 캘리브레이션과 로봇 실험까지.</p><div class="hero-actions"><a class="button" href="#research">연구 살펴보기 <span aria-hidden="true">↘</span></a><a class="text-link" href="#about">연구자 소개 <span aria-hidden="true">↗</span></a></div></div><div class="hero-art"><span class="axis-label">Fx / Fy / Fz + CONTACT POSITION</span>'''+img(hero,'촉각 센서가 장착된 실제 AIDIN-Hand 로봇손',False)+'''<span class="image-credit">AIDIN-HAND / FINGERTIP TACTILE SENSOR<br>PROTOTYPE / BACKGROUND EDITED</span></div></section></div><div class="research-band"><div class="wrap band-inner"><div><span>RESEARCH FOCUS</span><strong>접촉을 측정하고, 활용하는 연구</strong></div><div><span>SENSE</span><strong>3축 힘 · 접촉 위치</strong></div><div><span>BUILD</span><strong>센서 구조 · 전장 설계</strong></div><div><span>INTERACT</span><strong>로봇손 · 그리퍼 · 장갑</strong></div></div></div><section class="wrap section" id="research"><div class="section-head"><div><div class="eyebrow">SELECTED RESEARCH / 01—04</div><h2>주요 연구 활동</h2></div><p>직접 제작한 하드웨어와 실제 실험을 중심으로 연구를 소개합니다. 각 프로젝트에서 설계와 검증이 어디까지 진행되었는지 함께 정리했습니다.</p></div><div class="project-list">'''
for p in PROJECTS:
    home+='<article class="project-row"><span class="project-number">'+p['number']+' /</span><div class="project-copy"><div class="eyebrow">'+p['label']+'</div><h3><a href="'+p['id']+'.html">'+e(p['title']).replace('\n','<br>')+'</a></h3><p>'+e(p['card'])+'</p><span class="status">'+e(p['stage'])+'</span>'+tags(p['tags'])+'<a class="text-link" href="'+p['id']+'.html">연구 자세히 보기 <span aria-hidden="true">↗</span></a></div><a class="project-visual '+p['cardClass']+'" href="'+p['id']+'.html" aria-label="'+e(p['shortTitle'],quote=True)+' 자세히 보기">'+img(p['cardImage'],p['heroCaption'] if p['id']!='fingertip' else '로봇손에 장착된 손끝 촉각 센서와 센서 구조')+'<span class="visual-index">'+p['number']+' / '+('SIMULATION & CAD' if p['id']=='palm' else 'RESEARCH ARCHIVE')+'</span></a></article>'
home+='''</div></section><section class="wrap section approach" id="approach"><div class="section-head"><div><div class="eyebrow">FROM DESIGN TO EXPERIMENT</div><h2>하드웨어와 실험을 잇는 과정</h2></div><p>접촉면의 변형, 전기적 신호, 추정 알고리즘과 로봇 동작을 하나의 실험 흐름으로 연결합니다.</p></div><div class="steps"><div class="step"><b>01 / DESIGN</b><h3>구조·전극 설계</h3><p>접촉 하중이 센서에 전달되는 구조와 전극 배치를 검토하고 시뮬레이션으로 비교합니다.</p></div><div class="step"><b>02 / BUILD</b><h3>제작·전장 통합</h3><p>실리콘 성형, PCB 제작과 조립을 거쳐 측정·처리·통신 회로를 통합합니다.</p></div><div class="step"><b>03 / CALIBRATE</b><h3>계측·캘리브레이션</h3><p>기준 센서와 비교하고 훈련과 평가 데이터를 나눠 힘·위치 추정 성능을 확인합니다.</p></div><div class="step"><b>04 / APPLY</b><h3>로봇 적용·시험</h3><p>센서를 손가락과 그리퍼에 장착하고 실제 접촉과 파지 과정에서 출력을 확인합니다.</p></div></div></section><section class="about" id="about"><div class="wrap about-grid"><div><div class="eyebrow">ABOUT / YOUCHAN CHOI</div><h2>최유찬<br><span lang="en">Youchan Choi</span></h2><p class="affiliation">성균관대학교 지능형로봇학과 · 석사과정<br>Department of Intelligent Robotics<br>Sungkyunkwan University</p><a class="text-link" href="https://github.com/youchan0902" target="_blank" rel="noopener noreferrer">GitHub 프로필 <span aria-hidden="true">↗</span></a></div><div class="about-copy"><p>촉각 센서와 로봇 응용을 연구합니다. 센서의 구조와 전장을 설계하고, 신호를 취득·분석해 접촉 힘과 위치를 추정하는 방법을 다룹니다.</p><p>손끝 센서를 로봇손에 적용하는 연구에서 시작해 더 넓은 그리퍼 접촉면과 손바닥 전극 설계로 범위를 넓히고 있습니다. 웨어러블 로봇 연구에서는 장력·파지력 측정 장치와 구동 제어를 담당했습니다.</p><div class="research-title"><span>MASTER'S THESIS RESEARCH</span><p lang="en">Capacitive Tactile Sensors for Three-Axis Force and Contact-Position Estimation in Robotic Applications</p></div></div></div></section></main>'''+footer()+'</body></html>'
(DIST/'index.html').write_text(home,encoding='utf-8')
for index,p in enumerate(PROJECTS):project_page(p,index)
(DIST/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#183536"/><path d="M32 12 49 22 32 32 15 22Z M15 27 29 35 29 52 15 43Z M49 27 35 35 35 52 49 43Z" fill="#c8da91"/></svg>',encoding='utf-8')
(DIST/'.nojekyll').write_text('',encoding='utf-8')
print('Built index + 4 research pages with shared styles and accessible image viewer.')
