-- Tabela Cliente
CREATE TABLE Cliente (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20)
);

-- Tabela TipoVeiculo
CREATE TABLE TipoVeiculo (
    id INT PRIMARY KEY AUTO_INCREMENT,
    descricao VARCHAR(50) NOT NULL
);

-- Tabela Veiculo
CREATE TABLE Veiculo (
    id INT PRIMARY KEY AUTO_INCREMENT,
    modelo VARCHAR(50) NOT NULL,
    placa VARCHAR(10) UNIQUE NOT NULL,
    cliente_id INT NOT NULL,
    tipo_veiculo_id INT NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES Cliente(id),
    FOREIGN KEY (tipo_veiculo_id) REFERENCES TipoVeiculo(id)
);

-- Tabela TipoVaga
CREATE TABLE TipoVaga (
    id INT PRIMARY KEY AUTO_INCREMENT,
    descricao VARCHAR(50) NOT NULL
);

-- Tabela Vaga
CREATE TABLE Vaga (
    id INT PRIMARY KEY AUTO_INCREMENT,
    numero INT NOT NULL,
    tipo_vaga_id INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'LIVRE',
    FOREIGN KEY (tipo_vaga_id) REFERENCES TipoVaga(id)
);

-- Tabela Funcionario
CREATE TABLE Funcionario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    salario DECIMAL(10,2) NOT NULL
);

-- Tabela Estadia
CREATE TABLE Estadia (
    id INT PRIMARY KEY AUTO_INCREMENT,
    veiculo_id INT NOT NULL,
    vaga_id INT NOT NULL,
    entrada DATETIME NOT NULL,
    saida DATETIME,
    valor DECIMAL(10,2),
    FOREIGN KEY (veiculo_id) REFERENCES Veiculo(id),
    FOREIGN KEY (vaga_id) REFERENCES Vaga(id)
);

-- Tabela Transacao
CREATE TABLE Transacao (
    id INT PRIMARY KEY AUTO_INCREMENT,
    estadia_id INT NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    data DATE NOT NULL,
    tipo_transacao VARCHAR(50) NOT NULL,
    FOREIGN KEY (estadia_id) REFERENCES Estadia(id)
);

-- Tabela TabelaPrecos
CREATE TABLE TabelaPrecos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_vaga_id INT NOT NULL,
    preco_diaria DECIMAL(10,2) NOT NULL,
    preco_hora DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (tipo_vaga_id) REFERENCES TipoVaga(id)
);

-- Criação de um trigger para atualizar o status da vaga quando uma estadia é criada
DELIMITER //
CREATE TRIGGER atualiza_status_vaga_entrada
AFTER INSERT ON Estadia
FOR EACH ROW
BEGIN
    -- Atualiza a vaga para OCUPADA quando uma nova estadia é criada
    UPDATE Vaga SET status = 'OCUPADA' WHERE id = NEW.vaga_id;
END//
DELIMITER ;

-- Criação de um trigger para atualizar o status da vaga quando uma estadia é finalizada
DELIMITER //
CREATE TRIGGER atualiza_status_vaga_saida
AFTER UPDATE ON Estadia
FOR EACH ROW
BEGIN
    -- Verifica se a data de saída foi preenchida (estadia finalizada)
    IF NEW.saida IS NOT NULL AND OLD.saida IS NULL THEN
        -- Atualiza a vaga para LIVRE quando a estadia é finalizada
        UPDATE Vaga SET status = 'LIVRE' WHERE id = NEW.vaga_id;
    END IF;
END//
DELIMITER ;

-- Inserção de dados

-- Tipos de veículo
INSERT INTO TipoVeiculo (descricao) VALUES 
('Carro Pequeno'),
('Carro Grande'),
('Moto'),
('Caminhonete');

-- Tipos de vaga
INSERT INTO TipoVaga (descricao) VALUES 
('Padrão'),
('Idoso'),
('Motocicleta'),
('Deficiente');

-- Tabela de preços
INSERT INTO TabelaPrecos (tipo_vaga_id, preco_diaria, preco_hora) VALUES 
(1, 50.00, 5.00),
(2, 70.00, 8.00),
(3, 30.00, 3.00),
(4, 40.00, 4.00);

-- Vagas
INSERT INTO Vaga (numero, tipo_vaga_id, status) VALUES 
(101, 1, 'LIVRE'),
(102, 1, 'LIVRE'),
(103, 2, 'LIVRE'),
(104, 2, 'LIVRE'),
(201, 3, 'LIVRE'),
(202, 3, 'LIVRE'),
(301, 4, 'LIVRE'),
(105, 1, 'LIVRE'),
(106, 1, 'LIVRE'),
(107, 2, 'LIVRE'),
(203, 3, 'LIVRE'),
(204, 3, 'LIVRE'),
(302, 4, 'LIVRE'),
(303, 4, 'LIVRE'),
(401, 1, 'LIVRE'),
(402, 2, 'LIVRE'),
(403, 3, 'LIVRE');

