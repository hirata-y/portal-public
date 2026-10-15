/** Japanese query boundary adapter. Native vendor JS/WASM and native result objects stay intact. */
// A dedicated realm uses Pagefind's built-in no-Intl.Segmenter fallback.
// Never change Intl on the application page or edit the vendor bundle.
let worker,serial=0;const pending=new Map();
function request(query,options) {
 if(!worker){worker=new Worker(new URL('./pagefind-ja-worker.js',import.meta.url),{type:'module'});
 worker.onmessage=({data:m})=>{const p=pending.get(m.id);if(!p)return;pending.delete(m.id);clearTimeout(p.timer);m.error?p.reject(new Error(m.error)):p.resolve(m.response);};
 worker.onerror=()=>{for(const p of pending.values()){clearTimeout(p.timer);p.reject(new Error('日本語検索Workerを起動できません。'));}pending.clear();worker.terminate();worker=undefined;};}
 return new Promise((resolve,reject)=>{const id=++serial;const timer=setTimeout(()=>{pending.delete(id);reject(new Error('検索がタイムアウトしました。'));},30000);pending.set(id,{resolve,reject,timer});worker.postMessage({id,query,options});});
}
const JAPANESE=/^[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}\p{M}ー]+$/u;
const RUN=/[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}\p{M}ー]+/gu;
const MAX_VARIANTS=32;
let lexicon;
async function terms() {
  if(!lexicon)lexicon=fetch(new URL('./ja-terms.json',import.meta.url)).then(async r=>{
    if(!r.ok)throw new Error('日本語検索索引を読み込めません。');
    const j=await r.json();
    if(j.schema_version!==1||j.language!=='ja'||!Array.isArray(j.terms)||j.terms.length>50000||j.terms.some(t=>typeof t!=='string'||t.length>256||!JAPANESE.test(t)))throw new Error('日本語検索索引の形式を確認できません。');
    const map=new Map();
    for(const t of j.terms){const key=Array.from(t)[0];if(!map.has(key))map.set(key,[]);map.get(key).push(t);}
    for(const values of map.values())values.sort((a,b)=>b.length-a.length||a.localeCompare(b,'ja'));
    return map;
  }).catch(e=>{lexicon=undefined;throw e;});
  return lexicon;
}
function segmentations(text,map) {
  const memo=new Map();
  function visit(offset) {
    if(offset===text.length)return [[]];
    if(memo.has(offset))return memo.get(offset);
    const found=[];
    for(const term of map.get(Array.from(text.slice(offset))[0])||[]) {
      if(!text.startsWith(term,offset))continue;
      for(const rest of visit(offset+term.length)) {
        found.push([term,...rest]);
        if(found.length>MAX_VARIANTS)throw new Error('検索語の分割候補が多いため、短い語に分けて検索してください。');
      }
    }
    memo.set(offset,found);return found;
  }
  const found=visit(0);return found.length?found.map(v=>v.join(' ')):[text];
}
export async function queryVariants(query) {
  if(typeof query!=='string'||query.length>200)throw new TypeError('検索語は200文字以内で指定してください。');
  query=query.normalize('NFC').trim().replace(/^"(.*)"$/u,'$1');
  if(!query||!RUN.test(query)){RUN.lastIndex=0;return [query];}
  RUN.lastIndex=0;
  const map=await terms();let variants=[''],cursor=0;
  for(const match of query.matchAll(RUN)) {
    const lead=query.slice(cursor,match.index),options=segmentations(match[0],map),next=[];
    for(const prefix of variants)for(const choice of options){next.push(prefix+lead+' '+choice+' ');if(next.length>MAX_VARIANTS)throw new Error('検索語を短くして再検索してください。');}
    variants=next;cursor=match.index+match[0].length;
  }
  // Additional queries use native exact phrases to retain order/adjacency and avoid loose OR expansion.
  return [...new Set(variants.map(v=>'"'+(v+query.slice(cursor)).trim().replace(/\s+/g,' ')+'"'))];
}
export const init=()=>request(null,{});
export async function search(query,options={}) {
  const variants=await queryVariants(query);
  const responses=[];for(const q of variants)responses.push(await request(q,options));
  const unique=new Map();
  for(const response of responses)for(const result of response.results)if(!unique.has(result.id))unique.set(result.id,result);
  return { ...responses[0],results:[...unique.values()].map(r=>({...r,data:async()=>r.fragment})),unfilteredResultCount:unique.size,normalization:{queries:variants,method:'public-index-token-boundaries',native_version:'1.5.2',realm:'dedicated-worker-no-Intl-Segmenter'} };
}
