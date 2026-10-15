# Astro/Pagefind candidate only — NOT EXECUTED

This directory demonstrates a possible Astro static-site packaging of the unchanged P3-A pages. It is not a verified Astro build. The `src/pages/index.astro` contains the P3-A home markup; `public/` contains CSS/JS/theme/record source. Validate Astro parsing, route/asset paths and search behavior after installing fixed compatible versions and recording npm lockfile, in a network-enabled or pre-cached **local** development environment.

Suggested (separately authorized): `npm install --save-exact astro && npm install --save-dev --save-exact pagefind` followed by `npm run build` and `npm run index:pagefind`. Never mark tests as PASS merely because the template exists. `pagefind_extended` is required for Japanese segmentation; the npm wrapper normally supplies it. The wildcard dependency entries are intentionally **not production-pinned**; do not deploy until installed versions are locked and audited.

We cannot run the binaries here because npm registry returned DNS EAI_AGAIN and neither package is installed. No GitHub/Cloudflare project is created.
