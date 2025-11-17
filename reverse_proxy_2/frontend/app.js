async function sendEcho(){
  const msg=document.getElementById('msg').value||'';
  const res=await fetch('/api/echo',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})});
  const data=await res.json();
  document.getElementById('out').textContent=JSON.stringify(data,null,2);
}
async function getTime(){
  const res=await fetch('/api/time');
  const data=await res.json();
  document.getElementById('out').textContent=JSON.stringify(data,null,2);
}
