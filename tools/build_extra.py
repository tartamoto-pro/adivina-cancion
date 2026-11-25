# Genera calculo.html y total.html a partir de cole.html (mismo motor de juego).
# Ejecutar desde la carpeta del repositorio: python3 tools/build_extra.py
import json, re, subprocess

def read(f): return open(f, encoding='utf8').read()
def arr(src, name):
    m = re.search(r'const %s=(\[[\s\S]*?\]\]);' % name, src)
    return json.loads(m.group(1))

base = read('cole.html')
def swap_data(s, q_js, cats, lvls, default_lvls):
    i = s.index('const Q=['); j = s.index('const CATS='); k = s.index('\n', j) + 1
    s = s[:i] + q_js + '\nconst CATS=' + json.dumps(cats, ensure_ascii=False) + ';\n' + s[k:]
    s = re.sub(r'const LVLS=\[.*?\];', 'const LVLS=' + json.dumps(lvls, ensure_ascii=False) + ';', s, count=1)
    s = s.replace('lvls:["5","6","1e","2e"]', 'lvls:' + json.dumps(default_lvls))
    return s

def texts(s, key, title, brand, led, note, comment, colors):
    s = s.replace("'cole-", "'" + key + "-")
    s = s.replace('<title>Trivial del cole</title>', '<title>%s</title>' % title)
    s = s.replace('<h1>Trivial del cole</h1>', '<h1>%s</h1>' % title)
    s = s.replace('<p class="brand">Trivial del cole</p>', '<p class="brand">%s</p>' % brand)
    s = s.replace('<div class="led"><i></i>Pizarra</div>', '<div class="led"><i></i>%s</div>' % led)
    s = s.replace('Preguntas de lo que se suele dar en cada curso en España; cada colegio puede ir a un ritmo distinto.', note)
    a = s.index('/* VOICE'); b = s.index('*/', a) + 2
    s = s[:a] + comment + s[b:]
    for x, y in colors.items(): s = s.replace(x, y)
    return s

# ---------- Cálculo mental ----------
CALC_Q = r"""const Q=(()=>{let sd=20261125;const r=()=>{sd|=0;sd=sd+0x6D2B79F5|0;let t=Math.imul(sd^sd>>>15,1|sd);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296};
const R=(a,b)=>a+Math.floor(r()*(b-a+1));const out=[],used=new Set();
const mk=(c,l,txt,ans,sp)=>{if(used.has(txt))return;used.add(txt);
  const cand=[...new Set([ans+1,ans-1,ans+2,ans-2,ans+10,ans-10,ans+sp,ans-sp,ans+5])].filter(x=>x>=0&&x!==ans);
  for(let i=cand.length-1;i>0;i--){const j=Math.floor(r()*(i+1));[cand[i],cand[j]]=[cand[j],cand[i]]}
  out.push([txt,String(ans),cand.slice(0,3).map(String),c,String(l)])};
for(let n=0;n<90;n++){let a,b,q;
  a=R(2,20);b=R(2,20);mk('suma',1,`¿Cuánto es ${a} + ${b}?`,a+b,b);
  a=R(10,99);b=R(10,99);mk('suma',2,`¿Cuánto es ${a} + ${b}?`,a+b,20);
  a=R(100,999);b=R(10,999);mk('suma',3,`¿Cuánto es ${a} + ${b}?`,a+b,100);
  a=R(10,20);b=R(1,a);mk('resta',1,`¿Cuánto es ${a} − ${b}?`,a-b,3);
  a=R(30,99);b=R(10,a);mk('resta',2,`¿Cuánto es ${a} − ${b}?`,a-b,20);
  a=R(200,999);b=R(50,a);mk('resta',3,`¿Cuánto es ${a} − ${b}?`,a-b,100);
  a=R(2,10);b=R(2,10);mk('mult',1,`¿Cuánto es ${a} × ${b}?`,a*b,a);
  a=R(12,49);b=R(2,9);mk('mult',2,`¿Cuánto es ${a} × ${b}?`,a*b,b);
  a=R(11,25);b=R(11,25);mk('mult',3,`¿Cuánto es ${a} × ${b}?`,a*b,a);
  b=R(2,10);q=R(2,10);mk('div',1,`¿Cuánto es ${b*q} ÷ ${b}?`,q,3);
  b=R(2,9);q=R(11,30);mk('div',2,`¿Cuánto es ${b*q} ÷ ${b}?`,q,5);
  b=R(11,20);q=R(5,30);mk('div',3,`¿Cuánto es ${b*q} ÷ ${b}?`,q,5);}
return out})();"""
calc = swap_data(base, CALC_Q, [["suma","Sumas"],["resta","Restas"],["mult","Multiplicaciones"],["div","Divisiones"]],
                 [["1","Nivel 1 (fácil)"],["2","Nivel 2"],["3","Nivel 3 (difícil)"]], ["1","2"])
