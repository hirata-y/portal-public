import { readdirSync,readFileSync,mkdirSync,writeFileSync } from 'node:fs';
import { gunzipSync } from 'node:zlib';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
// Derive actual tokens from the generated PUBLIC Pagefind fragments, never member inputs.
export function createLexicon(dist) {
  const terms=new Set(),sources=[];
  const directory=join(dist,'pagefind','fragment');
  for(const name of readdirSync(directory).filter(n=>n.endsWith('.pf_fragment')).sort()) {
    const compressed=readFileSync(join(directory,name));
    const raw=gunzipSync(compressed).toString('utf8');
    if(!raw.startsWith('pagefind_dcd')) throw new Error('Unexpected Pagefind fragment encoding');
    const fragment=JSON.parse(raw.slice('pagefind_dcd'.length));
    if(!fragment.url?.startsWith('/')||fragment.url.includes('/members/'))throw new Error('Non-public index source');
    for(const term of fragment.content.split(/[\u200b\s]+/u)) {
      if(/^[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}\p{M}ー]+$/u.test(term)) terms.add(term.normalize('NFC'));
    }
    sources.push({path:'pagefind/fragment/'+name,sha256:createHash('sha256').update(compressed).digest('hex')});
  }
  const result={schema_version:1,pagefind_version:'1.5.2',language:'ja',terms:[...terms].sort(),source_fragments:sources};
  mkdirSync(join(dist,'search'),{recursive:true});
  writeFileSync(join(dist,'search','ja-terms.json'),JSON.stringify(result)+'\n');
  return {terms:terms.size,fragments:sources.length};
}
