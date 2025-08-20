from flask import Flask, abort, flash, json, request, render_template, redirect, url_for
from base_de_dados import get_db

app = Flask(__name__)
app.secret_key = 'senha'

@app.route('/')
def index():
    return render_template('index.html')

# Rota dos clientes
@app.route('/clientes')
def clientes():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM Cliente"
    params = []
    nome = request.args.get('nome')
    cpf = request.args.get('cpf')

    if nome:
        query += " WHERE nome LIKE %s"
        params.append(f"%{nome}%")
    if cpf:
        if nome:
            query += " AND cpf LIKE %s"
        else:
            query += " WHERE cpf LIKE %s"
        params.append(f"%{cpf}%")

    cursor.execute(query, params)
    clientes = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('clientes.html', clientes=clientes)

# Rota para edição de cliente
@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        # Processar atualização
        cursor.execute(
            "UPDATE Cliente SET nome=%s, cpf=%s, email=%s, telefone=%s WHERE id=%s",
            (
                request.form['nome'],
                request.form['cpf'],
                request.form.get('email'),
                request.form.get('telefone'),
                id
            )
        )
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('clientes'))
    
    # Carregar dados do cliente para edição
    cursor.execute(
        "SELECT * FROM Cliente WHERE id = %s", 
        (id,)
    )
    cliente = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template('editar_cliente.html', cliente=cliente)

