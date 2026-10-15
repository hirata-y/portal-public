import { mkdirSync,copyFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const dest=fileURLToPath(new URL('../astro_candidate/dist/tech-evidence/',import.meta.url));
mkdirSync(dest,{recursive:true});
copyFileSync(fileURLToPath(new URL('./pagefind_japanese_browser_probe.html',import.meta.url)),dest+'pagefind_japanese_browser_probe.html');
