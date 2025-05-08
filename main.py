from flask import Flask, request, redirect, render_template, flash
from datetime import date, timedelta

app = Flask(__name__)
app.secret_key = 'minha_chave'

livros = []

@app.route('/')
def index():
    return render_template('index.html', livros=livros, hoje=date.today())

@app.route('/adicionar_livro', methods=['GET', 'POST'])
def adicionar_livro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        codigo = len(livros)
        ano = date.today().year
        devolver_ate = None
        livro = {
            "codigo": codigo,
            "titulo": titulo,
            "autor": autor,
            "ano": ano,
            "devolver_ate": devolver_ate
        }
        livros.append(livro)
        flash('Livro adicionado com sucesso!')
        return redirect('/')
    return render_template('adicionar_livro.html')

@app.route('/emprestar_livro/<int:codigo>')
def emprestar_livro(codigo):
    livro = livros[codigo]
    if livro["devolver_ate"] is None:
        livro["devolver_ate"] = date.today() + timedelta(days=7)
        flash(f"Livro emprestado! Devolver até {livro['devolver_ate'].strftime('%d/%m/%Y')}.")
    else:
        flash("Este livro já está emprestado.")
    return redirect('/')

@app.route('/devolver_livro/<int:codigo>')
def devolver_livro(codigo):
    livro = livros[codigo]
    if livro["devolver_ate"] is not None:
        hoje = date.today()
        atraso = (hoje - livro["devolver_ate"]).days
        if atraso > 0:
            multa = 10 + atraso
            flash(f'Livro devolvido com {atraso} dias de atraso. Multa: R${multa}')
        else:
            flash('Livro devolvido no prazo.')
        livro["devolver_ate"] = None
    else:
        flash('Este livro não está emprestado.')
    return redirect('/')

@app.route('/editar_livro/<int:codigo>', methods=['GET', 'POST'])
def editar_livro(codigo):
    livro = livros[codigo]
    if request.method == 'POST':
        livro["titulo"] = request.form['titulo']
        livro["autor"] = request.form['autor']
        flash('Livro atualizado com sucesso!')
        return redirect('/')
    return render_template('editar_livro.html', livro=livro)

@app.route('/apagar_livro/<int:codigo>')
def apagar_livro(codigo):
    del livros[codigo]
    flash('Livro excluído com sucesso!')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)