-- Clientes
INSERT INTO Cliente (nome, cpf, email, telefone) VALUES
('João Silva', '123.456.789-00', 'joao@email.com', '(31) 9999-8888'),
('Maria Souza', '987.654.321-00', 'maria@email.com', '(31) 9777-6666'),
('Carlos Oliveira', '456.789.123-00', NULL, '(31) 9555-4444'),
('Ana Paula Fernandes', '111.222.333-44', 'ana.fernandes@email.com', '(21) 98888-7777'),
('Roberto Carlos Almeida', '222.333.444-55', 'roberto.carlos@email.com', '(31) 97777-6666'),
('Juliana Santos', '333.444.555-66', 'juliana.s@email.com', '(11) 96666-5555'),
('Marcos Vinicius Oliveira', '444.555.666-77', 'marcos.vinicius@empresa.com', '(41) 95555-4444'),
('Fernanda Lima', '555.666.777-88', 'fernanda.l@email.com', '(51) 94444-3333'),
('Ricardo Nogueira', '666.777.888-99', 'ricardo.n@email.com', '(71) 93333-2222'),
('Patrícia Gonçalves', '777.888.999-00', 'patricia.g@email.com', '(81) 92222-1111'),
('Gustavo Henrique Silva', '888.999.000-11', 'gustavo.h@empresa.com', '(98) 91111-0000'),
('Camila Rocha', '999.000.111-22', 'camila.rocha@email.com', '(67) 90000-9999'),
('Luciano Pereira', '000.111.222-33', 'luciano.p@email.com', '(85) 98989-8888');

-- Veículos
INSERT INTO Veiculo (modelo, placa, cliente_id, tipo_veiculo_id) VALUES 
('Fiat Uno', 'ABC-1234', 1, 1),
('Honda Civic', 'DEF-5678', 1, 2),
('Honda CG 160', 'GHI-9012', 2, 3),
('Toyota Hilux', 'JKL-3456', 3, 4),
('Volkswagen Gol', 'MNO-7890', 4, 1),
('Chevrolet Onix', 'PQR-1234', 5, 1),
('Ford Ranger', 'STU-5678', 6, 4),
('Yamaha Factor', 'VWX-9012', 7, 3),
('Hyundai HB20', 'YZA-3456', 8, 1),
('Jeep Renegade', 'BCD-7890', 9, 2),
('Suzuki Burgman', 'EFG-1234', 10, 3),
('Toyota Corolla', 'HIJ-5678', 11, 2),
('Honda Biz', 'KLM-9012', 12, 3),
('Fiat Toro', 'NOP-3456', 13, 4);

-- Funcionários
INSERT INTO Funcionario (nome, cpf, cargo, salario) VALUES 
('Pedro Alves', '111.222.333-44', 'Gerente', 3500.00),
('Ana Costa', '555.666.777-88', 'Atendente', 2200.00),
('Lucas Mendes', '999.888.777-66', 'Vigilante', 1800.00),
('Márcio Andrade', '123.456.789-01', 'Supervisor', 4200.00),
('Beatriz Ramos', '234.567.890-12', 'Atendente', 2300.00),
('Rodrigo Santos', '345.678.901-23', 'Vigilante', 1900.00),
('Tatiane Costa', '456.789.012-34', 'Contadora', 3800.00),
('Felipe Oliveira', '567.890.123-45', 'Assistente Administrativo', 2500.00),
('Vanessa Souza', '678.901.234-56', 'Recepcionista', 2100.00),
('Daniel Martins', '789.012.345-67', 'Manutenção', 2800.00),
('Larissa Ferreira', '890.123.456-78', 'Atendente', 2300.00),
('Eduardo Lima', '901.234.567-89', 'Gerente de Operações', 4500.00),
('Simone Alencar', '012.345.678-90', 'RH', 3200.00);

-- Estadias (exemplo de veículo estacionado)
INSERT INTO Estadia (veiculo_id, vaga_id, entrada)
VALUES
(1, 1, NOW() - INTERVAL 2 HOUR),  -- Vaga 101
(3, 5, NOW() - INTERVAL 1 HOUR),  -- Vaga 201
(5, 8, NOW() - INTERVAL 30 MINUTE); -- Vaga 105

-- Transações
INSERT INTO Transacao (estadia_id, valor, data, tipo_transacao) VALUES 
(1, 22.50, '2023-11-01', 'Pagamento'),
(1, 5.00, '2023-11-01', 'Taxa Serviço'),
(3, 48.75, '2023-11-02', 'Pagamento'),
(3, 2.50, '2023-11-02', 'Taxa Serviço'),
(4, 65.20, '2023-11-02', 'Pagamento'),
(5, 19.50, '2023-11-02', 'Pagamento'),
(6, 20.25, '2023-11-02', 'Pagamento'),
(7, 85.00, '2023-11-03', 'Pagamento'),
(7, 5.00, '2023-11-03', 'Taxa Serviço');