calc = calc.replace('const TOTAL=20;', 'const TOTAL=15;')
calc = texts(calc, 'calc', 'Cálculo mental', 'Cálculo mental', 'Contrarreloj',
  'Las operaciones se generan solas. Nivel 1: tablas y números pequeños; nivel 2: números de dos cifras; nivel 3: números grandes.',
  """/* VOICE: contrarreloj de cálculo, directo y claro, números grandes
   IDEA: una calculadora de bolsillo: la operación sale en su pantalla
   PICTURE: carcasa gris oscura con pantalla verde clara y piloto
   COLOUR and TYPE: gris carcasa, pantalla verde LCD, botones naranja; Fredoka + Nunito
   LAYOUT: una columna: marcador, calculadora, 4 botones; ajustes debajo */""",
  {'--shell:#8a5a33':'--shell:#3d4552','--shell2:#6b4426':'--shell2:#2a3039','--lcd:#2f5d46':'--lcd:#cfe3c0','--lcd2:#244a37':'--lcd2:#b4cda3',
   '--lcdink:#f4f7ef':'--lcdink:#1f2a1a','--btn:#f2d46b':'--btn:#ff9f43','--bg:#eef3ea':'--bg:#eef0f4','--bg:#121a15':'--bg:#14161b','#5c3a1f':'#1c2027'})
open('calculo.html','w',encoding='utf8').write(calc)

# ---------- Trivial total ----------
rows = []
songs = arr(read('canciones.html'), 'ES')
for p, a, w, ar, y in songs:
    rows.append([f'Completa la canción de {ar}: «{p.strip()} ___»', a, w, 'canc', '2' if y < 2000 else '1'])
for f, c in [('minecraft.html','mc'),('pokemon.html','pk'),('harrypotter.html','hp')]:
    for q, a, w, _, l in arr(read(f), 'Q'): rows.append([q, a, w, c, str(l)])
for q, a, w, _, l in arr(read('cole.html'), 'Q'):
    rows.append([q, a, w, 'cole', '1' if l in ('5','6') else '2'])
total_q = 'const Q=[\n' + ',\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '];'
tot = swap_data(base, total_q, [["canc","Canciones"],["mc","Minecraft"],["pk","Pokémon"],["hp","Harry Potter"],["cole","Cole"]],
                [["1","Fácil"],["2","Difícil"]], ["1","2"])
tot = texts(tot, 'total', 'Trivial total', 'Trivial total', 'Todos los juegos',
  'Mezcla preguntas de canciones, Minecraft, Pokémon, Harry Potter y el cole. En canciones, «difícil» son las de antes del 2000.',
  """/* VOICE: gran concurso familiar, festivo y claro
   IDEA: el panel de un plató de concurso: la pregunta sale en la pantalla grande
   PICTURE: marco rojo de plató con pantalla azul noche y piloto
   COLOUR and TYPE: rojo plató, azul pantalla, botones amarillos; Fredoka + Nunito
   LAYOUT: una columna: marcador, panel, 4 botones; ajustes debajo */""",
  {'--shell:#8a5a33':'--shell:#c0392b','--shell2:#6b4426':'--shell2:#922b21','--lcd:#2f5d46':'--lcd:#1d3557','--lcd2:#244a37':'--lcd2:#16294a',
   '--lcdink:#f4f7ef':'--lcdink:#f1f4ff','--btn:#f2d46b':'--btn:#ffd23f','--bg:#eef3ea':'--bg:#fff3e8','--bg:#121a15':'--bg:#1a1214','#5c3a1f':'#5a1d17'})
open('total.html','w',encoding='utf8').write(tot)
print('calculo ok; total', len(rows))
