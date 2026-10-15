import { spawnSync } from 'node:child_process';
import { rmSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
// Do not re-index a previous diagnostics page or stale index on repeated runs.
rmSync('dist/tech-evidence',{recursive:true,force:true});
rmSync('dist/pagefind',{recursive:true,force:true});
const cli=fileURLToPath(new URL('../astro_candidate/node_modules/pagefind/lib/runner/bin.cjs',import.meta.url));
const result=spawnSync(process.execPath,[cli,'--site','dist','--force-language','ja'],{stdio:'inherit'});
if(result.error) throw result.error;
if(result.status!==0)process.exit(result.status ?? 1);
const { createLexicon } = await import('./create_ja_lexicon.mjs');
console.log('Japanese lexicon:',createLexicon('dist'));
await import('./copy_probe.mjs');
