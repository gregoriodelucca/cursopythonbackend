from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import asyncio

app = FastAPI()

# Simulando um banco de dados em memória
contas_bancarias = {}

# Modelo de dados para criar uma conta bancária
class Conta(BaseModel):
    titular: str
    saldo: float = 0.0

# Modelo de dados para realizar uma transferência
class Transferencia(BaseModel):
    numero_conta_origem: int
    numero_conta_destino: int
    valor: float

@app.post("/criar_conta/")
async def criar_conta(conta: Conta):
    numero_conta = random.randint(1000, 9999)
    if numero_conta in contas_bancarias:
        raise HTTPException(status_code=400, detail="Número da conta já existe.")
    
    contas_bancarias[numero_conta] = conta
    return {"numero_conta": numero_conta, "titular": conta.titular, "saldo": conta.saldo}

@app.get("/consultar_saldo/{numero_conta}")
async def consultar_saldo(numero_conta: int):
    conta = contas_bancarias.get(numero_conta)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada.")
    return {"numero_conta": numero_conta, "saldo": conta.saldo}

@app.post("/transferir/")
async def transferir(transferencia: Transferencia):
    conta_origem = contas_bancarias.get(transferencia.numero_conta_origem)
    conta_destino = contas_bancarias.get(transferencia.numero_conta_destino)
    
    if not conta_origem:
        raise HTTPException(status_code=404, detail="Conta de origem não encontrada.")
    
    if not conta_destino:
        raise HTTPException(status_code=404, detail="Conta de destino não encontrada.")
    
    if conta_origem.saldo < transferencia.valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente.")
    
    # Simulando uma operação assíncrona de transferência
    await asyncio.sleep(1)  # Simulando um pequeno delay como se fosse uma operação de I/O
    
    conta_origem.saldo -= transferencia.valor
    conta_destino.saldo += transferencia.valor
    
    return {"numero_conta_origem": transferencia.numero_conta_origem,
            "numero_conta_destino": transferencia.numero_conta_destino,
            "valor": transferencia.valor,
            "novo_saldo_origem": conta_origem.saldo,
            "novo_saldo_destino": conta_destino.saldo}
