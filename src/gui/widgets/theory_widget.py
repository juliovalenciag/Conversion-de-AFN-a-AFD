from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore              import QUrl, QSize

class TheoryWidget(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(QSize(600, 400))

        html = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <script>
    window.MathJax = {
      tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] }
    };
  </script>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
  <style>
    body { background: #2b2b2b; color: #f8f8f2; font-family: sans-serif; padding: 20px; }
    h1, h2 { color: #66d9ef; }
    code { background: #272822; padding: 2px 4px; border-radius: 4px; }
    ul { margin-left: 1em; }
  </style>
</head>
<body>
  <h1>Guía de Conversión AFN → AFD</h1>

  <h2>1. Definir la quíntupla del AFN</h2>
  <p>
    Sea $$M=(Q,\\Sigma,\\delta,q_0,F)$$ donde:
  </p>
  <ul>
    <li><b>Q</b>: conjunto de estados</li>
    <li><b>Σ</b>: alfabeto (sin ε)</li>
    <li><b>δ</b>: $$Q\\times(Σ\\cup\\{ε\\})\\to 𝒫(Q)$$</li>
    <li><b>q₀</b>: estado inicial</li>
    <li><b>F</b>: conjunto de finales</li>
  </ul>

  <h2>2. Tabla de transiciones del AFN</h2>
  <p>
    Construye una tabla con filas para cada \\(q∈Q\\) y columnas para cada símbolo de Σ y ε, donde cada celda es \\(δ(q,a)\\subseteq Q\\).
  </p>

  <h2>3. Construir el AFD por subconjuntos</h2>
  <ol>
    <li>
      Para un conjunto de estados \\(T\\), su <b>ε-closure</b> es
      $$ε\\text{-closure}(T)=\\bigcup_{p∈T}ε\\text{-closure}(p).$$
    </li>
    <li>
      Estado inicial del AFD: $$T_0=ε\\text{-closure}(\\{q_0\\}).$$
    </li>
    <li>
      Para cada símbolo \\(a∈Σ\\), definimos
      $$\\delta'(T,a)=ε\\text{-closure}\\bigl(\\bigcup_{p∈T}\\delta(p,a)\\bigr).$$
    </li>
    <li>
      Repetir hasta no generar nuevos conjuntos.
    </li>
  </ol>

  <h2>4. Definir la quíntupla del AFD</h2>
  <p>
    Sea $$M'=(Q',Σ,δ',q'_0,F')$$ donde:
  </p>
  <ul>
    <li><b>Q'</b>: subconjuntos alcanzables de Q</li>
    <li><b>q′₀</b>: ε-closure({q₀})</li>
    <li><b>F′</b>: aquellos subconjuntos que intersectan F</li>
  </ul>

  <h2>5. Tabla de transiciones del AFD</h2>
  <p>Filas para cada \\(S∈Q'\\), columnas para cada \\(a∈Σ\\).</p>
</body>
</html>
        """
        self.setHtml(html, QUrl("about:blank"))
