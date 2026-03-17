"""
seed.py
Popula o banco de dados com os dados iniciais:
  - 20 locais do locais.json do frontend
  - 4 usuários de teste (mesmos do usuarios.json), incluindo os profs avaliadores
  - 5 avaliações iniciais

Execute: python seed.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine, Base
import app.models  # noqa — registra todos os models
from app.models.usuario import Usuario
from app.models.local import Local
from app.models.avaliacao import Avaliacao
from app.security import hash_senha
from datetime import datetime, timezone


# ── Dados dos locais (espelho do src/data/locais.json) ────────
LOCAIS = [
    {"id":1,"nome":"Shopping Rio Poty","tipo":"shopping","tipo_label":"Shopping Center","endereco":"Av. Marechal Castelo Branco, 4230 — Ilhotas","bairro":"Ilhotas","lat":-5.0878,"lng":-42.8007,"descricao":"Shopping com estrutura completa de acessibilidade.","rampa":True,"banheiro_adaptado":True,"vaga_pcd":True,"elevador":True,"entrada_acessivel":True,"calcada_acessivel":True},
    {"id":2,"nome":"Shopping da Cidade","tipo":"shopping","tipo_label":"Shopping Center","endereco":"Av. Frei Serafim, 1234 — Centro","bairro":"Centro","lat":-5.0915,"lng":-42.8019,"descricao":"Shopping no centro com boa acessibilidade.","rampa":True,"banheiro_adaptado":True,"vaga_pcd":True,"elevador":True,"entrada_acessivel":True,"calcada_acessivel":False},
    {"id":3,"nome":"Teresina Shopping","tipo":"shopping","tipo_label":"Shopping Center","endereco":"Av. Raul Lopes, 1000 — Jóquei","bairro":"Jóquei","lat":-5.0756,"lng":-42.7832,"descricao":"Shopping moderno com recursos de acessibilidade.","rampa":True,"banheiro_adaptado":True,"vaga_pcd":True,"elevador":True,"entrada_acessivel":True,"calcada_acessivel":True},
    {"id":4,"nome":"Hospital Getúlio Vargas (HGV)","tipo":"hospital","tipo_label":"Hospital / UPA","endereco":"Av. Frei Serafim, 2352 — Ilhotas","bairro":"Ilhotas","lat":-5.0887,"lng":-42.8034,"descricao":"Principal hospital público de Teresina com ampla estrutura.","rampa":True,"banheiro_adaptado":True,"vaga_pcd":True,"elevador":True,"entrada_acessivel":True,"calcada_acessivel":True},
    {"id":5,"nome":"UFPI — Campus Ministro Petrônio Portela","tipo":"educacao","tipo_label":"Instituição de Ensino","endereco":"Campus Universitário — Ininga","bairro":"Ininga","lat":-5.0669,"lng":-42.7679,"descricao":"Maior universidade do Piauí.","rampa":True,"banheiro_adaptado":True,"vaga_pcd":True,"elevador":False,"entrada_acessivel":True,"calcada_acessivel":False},
    {"id":6,"nome":"Praça da Liberdade","tipo":"espaco_publico","tipo_label":"Praça / Parque","endereco":"Praça da Liberdade — Centro","bairro":"Centro","lat":-5.0921,"lng":-42.8035,"descricao":"Praça central com calçadas reformadas.","rampa":True,"banheiro_adaptado":False,"vaga_pcd":False,"elevador":False,"entrada_acessivel":True,"calcada_acessivel":True},
    {"id":7,"nome":"Estação Cidadania (SEMCASPI)","tipo":"servico_publico","tipo_label":"Serviço Público","endereco":"Av. João XXIII, 2551 — Redenção","bairro":"Redenção","lat":-5.0823,"lng":-42.7934,"descricao":"Centro de assistência social com boa acessibilidade.","rampa":True,"banheiro_adaptado":True,"vaga_pcd":True,"elevador":False,"entrada_acessivel":True,"calcada_acessivel":True},
    {"id":8,"nome":"Banco do Brasil — Agência Centro","tipo":"banco","tipo_label":"Agência Bancária","endereco":"Rua Álvaro Mendes, 220 — Centro","bairro":"Centro","lat":-5.0908,"lng":-42.8021,"descricao":"Agência com recursos básicos de acessibilidade.","rampa":True,"banheiro_adaptado":False,"vaga_pcd":True,"elevador":False,"entrada_acessivel":True,"calcada_acessivel":False},
    {"id":9,"nome":"Mercado do Peixe","tipo":"mercado","tipo_label":"Mercado / Feira","endereco":"Margem do Rio Parnaíba — Porto","bairro":"Porto","lat":-5.0958,"lng":-42.8089,"descricao":"Mercado tradicional com piso irregular.","rampa":False,"banheiro_adaptado":False,"vaga_pcd":False,"elevador":False,"entrada_acessivel":False,"calcada_acessivel":False},
    {"id":10,"nome":"Centro Cultural Afro-Piauiense","tipo":"cultura","tipo_label":"Cultura e Lazer","endereco":"Rua Coelho de Resende, 345 — Centro","bairro":"Centro","lat":-5.0942,"lng":-42.8015,"descricao":"Centro cultural com estrutura parcialmente adaptada.","rampa":True,"banheiro_adaptado":False,"vaga_pcd":False,"elevador":False,"entrada_acessivel":True,"calcada_acessivel":True},
    {"id":11,"nome":"Aeroporto Senador Petrônio Portela","tipo":"transporte","tipo_label":"Terminal / Transporte","endereco":"Av. Centenário, S/N — São Cristóvão","bairro":"São Cristóvão","lat":-5.0597,"lng":-42.8236,"descricao":"Aeroporto com estrutura completa de acessibilidade.","rampa":True,"banheiro_adaptado":True,"vaga_pcd":True,"elevador":True,"entrada_acessivel":True,"calcada_acessivel":True},
    {"id":12,"nome":"UPA Norte","tipo":"hospital","tipo_label":"Hospital / UPA","endereco":"Rua Deputado Tibério Nunes, 100 — Monte Castelo","bairro":"Monte Castelo","lat":-5.0598,"lng":-42.7891,"descricao":"Unidade de pronto atendimento com recursos básicos.","rampa":True,"banheiro_adaptado":True,"vaga_pcd":True,"elevador":False,"entrada_acessivel":True,"calcada_acessivel":False},
    {"id":13,"nome":"DETRAN-PI — Sede","tipo":"servico_publico","tipo_label":"Serviço Público","endereco":"Av. Pedro Freitas, S/N — São Pedro","bairro":"São Pedro","lat":-5.0745,"lng":-42.7768,"descricao":"Sede do Detran com estacionamento adaptado.","rampa":True,"banheiro_adaptado":True,"vaga_pcd":True,"elevador":False,"entrada_acessivel":True,"calcada_acessivel":True},
    {"id":14,"nome":"Parque da Cidadania","tipo":"espaco_publico","tipo_label":"Praça / Parque","endereco":"Av. Homero Castelo Branco — Jóquei","bairro":"Jóquei","lat":-5.0721,"lng":-42.7802,"descricao":"Parque urbano com pistas e estrutura acessível.","rampa":True,"banheiro_adaptado":True,"vaga_pcd":True,"elevador":False,"entrada_acessivel":True,"calcada_acessivel":True},
    {"id":15,"nome":"IFPI — Campus Teresina Central","tipo":"educacao","tipo_label":"Instituição de Ensino","endereco":"Av. Álvaro Mendes, 94 — Centro","bairro":"Centro","lat":-5.0928,"lng":-42.8004,"descricao":"Instituto federal com adaptações parciais.","rampa":True,"banheiro_adaptado":True,"vaga_pcd":False,"elevador":False,"entrada_acessivel":True,"calcada_acessivel":True},
    {"id":16,"nome":"Prefeitura Municipal de Teresina","tipo":"servico_publico","tipo_label":"Serviço Público","endereco":"Rua Firmino Pires, 121 — Centro","bairro":"Centro","lat":-5.0914,"lng":-42.8027,"descricao":"Sede da prefeitura com adaptações básicas.","rampa":True,"banheiro_adaptado":False,"vaga_pcd":True,"elevador":False,"entrada_acessivel":True,"calcada_acessivel":False},
    {"id":17,"nome":"Teatro 4 de Setembro","tipo":"cultura","tipo_label":"Cultura e Lazer","endereco":"Praça Rio Branco, S/N — Centro","bairro":"Centro","lat":-5.0901,"lng":-42.8032,"descricao":"Teatro histórico sem adaptações para PCD.","rampa":False,"banheiro_adaptado":False,"vaga_pcd":False,"elevador":False,"entrada_acessivel":False,"calcada_acessivel":False},
    {"id":18,"nome":"Supermercado Irmãos Gonçalves — Morros","tipo":"supermercado","tipo_label":"Supermercado","endereco":"Av. Zequinha Freire, S/N — Morros","bairro":"Morros","lat":-5.0489,"lng":-42.7912,"descricao":"Supermercado com estrutura parcialmente adaptada.","rampa":True,"banheiro_adaptado":False,"vaga_pcd":True,"elevador":False,"entrada_acessivel":True,"calcada_acessivel":False},
    {"id":19,"nome":"Arena Ytacoatiara (Arena da Cidade)","tipo":"esporte","tipo_label":"Complexo Esportivo","endereco":"Av. Elias Fausto, S/N — Aeroporto","bairro":"Aeroporto","lat":-5.0634,"lng":-42.8121,"descricao":"Arena esportiva com estrutura de acessibilidade.","rampa":True,"banheiro_adaptado":True,"vaga_pcd":True,"elevador":False,"entrada_acessivel":True,"calcada_acessivel":True},
    {"id":20,"nome":"SESC Teresina","tipo":"cultura","tipo_label":"Cultura e Lazer","endereco":"Av. Elias Fausto, 400 — Aeroporto","bairro":"Aeroporto","lat":-5.0651,"lng":-42.8098,"descricao":"Espaço cultural com boa estrutura de acessibilidade.","rampa":True,"banheiro_adaptado":True,"vaga_pcd":True,"elevador":True,"entrada_acessivel":True,"calcada_acessivel":True},
]

USUARIOS = [
    {"nome": "Kauan Santos",  "email": "kauan@teresina.gov.br", "senha": "senha123", "perfil": "cidadao"},
    {"nome": "Aldir Silva","email": "aldir@teresina.gov.br",        "senha": "aldir2024","perfil": "cidadao"},
    {"nome": "Constantino Augusto", "email": "constantino@teresina.gov.br",  "senha": "constantino2026", "perfil": "cidadao"},
    {"nome": "Admin Sistema", "email": "admin@teresina.gov.br",  "senha": "admin123", "perfil": "admin"},
]

AVALIACOES = [
    {"user_id": 2, "local_id": 4, "acessivel": True,  "comentario": "Excelente estrutura!                O hospital possui rampas largas, elevadores funcionando e banheiros adaptados em todos os andares.", "data": datetime(2026, 2, 10, 14, 30, tzinfo=timezone.utc)},
    {"user_id": 1, "local_id": 4, "acessivel": True,  "comentario": "Fui acompanhar minha mãe cadeirante e não tivemos nenhuma dificuldade. As vagas PCD são bem sinalizadas.", "data": datetime(2026, 1, 22, 9, 15, tzinfo=timezone.utc)},
    {"user_id": 1, "local_id": 9, "acessivel": False, "comentario": "Infelizmente o acesso é muito difícil. O piso é irregular, não há rampa na entrada e o espaço interno é estreito.", "data": datetime(2026, 2, 28, 11, 0, tzinfo=timezone.utc)},
    {"user_id": 2, "local_id": 1, "acessivel": True,  "comentario": "Shopping muito bem adaptado. Piso otimo em todo o corredor principal, elevadores espaçosos.", "data": datetime(2026, 3, 1, 16, 45, tzinfo=timezone.utc)},
    {"user_id": 1, "local_id": 17,"acessivel": False, "comentario": "Teatro histórico lindo, mas sem nenhuma adaptação para PCD. Escadas na entrada, corredores estreitos.", "data": datetime(2026, 2, 14, 19, 20, tzinfo=timezone.utc)},
]


def seed():
    print("🌱 Iniciando seed do banco de dados...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # ── Locais ────────────────────────────────────────────
        if db.query(Local).count() == 0:
            for d in LOCAIS:
                db.add(Local(**d))
            db.commit()
            print(f"  ✅ {len(LOCAIS)} locais inseridos.")
        else:
            print("  ⏭️  Locais já existem, pulando.")

        # ── Usuários ──────────────────────────────────────────
        if db.query(Usuario).count() == 0:
            usuarios_criados = []
            for d in USUARIOS:
                u = Usuario(
                    nome=d["nome"],
                    email=d["email"],
                    senha_hash=hash_senha(d["senha"]),
                    perfil=d["perfil"],
                )
                db.add(u)
                usuarios_criados.append(u)
            db.commit()
            print(f"  ✅ {len(USUARIOS)} usuários inseridos.")
        else:
            print("  ⏭️  Usuários já existem, pulando.")

        # ── Avaliações ────────────────────────────────────────
        if db.query(Avaliacao).count() == 0:
            for d in AVALIACOES:
                db.add(Avaliacao(**d))
            db.commit()
            print(f"  ✅ {len(AVALIACOES)} avaliações inseridas.")
        else:
            print("  ⏭️  Avaliações já existem, pulando.")

        print("\n🎉 Seed concluído com sucesso!")
        print("\nCredenciais de teste:")
        for u in USUARIOS:
            print(f"  {u['email']} | senha: {u['senha']}")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro no seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()