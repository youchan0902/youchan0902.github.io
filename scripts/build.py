from pathlib import Path
from html import escape as e
import json, shutil, hashlib, re

ROOT=Path(__file__).resolve().parents[1]
BASE_DIST=ROOT/'dist';BASE_DIST.mkdir(exist_ok=True)
DIST=BASE_DIST
LANG='ko'
UI_EN=json.loads((ROOT/'content/ui.en.json').read_text('utf-8'))
for name in ['site.css','site.js']:
    shutil.copy2(ROOT/'src'/name,DIST/name)
VERSION=hashlib.sha256((ROOT/'src/site.css').read_bytes()+(ROOT/'src/site.js').read_bytes()).hexdigest()[:10]


def contact_links():
    return '<address class="profile-contact" aria-label="연락처"><a href="mailto:dbcks0902@skku.edu">dbcks0902@skku.edu</a><a href="mailto:dbcks0902@naver.com">dbcks0902@naver.com</a><a href="tel:+821035783364">+82 10-3578-3364</a></address>'

def write_page(filename, html):
    other=('en/'+filename) if LANG=='ko' else ('../'+filename)
    language='en' if LANG=='ko' else 'ko'
    switch='<a class="language-switch" href="'+other+'" hreflang="'+language+'" lang="'+language+'" aria-label="'+('Switch to English' if LANG=='ko' else 'Switch to Korean')+'">'+('English' if LANG=='ko' else 'KO')+'</a>'
    html=html.replace('<!--LANG_SWITCH-->',switch)
    html=html.replace('</head>','<link rel="alternate" hreflang="ko" href="https://youchan0902.github.io/'+filename+'"><link rel="alternate" hreflang="en" href="https://youchan0902.github.io/en/'+filename+'"></head>')
    if LANG=='en':
        html=html.replace('<html lang="ko">','<html lang="en">')
        for source,target in sorted(UI_EN.items(),key=lambda pair:len(pair[0]),reverse=True):
            html=html.replace(e(source,quote=True),e(target,quote=True))
        html=re.sub(r'((?:src|href|poster|data-lightbox)=")(?=(?:assets/|media/|documents/|fonts/|site\.css|site\.js|favicon\.svg))',r'\1../',html)
        html=html.replace('<h2>Youchan Choi<br><span lang="en">Youchan Choi</span></h2>','<h2>Youchan Choi</h2>')
        html=html.replace('<h1>Youchan Choi<span lang="en">Youchan Choi</span></h1>','<h1>Youchan Choi</h1>')
        assert not re.search('[가-힣]',html), 'Untranslated Korean text in '+filename
    (DIST/filename).write_text(html,encoding='utf-8')

def head(title,description):
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(description,quote=True)}"><meta name="theme-color" content="#183536"><meta property="og:type" content="website"><meta property="og:title" content="{e(title,quote=True)}"><meta property="og:description" content="{e(description,quote=True)}"><title>{e(title)}</title><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="preload" href="fonts/PretendardVariable.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="site.css?v={VERSION}"><script src="site.js?v={VERSION}" defer></script></head><body><a class="skip" href="#main">본문으로 건너뛰기</a>'''

def nav():
    return '''<header class="site-header"><nav class="wrap nav" aria-label="주요 메뉴"><a class="brand" href="index.html">최유찬<small>YOUCHAN CHOI / RESEARCH</small></a><button class="menu-toggle" aria-expanded="false" aria-controls="nav-links">메뉴 +</button><div class="nav-links" id="nav-links"><a href="index.html#research">연구 활동</a><a href="index.html#approach">연구 과정</a><a href="cv.html">연구자 소개 · CV</a><a class="github-link" href="https://github.com/youchan0902" target="_blank" rel="noopener noreferrer">GitHub ↗</a><!--LANG_SWITCH--></div></nav></header>'''

def footer():
    return '''<footer class="wrap footer"><span>© 2026 YOUCHAN CHOI · TACTILE SENSING &amp; ROBOTICS</span><a href="https://github.com/youchan0902" target="_blank" rel="noopener noreferrer">GitHub / youchan0902 ↗</a></footer>'''

def tags(values):return '<div class="tags">'+''.join('<span>'+e(x)+'</span>' for x in values)+'</div>'
def paragraphs(values):return ''.join('<p>'+e(x)+'</p>' for x in values)

