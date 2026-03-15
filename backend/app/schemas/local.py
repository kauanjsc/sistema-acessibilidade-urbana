"""
schemas/local.py
Schemas Pydantic para locais — espelha a estrutura do frontend.
"""

from pydantic import BaseModel, ConfigDict


class AcessibilidadeSchema(BaseModel):
    """Sub-objeto com os recursos de acessibilidade (igual ao frontend)."""
    rampa:            bool = False
    banheiroAdaptado: bool = False
    vagaPCD:          bool = False
    elevador:         bool = False
    entradaAcessivel: bool = False
    calcadaAcessivel: bool = False


class LocalResponse(BaseModel):
    """
    Resposta de um local — estrutura idêntica ao locais.json do frontend
    para máxima compatibilidade sem alterar o Vue.
    """
    model_config = ConfigDict(from_attributes=True)

    id:         int
    nome:       str
    tipo:       str
    tipoLabel:  str           # alias de tipo_label
    endereco:   str
    bairro:     str
    lat:        float
    lng:        float
    descricao:  str | None
    acessibilidade: AcessibilidadeSchema

    @classmethod
    def from_orm_local(cls, local) -> "LocalResponse":
        """
        Constrói o schema a partir do ORM Local,
        remontando o sub-objeto 'acessibilidade'.
        """
        return cls(
            id=local.id,
            nome=local.nome,
            tipo=local.tipo,
            tipoLabel=local.tipo_label,
            endereco=local.endereco,
            bairro=local.bairro,
            lat=local.lat,
            lng=local.lng,
            descricao=local.descricao,
            acessibilidade=AcessibilidadeSchema(
                rampa=local.rampa,
                banheiroAdaptado=local.banheiro_adaptado,
                vagaPCD=local.vaga_pcd,
                elevador=local.elevador,
                entradaAcessivel=local.entrada_acessivel,
                calcadaAcessivel=local.calcada_acessivel,
            ),
        )