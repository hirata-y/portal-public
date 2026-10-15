"""One scanner for real dist and fault injection, including gzip Pagefind fragments."""
import gzip,json

def scan(root,canary):
 findings=[]
 for p in root.rglob('*'):
  if not p.is_file():continue
  rel=str(p.relative_to(root));data=p.read_bytes()
  if canary in data:findings.append('canary:'+rel)
  if data.startswith(b'\x1f\x8b'):
   decoded=gzip.decompress(data)
   if canary in decoded:findings.append('decoded_canary:'+rel)
   if decoded.startswith(b'pagefind_dcd{'):
    j=json.loads(decoded[len(b'pagefind_dcd'):])
    # Japanese segmentation inserts zero-width spaces inside Latin tokens as well.
    if canary.decode() in j.get('content','').replace('\u200b',''):findings.append('decoded_content_canary:'+rel)
    if '/members/' in j.get('url',''):findings.append('decoded_private_url:'+rel)
  if p.name in ('canary.html','members-index.json') or 'members' in p.relative_to(root).parts:findings.append('private_path:'+rel)
 return findings