def card_image(project):
    if project.get('cardRotation') == 90:
        # Rotate the original raster only in the page, retaining its exact pixels.
        return '<svg class="rotated-research-image" viewBox="0 0 470 264" role="img" aria-label="로봇손의 손끝 촉각 센서와 내부 구조"><image href="assets/'+e(project['cardImage'])+'" width="264" height="470" transform="translate(470 0) rotate(90)"/></svg>'
    return img(project['cardImage'],project['heroCaption'])

def annotated_hand(source):
    return '<a class="annotated-hand" href="fingertip.html" aria-label="손끝에 장착한 3축 촉각 센서 연구 보기">'+img(source,'촉각 센서가 장착된 실제 AIDIN-Hand 로봇손',False)+'''<svg class="sensor-overlay" viewBox="0 0 1243 1266" aria-hidden="true"><ellipse cx="170" cy="690" rx="150" ry="200"/><path d="M310 765 L435 1100 L545 1100"/><circle cx="310" cy="765" r="7"/><rect x="540" y="1094" width="470" height="78" rx="5"/><text x="564" y="1144">3축 손끝 촉각 센서 ↗</text></svg></a>'''

def research_video(video):
    return '<figure class="video-figure"><video controls playsinline preload="none" poster="assets/'+e(video['poster'])+'" aria-label="'+e(video['title'],quote=True)+'"><source src="media/'+e(video['src'])+'" type="video/mp4"><p><a href="media/'+e(video['src'])+'">실험 영상 열기</a></p></video><figcaption>'+e(video['caption'])+'</figcaption></figure>'
