import subprocess,sys,pathlib,json,datetime,time
out=pathlib.Path(__file__).resolve().parent
label=sys.argv[1];cwd=sys.argv[2];args=sys.argv[3:];start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
p=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(out/(label+'.log')).write_bytes(p.stdout)
meta={'command':args,'cwd':cwd,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t,'exit':p.returncode}
(out/(label+'.command.json')).write_text(json.dumps(meta,indent=2));print(json.dumps(meta));print(p.stdout.decode(errors='replace')[-1800:]);sys.exit(p.returncode)
