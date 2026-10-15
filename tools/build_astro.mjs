import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const cli=fileURLToPath(new URL('../astro_candidate/node_modules/astro/bin/astro.mjs',import.meta.url));
const result=spawnSync(process.execPath,[cli,'build'],{stdio:'inherit',env:{...process.env,ASTRO_TELEMETRY_DISABLED:'1'}});
if(result.error) throw result.error;
process.exit(result.status ?? 1);