def img(src,alt,lazy=True,cls=''):
    assert (BASE_DIST/'assets'/src).is_file(),src
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
        if 'video' in s:out+=research_video(s['video'])
        if 'scope' in s:out+='<div class="scope"><strong>연구 범위</strong><br>'+e(s['scope'])+'</div>'
        out+='</section>'
    refs=''.join('<p><a href="'+e(ref['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">'+e(ref['title'])+' ↗</a></p>' for ref in p.get('references',[]))
    out+='<div class="source-note"><span class="note-title">자료와 해석</span>'+e(p['sourceNote'])+refs+'</div></div></div></div></main>'
    nxt=PROJECTS[(index+1)%len(PROJECTS)]
    out+='<div class="next-project"><div class="wrap next-inner"><div class="eyebrow">NEXT PROJECT / '+nxt['number']+'</div><a href="'+nxt['id']+'.html">'+e(nxt['shortTitle'])+' ↗</a></div></div>'+footer()+lightbox()+'</body></html>'
    write_page(p['id']+'.html',out)

def cv_page():
    cv=json.loads((ROOT/('content/cv.en.json' if LANG=='en' else 'content/cv.json')).read_text('utf-8'))
    pdf='documents/CV_YouchanChoi.pdf'
    assert (BASE_DIST/pdf).is_file()
    out=head('연구자 소개 · CV | 최유찬',cv['summary'])+nav()
    out+='<main id="main" class="wrap cv-main"><a class="back" href="index.html">← 홈페이지</a><header class="cv-hero"><div><div class="eyebrow">RESEARCHER PROFILE / CURRICULUM VITAE</div><h1>'+e(cv['koreanName'])+'<span lang="en">'+e(cv['name'])+'</span></h1><p class="lead">'+e(cv['summary'])+'</p>'+contact_links()+'</div><div class="cv-intro"><span class="eyebrow">RESEARCH INTERESTS</span><h2>촉각 센서<br>로봇손<br>소프트 로보틱스</h2><p>성균관대학교 지능형로봇학과<br>석사과정</p></div></header>'
    out+='<div class="cv-actions"><a class="button" href="'+pdf+'" target="_blank" rel="noopener noreferrer">CV PDF 보기 ↗</a><a class="text-link" href="'+pdf+'" download="CV_YouchanChoi.pdf">PDF 다운로드 ↓</a><a class="text-link" href="#cv-document">이 페이지에서 보기 ↓</a></div>'
    out+='<div class="cv-grid"><section class="cv-section"><div class="eyebrow">EDUCATION</div><h2>학력</h2>'
    for item in cv['education']:
        out+='<article class="cv-entry"><span class="cv-period">'+e(item['period'])+'</span><h3>'+e(item['school'])+'</h3><p>'+e(item['degree'])+'</p><p class="cv-detail">'+e(item['detail'])+'</p></article>'
    out+='</section><section class="cv-section"><div class="eyebrow">TOOLS & SKILLS</div><h2>사용 기술</h2>'+tags(cv['skills'])+'<div class="cv-conferences"><h3>학회 활동</h3><ul>'+''.join('<li>'+e(a)+'</li>' for a in cv['activities'])+'</ul></div></section></div>'
    out+='<section class="cv-section"><div class="eyebrow">RESEARCH EXPERIENCE</div><h2>연구 경험</h2><div class="cv-experience">'
    for item in cv['experience']:
        out+='<article class="cv-entry"><span class="cv-period">'+e(item['period'])+'</span><h3>'+e(item['title'])+'</h3><p>'+e(item['description'])+'</p>'
        if item.get('status'):out+='<p class="cv-detail">'+e(item['status'])+'</p>'
        if item.get('link'):out+='<a class="text-link" href="'+e(item['link'])+'">관련 연구 보기 ↗</a>'
        out+='</article>'
    out+='</div></section><section class="cv-section cv-document" id="cv-document"><div class="section-head"><div><div class="eyebrow">CURRICULUM VITAE / PDF</div><h2>CV 원문</h2></div><a class="text-link" href="'+pdf+'" target="_blank" rel="noopener noreferrer">PDF로 크게 보기 ↗</a></div><a class="cv-preview" href="'+pdf+'" target="_blank" rel="noopener noreferrer" aria-label="최유찬 CV PDF 새 탭에서 열기">'+img('cv-preview.png','최유찬 영문 CV. 학력, 연구 경험, 학회 활동과 사용 기술을 담은 원문.')+'</a></section></main>'+footer()+'</body></html>'
    write_page('cv.html',out)

for LANG in ['ko','en']:
    DIST=BASE_DIST if LANG=='ko' else BASE_DIST/'en'
    DIST.mkdir(exist_ok=True)
    PROJECTS=json.loads((ROOT/('content/projects.en.json' if LANG=='en' else 'content/projects.json')).read_text('utf-8'))
    hero='hand-hero-white.png'
    home=head('최유찬 | Tactile Sensing & Robotics','최유찬의 촉각 센서와 로봇 연구. 3축 손끝 센서, 그리퍼 센서, 웨어러블 로봇 장갑과 프린징 효과 기반 손바닥 센서 설계를 소개합니다.')+nav()
    home+='''<main id="main"><div class="wrap"><a class="profile-entry" href="cv.html"><span>연구자 소개<small>YOUCHAN CHOI · CV</small></span><b aria-hidden="true">↗</b></a>'''+contact_links()+'''<section class="home-hero" aria-labelledby="hero-title"><div class="hero-copy"><div class="eyebrow">TACTILE SENSING &amp; ROBOTICS</div><h1 id="hero-title">로봇의 손끝에<br>감각을 더하다<em>.</em></h1><p class="lead">촉각 센서로 접촉하는 힘과 위치를 측정합니다.<br>센서와 회로를 설계·제작하고,<br>로봇손과 그리퍼에서 동작을 확인합니다.</p><div class="hero-actions"><a class="button" href="#research">연구 살펴보기 <span aria-hidden="true">↘</span></a><a class="text-link" href="cv.html">연구자 소개 · CV <span aria-hidden="true">↗</span></a></div></div><div class="hero-art"><span class="axis-label">Fx / Fy / Fz + CONTACT POSITION</span>'''+annotated_hand(hero)+'''<span class="image-credit">AIDIN-HAND / FINGERTIP TACTILE SENSOR<br>PROTOTYPE / BACKGROUND EDITED</span></div></section></div><div class="research-band"><div class="wrap band-inner"><div><span>RESEARCH FOCUS</span><strong>접촉을 측정하고, 활용하는 연구</strong></div><div><span>SENSE</span><strong>3축 힘 · 접촉 위치</strong></div><div><span>BUILD</span><strong>센서 구조 · 전장 설계</strong></div><div><span>INTERACT</span><strong>로봇손 · 그리퍼 · 장갑</strong></div></div></div><section class="wrap section" id="research"><div class="section-head"><div><div class="eyebrow">SELECTED RESEARCH / 01—04</div><h2>주요 연구 활동</h2></div><p>손끝·그리퍼 촉각 센서, 웨어러블 장갑과 손바닥 센서 설계를 소개합니다.</p></div><div class="project-list">'''
    for p in PROJECTS:
        home+='<article class="project-row"><span class="project-number">'+p['number']+' /</span><div class="project-copy"><div class="eyebrow">'+p['label']+'</div><h3><a href="'+p['id']+'.html">'+e(p['title']).replace('\n','<br>')+'</a></h3><p>'+e(p['card'])+'</p><span class="status">'+e(p['stage'])+'</span>'+tags(p['tags'])+'<a class="text-link" href="'+p['id']+'.html">연구 자세히 보기 <span aria-hidden="true">↗</span></a></div><a class="project-visual '+p['cardClass']+'" href="'+p['id']+'.html" aria-label="'+e(p['shortTitle'],quote=True)+' 자세히 보기">'+card_image(p)+'<span class="visual-index">'+p['number']+' / '+('SIMULATION & CAD' if p['id']=='palm' else 'RESEARCH ARCHIVE')+'</span></a></article>'
    home+='''</div></section><section class="wrap section approach" id="approach"><div class="section-head"><div><div class="eyebrow">FROM DESIGN TO EXPERIMENT</div><h2>하드웨어와 실험을 잇는 과정</h2></div><p>센서 구조 설계에서 시작해 제작, 기준 센서 비교와 로봇 적용으로 이어갑니다.</p></div><div class="steps"><div class="step"><b>01 / DESIGN</b><h3>구조·전극 설계</h3><p>접촉 하중이 센서에 전달되는 구조와 전극 배치를 검토하고 시뮬레이션으로 비교합니다.</p></div><div class="step"><b>02 / BUILD</b><h3>제작·전장 통합</h3><p>실리콘 성형, PCB 제작과 조립을 거쳐 측정·처리·통신 회로를 통합합니다.</p></div><div class="step"><b>03 / CALIBRATE</b><h3>계측·캘리브레이션</h3><p>기준 센서와 비교하고 훈련과 평가 데이터를 나눠 힘·위치 추정 성능을 확인합니다.</p></div><div class="step"><b>04 / APPLY</b><h3>로봇 적용·시험</h3><p>센서를 손가락과 그리퍼에 장착하고 실제 접촉과 파지 과정에서 출력을 확인합니다.</p></div></div></section><section class="about" id="about"><div class="wrap about-grid"><div><div class="eyebrow">ABOUT / YOUCHAN CHOI</div><h2>최유찬<br><span lang="en">Youchan Choi</span></h2><p class="affiliation">성균관대학교 지능형로봇학과 · 석사과정<br>Department of Intelligent Robotics<br>Sungkyunkwan University</p><a class="text-link" href="https://github.com/youchan0902" target="_blank" rel="noopener noreferrer">GitHub 프로필 <span aria-hidden="true">↗</span></a></div><div class="about-copy"><p>로봇이 접촉 상태를 파악할 수 있도록 촉각 센서의 구조와 회로를 설계합니다. 정전용량 신호에서 힘과 접촉 위치를 추정하고, 기준 센서와 비교해 성능을 평가합니다.</p><p>소형 손끝 센서의 3축 측정 원리를 그리퍼 접촉면으로 확장했으며, 손바닥용 전극 구조도 시뮬레이션하고 있습니다. 웨어러블 로봇 연구에서는 장력·파지력 측정 장치와 구동 제어를 담당했습니다.</p><div class="research-title"><span>MASTER'S THESIS RESEARCH</span><p lang="en">Capacitive Tactile Sensors for Three-Axis Force and Contact-Position Estimation in Robotic Applications</p></div></div></div></section></main>'''+footer()+'</body></html>'
    write_page('index.html',home)
    for index,p in enumerate(PROJECTS):project_page(p,index)
    cv_page()
(BASE_DIST/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#183536"/><path d="M32 12 49 22 32 32 15 22Z M15 27 29 35 29 52 15 43Z M49 27 35 35 35 52 49 43Z" fill="#c8da91"/></svg>',encoding='utf-8')
(BASE_DIST/'.nojekyll').write_text('',encoding='utf-8')
print('Built Korean and English versions: 12 pages total.')
