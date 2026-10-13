#!/usr/bin/env python3
"""Collect attributable RSS extracts. Never fabricate articles or silently publish a short edition."""
import json,re,html,calendar,datetime,urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo
import feedparser
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data';ED=DATA/'editions'
TODAY=datetime.datetime.now(ZoneInfo('Europe/Rome')).date()
SOURCES=[('HR','CIPD','https://www.cipd.org/en/about/news/rss/'),('HR','SHRM','https://www.shrm.org/rss/pages/news.aspx'),('AI','Google AI','https://blog.google/technology/ai/rss/'),('AI','OpenAI','https://openai.com/news/rss.xml'),('Startup','TechCrunch','https://techcrunch.com/category/startups/feed/'),('Economia','BBC Business','https://feeds.bb.co.uk/news/business/rss.xml'),('Scienza','NASA','https://www.nasa.gov/feed/'),('Scienza','Nature','https://www.nature.com/nature.rss'),('Cultura','The Guardian Culture','https://www.theguardian.com/culture/rss'),('Sport','BBC Sport','https://feeds.bbci.co.uk/sport/rss.xml'),('Curiosità','Atlas Obscura','https://www.atlasobscura.com/feeds/latest'),('AI','MIT Technology Review','https://www.technologyreview.com/feed/')]
def clean(x):return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',x or ''))).strip()
def date_of(entry):
 for field in ('published_parsed','updated_parsed'):
  p=entry.get(field)
  if p:
   try:return datetime.datetime.fromtimestamp(calendar.timegm(p),datetime.timezone.utc).date()
   except (ValueError,OverflowError):pass
 return None
def get(cat,name,url):
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'LaVariabile/2.0 RSS collector'})
  with urllib.request.urlopen(req,timeout=12) as resp:raw=resp.read(1200000)
  items=[]
  for e in feedparser.parse(raw).entries[:30]:
   d=date_of(e)
   if d is None or (TODAY-d).days not in (0,1,2):continue
   link=e.get('link','');title=clean(e.get('title',''));summary=clean(e.get('summary','') or e.get('description',''))
   if not link.startswith(('https://','http://')) or len(title)<15 or len(summary)<120:continue
   items.append({'category':cat,'title':title,'summary':summary[:850],'why':'','published':d.isoformat(),'source':name,'url':link})
  return items
 except Exception as exc:
  print(f'Fonte non disponibile: {name} ({type(exc).__name__})');return []
def main():
 ED.mkdir(parents=True,exist_ok=True);path=ED/(TODAY.isoformat()+'.json')
 if path.exists():print('Edizione già presente.');return
 idxfile=DATA/'index.json';idx=json.loads(idxfile.read_text(encoding='utf-8'))
 old=set()
 for d in idx.get('editions',[])[:15]:
  try:
   for a in json.loads((ED/(d+'.json')).read_text(encoding='utf-8')).get('articles',[]):old.add(a['url'].split('?')[0].rstrip('/'))
  except (FileNotFoundError,KeyError,ValueError):pass
 articles=[];seen=set();counts={};candidates=[]
 for cat,name,url in SOURCES:candidates.extend(get(cat,name,url))
 candidates.sort(key=lambda x:x['published'],reverse=True)
 for a in candidates:
  key=a['url'].split('?')[0].rstrip('/')
  if key in seen or key in old or counts.get(a['category'],0)>=4:continue
  articles.append(a);seen.add(key);counts[a['category']]=counts.get(a['category'],0)+1
  if len(articles)==12:break
 if len(articles)<10:print(f'Solo {len(articles)} articoli RSS idonei: mantengo ultima edizione.');return
 edition={'date':TODAY.isoformat(),'articles':articles,'outsideRadar':None,'idea':None,'watch':[],'editorialNote':'Estratti RSS attribuiti, non articoli originali verificati integralmente.'}
 temp=path.with_suffix('.tmp');temp.write_text(json.dumps(edition,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temp.replace(path)
 idx['editions']=[TODAY.isoformat()]+[d for d in idx.get('editions',[]) if d!=TODAY.isoformat()];idxfile.write_text(json.dumps(idx,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(f'Nuova edizione: {TODAY}, {len(articles)} articoli')
if __name__=='__main__':main()