# Rota para veículos do cliente
@app.route('/clientes/<int:cliente_id>/veiculos')
def veiculos_cliente(cliente_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Buscar os veículos do cliente específico
    cursor.execute("""
        SELECT v.id, v.modelo, v.placa, tv.descricao as tipo 
        FROM Veiculo v
        JOIN TipoVeiculo tv ON v.tipo_veiculo_id = tv.id
        WHERE v.cliente_id = %s
    """, (cliente_id,))
    veiculos = cursor.fetchall()
    
    # Buscar informações do cliente
    cursor.execute(
        "SELECT nome FROM Cliente WHERE id = %s", 
        (cliente_id,)
    )
    cliente = cursor.fetchone()
    
    cursor.close()
    db.close()
    
    return render_template(
        'veiculos_cliente.html', 
        veiculos=veiculos,
        cliente=cliente
    )

#Rota para editar veículo
@app.route('/veiculos/editar/<int:id>', methods=['GET', 'POST'])
def editar_veiculo(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        # Processar atualização do veículo
        cursor.execute("""
        UPDATE Veiculo SET
            modelo = %s,
            placa = %s,
            tipo_veiculo_id = %s
            WHERE id = %s
    """, (
        request.form['modelo'],
        request.form['placa'],
        request.form['tipo_veiculo_id'],
        id
    )
)
        veiculo = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('veiculos'))
    
    # Carregar dados do veículo para edição
    cursor.execute(
        """
        SELECT v.*, c.nome as cliente_nome
        FROM Veiculo v
        JOIN Cliente c ON v.cliente_id = c.id
        WHERE v.id = %s
    """, (id,))
    veiculo = cursor.fetchone()
    
    # Carregar tipos de veículo para o select
    cursor.execute(
        "SELECT * FROM TipoVeiculo"
    )
    tipos_veiculo = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return render_template(
        'editar_veiculo.html', 
        veiculo=veiculo,
        tipos_veiculo=tipos_veiculo
    )

# Rota para Veículos
@app.route('/veiculos')
def veiculos():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Query base
    query = """
    SELECT
        v.id,
        v.modelo,
        v.placa,
        c.nome as cliente_nome,
        tv.descricao as tipo_veiculo
    FROM Veiculo v
    JOIN Cliente c ON v.cliente_id = c.id
    JOIN TipoVeiculo tv ON v.tipo_veiculo_id = tv.id
    """
    
    params = []
    conditions = []
    
    # Filtro por placa
    placa = request.args.get('placa')
    if placa:
        conditions.append("v.placa LIKE %s")
        params.append(f"%{placa}%")
    
    # Filtro por cliente (nome do proprietário)
    cliente = request.args.get('cliente')
    if cliente:
        conditions.append("c.nome LIKE %s")
        params.append(f"%{cliente}%")
    
    # Adiciona WHERE se houver filtros
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    # Executa a query com os parâmetros
    cursor.execute(query, tuple(params))
    veiculos = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return render_template('veiculos.html', veiculos=veiculos)

#Rota para histórico de veículos
@app.route('/historico/<int:veiculo_id>')
def historico_veiculo(veiculo_id):
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        # Buscar veículo (usando nomes corretos das tabelas)
        cursor.execute("""
            SELECT v.*, c.nome as cliente_nome 
            FROM Veiculo v
            JOIN Cliente c ON v.cliente_id = c.id
            WHERE v.id = %s
        """, (veiculo_id,))
        veiculo_data = cursor.fetchone()
        
        if not veiculo_data:
            return "Veículo não encontrado", 404
        
        # Buscar estadias (nome correto da tabela)
        cursor.execute("""
            SELECT vaga_id as vaga_numero, entrada, saida, valor 
            FROM Estadia 
            WHERE veiculo_id = %s
            ORDER BY entrada DESC
        """, (veiculo_id,))
        estadias_data = cursor.fetchall()
        
        # Buscar transações (ajustando o JOIN)
        cursor.execute("""
            SELECT t.data, t.tipo_transacao, t.valor 
            FROM Transacao t
            JOIN Estadia e ON t.estadia_id = e.id
            WHERE e.veiculo_id = %s
            ORDER BY t.data DESC
        """, (veiculo_id,))
        transacoes_data = cursor.fetchall()
        
        return render_template('historico_veiculo.html',
                            veiculo=veiculo_data,
                            estadias=estadias_data,
                            transacoes=transacoes_data)
                            
    except Exception as e:
        app.logger.error(f"Erro no histórico: {str(e)}", exc_info=True)
        return "Ocorreu um erro ao processar o histórico", 500
        
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# Rota para Vagas
@app.route('/vagas')
def vagas():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Query base
    query = """
    SELECT 
        v.id,
        v.numero,
        tv.descricao as tipo,
        v.status,
        IFNULL(CONCAT(ve.modelo, ' (', ve.placa, ')'), '-') as veiculo_info,
        CASE
            WHEN v.status = 'OCUPADA' AND e.entrada IS NOT NULL THEN
                CONCAT(
                    TIMESTAMPDIFF(HOUR, e.entrada, NOW()), 'h ',
                    TIMESTAMPDIFF(MINUTE, e.entrada, NOW()) % 60, 'm'
                )
            ELSE '-'
        END as tempo_ocupacao
    FROM Vaga v
    JOIN TipoVaga tv ON v.tipo_vaga_id = tv.id
    LEFT JOIN Estadia e ON e.vaga_id = v.id AND e.saida IS NULL
    LEFT JOIN Veiculo ve ON e.veiculo_id = ve.id
    WHERE 1=1
    """
    
    params = []
    
    # Filtro por status
    status = request.args.get('status')
    if status:
        query += " AND v.status = %s"
        params.append(status.upper())
    
    # Filtro por tipo
    tipo = request.args.get('tipo')
    if tipo:
        query += " AND v.tipo_vaga_id = %s"
        params.append(tipo)
    
    query += " ORDER BY v.numero"
    
    cursor.execute(query, params)
    vagas = cursor.fetchall()
    
    cursor.execute("SELECT * FROM TipoVaga")
    tipos_vaga = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return render_template('vagas.html', 
                         vagas=vagas,
                         tipos_vaga=tipos_vaga,
                         status_filtro=status)

# Rota para Estadias
@app.route('/estadias')
def estadias():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Query base
    query = """
    SELECT e.id, v.modelo, v.placa, g.numero as vaga, 
           e.entrada, e.saida, e.valor,
           CASE WHEN e.saida IS NULL THEN 'Em andamento' ELSE 'Concluída' END as status
    FROM Estadia e
    JOIN Veiculo v ON e.veiculo_id = v.id
    JOIN Vaga g ON e.vaga_id = g.id
    WHERE 1=1
    """
    
    params = []
    
    # Filtro por status
    status = request.args.get('status')
    if status == 'andamento':
        query += " AND e.saida IS NULL"
    elif status == 'concluida':
        query += " AND e.saida IS NOT NULL"
    
    # Filtro por placa
    placa = request.args.get('placa')
    if placa:
        query += " AND v.placa LIKE %s"
        params.append(f"%{placa}%")
    
    query += " ORDER BY e.entrada DESC"
    
    cursor.execute(query, params)
    estadias = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return render_template('estadias.html', estadias=estadias)

# Rota para Registrar Entrada
@app.route('/registrar_entrada', methods=['GET', 'POST'])
def registrar_entrada():
    if request.method == 'POST':
        # Lógica para processar o formulário de entrada
        veiculo_id = request.form['veiculo_id']
        vaga_id = request.form['vaga_id']
        estadia = request.form['estadia_id']

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO Estadia (veiculo_id, vaga_id, entrada) VALUES (%s, %s, NOW())",
            (veiculo_id, vaga_id)
        )
        db.commit()
        
        cursor.execute("""
        SELECT e.*, v.modelo, v.placa, g.numero as vaga_numero
        FROM Estadia e
        JOIN Veiculo v ON e.veiculo_id = v.id
        JOIN Vaga g ON e.vaga_id = g.id
        WHERE e.id = %s AND e.saida IS NULL
    """, (estadia.id,))
    estadia = cursor.fetchone()
    
    if not estadia:
        flash('Estadia não encontrada ou já finalizada', 'danger')
        return redirect(url_for('estadias'))
    
    cursor.close()
    db.close()
        
    return redirect(url_for('estadias'))


