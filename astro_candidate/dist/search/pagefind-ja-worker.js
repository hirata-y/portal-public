// This affects this dedicated Worker only. Pagefind's own fallback preserves
// presegmented spaces; the original generated vendor bundle stays byte-exact.
Object.defineProperty(Intl,'Segmenter',{value:undefined,configurable:true});
const nativeModule=import('../pagefind/pagefind.js');
let queue=Promise.resolve();
self.onmessage=({data:m})=>{queue=queue.then(async()=>{
 try {
  const native=await nativeModule;
  if(m.query===null){await native.init();self.postMessage({id:m.id,response:{ready:true}});return;}
  const response=await native.search(m.query,m.options);
  const results=await Promise.all(response.results.map(async r=>{const {data,...fields}=r;return {...fields,fragment:await data()};}));
  self.postMessage({id:m.id,response:{...response,results}});
 }catch(e){self.postMessage({id:m.id,error:String(e)});}
});};