#Rota de saida
@app.route('/registrar_saida/<int:estadia_id>', methods=['GET', 'POST'])
def registrar_saida(estadia_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        try:
            # Primeiro: Obter o tipo da vaga associada à estadia
            cursor.execute("""
                SELECT v.tipo_vaga_id 
                FROM Vaga v
                JOIN Estadia e ON v.id = e.vaga_id
                WHERE e.id = %s
            """, (estadia_id,))
            tipo_vaga = cursor.fetchone()
            
            if not tipo_vaga:
                flash('Vaga não encontrada', 'danger')
                return redirect(url_for('estadias'))
            
            # Segundo: Calcular o valor baseado no tempo
            cursor.execute("""
                SELECT 
                    entrada,
                    TIMESTAMPDIFF(HOUR, entrada, NOW()) as horas_decorridas
                FROM Estadia
                WHERE id = %s
            """, (estadia_id,))
            tempo_estadia = cursor.fetchone()
            
            # Calcular o valor
            if tempo_estadia['horas_decorridas'] > 12:
                cursor.execute("""
                    SELECT preco_diaria 
                    FROM TabelaPrecos 
                    WHERE tipo_vaga_id = %s
                """, (tipo_vaga['tipo_vaga_id'],))
            else:
                cursor.execute("""
                    SELECT preco_hora 
                    FROM TabelaPrecos 
                    WHERE tipo_vaga_id = %s
                """, (tipo_vaga['tipo_vaga_id'],))
            
            preco = cursor.fetchone()
            valor = preco['preco_diaria'] if tempo_estadia['horas_decorridas'] > 12 else preco['preco_hora'] * tempo_estadia['horas_decorridas']
            
            # Terceiro: Atualizar a estadia
            cursor.execute("""
                UPDATE Estadia 
                SET saida = NOW(),
                    valor = %s
                WHERE id = %s
            """, (valor, estadia_id))
            
            # Quarto: Atualizar o status da vaga
            cursor.execute("""
                UPDATE Vaga v
                JOIN Estadia e ON v.id = e.vaga_id
                SET v.status = 'LIVRE'
                WHERE e.id = %s
            """, (estadia_id,))
            
            db.commit()
            flash('Saída registrada com sucesso!', 'success')
            return redirect(url_for('estadias'))
            
        except Exception as e:
            db.rollback()
            flash(f'Erro ao registrar saída: {str(e)}', 'danger')
            return redirect(url_for('estadias'))
    
    # Código GET permanece o mesmo (para mostrar a página de confirmação)
    cursor.execute("""
        SELECT e.*, v.modelo, v.placa, g.numero as vaga_numero
        FROM Estadia e
        JOIN Veiculo v ON e.veiculo_id = v.id
        JOIN Vaga g ON e.vaga_id = g.id
        WHERE e.id = %s AND e.saida IS NULL
    """, (estadia_id,))
    estadia = cursor.fetchone()
    
    if not estadia:
        flash('Estadia não encontrada ou já finalizada', 'danger')
        return redirect(url_for('estadias'))
    
    entrada = estadia['entrada']
    tempo_decorrido = datetime.now() - entrada
    horas = int(tempo_decorrido.total_seconds() // 3600)
    minutos = int((tempo_decorrido.total_seconds() % 3600) // 60)
    
    cursor.close()
    db.close()
    
    return render_template('confirmar_saida.html',
                         estadia=estadia,
                         horas=horas,
                         minutos=minutos)

#Rota detalhes estadias
@app.route('/estadias/<int:estadia_id>')
def detalhes_estadia(estadia_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Buscar os detalhes da estadia
    cursor.execute("""
        SELECT e.*, v.modelo, v.placa, g.numero as vaga_numero, 
               c.nome as cliente_nome
        FROM Estadia e
        JOIN Veiculo v ON e.veiculo_id = v.id
        JOIN Vaga g ON e.vaga_id = g.id
        JOIN Cliente c ON v.cliente_id = c.id
        WHERE e.id = %s
    """, (estadia_id,))
    estadia = cursor.fetchone()
    
    if not estadia:
        abort(404)  # Retorna erro 404 se não encontrar a estadia
    
    cursor.close()
    db.close()
    
    return render_template('detalhes_estadia.html', estadia=estadia)

# Rota para Transações
@app.route('/transacoes')
def transacoes():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    query = """
    SELECT 
        t.data,
        t.tipo_transacao,
        t.valor,
        v.placa,
        v.modelo,
        e.entrada,
        e.saida
    FROM Transacao t
    LEFT JOIN Estadia e ON t.estadia_id = e.id
    LEFT JOIN Veiculo v ON e.veiculo_id = v.id
    WHERE 1=1
    """
    
    params = []
    
    # Filtros
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    placa = request.args.get('placa')
    
    if data_inicio and data_fim:
        query += " AND t.data BETWEEN %s AND %s"
        params.extend([data_inicio, data_fim])
    elif data_inicio:
        query += " AND t.data >= %s"
        params.append(data_inicio)
    elif data_fim:
        query += " AND t.data <= %s"
        params.append(data_fim)
    
    if placa:
        query += " AND v.placa LIKE %s"
        params.append(f"%{placa}%")
    
    query += " ORDER BY t.data DESC"
    
    cursor.execute(query, params)
    transacoes = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return render_template('transacoes.html', transacoes=transacoes)

@app.template_filter('format_datetime')
def format_datetime(value):
    if value is None:
        return '-'
    return value.strftime('%d/%m/%Y %H:%M')

@app.template_filter('format_currency')
def format_currency(value):
    if value is None:
        return '-'
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@app.template_filter('format_time')
def format_time(value):
    if value is None:
        return '-'
    return value.strftime('%H:%M')

# Filtros para formatação
from datetime import datetime

@app.template_filter('format_datetime')
def format_datetime(value):
    if value is None:
        return '-'
    return value.strftime('%d/%m/%Y %H:%M')

@app.template_filter('format_date')
def format_date(value):
    if value is None:
        return '-'
    return value.strftime('%d/%m/%Y')

@app.template_filter('format_currency')
def format_currency(value):
    if value is None:
        return '-'
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

if __name__ == '__main__':
    app.run(debug=True)